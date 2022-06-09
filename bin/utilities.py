# coding: utf-8

# Copyright 2022, Robert Dyer, Samuel W. Flint,
#                 and University of Nebraska Board of Regents
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import logging
import os
import sys

STUDY_JSON = 'study-config.json'
JOBS_JSON = 'jobs.json'

CREDENTIALS_FILE = 'boa-credentials.txt'

QUERY_ROOT = 'boa/'
SNIPPET_ROOT = QUERY_ROOT + 'snippets/'

DATA_ROOT = 'data/'
TXT_ROOT = DATA_ROOT + 'txt/'
CSV_ROOT = DATA_ROOT + 'csv/'
PQ_ROOT = DATA_ROOT + 'parquet/'

ANALYSIS_ROOT = 'analyses/'

logger = logging.getLogger('boa.logger')
logger.addHandler(logging.StreamHandler(sys.stderr))

def get_credentials():
    user = None
    password = None

    try:
        with open(CREDENTIALS_FILE, 'r') as fh:
            creds = [line.strip() for line in fh.readlines()]
        if len(creds) > 0:
            user = creds[0]
        if len(creds) > 1:
            password = creds[1]
    except:
        pass

    if not user or not password:
        import getpass
        try:
            import keyring
            user = user or getpass.getuser()
            password = keyring.get_password('boaapi', user)
            if password is None:
                raise Exception()
        except:
            if not user:
                user = input('Username [%s]: ' % getpass.getuser())
            if not user:
                user = getpass.getuser()
            password = getpass.getpass()

    return (user, password)

client = None
def get_client():
    global client
    if client is None:
        from boaapi.boa_client import BoaClient, BOA_API_ENDPOINT
        client = BoaClient(endpoint = BOA_API_ENDPOINT)
        client.login(*get_credentials())
    return client

def close_client():
    global client
    client.close()
    client = None

config = None
def get_query_config(filename = STUDY_JSON):
    global config
    if config is None:
        try:
            with open(filename, 'r') as fh:
                config = json.load(fh)
        except:
            logger.critical(f'Problem reading job configuration file "{filename}"')
            exit(10)
    return config

job_data = None
def get_query_data():
    global job_data

    if job_data is not None:
        return job_data

    try:
        with open(JOBS_JSON, 'r') as fh:
            query_data = json.load(fh)
        return query_data
    except:
        return { "$schema": "schemas/0.1.0/jobs.schema.json" }

def update_query_data(target, job_id, sha256):
    global job_data
    old_job_data = get_query_data()
    old_job_data[target] = { 'job': int(job_id), 'sha256': sha256 }
    job_data = old_job_data
    if os.path.exists(JOBS_JSON):
        os.chmod(JOBS_JSON, 0o644)
    with open(JOBS_JSON, 'w') as fh:
        json.dump(job_data, fh, indent = 2)
    os.chmod(JOBS_JSON, 0o444)

def expand_replacements(replacements, query):
    if len(replacements) > 0:
        import re
        has_replaced = True
        while has_replaced:
            has_replaced = False
            for (before, after) in replacements:
                replaced = re.sub(before, after, query)
                if query != replaced:
                    has_replaced = True
                    query = replaced
    return query

def build_replacements(global_replacements, local_replacements, only_files=False):
    replacements = {}
    repls = []
    replacement_includes_string = False
    for replacements_list in [local_replacements, global_replacements]:
        for repl in replacements_list:
            target = repl['target']
            if target not in replacements:
                if 'replacement' in repl:
                    replacement_includes_string = True
                    if not only_files:
                        replacements[target] = repl['replacement']
                else:
                    if only_files:
                        replacements[target] = SNIPPET_ROOT + repl['file']
                    else:
                        try:
                            with open(SNIPPET_ROOT + repl['file'], 'r') as fh:
                                replacements[target] = fh.read()
                        except FileNotFoundError as e:
                            raise FileNotFoundError(f"Snippet file '{repl['file']}' not found for substitution '{repl['target']}'.") from e
                if target in replacements:
                    repls.append((target, replacements[target]))
    if replacement_includes_string and only_files:
        repls.append(('', STUDY_JSON))
    return repls

def get_make_public(target):
    config = get_query_config()
    try:
        return config['queries'][target]['make_public']
    except:
        return True

def get_dataset(target):
    config = get_query_config()
    dataset_name = config['queries'][target]['dataset']

    if dataset_name in config['datasets']:
        client = get_client()
        return client.get_dataset(config['datasets'][dataset_name])

    logger.critical(f'Dataset named "{dataset_name}" is not known.')
    exit(20)

def prepare_query(target):
    from hashlib import sha256

    config = get_query_config()
    query_info = config['queries'][target]

    with open(QUERY_ROOT + query_info['query'], 'r') as fh:
        query = fh.read()

    query_substitutions = build_replacements(config.get('substitutions', []), query_info.get('substitutions', []))
    query = expand_replacements(query_substitutions, query)

    return (query, sha256(str.encode(get_dataset(target)['name'] + query)).hexdigest())

def is_run_needed(target):
    query_data = get_query_data()
    if target not in query_data:
        return True

    oldhash = query_data[target]['sha256']
    _, newhash = prepare_query(target)
    return oldhash != newhash

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
import os
import json

import logging

logger = logging.getLogger('boa.logger')

def get_credentials():
    try:
        with open('boa-credentials.txt', 'r') as fh:
            creds = [line.strip() for line in fh.readlines()]
        user = creds[0]
        password = creds[1]
    except:
        import getpass
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

config = None
def get_query_config(filename = 'job-config.json'):
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
        with open('jobs.json', 'r') as fh:
            query_data = json.load(fh)
        return query_data
    except:
        return {}

def update_query_data(target, job_id, sha256):
    global job_data
    old_job_data = get_query_data()
    old_job_data[target] = { 'job': job_id, 'sha256': sha256 }
    job_data = old_job_data
    with open('jobs.json', 'w') as fh:
        json.dump(job_data, fh, indent = 2)

def expand_replacements(replacements, query):
    if len(replacements) > 0:
        import re
        has_replaced = True
        while has_replaced:
            has_replaced = False
            for (before, after) in replacements:
                replaced = re.sub(before, after, text)
                if query != replaced:
                    has_replaced = True
                    query = replaced
    return query

def build_replacements(global_replacements, local_replacements, only_files=False):
    replacements = {}
    repls = []
    for replacements_list in [local_replacements, global_replacements]:
        for repl in replacements_list:
            target = repl['target']
            if target not in replacements:
                if repl['kind'] == 'text':
                    if not only_files:
                        replacements[target] = repl['replacement']
                else:
                    if only_files:
                        replacements[target] = repl['replacement']
                    else:
                        with open(repl['replacement'], 'r') as fh:
                            replacement = fh.read()
                        replacements[target] = replacement
                repls.append((target, replacements[target]))
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

    with open(query_info['query'], 'r') as fh:
        query = fh.read()

    query_substitutions = build_replacements(config['substitutions'], query_info['substitutions'])
    query = expand_replacements(query_substitutions, query)

    return (query, sha256(str.encode(query)).hexdigest())

def is_run_needed(target):
    if not os.path.exists(target):
        return True

    query_data = get_query_data()
    if target not in query_data:
        return True

    oldhash = query_data[target]['sha256']
    _, newhash = prepare_query(target)
    return oldhash != newhash
# coding: utf-8

import json
import logging
import os
import sys
import time

STUDY_JSON = 'study-config.json'
JOBS_JSON = 'jobs.json'

QUERY_ROOT = 'boa/'
SNIPPET_ROOT = QUERY_ROOT + 'snippets/'

DATA_ROOT = 'data/'
TXT_ROOT = DATA_ROOT + 'txt/'
CSV_ROOT = DATA_ROOT + 'csv/'
PQ_ROOT = DATA_ROOT + 'parquet/'

ANALYSIS_ROOT = 'analyses/'

ADMIN_PREFIX = '[admin] '

logger = logging.getLogger('boa.logger')
logger.addHandler(logging.StreamHandler(sys.stderr))


def get_credentials():
    user = None
    password = None

    from dotenv import load_dotenv
    load_dotenv()

    import getpass
    user = os.environ['BOA_API_USER'] if 'BOA_API_USER' in os.environ else input('Username [%s]: ' % getpass.getuser())
    password = os.environ['BOA_API_PW'] if 'BOA_API_PW' in os.environ else None

    if not password:
        try:
            import keyring
            password = keyring.get_password('boaapi', user)
            if password is None:
                raise Exception()
        except:
            password = getpass.getpass()

    return (user, password)


client = None


def get_client():
    global client
    if client is None:
        from boaapi.boa_client import BoaClient, BOA_API_ENDPOINT
        client = BoaClient(endpoint=BOA_API_ENDPOINT)
        client.login(*get_credentials())
    return client


def close_client():
    global client
    if client:
        client.close()
    client = None


config = None


def get_query_config(filename=STUDY_JSON):
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
        return {"$schema": "schemas/0.1.2/jobs.schema.json"}


def update_query_data(target, job_id, hash):
    global job_data
    old_job_data = get_query_data()
    old_job_data[target] = {'job': int(job_id), 'job-hash': hash}
    job_data = old_job_data
    if os.path.exists(JOBS_JSON):
        os.chmod(JOBS_JSON, 0o644)
    with open(JOBS_JSON, 'w') as fh:
        json.dump(job_data, fh, indent=2)
    os.chmod(JOBS_JSON, 0o444)


def expand_replacements(replacements, query):
    if len(replacements) > 0:
        import re
        has_replaced = True
        while has_replaced:
            has_replaced = False
            for (before, after) in replacements:
                after = (r'\g<1>\g<2>' + after.strip()).replace('\n', '\n\\1') + r'\3'
                before = re.sub(r'([{}])', r'\\\1', before)
                replaced = re.sub(r'([ \t]*)(.*(?=' + before + '))' + before + '(\n?)',
                                  after,
                                  query).replace('#WHY#', '\\')
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
                        replacements[target] = repl['replacement'].replace('\\', '#WHY#')
                else:
                    if only_files:
                        replacements[target] = SNIPPET_ROOT + repl['file']
                    else:
                        try:
                            with open(SNIPPET_ROOT + repl['file'], 'r') as fh:
                                replacements[target] = fh.read().replace('\\', '#WHY#')
                        except FileNotFoundError as e:
                            raise FileNotFoundError(f"Snippet file '{repl['file']}' not found for substitution '{repl['target']}'.") from e
                if target in replacements:
                    repls.append((target, replacements[target]))
    if replacement_includes_string and only_files:
        repls.append(('', STUDY_JSON))
    return repls


def get_make_public(config, target):
    try:
        return config['queries'][target]['public']
    except:
        return True


def get_dataset(config, target):
    dataset_name = config['queries'][target]['dataset']

    if dataset_name in config['datasets']:
        client = get_client()
        ds = client.get_dataset(config['datasets'][dataset_name])
        if ds is None:
            ds = client.get_dataset(ADMIN_PREFIX + config['datasets'][dataset_name])
        return ds

    logger.critical(f'Dataset named "{dataset_name}" is not known.')
    exit(20)


def prepare_query(config, target):
    from hashlib import sha256

    query_info = config['queries'][target]

    with open(QUERY_ROOT + query_info['query'], 'r') as fh:
        query = fh.read()

    query_substitutions = build_replacements(config.get('substitutions', []),
                                             query_info.get('substitutions', []))
    query = expand_replacements(query_substitutions, query)

    return (query, sha256(str.encode(get_dataset(config, target)['name'] + query)).hexdigest())


def is_run_needed(config, target):
    query_data = get_query_data()

    _, newhash = prepare_query(config, target)
    logger.debug('new query hash = ' + newhash)

    if target not in query_data:
        return True

    oldhash = query_data[target]['job-hash']
    logger.debug('old query hash = ' + oldhash)

    return oldhash != newhash

class Timer:
    def __init__(self):
        self._start = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc_info):
        if self._start is not None:
            elapsed = time.perf_counter() - self._start
            self._start = None

            logger.debug(f'Elapsed time: {elapsed:0.4f} seconds')

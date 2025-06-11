#!/usr/bin/env python3
# coding: utf-8

from dotenv import load_dotenv
from hashlib import md5
import json
import os
from pathlib import Path
import requests
import sys


load_dotenv()

if not 'ZENODO_API_TOKEN' in os.environ:
    print('You need to set the ZENODO_API_TOKEN environment variable in your .env file.')
    sys.exit(-1)


ZENODO_API_ENDPOINT = os.environ['ZENODO_API_ENDPOINT'] if 'ZENODO_API_ENDPOINT' in os.environ else 'https://zenodo.org'
JSON_FILENAME = '.zenodo.json'

params = {'access_token': os.environ['ZENODO_API_TOKEN']}
headers = {'Content-Type': 'application/json'}

json_data = None


def get_json():
    with open(JSON_FILENAME) as f:
        return json.load(f)


def save_json():
    with open(JSON_FILENAME, 'w') as f:
        f.write(json.dumps(json_data, indent=4))


def get_deposition_id():
    if 'prereserve_doi' in json_data:
        if isinstance(json_data['prereserve_doi'], dict) and 'recid' in json_data['prereserve_doi']:
            return json_data['prereserve_doi']['recid']
    return None


def create_deposition():
    global json_data

    r = requests.post(f'{ZENODO_API_ENDPOINT}/api/deposit/depositions',
                      params=params, json={}, headers=headers)
    if r.status_code == 201:
        json_data['prereserve_doi'] = r.json()['metadata']['prereserve_doi']
        save_json()
        print('created new deposition:', json_data['prereserve_doi']['recid'])
        print('DOI:', json_data['prereserve_doi']['doi'])
        return json_data['prereserve_doi']['recid']

    print(json.dumps(r.json(), indent=2))
    return None


def create_default_json():
    with open(JSON_FILENAME, 'w') as f:
        f.write("""{
    "title": "TODO: provide a title for the dataset",
    "description": "TODO: provide a description",
    "keywords": [
        "kw1",
        "kw2"
    ],
    "communities": [
        {
            "identifier": "zenodo"
        }
    ],
    "upload_type": "dataset",
    "language": "eng",
    "creators": [
        {
            "affiliation": "Anonymous",
            "name": "Anonymous"
        }
    ],
    "access_right": "open",
    "license": "cc-by-4.0",
    "version": "1.0.0",
    "prereserve_doi": true
}""")
    print('A placeholder .zenodo.json file was created. Please edit it and re-run the script.')
    sys.exit(0)


def get_deposition(deposition_id):
    r = requests.get(f'{ZENODO_API_ENDPOINT}/api/deposit/depositions/{deposition_id}',
                     params=params, json={}, headers=headers)
    if r.status_code == 200:
        bucket_url = r.json()['links']['bucket']
        files = {x['filename']: {'size': x['filesize'], 'checksum': x['checksum']} for x in r.json()['files']}
        return (bucket_url, files)

    print(json.dumps(r.json(), indent=2))
    sys.exit(-1)


def upload_file(bucket_url, files, filename):
    file_size = os.stat(filename).st_size
    found = filename in files and file_size == files[filename]['size']
    if found:
        print('checking checksum for:', filename)
        with open(filename, 'rb') as f:
            checksum = md5(f.read()).hexdigest()
        found = files[filename]['checksum'] == checksum

    if not found:
        print('uploading:', filename)
        with open(filename, 'rb') as fp:
            try:
                from tqdm import tqdm
                from tqdm.utils import CallbackIOWrapper

                with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as t:
                    wrapped_file = CallbackIOWrapper(t.update, fp, 'read')
                    r = requests.put(
                        f'{bucket_url}/{filename}',
                        data=wrapped_file,
                        params=params,
                        json={},
                    )
            except ImportError:
                r = requests.put(
                    f'{bucket_url}/{filename}',
                    data=fp,
                    params=params,
                    json={},
                )
            
            if r.status_code != 200:
                print(json.dumps(r.json(), indent=2))
    else:
        print('already uploaded:', filename)


def update_metadata(deposition_id):
    data = {}
    with open(JSON_FILENAME) as f:
        data['metadata'] = json.load(f)
    r = requests.put(f'{ZENODO_API_ENDPOINT}/api/deposit/depositions/{deposition_id}',
                     params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        print('There was a problem updating the deposition metadata.')
        print(json.dumps(r.json(), indent=2))
    else:
        print(f'Deposition {deposition_id} metadata updated successfully.')


def print_bibtex():
    from datetime import datetime
    year = datetime.now().year
    month = datetime.now().month

    authors = ''
    for person in json_data['creators']:
        if len(authors) > 0:
            authors += ' and '
        authors += person['name']

    print(f"""@misc{{replication-package,
  title={{{json_data['title']}}},
  DOI={{{json_data['prereserve_doi']['doi']}}},
  publisher={{Zenodo}},
  author={{{authors}}},
  year={{{year}}},
  month={{{month}}}
}}""")
    pass


if __name__ == '__main__':
    # make sure we have a JSON metadata file
    if not Path(JSON_FILENAME).exists():
        create_default_json()

    json_data = get_json()

    # ensure there is a deposition
    deposition_id = get_deposition_id() or create_deposition()
    if not deposition_id:
        print('unable to create a Zenodo deposition')
        sys.exit(-1)

    # ensure all files uploaded
    print('uploading files to:', deposition_id)
    (bucket_url, files) = get_deposition(deposition_id)
    for filepath in Path().glob('*.zip'):
        upload_file(bucket_url, files, str(filepath))
    upload_file(bucket_url, files, 'README.md')

    update_metadata(deposition_id)

    print_bibtex()

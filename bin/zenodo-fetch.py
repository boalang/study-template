#!/usr/bin/env python3
# coding: utf-8

from dotenv import load_dotenv
import json
import os
import requests
import sys


load_dotenv()

if not 'ZENODO_API_TOKEN' in os.environ:
    print('You need to set the ZENODO_API_TOKEN environment variable in your .env file.')
    sys.exit(-1)


ZENODO_API_ENDPOINT = os.environ['ZENODO_API_ENDPOINT'] if 'ZENODO_API_ENDPOINT' in os.environ else 'https://zenodo.org'

params = {'access_token': os.environ['ZENODO_API_TOKEN']}
headers = {'Content-Type': 'application/json'}


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('you must specify the record ID to fetch')
        sys.exit(-1)

    deposition_id = int(sys.argv[1])
    r = requests.get(f'{ZENODO_API_ENDPOINT}/api/deposit/depositions/{deposition_id}',
                     params=params, json={}, headers=headers)
    if r.status_code == 200:
        data = r.json()['metadata']
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(r.json(), indent=2))

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


ZENODO_API_ENDPOINT = 'https://sandbox.zenodo.org'

params = {'access_token': os.environ['ZENODO_API_TOKEN']}
headers = {'Content-Type': 'application/json'}


def delete():
    r = requests.get(f'{ZENODO_API_ENDPOINT}/api/deposit/depositions',
                     params=params, json={}, headers=headers)
    if r.status_code == 200:
        if len(r.json()) > 0:
            for i in r.json():
                r = requests.delete(f'{ZENODO_API_ENDPOINT}/api/deposit/depositions/' + str(
                    i['record_id']), params=params, json={}, headers=headers)
                if r.status_code == 204:
                    print('deleting', i['record_id'])
            delete()
    else:
        print(json.dumps(r.json(), indent=2))


if __name__ == '__main__':
    delete()

#!/usr/bin/env python3
# coding: utf-8

import json
import os
from pathlib import Path
import subprocess
import sys


JSON_FILENAME = '.zenodo.json'


def get_deposition_id():
    if 'prereserve_doi' in json_data:
        if isinstance(json_data['prereserve_doi'], dict) and 'recid' in json_data['prereserve_doi']:
            return json_data['prereserve_doi']['recid']
    return None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: zenodo-download.py <filename>')
        sys.exit(-1)
    filename = sys.argv[1]

    # make sure we have a JSON metadata file
    if not Path(JSON_FILENAME).exists():
        print('no Zenodo JSON metadata file found')
        sys.exit(-1)

    with open(JSON_FILENAME) as f:
        json_data = json.load(f)

    # ensure there is a deposition
    deposition_id = get_deposition_id()
    if not deposition_id:
        print('unable to find a Zenodo deposition')
        sys.exit(-1)

    # download the file
    print('downloading file...')

    try:
        os.remove(filename)
    except:
        pass

    url = f'https://zenodo.org/records/{deposition_id}/files/{filename}?download=1'
    proc = subprocess.run(['curl', '-L', '--fail-with-body', '-o', filename, url])

    if proc.returncode == 0:
        print('download complete')
    else:
        print(f'error downloading file "{filename}" from "{url}"')
        try:
            os.remove(filename)
        except:
            pass
        sys.exit(-1)

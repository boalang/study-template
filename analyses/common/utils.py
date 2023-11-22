# coding: utf-8

import json
import os
from typing import Optional


__all__ = [
    '_resolve_dir',
    '_get_dir',
    'get_dataset',
]

def _resolve_dir(dir: str) -> str:
    curdir = os.getcwd()
    if curdir.endswith('/analyses'):
        return '../' + dir
    return dir

def _get_dir(subdir: Optional[str]) -> str:
    if subdir is None:
        return ''
    return subdir + '/'

def get_dataset(filename: str, subdir: Optional[str]=None) -> str:
    study_config = _resolve_dir('study-config.json')
    with open(study_config) as f:
        study_config = json.load(f)

    datasets = study_config['datasets']
    queries = study_config['queries']
    query = queries[f'{_get_dir(subdir)}{filename}.txt']

    return datasets[query['dataset']]

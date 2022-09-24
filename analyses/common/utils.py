# coding: utf-8

import os
from typing import Optional


__all__ = [
    "_resolve_dir",
    "_get_dir",
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

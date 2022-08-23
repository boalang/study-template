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
import pandas as pd
from typing import Optional, Union, List, Callable

from .utils import _resolve_dir, _get_dir

__all__ = [
    "get_df",
    "get_deduped_df",
    ]

def get_df(filename: str, subdir: Optional[str]=None, header: Optional[Union[List[int], bool, str]]=None, precache_function: Optional[Callable[[pd.DataFrame], pd.DataFrame]]=None, **kwargs):
    '''Loads a CSV file into a DataFrame.

    Args:
        filename (str): the CSV file to load, without the '.csv' extension
        subdir (Optional[str], optional): the sub-directory, underneath 'data/csv/', that it lives in. Defaults to None.
        precache_function (Callable[DataFrame] -> DataFrame, optional): a function to modify the the data frame before caching.

    Returns:
        pd.DataFrame: the CSV file as a Pandas DataFrame
    '''
    try:
        df = pd.read_parquet(_resolve_dir(f'data/parquet/{_get_dir(subdir)}{filename}.parquet'))
    except:
        df = pd.read_csv(_resolve_dir(f'data/csv/{_get_dir(subdir)}{filename}.csv'), index_col=False, header=header, **kwargs)
        if precache_function:
            df = precache_function(df)
        os.makedirs(_resolve_dir(f'data/parquet/{_get_dir(subdir)}'), 0o755, True)
        df.to_parquet(_resolve_dir(f'data/parquet/{_get_dir(subdir)}{filename}.parquet'), compression='gzip')
    return df

def get_deduped_df(filename: str, subdir: Optional[str]=None, ts=False, **kwargs):
    '''Loads a CSV file into a DataFrame and de-duplicates the data.

    This function assumes your table has columns named 'project' and 'file', and no column named 'hash'.

    Args:
        filename (str): the CSV file to load, without the '.csv' extension
        subdir (Optional[str], optional): the sub-directory, underneath 'data/csv/', that it lives in. Defaults to None.

    Returns:
        pd.DataFrame: the CSV file as a Pandas DataFrame
    '''
    try:
        df = pd.read_parquet(_resolve_dir(f'data/parquet/{_get_dir(subdir)}{filename}-deduped.parquet'))
    except:
        if ts:
            df = _remove_dupes(get_df(filename, subdir, **kwargs), subdir, names=['var', 'hash', 'project', 'ts', 'file'])
        else:
            df = _remove_dupes(get_df(filename, subdir, **kwargs), subdir)
        os.makedirs(_resolve_dir(f'data/parquet/{_get_dir(subdir)}'), 0o755, True)
        df.to_parquet(_resolve_dir(f'data/parquet/{_get_dir(subdir)}{filename}-deduped.parquet'), compression='gzip')
    return df

def _remove_dupes(df: pd.DataFrame, subdir: Optional[str]=None, names=['var', 'hash', 'project', 'file']):
    df2 = get_df('dupes', subdir, names=names).drop(columns=['var'])

    df2 = df2[df2.duplicated(subset=['hash'])]
    df3 = pd.merge(df, df2, how='left', left_on=['project', 'file'], right_on=['project', 'file'])
    # df4 consists of rows in df3 where 'hash' is 'NaN' (meaning that they did not exist in df2.duplicated(subset=['hash']))
    df4 = df3[pd.isnull(df3['hash'])]
    return df4.drop(columns=['hash'])

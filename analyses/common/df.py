# coding: utf-8

import os
import pandas as pd
from typing import Optional, List, Callable

from .utils import _resolve_dir, _get_dir

__all__ = [
    "get_df",
    "get_deduped_df",
    ]

def get_df(filename: str, subdir: Optional[str]=None, drop: Optional[List[str]]=None, precache_function: Optional[Callable[[pd.DataFrame], pd.DataFrame]]=None, **kwargs) -> pd.DataFrame:
    '''Loads a CSV file into a DataFrame. Extra keyword arguments are passed directly to read_csv.

    Args:
        filename (str): the CSV file to load, without the '.csv' extension
        subdir (Optional[str], optional): the sub-directory, underneath 'data/csv/', that it lives in. Defaults to None.
        drop (Optional[List[str]], optional): Any columns to drop from the table after loading. Defaults to None.
        precache_function (Callable[DataFrame] -> DataFrame, optional): a function to modify the the data frame before caching. Defaults to None.

    Returns:
        pd.DataFrame: the CSV file as a Pandas DataFrame
    '''
    try:
        df = pd.read_parquet(_resolve_dir(f'data/parquet/{_get_dir(subdir)}{filename}.parquet'))
    except:
        df = pd.read_csv(_resolve_dir(f'data/csv/{_get_dir(subdir)}{filename}.csv'), index_col=False, **kwargs)
        if drop:
            df = df.drop(drop, axis=1)
        if precache_function:
            df = precache_function(df)
        os.makedirs(_resolve_dir(f'data/parquet/{_get_dir(subdir)}'), 0o755, True)
        df.to_parquet(_resolve_dir(f'data/parquet/{_get_dir(subdir)}{filename}.parquet'), compression='gzip')
    return df

def get_deduped_df(filename: str, subdir: Optional[str]=None, dupesdir: Optional[str]=None, drop: Optional[List[str]]=None, precache_function: Optional[Callable[[pd.DataFrame], pd.DataFrame]]=None, ts: bool=False, **kwargs) -> pd.DataFrame:
    '''Loads a CSV file into a DataFrame and de-duplicates the data.

    This function assumes your table has columns named 'project' and 'file', and no column named 'hash'.

    Args:
        filename (str): the CSV file to load, without the '.csv' extension
        subdir (Optional[str], optional): the sub-directory, underneath 'data/csv/', that it lives in. Defaults to None.
        dupesdir (Optional[str], optional): the sub-directory, underneath 'data/csv/', that the dupes file lives in. Defaults to None.
        drop (Optional[List[str]], optional): Any columns to drop from the table after loading. Defaults to None.
        precache_function (Callable[DataFrame] -> DataFrame, optional): a function to modify the the data frame before caching. Defaults to None.
        ts (bool): if the hash file also has the file timestamps or not

    Returns:
        pd.DataFrame: the CSV file as a Pandas DataFrame
    '''
    try:
        df = pd.read_parquet(_resolve_dir(f'data/parquet/{_get_dir(subdir)}{filename}-deduped.parquet'))
    except:
        if ts:
            df = _remove_dupes(get_df(filename, subdir, drop, precache_function, **kwargs), dupesdir, names=['var', 'hash', 'project', 'ts', 'file'])
        else:
            df = _remove_dupes(get_df(filename, subdir, drop, precache_function, **kwargs), dupesdir)
        os.makedirs(_resolve_dir(f'data/parquet/{_get_dir(subdir)}'), 0o755, True)
        df.to_parquet(_resolve_dir(f'data/parquet/{_get_dir(subdir)}{filename}-deduped.parquet'), compression='gzip')
    return df

def _remove_dupes(df: pd.DataFrame, dupesdir: Optional[str]=None, names=['var', 'hash', 'project', 'file']) -> pd.DataFrame:
    df2 = get_df('dupes', dupesdir, names=names).drop(columns=['var'])

    df2 = df2[df2.duplicated(subset=['hash'])]
    df3 = pd.merge(df, df2, how='left', left_on=['project', 'file'], right_on=['project', 'file'])
    # df4 consists of rows in df3 where 'hash' is 'NaN' (meaning that they did not exist in df2.duplicated(subset=['hash']))
    df4 = df3[pd.isnull(df3['hash'])]
    return df4.drop(columns=['hash'])

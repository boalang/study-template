# coding: utf-8

# Copyright 2022, Robert Dyer,
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
import sys
import pandas as pd
from typing import Optional, Union, List

__all__ = [
    "get_df",
    "get_deduped_df",
    "get_styler",
    "highlight_cols",
    "highlight_rows",
    "save_table",
    ]

def _get_dir(subdir: Optional[str]):
    if subdir is None:
        return ''
    return subdir + '/'

def get_df(filename: str, subdir: Optional[str]=None, header: Optional[Union[List[int], bool]]=None, **kwargs):
    '''Loads a CSV file into a DataFrame.

    Args:
        filename (str): the CSV file to load, without the '.csv' extension
        subdir (Optional[str], optional): the sub-directory, underneath 'data/csv/', that it lives in. Defaults to None.

    Returns:
        pd.DataFrame: the CSV file as a Pandas DataFrame
    '''
    try:
        df = pd.read_parquet(f'data/parquet/{_get_dir(subdir)}{filename}.parquet')
    except:
        df = pd.read_csv(f'data/csv/{_get_dir(subdir)}{filename}.csv', index_col=False, header=header, **kwargs)
        os.makedirs(f'data/parquet/{_get_dir(subdir)}', 0o755, True)
        df.to_parquet(f'data/parquet/{_get_dir(subdir)}{filename}.parquet', compression='gzip')
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
        df = pd.read_parquet(f'data/parquet/{_get_dir(subdir)}{filename}-deduped.parquet')
    except:
        if ts:
            df = _remove_dupes(get_df(filename, subdir, **kwargs), subdir, names=['var', 'hash', 'project', 'ts', 'file'])
        else:
            df = _remove_dupes(get_df(filename, subdir, **kwargs), subdir)
        os.makedirs(f'data/parquet/{_get_dir(subdir)}', 0o755, True)
        df.to_parquet(f'data/parquet/{_get_dir(subdir)}{filename}-deduped.parquet', compression='gzip')
    return df

def _remove_dupes(df: pd.DataFrame, subdir: Optional[str]=None, names=['var', 'hash', 'project', 'file']):
    df2 = get_df('dupes', subdir, names=names).drop(columns=['var'])

    df2 = df2[df2.duplicated(subset=['hash'])]
    df3 = pd.merge(df, df2, how='left', left_on=['project', 'file'], right_on=['project', 'file'])
    # df4 consists of rows in df3 where 'hash' is 'NaN' (meaning that they did not exist in df2.duplicated(subset=['hash']))
    df4 = df3[pd.isnull(df3['hash'])]
    return df4.drop(columns=['hash'])

def get_styler(df):
    if isinstance(df, pd.Series):
        return df.to_frame().style
    return df.style

def highlight_cols(styler):
    styler = styler.applymap_index(lambda x: 'textbf:--rwrap;', axis='columns')
    styler = styler.format_index(None, escape='latex', axis='columns')
    return styler.hide(names=True, axis='columns')

def highlight_rows(styler):
    styler = styler.applymap_index(lambda x: 'textbf:--rwrap;', axis='index')
    styler = styler.format_index(None, escape='latex', axis='index')
    return styler.hide(names=True, axis='index')

_colsepname = ''
def save_table(styler, filename: str, subdir: Optional[str]=None, decimals: Optional[int]=2, thousands: Optional[str]=',', colsep: Optional[str]=None, **kwargs):
    '''Saves a DataFrame to a LaTeX table.

    Args:
        styler: A Pandas Styler object for formatting a table.
        filename (str): The filename to save to, including '.tex' extension. Files are saved under 'tables/'.
        subdir (Optional[str]): the sub-directory, underneath 'tables/', to save in. Defaults to None.
        decimals (Optional[int]): How many decimal places for floats. Defaults to 2.
        thousands (Optional[str]): What mark should be used for thousands separator.  Defaults to ','.
        colsep (Optional[str]): If False, use default column separators.  If a string, it is the column separator units. Defaults to False.
    '''
    global _colsepname
    if colsep:
        _colsepname = _colsepname + 'A'

    with pd.option_context("max_colwidth", 1000):
        tab1 = styler.format(None, precision=decimals, thousands=thousands, escape='latex').to_latex(**kwargs)

    os.makedirs(f'tables/{_get_dir(subdir)}', 0o755, True)
    with open(f'tables/{_get_dir(subdir)}{filename}', 'w', encoding='utf-8') as f:
        f.write('% DO NOT EDIT\n')
        f.write('% this file was automatically generated by ' + os.path.basename(sys.argv[0]) + '\n')
        if colsep:
            f.write('\\newcommand{\\oldtabcolsep' + _colsepname + '}{\\tabcolsep}\n')
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + '}\n')
        f.write(tab1)
        if colsep:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + _colsepname + '}\n')

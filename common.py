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
import pandas as pd

def _get_dir(subdir):
    if subdir is None:
        return ''
    return subdir + '/'

def get_df(filename, subdir=None, **kwargs):
    try:
        df = pd.read_parquet(f'data/parquet/{_get_dir(subdir)}{filename}.parquet')
    except:
        df = pd.read_csv(f'data/csv/{_get_dir(subdir)}{filename}.csv', header=None, index_col=False, **kwargs)
        os.makedirs(f'data/parquet/{_get_dir(subdir)}', 0o755, True)
        df.to_parquet(f'data/parquet/{_get_dir(subdir)}{filename}.parquet', compression='gzip')
    return df

def get_deduped_df(filename, subdir=None, ts=False, **kwargs):
    '''This function assumes your table has columns named 'project' and 'file', and no column named 'hash'.'''
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

def _remove_dupes(df, subdir=None, names=['var', 'hash', 'project', 'file']):
    df2 = get_df('dupes', subdir, names=names).drop(columns=['var'])

    df2 = df2[df2.duplicated(subset=['hash'])]
    df3 = pd.merge(df, df2, how='left', left_on=['project', 'file'], right_on=['project', 'file'])
    # df4 consists of rows in df3 where 'hash' is 'NaN' (meaning that they did not exist in df2.duplicated(subset=['hash']))
    df4 = df3[pd.isnull(df3['hash'])]
    return df4.drop(columns=['hash'])

colsepname = ''
def save_table(df, filename, subdir=None, decimals=2, colsep=False, **kwargs):
    global colsepname
    if not colsep is False:
        colsepname = colsepname + 'A'

    pd.options.display.float_format = ('{:,.' + str(decimals) + 'f}').format

    with pd.option_context("max_colwidth", 1000):
        tab1 = df.to_latex(**kwargs)

    with open(f'tables/{_get_dir(subdir)}{filename}', 'w', encoding='utf-8') as f:
        f.write('% DO NOT EDIT\n')
        f.write('% this file was automatically generated\n')
        if not colsep is False:
            f.write('\\newcommand{\\oldtabcolsep' + colsepname + '}{\\tabcolsep}\n')
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + '}\n')
        f.write(tab1)
        if not colsep is False:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + colsepname + '}\n')

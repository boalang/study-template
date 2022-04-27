import pandas as pd

def get_dir(subdir):
    if subdir is None:
        return ''
    return subdir + '/'

def get_df(filename, subdir=None, **kwargs):
    try:
        df = pd.read_parquet(f'data/parquet/{get_dir(subdir)}{filename}.parquet')
    except:
        df = pd.read_csv(f'data/csv/{get_dir(subdir)}{filename}.csv', header=None, index_col=False, **kwargs)
        df.to_parquet(f'data/parquet/{get_dir(subdir)}{filename}.parquet', compression='gzip')
    return df

def get_deduped_df(filename, subdir=None, ts=False, **kwargs):
    try:
        df = pd.read_parquet(f'data/parquet/{get_dir(subdir)}{filename}-deduped.parquet')
    except:
        if ts:
            df = remove_dupes(get_df(filename, subdir, **kwargs), subdir, names=['var', 'hash', 'project', 'ts', 'file'])
        else:
            df = remove_dupes(get_df(filename, subdir, **kwargs), subdir)
        df.to_parquet(f'data/parquet/{get_dir(subdir)}{filename}-deduped.parquet', compression='gzip')
    return df

def remove_dupes(df, subdir=None, names=['var', 'hash', 'project', 'file']):
    df2 = get_df('dupes', subdir, names).drop(columns=['var'])

    df2 = df2[df2.duplicated(subset=['hash'])]
    df3 = pd.merge(df, df2, how='left', left_on=['project', 'file'], right_on=['project', 'file'])
    # df4 consists of rows in df3 where 'hash' is 'NaN' (meaning that they did not exist in df2.duplicated(subset=['hash']))
    df4 = df3[pd.isnull(df3['hash'])]
    return df4.drop(columns=['hash'])

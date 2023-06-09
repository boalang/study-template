#!/usr/bin/env python3
# coding: utf-8

import csv
from io import StringIO
import pandas as pd
import sys


def convertToMultiset(x):
    reader = csv.reader(StringIO(x), delimiter=',')
    for row in reader:
        s = set(row)
        if '' in s:
            s.remove('')
        return s
    return set()

def convertToSet(ms):
    try:
        return { x[x.index(':') + 1:] for x in ms }
    except Exception as e:
        print(ms)
        raise e

def jaccard(set1, set2):
    intersection = len(set1.intersection(set2))
    return float(intersection) / (len(set1) + len(set2) - intersection)

if __name__ == '__main__':
    df = pd.read_csv(sys.argv[1], header=None, names=['var', 'project', 'file', 'tokens']).drop(columns=['var'])
    df['mstokens'] = df['tokens'].apply(convertToMultiset)
    df['tokens'] = df['mstokens'].apply(convertToSet)

    vals = df['tokens'].values.tolist()
    msvals = df['mstokens'].values.tolist()
    df = df.drop(columns=['tokens', 'mstokens'])

    end = len(vals)
    if len(sys.argv) > 3:
        end = int(sys.argv[3])

    start = 0
    if len(sys.argv) > 2:
        start = int(sys.argv[2])
        vals = vals[start:]
        msvals = msvals[start:]

    totalpairs = len(vals) * (len(vals) - 1) // 2

    try:
        from tqdm import tqdm
        pbar = tqdm(total=totalpairs, dynamic_ncols=True) if totalpairs > 1000000 else None
    except ImportError:
        pbar = None

    try:
        dupes = set()
        for index, val in enumerate(vals[:(end - start)]):
            for index2, val2 in enumerate(vals):
                if index2 > index:
                    if pbar is not None:
                        pbar.update(1)
                    j = jaccard(val, val2)
                    if j <= 0.8:
                        j = 10.1 + jaccard(msvals[index], msvals[index2])
                    if j > 10.8:
                        row = df.iloc[start + index]
                        row2 = df.iloc[start + index2]

                        dupe = (int(row['project']), row['file'])
                        if dupe not in dupes:
                            tqdm.write(f"{row['project']},-1,\"{row['file']}\"")
                            dupes.add(dupe)

                        dupe = (int(row2['project']), row2['file'])
                        if dupe not in dupes:
                            tqdm.write(f"{row2['project']},{j},\"{row2['file']}\"")
                            dupes.add(dupe)
    finally:
        if pbar is not None:
            pbar.close()

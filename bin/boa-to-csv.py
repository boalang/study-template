#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import re


def valid_file(parser, arg):
    if os.path.exists(arg):
        return arg
    parser.error(f'Invalid path: {arg}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('boaToCsv.py')
    parser.add_argument('--test',
                        '-t',
                        action='append',
                        type=str,
                        help='add a "column,test" pair, where the given column keeps consuming the row until the given regex test matches')
    parser.add_argument('--drop',
                        '-d',
                        action='append',
                        type=int,
                        help='columns (0-indexed) to drop when converting')
    parser.add_argument('--header',
                        type=str,
                        help='a header row to prepend to the CSV output')
    parser.add_argument('--numidx',
                        type=int,
                        default=None,
                        help='number of indices in the Boa output - if not given, infers from the first line')
    parser.add_argument('filename',
                        metavar='boa-jobXX-output.txt',
                        action='store',
                        type=lambda x: valid_file(parser, x),
                        help='path to the Boa output file to convert')

    args = parser.parse_args()

    filesize = os.path.getsize(args.filename)
    try:
        from tqdm import tqdm
        pbar = tqdm(total=filesize) if filesize > 250000 else None
    except ImportError:
        pbar = None

    drop = []
    if args.drop is not None:
        for x in args.drop:
            drop.append(x)

    test = []
    ext = {}
    if args.test is not None:
        for x in args.test:
            xs = x.split(',')
            test.append(int(xs[0]))
            ext[int(xs[0])] = xs[1]

    try:
        with open(args.filename, encoding='utf-8') as f:
            if args.header is not None:
                print(args.header)

            s = f.readline()
            while s is not None and len(s) > 0:
                if pbar is not None:
                    pbar.update(len(s))

                if len(s.strip()) == 0:
                    continue

                s = s[:-1].replace('\\n', '\\\\n').replace('"', '""')
                parts = []

                cur = 0
                idx = s.find('[', cur)
                if idx > -1:
                    parts.append('"' + s[cur:idx] + '"')
                    cur = idx + 1

                    idx = s.find('][', cur)
                    while idx > -1 and idx < len(s) and (args.numidx is None or len(parts) < args.numidx):
                        if len(parts) in test:
                            while idx > -1 and idx < len(s) and not re.search(ext[len(parts)], s[cur:idx].lower()):
                                idx = s.find('][', idx + 2)
                            if idx == -1 or idx == len(s):
                                break
                        parts.append('"' + s[cur:idx] + '"')
                        cur = idx + 2
                        idx = s.find('][', cur)

                if args.numidx is None:
                    args.numidx = len(parts)

                idx = s.find('] = ', cur)
                if idx > -1:
                    parts.append('"' + s[cur:idx] + '"')
                    cur = idx + 1

                idx = s.find(' = ', cur)
                if idx > -1:
                    parts.append('"' + s[idx + 3:] + '"')

                parts2 = [x for i, x in enumerate(parts) if i not in drop]
                print(','.join(parts2))
                s = f.readline()
    finally:
        if pbar is not None:
            pbar.close()

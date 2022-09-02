#!/usr/bin/env python3
# coding: utf-8

import os
import sys

if __name__ == '__main__':
    filesize = os.path.getsize(sys.argv[1])
    try:
        from tqdm import tqdm
        pbar = tqdm(total=filesize) if filesize > 250000 else None
    except ImportError:
        pbar = None

    try:
        with open(sys.argv[1], 'r') as f:
            last = None
            lastline = None

            line = f.readline()
            while line:
                if pbar is not None:
                    pbar.update(len(line))
                current = line[2:line.find(']')]

                if current == last:
                    if lastline:
                        print(lastline, end='')
                        lastline = None
                    print(line, end='')
                else:
                    lastline = line

                last = current
                line = f.readline()
    finally:
        if pbar is not None:
            pbar.close()

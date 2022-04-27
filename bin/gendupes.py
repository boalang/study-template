#!/usr/bin/env python3
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
                current = line[2:line.find(']', line.find('][') + 2)]

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

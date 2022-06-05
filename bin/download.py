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
from boaapi.status import CompilerStatus, ExecutionStatus
from utilities import *

def run_query(target):
    logger.info('Running query again...')

    client = get_client()
    query, sha256 = prepare_query(target)
    job = client.query(query, get_dataset(target))

    logger.debug(f'Job {job.id} is running.')
    job.wait()
    logger.debug(f'Job {job.id} is complete.')

    if job.compiler_status is CompilerStatus.ERROR:
        logger.error(f'Job {job.id} had a compilation error.')
        logger.error(job.get_compiler_errors())
        exit(21)
    if job.exec_status is ExecutionStatus.ERROR:
        logger.error(f'Job {job.id} had an execution error.')
        logger.error(f'See url: {job.get_url()}')
        exit(22)

    update_query_data(target, job.id, sha256)

    outputPath = os.path.join(TXT_ROOT, target)
    if os.path.exists(outputPath):
        os.unlink(outputPath)

def download_query(target):
    logger.info(f'Downloading query output "{target}"...')

    job_data = get_query_data()

    client = get_client()
    job = client.get_job(job_data[target]['job'])

    job.set_public(get_make_public(target))

    target = TXT_ROOT + target
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w') as fh:
        fh.write(job.output())

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('target')
    args = parser.parse_args()

    verbosity = min(max(3 - args.verbose, 1), 3) * 10
    logger.setLevel(verbosity)
    logger.info(f'Setting verbosity to {verbosity}')

    target = args.target[len(TXT_ROOT):] # trim off 'data/txt/'

    if is_run_needed(target):
        run_query(target)

    if not os.path.exists(args.target):
        download_query(target)

    close_client()

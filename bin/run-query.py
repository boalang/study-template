#!/usr/bin/env python3
# coding: utf-8

from boaapi.status import CompilerStatus, ExecutionStatus
from utilities import *


def run_query(target, dataset):
    client = get_client()

    with open(target, 'r') as fh:
        query = fh.read()
    job = client.query(query, client.get_dataset(dataset))

    logger.debug(f'Job {job.id} is running...')
    with Timer():
        job.wait()
    logger.debug(f'Job {job.id} is complete.')

    if job.compiler_status is CompilerStatus.ERROR:
        logger.error(f'Job {job.id} had a compilation error.')
        for error in job.get_compiler_errors():
            logger.error(error)
        exit(21)
    if job.exec_status is ExecutionStatus.ERROR:
        logger.error(f'Job {job.id} had an execution error.')
        logger.error(f'See url: {job.get_url()}')
        exit(22)

    return job


def download_query(job, output):
    logger.info(f'Downloading query output "{output}"...')

    try:
        with Timer():
            with open(output, mode='w') as fh:
                fh.write(job.output())
    except Exception as e:
        print(e)
        exit(30)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--output', '-o', action='store', required=True)
    parser.add_argument('--verbose', '-v', action='count', default=3)
    parser.add_argument('queryfile')
    parser.add_argument('dataset')
    args = parser.parse_args()

    verbosity = min(max(3 - args.verbose, 1), 3) * 10
    logger.setLevel(verbosity)
    logger.info(f'Setting verbosity to {verbosity}')

    job = run_query(args.queryfile, args.dataset)
    download_query(job, args.output)

    close_client()

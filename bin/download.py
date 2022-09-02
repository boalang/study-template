#!/usr/bin/env python3
# coding: utf-8

from boaapi.status import CompilerStatus, ExecutionStatus
from hashlib import md5
from pathlib import Path
from utilities import *


def run_query(target):
    logger.info('Running query again...')

    client = get_client()
    query, sha256 = prepare_query(target)
    job = client.query(query, get_dataset(target))

    logger.debug(f'Job {job.id} is running...')
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

    update_query_data(target, job.id, sha256)

    target_path = Path(TXT_ROOT, target)
    if target_path.exists():
        target_path.unlink()


def download_query(target):
    logger.info(f'Downloading query output "{target}"...')

    job_data = get_query_data()

    client = get_client()
    job = client.get_job(job_data[target]['job'])

    job.set_public(get_make_public(target))

    target_path = Path(TXT_ROOT, target)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target_path.open(mode='w') as fh:
            fh.write(job.output())
    finally:
        # verifyDownload(target)
        pass


def verifyDownload(target):
    target_path = Path(TXT_ROOT, target)

    if not target_path.exists():
        return False

    job_data = get_query_data()

    client = get_client()
    job = client.get_job(job_data[target]['job'])

    actual_size = target_path.stat().st_size
    expected_size = int(job.output_size())
    if actual_size != expected_size:
        logger.warning(f"Downloaded output of {target} is {actual_size}, should be {expected_size}, deleting.")
        target_path.unlink()
        return False

    expected_hash = job.output_hash()
    with target_path.open(mode='r') as fh:
        data = fh.read(expected_hash[0])
    actual_hash = md5(str.encode(data)).hexdigest()
    if expected_hash[1] != actual_hash:
        logger.warning(f"Downloaded output of {target} has bad hash, retrying with different encoding.")
        data = str.encode(data, 'ascii', 'replace').decode('utf8')
        actual_hash = md5(str.encode(data)).hexdigest()
        if expected_hash[1] != actual_hash:
            logger.warning(f"Downloaded output of {target} has bad hash ({actual_hash}, was expecting {expected_hash[1]}), deleting.")
            target_path.unlink()
            return False

    target_path.touch()
    return True


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('target')
    args = parser.parse_args()

    verbosity = min(max(3 - args.verbose, 1), 3) * 10
    logger.setLevel(verbosity)
    logger.info(f'Setting verbosity to {verbosity}')

    target = args.target[len(TXT_ROOT):]  # trim off 'data/txt/'

    if is_run_needed(target):
        run_query(target)

    if not verifyDownload(target):
        download_query(target)

    close_client()

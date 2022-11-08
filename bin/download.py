#!/usr/bin/env python3
# coding: utf-8

from boaapi.status import CompilerStatus, ExecutionStatus
from hashlib import md5
from pathlib import Path
from utilities import *


def run_query(config, target):
    logger.info('Running query again...')

    client = get_client()
    query, hash = prepare_query(config, target)
    job = client.query(query, get_dataset(config, target))

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

    update_query_data(target, job.id, hash)

    target_path = Path(TXT_ROOT, target)
    if target_path.exists():
        target_path.unlink()


def download_query(config, target):
    target_path = Path(TXT_ROOT, target)
    logger.info(f'Downloading query output "{target_path}"...')

    job_data = get_query_data()

    client = get_client()
    job = client.get_job(job_data[target]['job'])

    job.set_public(get_make_public(config, target))

    target_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Timer():
            with target_path.open(mode='w') as fh:
                fh.write(job.output())
    except Exception as e:
        target_path.unlink()
        print(e)
        exit(30)
    finally:
        verifyDownload(target)


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
    with target_path.open(mode='rb') as fh:
        data = fh.read(expected_hash[0])
    actual_hash = md5(data).hexdigest()
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

    config = get_query_config()
    target = args.target[len(TXT_ROOT):]  # trim off 'data/txt/'

    if is_run_needed(config, target):
        run_query(config, target)

    if not verifyDownload(target):
        download_query(config, target)

    close_client()

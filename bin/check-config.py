#!/usr/bin/env python3
# coding: utf-8

import subprocess
from utilities import *


if __name__ == '__main__':
    config = get_query_config()
    data = get_query_data()

    for target in data:
        if target != "$schema":
            if 'queries' in config and target in config['queries']:
                newhash = sha256(str.encode(json.dumps(config['queries'][target], indent=2))).hexdigest()
            else:
                newhash = 'new'

            if target in data and 'config-hash' in data[target]:
                oldhash = data[target]['config-hash']
            else:
                oldhash = 'old'

            if oldhash != newhash:
                print('config cache changed for:', TXT_ROOT + target)
                print('  --> calling `make clean-' + TXT_ROOT + target + '`')
                subprocess.run(['make', f'clean-{TXT_ROOT}{target}'], stdout=sys.stdout, stderr=sys.stderr)

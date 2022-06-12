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
from utilities import get_query_config, build_replacements, TXT_ROOT, CSV_ROOT, PQ_ROOT, ANALYSIS_ROOT

if __name__ == '__main__':
    configuration = get_query_config()

    print('# DO NOT EDIT')
    print('# this file was automatically generated')
    print('DOWNLOAD:=bin/download.py $(VERBOSE)')
    print('BOATOCSV:=bin/boa-to-csv.py')
    print('GENDUPES:=bin/gendupes.py')
    print('MKDIR:=mkdir -p')
    print('')

    print('.PHONY: data')
    print('data: txt csv')

    txt = []
    csv = []

    for target in configuration['queries']:
        query_info = configuration['queries'][target]
        substitution_files = [x for (_, x) in build_replacements(configuration.get('substitutions', []), query_info.get('substitutions', []), only_files = True)]
        target = TXT_ROOT + target
        txt.append(target)

        clean_target = f'clean-{target}'

        print('')
        print(f'# Make targets for {target}')
        print(f'{clean_target} := {clean_target}')

        if 'csv' in query_info and 'output' in query_info['csv']:
            csv_info = query_info['csv']
            csv_output = CSV_ROOT + csv_info['output']
            csv.append(csv_output)

            filename = csv_info['output'][:-4]
            print('')
            print(f'{clean_target} += {csv_output}')
            print(f'{clean_target} += {PQ_ROOT}{filename}.parquet')
            print(f'{clean_target} += {PQ_ROOT}{filename}-deduped.parquet')
            print(f'{csv_output}: {target}')
            print('\t@$(MKDIR) $(dir $@)')
            string = '\t$(PYTHON) $(BOATOCSV)'
            if 'test' in csv_info:
                for test in csv_info['test']:
                    string += ' -t "' + test.replace('$', '$$') + '"'
            if 'drop' in csv_info:
                for d in csv_info['drop']:
                    string += f' -d {int(d)}'
            if 'header' in csv_info:
                string += f' --header "{csv_info["header"]}"'
            if 'numidx' in csv_info:
                string += f' --numidx {int(csv_info["index"])}'
            string += ' $< > $@'
            print(string)
            print(f'\t@$(RM) {PQ_ROOT}{filename}.parquet')
            print(f'\t@$(RM) {PQ_ROOT}{filename}-deduped.parquet')

        if 'gendupes' in query_info and 'output' in query_info['gendupes']:
            dupes_info = query_info['gendupes']
            dupes_txt = TXT_ROOT + dupes_info['output']
            txt.append(dupes_txt)

            print('')
            print(f'{clean_target} += {dupes_txt}')
            print(f'{dupes_txt}: {target} $(word 1, $(GENDUPES))')
            print('\t@$(MKDIR) $(dir $@)')
            print('\t$(PYTHON) $(GENDUPES) $< > $@')

            if 'csv' in dupes_info:
                dupes_csv  = CSV_ROOT + dupes_info['csv']
                csv.append(dupes_csv)

                print('')
                print(f'{clean_target} += {dupes_csv}')
                print(f'{clean_target} += {PQ_ROOT}$**/dupes.parquet')
                print(f'{clean_target} += {PQ_ROOT}$**/*-deduped.parquet')
                print(f'{dupes_csv}: {dupes_txt}')
                print('\t$(PYTHON) $(BOATOCSV) $< > $@')
                print(f'\t@$(RM) {PQ_ROOT}$**/dupes.parquet')
                print(f'\t@$(RM) {PQ_ROOT}$**/*-deduped.parquet')

        print('')
        string = f'boa/{query_info["query"]} '
        string += ' '.join(substitution_files)
        print(f'{target}: {string.strip()}')
        print('\t$(PYTHON) $(DOWNLOAD) $@')
        print('')

        print(f'.PHONY: {clean_target}')
        print(f'{clean_target}:')
        print(f'\t$(RM) $({clean_target}) ')

    print('')
    print('.PHONY: txt csv')
    print('txt: ' + ' '.join(txt))
    print('csv: ' + ' '.join(csv))


    analyses = []

    for script in configuration['analyses']:
        target = script.split('.')[0]
        analyses.append(target)

        inputs = configuration['analyses'][script]['input']
        inputs = [CSV_ROOT + x for x in inputs]

        print('')
        print(f'{target}: data {ANALYSIS_ROOT}{script} ' + ' '.join(inputs))
        print(f'\t$(PYTHON) {ANALYSIS_ROOT}{script}')

    if len(analyses) > 0:
        print('')
        print('.PHONY: analysis ' + ' '.join(analyses))
        print('analysis: ' + ' '.join(analyses))

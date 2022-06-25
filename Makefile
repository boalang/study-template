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

PYTHON:=python3
VERBOSE:=

ZIP:=zip
ZIPOPTIONS:=-u -r
ZIPIGNORES:=-x \*/.DS_Store -x \*/.gitkeep -x data/csv/\*


.PHONY: all
all: data analysis

include Makefile.study

Makefile.study: study-config.json bin/build-makefile.py
	jsonschema --instance study-config.json schemas/0.1.0/study-config.schema.json
	$(PYTHON) bin/build-makefile.py > $@


####################
# packaging targets
#
.PHONY: zip
zip:
	-$(ZIP) replication-pkg.zip $(ZIPOPTIONS) .vscode/*.json analyses/**/*.py analyses/*.py bin/**/*.py bin/*.py boa/ data/ figures/ schemas/ tables/ jobs.json LICENSE Makefile README.md requirements.txt study-config.json $(ZIPIGNORES)


################
# clean targets
#
.PHONY: clean clean-data clean-csv clean-pq clean-txt clean-zip clean-all

clean:
	rm -Rf __pycache__ bin/__pycache__
	rm -f figures/**/*.pdf figures/*.pdf
	rm -f tables/**/*.tex tables/*.tex

clean-data: clean-csv clean-pq clean-txt

clean-csv:
	rm -f data/csv/**/*.csv data/csv/*.csv

clean-pq:
	rm -f data/parquet/**/*.parquet data/parquet/*.parquet

clean-txt:
	rm -f data/txt/**/*.txt data/txt/*.txt

clean-zip:
	rm -f *.zip

clean-all: clean clean-data clean-zip

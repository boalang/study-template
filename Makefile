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

.PHONY: all
all: data analysis

include Makefile.jobs

Makefile.jobs: study-config.json bin/build-makefile.py
	jsonschema --instance study-config.json schemas/0.1.0/study-config.schema.json
	$(PYTHON) bin/build-makefile.py > $@


####################
# packaging targets
#
ZIP:=zip

ZIPOPTIONS:=-u -r
ZIPIGNORES:=-x \*/.DS_Store -x \*/.gitkeep -x data/csv/\*/\*.csv -x data/csv/*.csv

.PHONY: zip
zip:
	-$(ZIP) replication-pkg.zip $(ZIPOPTIONS) Makefile README.md LICENSE requirements.txt study-config.json jobs.json *.py bin/*.py boa/ figures/ tables/ data/ $(ZIPIGNORES)


################
# clean targets
#
.PHONY: clean clean-csv clean-pq clean-txt clean-zip clean-all

clean:
	rm -Rf __pycache__ bin/__pycache__
	rm -f figures/*/*.pdf figures/*.pdf
	rm -f tables/*/*.tex tables/*.tex

clean-csv:
	rm -f data/csv/*/*.csv data/csv/*.csv

clean-pq:
	rm -f data/parquet/*/*.parquet data/parquet/*.parquet

clean-txt:
	rm -f data/txt/*/*.txt data/txt/*.txt

clean-zip:
	rm -f *.zip

clean-all: clean clean-csv clean-pq clean-txt clean-zip

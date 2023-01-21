PYTHON:=python3
VERBOSE:=

ZIP:=zip
ZIPOPTIONS:=-u -r
ZIPIGNORES:=-x \*/.DS_Store -x \*/.gitkeep -x data/csv/\*


.PHONY: all
all: analysis

include Makefile.study

Makefile.study: study-config.json bin/build-makefile.py
	jsonschema --instance study-config.json schemas/0.1.2/study-config.schema.json
	$(PYTHON) bin/build-makefile.py > $@


####################
# packaging targets
#
.PHONY: package zip zenodo
zip: package
package:
	-$(ZIP) replication-pkg.zip $(ZIPOPTIONS) .vscode/*.json analyses/**/*.py analyses/*.py bin/**/*.py bin/*.py boa/ figures/ schemas/ tables/ jobs.json LICENSE Makefile README.md requirements.txt study-config.json $(ZIPIGNORES)
	-$(ZIP) data.zip $(ZIPOPTIONS) data/txt/ $(ZIPIGNORES)
	-$(ZIP) data-cache.zip $(ZIPOPTIONS) data/parquet/ $(ZIPIGNORES)

zenodo:
	$(PYTHON) bin/zenodo.py


################
# clean targets
#
.PHONY: clean clean-data clean-csv clean-pq clean-txt clean-zip clean-all

clean:
	${RM} -R __pycache__ bin/__pycache__
	${RM} figures/**/*.pdf figures/*.pdf figures/**/*.png figures/*.png
	${RM} tables/**/*.tex tables/*.tex

clean-data: clean-csv clean-pq clean-txt

clean-csv:
	${RM} data/csv/**/*.csv data/csv/*.csv

clean-pq:
	${RM} data/parquet/**/*.parquet data/parquet/*.parquet

clean-txt:
	${RM} data/txt/**/*.txt data/txt/*.txt

clean-zip:
	${RM} replication-pkg.zip data.zip data-cache.zip

clean-all: clean clean-data clean-zip

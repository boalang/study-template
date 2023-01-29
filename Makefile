# be sure to change this name if you build a Docker image
DOCKER-IMAGE:=study-template

# you might need to update some paths below, but probably not
PYTHON:=python3
VERBOSE:=

ZIP:=zip
ZIPOPTIONS:=-u -r
ZIPIGNORES:=-x \*/.DS_Store -x \*/.gitkeep -x data/csv/\*

DOWNLOAD:=$(PYTHON) bin/download.py $(VERBOSE)
BOATOCSV:=$(PYTHON) bin/boa-to-csv.py

JSONSCHEMA:=jsonschema
SED:=sed
MKDIR:=mkdir -p
CP:=cp -f


############################
# DO NOT MODIFY BELOW HERE #
############################

.PHONY: all
all: analysis

.PHONY: data
data: txt csv

include Makefile.study

Makefile.study: study-config.json bin/build-makefile.py
	$(JSONSCHEMA) --instance study-config.json schemas/0.1.2/study-config.schema.json
	$(PYTHON) bin/build-makefile.py > $@


####################
# packaging targets
#
.PHONY: package zip zenodo
zip: package
package:
	@$(CP) requirements.txt requirements.txt.save
	@$(SED) 's/>=/==/g' requirements.txt.save > requirements.txt
	-$(ZIP) replication-pkg.zip $(ZIPOPTIONS) .vscode/*.json analyses/**/*.py analyses/*.py bin/**/*.py bin/*.py boa/ figures/ schemas/ tables/ jobs.json LICENSE Makefile README.md requirements.txt study-config.json $(ZIPIGNORES)
	@$(CP) requirements.txt.save requirements.txt
	@$(RM) requirements.txt.save
	-$(ZIP) data.zip $(ZIPOPTIONS) data/txt/ $(ZIPIGNORES)
	-$(ZIP) data-cache.zip $(ZIPOPTIONS) data/parquet/ $(ZIPIGNORES)

.PHONY: docker run-docker
docker:
	@$(CP) requirements.txt requirements.txt.save
	@$(SED) 's/>=/==/g' requirements.txt.save > requirements.txt
	docker build -t $(DOCKER-IMAGE):latest .
	@$(CP) requirements.txt.save requirements.txt
	@$(RM) requirements.txt.save

run-docker: docker
	docker run -it -v $(shell pwd):/study $(DOCKER-IMAGE):latest

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

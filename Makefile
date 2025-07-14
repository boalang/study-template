# be sure to change this name if you build a Docker image
DOCKER-IMAGE:=study-template
IMAGE-STAMP:=.docker_built

# you might need to update some paths below, but probably not
PYTHON:=python3
VERBOSE:=

ZIP:=zip
ZIPOPTIONS:=-u -r
ZIPIGNORES:=-x \*.DS_Store\* -x \*.gitkeep\* -x data/csv/\*
ZENODO_DOWNLOAD=$(PYTHON) bin/zenodo-download.py

DOWNLOAD:=$(PYTHON) bin/download.py $(VERBOSE)
BOATOCSV:=$(PYTHON) bin/boa-to-csv.py

JSONSCHEMA:=check-jsonschema
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
	$(JSONSCHEMA) --verbose --schemafile schemas/0.1.2/study-config.schema.json study-config.json
	$(PYTHON) bin/build-makefile.py > $@


####################
# packaging targets
#
.PHONY: zip package package-replication package-data package-cache zenodo
zip: package
package: package-replication package-data package-cache

package-replication:
	@$(CP) requirements.txt requirements.txt.save
	@$(SED) 's/>=/==/g' requirements.txt.save > requirements.txt
	@$(CP) requirements-optional.txt requirements-optional.txt.save
	@$(SED) 's/>=/==/g' requirements-optional.txt.save > requirements-optional.txt
	-@echo "updating replication-pkg.zip..."; $(ZIP) replication-pkg.zip $(ZIPOPTIONS) .vscode/*.json $(shell find analyses/ -type f -name '*.py') $(shell find bin/ -type f -name '*.py') boa/ figures/ schemas/ tables/ jobs.json LICENSE Makefile Dockerfile README.md requirements.txt requirements-optional.txt study-config.json $(ZIPIGNORES)
	@$(CP) requirements.txt.save requirements.txt
	@$(CP) requirements-optional.txt.save requirements-optional.txt
	@$(RM) requirements.txt.save requirements-optional.txt.save
package-data:
	-@echo "updating data.zip..."; $(ZIP) data.zip $(ZIPOPTIONS) data/txt/ $(ZIPIGNORES)
package-cache:
	-@echo "updating data-cache.zip..."; $(ZIP) data-cache.zip $(ZIPOPTIONS) data/parquet/ $(ZIPIGNORES)

.PHONY: docker run-docker
docker: $(IMAGE-STAMP)
	@if [ "$$(cat $(IMAGE-STAMP))" -eq 0 ]; then :; else echo "Docker image build failed" && rm -f $(IMAGE-STAMP) && exit 1; fi

$(IMAGE-STAMP): Dockerfile requirements.txt
	@$(CP) requirements.txt requirements.txt.save
	@$(SED) 's/>=/==/g' requirements.txt.save > requirements.txt
	@$(CP) requirements-optional.txt requirements-optional.txt.save
	@$(SED) 's/>=/==/g' requirements-optional.txt.save > requirements-optional.txt
	-docker build -t $(DOCKER-IMAGE):latest . ; echo $$? > $(IMAGE-STAMP)
	@$(CP) requirements.txt.save requirements.txt
	@$(CP) requirements-optional.txt.save requirements-optional.txt
	@$(RM) requirements.txt.save requirements-optional.txt.save

run-docker: docker
	docker run -it -v $(shell pwd):/study $(DOCKER-IMAGE):latest

zenodo:
	$(PYTHON) bin/zenodo.py


##########################
# downloading from Zenodo
#
get-data:
	$(ZENODO_DOWNLOAD) data.zip

get-cache:
	$(ZENODO_DOWNLOAD) data-cache.zip


################
# clean targets
#
.PHONY: clean clean-figures clean-tables clean-data clean-csv clean-pq clean-txt clean-zip clean-all

clean: clean-figures clean-tables
	${RM} -R __pycache__ bin/__pycache__ analyses/**/__pycache__ analyses/__pycache__

clean-figures:
	${RM} figures/**/*.pdf figures/*.pdf figures/**/*.png figures/*.png

clean-tables:
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

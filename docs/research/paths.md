Here is an overview of the folder layout of the study template.

There are a few files in the root to be aware of.  There is a README and
LICENSE file for the study template.  Note that the README is named
`README-study-template.md`.  There is a second README named `sample-README.md`
that is a template for the README for your study.  You should copy this file to
`README.md` and edit it to describe your study.  Also update the `LICENSE` file
to reflect the license for your study.

There is also a `Makefile` to control running the analyses.  To go with that, a
`Makefile.study` gets automatically regenerated as you modify your study.

The `study-config.json` is the main entry point for the study.  This is where
you define datasets to query, queries, where to store the output, and the
analyses to run on that data.  This is the file that you will need to edit.
This is described further in other sections of the documentation.

Finally, there is a `jobs.json` that tracks the Boa job numbers for any queries
run. This file should not be directly modified.

### Queries: `boa/`

These are the Boa queries used to generate data for the paper.  You are free to
organize this folder however you like, for example by making subfolders for
different categories of queries.  If your study is querying multiple languages,
you may want to make a subfolder for each language.

### Data: `data/`

This is the output of the Boa queries (the `.txt`) files, as well as processed
versions of that output (`.csv` and `.parquet`).  While it can be sometimes
useful to inspect the raw output, most of the time you should not need to
access files in this folder.

### Analyses: `analyses/`

This is where the Python scripts for generating figures and tables go.

There is a subfolder `common/` that contains helper functions for processing
the data and generating figures/tables.

### Generated Figures: `figures/`

Any generated figures (`.pdf`) from the analyses will go into this folder.

### Generated Tables: `tables/`

Any generated tables (`.tex`) from the analyses will go into this folder.

### Other Folders

The `bin/` folder has scripts used by the study template for things like
submitting queries to Boa and downloading output, managing the Zenodo deposit,
and keeping the Makefile up to date.  You generally will not need to manually
run most of these, as the Makefile should manage things for you.

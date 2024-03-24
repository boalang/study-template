NOTE: this is a sample of a README.md file you could include with your
replication package.  You will want to rename this file to `README.md`.  Feel
free to use this as a starting point for your readme, as it has instructions
on using the generated replication pacakge.
================================

# Replication Package
## TODO: Put the name of your paper here

This replication package contains all data and scripts needed to reproduce the
results from the paper.

**TLDR: download `replication-pkg.zip` and `data-cache.zip` and run `make
reproduce` to re-generate all tables/figures.**

Note that all data was originally processed on a **TODO: put computer
information here**.

The raw data (`*.txt` files from Boa) is very large - around 14 GB
uncompressed.  The cached Parquet files are quite a bit smaller.  Depending on
your needs, you can probably skip downloading the `data.zip` file and only grab
the `data-cache.zip` file.  This should be enough to allow running `make
reproduce` to re-generate all tables and figures from the paper.

If you plan to make changes to any of the queries or analysis scripts, you will
probably want to also download `data.zip` and then run `make csv` to generate
all CSV files from the TXT files.

------------------------------------------------------

## Boa Study Template

This replication package utilizes the [Boa Study
Template](https://github.com/boalang/study-template).  For general details on
how to use replication packages built with the study template, see the [Using a
Replication
documentation](https://boalang.github.io/study-template/v0.3.0/replications/).

If you want to work with this package beyond simply re-generating the paper's
figures and tables, we **strongly** encourage you to utilize [Visual Studio
Code](https://code.visualstudio.com/) with the [Boa Language and Infrastructure
Extension](https://marketplace.visualstudio.com/items?itemName=Boa.boalang)
installed.  For more information, see the [Using the Template
documentation](https://boalang.github.io/study-template/v0.3.0/research/).

If you have that extension, you can avoid running terminal commands (like
`make`) and instead simply open the [study-config.json](study-config.json) file
to control what files you download, which analyses you run, etc.  For more
details on working with Boa's study template, see the [Using the Template
documentation](https://boalang.github.io/study-template/v0.3.0/research/).

------------------------------------------------------

## Requirements

You need a GNU Make compatible build system.  Tested on GNU Make 3.81.

Note that the Boa jobs themselves are marked public, so you do not need a Boa
user to view the actual jobs/output via the website.  However, the Boa API
requires a user/password to use it, so programmatically downloading (even
public jobs) currently requires authenticating.  You can, however, manually
download each of the query outputs from the public URLs.

### Python Requirements

Python 3 is required for all scripts.  Tested on Python **TODO: put Python
version used here**.

See `requirements.txt` for the package requirements.  To install them, run:

> pip3 install -r requirements.txt

There are also optional packages you can install to improve your experience.

#### Optional Python Requirements

If you install `tqdm>=4.64.0`, some scripts will display a progress bar.  This
can be very useful when processing extremely large (multi-GB) output files.

If you install `keyring>=23.8.2`, you can store your Boa API credentials in
your OS's keyring.  This is more secure than storing it in plaintext in the
`.env` file.  If you don't utilize either of those options, it will prompt you
for your username/password (once for **each** output it tries to download!).

------------------------------------------------------

## Docker Support

If you have Docker installed, you can use the provided `Dockerfile` to build an
image capable of running all the scripts.  This is the easiest way to get a
working environment.  To build and run the image, run:

> make run-docker

------------------------------------------------------

## File Organization

Here is an overview of the folders layout.  The root contains scripts for
generating tables/figures for the paper, a `Makefile` for running scripts, and
this `README.md` file.

### Subdir: `boa`
These are the Boa queries used to generate data for the paper.

### Subdir: `data`
This is the output of the Boa queries (the `.txt`) files, as well as processed
versions of that output (`.csv` and `.parquet`).

### Subdir: `figures`
Any generated figures (`.pdf`) will go into this folder.

### Subdir: `tables`
Any generated tables (`.tex`) will go into this folder.

------------------------------------------------------

## Getting Boa Output

**NOTE**: This step is only needed if you don't already have the output
downloaded!  If you downloaded `data.zip`, you can skip this step!

The first step is to run Boa queries to generate output TXT data for further
processing: `make txt`

### Processing the Boa Output

The Boa output is in a custom format, so first we convert it all into standard
CSV format: `make csvs`

If you use the `make data` command instead of manually obtaining the outputs,
you do not need to do anything else as it will call this target for you.

------------------------------------------------------

## Generating Figures and Tables

To generate all the figures and tables for the paper, you need to run the
analysis for each specific research question on the output from Boa.  There is
also a helper target to run all analyses:

> make analysis

Note that this triggers download of any missing Boa query outputs.  Or you can
run all analyses on only the cached data:

> make reproduce

If you want to run individual analyses, you can also do so:

> make rq1**TODO: update for your analysis script names**

> make rq2

You can also run a single analysis on the cached data by adding `-reproduce` to
the target name:

> make rq1-reproduce**TODO: update for your analysis script names**

> make rq2-reproduce

This replication package utilizes the [Boa Study
Template](https://github.com/boalang/study-template).  If you want to work with
this package beyond simply re-generating the paper's figures and tables, we
**strongly** encourage you to utilize [Visual Studio
Code](https://code.visualstudio.com/) with the [Boa Language and Infrastructure
Extension](vscode.md) installed.  For more information, see [Using the
Template](research/index.md).

If you have that extension, you can avoid running terminal commands (like
`make`) and instead simply open the study-config.json file to control what
files you download, which analyses you run, etc.  For more details on working
with Boa's study template, see the [online
documentation](https://github.com/boalang/study-template).

------------------------------------------------------

## Requirements

You need a GNU Make compatible build system.  Tested on GNU Make 3.81.

You will also need Python to run the analyses.  See the [Python
requirements](requirements.md#python-requirements) for more information.

Note that the Boa jobs themselves are marked public, so you do not need a Boa
user to view the actual jobs/output via the website.  However, the Boa API
requires a user/password to use it, so programmatically downloading (even
public jobs) currently requires authenticating.  You can, however, manually
download each of the query outputs from the public URLs.


------------------------------------------------------

## Docker Support

If you have Docker installed, you can use the provided `Dockerfile` to build an
image capable of running all the scripts.  This is the easiest way to get a
working environment.  To build and run the image, run:

```sh linenums="0"
make run-docker
```

------------------------------------------------------

## File Organization

The organization of a replication package is the same as in the original study.
See the page on [Paths](research/paths.md) for more information.

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

```sh linenums="0"
make analysis
```

Note that this triggers download of any missing Boa query outputs.  Or you can
run all analyses on only the cached data:

```sh linenums="0"
make reproduce
```

If you want to run individual analyses, you can also do so.  The specific
target names will vary based on the specific replication package, but often
they are named based on research question:

```sh linenums="0"
make rq1
```

```sh linenums="0"
make rq2
```

You can also run a single analysis on the cached data by adding `-reproduce` to
the target name:

```sh linenums="0"
make rq1-reproduce
```

```sh linenums="0"
make rq2-reproduce
```

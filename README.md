# boalang/study-template

A template for setting up an empirical study utilizing the Boa infrastructure.

Note that a username/password to the Boa website and API are required.  You
can request one here: https://boa.cs.iastate.edu/request/

Once you have an API login, edit the file `boa-credentials.txt` and enter your
username on the first line, then save and close the file.  We recommend also
setting your password in your OS keyring, so you are not prompted to enter it
each time a download triggers.  To do this, first install the keyring Python
package and then run:

```
keyring set boaapi <username>
```

where `<username>` is your Boa username.

## Requirements

You need a GNU Make compatible build system.  Tested on GNU Make 3.81.

### Python Requirements

Python 3 is required for all scripts.  Tested on Python 3.9.12.

See `requirements.txt` for the package requirements.  To install them, run:

```
pip3 install -r requirements.txt
```

There are also optional packages you can install to improve the experience.

#### Optional Python Requirements

If you install `tqdm`, some of the scripts will display a progress bar.  This
can be very useful when processing extremely large (multi-GB) output files.

If you install `keyring`, you can store your API credentials in your OS's
keyring.  This is more secure than storing it in plaintext in the
`boa-credentials.txt` file.  If you don't utilize either of those options, it
will prompt you for your username/password (once for **each** output it tries
to download!).

## Adding Queries

All information about what queries to run and where to download output is
stored in the `study-config.json` file.  This file is used to automatically
create a `Makefile.study` with make targets for each output file.

All Boa queries must reside under the `boa/` folder.  There are two sub-folders
under the query folder: `queries` and `snippets`.  `queries` is where you store
most of your Boa queries.  A few re-usable queries and examples are already
provided there.

The `snippets` folder is where the query templating system looks for any
included files.  The template system is described in the next section.

### `study-config.json` Schema

The most important file for your study is the `study-config.json` configuration
file.  This file defines all datasets, all queries (and their output file
paths), and any template substitutions needed to build the queries.

```json
  "datasets": {
    "custom_name": "Name of Boa Dataset",
    ...
  },
```

The first thing to include is at least one dataset.  Datasets are listed in the
`datasets` object.  Each dataset must have a unique `custom_name`.  This is the
name used to reference the dataset in a query.  The value is the name of the
Boa dataset, as on the Boa website.  You can list as many datasets here as you
want.

Listing datasets here makes it easy to repeat a study on a new dataset, as you
only need to update a single entry in the JSON file and all queries will pick
up the change.

The next object in the study config is the `queries` object:

```json
  "queries": {
    "kotlin/hashes.txt": {
      "query": "queries/hashes.boa",
      "dataset": "kotlin",
      "gendupes": {
        "output": "kotlin/dupes.txt",
        "csv": "kotlin/dupes.csv"
      }
    },
    "kotlin/rq1.txt": {
      "query": "queries/rq1.boa",
      "dataset": "kotlin",
      "csv": {
        "output": "kotlin/rq1.csv",
        "test": ["3,\\.kts?$"]
      }
    },
    ...
  },
```

This object contains output filenames as keys.  Note that all output here is
coming from Boa queries, so they are always TXT files stored under `data/txt/`.
You omit that prefix in the file paths listed here.  You can include
sub-folders if you want.

The values must have, at a minimum, `query` and `dataset` keys listing the path
to the Boa query stored under `boa/` (again, you omit that prefix here, but you
can point to any path under that folder) and the name of a dataset defined
earlier.

If for some reason you don't want the Boa job to be marked public, you can set
the `public` key to `false`.  By default, all submitted jobs will be marked
public after submission.

A query can also indicate if it should be converted to CSV format.  Most
queries probably want to convert to CSV, so you can easily load the data into
Pandas for analysis.  This is indicated by adding a `csv` key.  The value is an
object listing the `output` path for the CSV file (stored in `data/csv/`, with
the prefix omitted here) and some optional parameters:

* `test` (can be repeated)
  * Add a `"column,test"` pair, where the given column keeps consuming the row
    until the given regex test matches. This is useful because the output from
    Boa does not escape, so if a column (other than the last) contains strings
    and if those strings wind up having `][` in them (as some filenames do),
    the conversion script might break and create a jagged CSV table.
* `drop` (can be repeated)
  * Drop a column (0-indexed) when converting.
* `header`
  * A header row to prepend to the CSV output.  Can be useful it you think
    others might use the generated CSV files outside of your own analyses.
* `index`
  * Number of indices in the Boa output - if not given, infers from the first
    line.  This is usually not needed.

Finally, a query can also indicate if the `gendupes.py` script should run on
the output file.  This is used for queries that output file hashes from Boa, to
allow identifying duplicate files (based on matching AST hashes) for later
de-duplication during analysis.  The value takes the `output` path where to
store the generated TXT file with duplicate hash data (stored in `data/txt/`,
with the prefix omitted here).  It can also provide an optional `csv` key to
convert the generated TXT file into CSV format.

```json
  "substitutions": [
    {
      "target": "{@escape@}",
      "file": "escape.boa"
    },
    {
      "target": "{@project-filter@}",
      "replacement": ""
    }
  ]
```

The next object is the list of global template substitutions.  These
substitutions are available to every query, but can be overridden by specific
queries.  See the next section for more details.

```json
  "analyses": {
    "rq1.py": {
      "input": [
        "kotlin/rq1.csv",
        "kotlin/dupes.csv"
      ]
    }
  }
```

The last object is the list of analysis scripts you want to run.  See the
section on adding an analysis for more details.

### Query Templates

Query templates are defined through a list of substitutions.  Substitutions are
defined using two keys.  The `target` key is mandatory, containing the text
which is replaced in the query.  Targets must start with `{@` and end with
`@}`.  Target names are restricted to alpha-numeric characters, and some
special characters like `-_:.`.  Then, either `replacement` or `file` are used,
with `replacement` providing the text directly, and `file` being the name of a
file under `boa/snippets` which replaces `target`.  Care must be taken to
ensure that the query is valid Boa code after substitution is completed.

Before performing substitutions, a substitutions list is constructed, first from
local substitutions then from global substitutions.  If two substitutions
define the same `target`, the first one defined is used.  Substition will
iterate through the substitutions list until a loop has been completed without
any substitutions (i.e., a steady state has been reached).

## Adding Analyses

There is one sample analysis given in `analyses/rq1.py`.  This relies on the sample
query given in `boa/queries/rq1.boa` and makes use of deduplication, which relies
(indirectly) on the query given in `boa/queries/hashes.boa`.  This analysis will
generate a single result, the table in `tables/kotlin/rq1.tex`.

The steps to add a new analysis are as follows:

1. Create a new Boa query (e.g., `foo.boa`):\
   a. Store the file in `boa/queries/` - note you can create sub-folders here
      if you want.\
   b. Add any missing common snippets into `boa/snippets/`.\
   c. Add the query into the `study-config.json`.\
   d. Repeat Step 1 as many times as necessary.
2. Create a new Python script to analyze the data (e.g., `foo.py`) in the top
   folder.
3. Add a new entry to the `study-config.json` in the `analyses` object.\
   a. The name of the entry is the script filename (e.g., `foo.py`, without
      the `analyses/` prefix).\
   b. Add an `input` key, that is an array of CSV filenames that the analysis
      depends on.

Once this is done, you should be able to run `make foo` (the target is the
name of the script, without the file extension) to run the analysis task, or
run `make analysis` to run all analysis tasks.

## Building and the `jobs.json` Cache

To build, run `make`.  This will submit all queries, download their outputs,
convert them (where necessary), and run all analysis tasks to generate the
output tables/figures.

As Boa queries are submitted, the are marked public (unless specified not to)
and details about the submitted Boa job are cached in `jobs.json`.  This file
contains keys that are the name of an output TXT file (without the `data/txt/`
prefix).  The values are the `job` number and a `sha256` hash of the source
query (after running through the template engine).  The hash is used to
determine if the source query has changed and trigger re-submitted it.
Otherwise, the downloader will simply grab the output from the `job` specified.

## Packaging

If you run `make zip`, a replication package ZIP file will be generated.

## Cleanup

There are several `make` targets to clean up:

- `make clean` cleans up some temporary files and analysis outputs
- `make clean-csv` removes generates CSV files
- `make clean-pq` removes cached intermediate Parquet files
- `make clean-txt` removes downloaded TXT files
- `make clean-zip` removes any ZIP files
- `make clean-all` runs all of the clean targets

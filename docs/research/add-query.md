# Adding Queries

All information about what queries to run and where to download output is
stored in the [`study-config.json`](https://raw.githubusercontent.com/boalang/study-template/main/study-config.json) file.  This file is used
to automatically create a `Makefile.study` with make targets
for each output file.

All Boa queries must reside under the `boa/` folder.  There are two
sub-folders under the query folder: `boa/queries/` and
`boa/snippets/`.  `boa/queries/` is where you
store most of your Boa queries.  A few re-usable queries and examples are
already provided there.

The `boa/snippets/` folder is where the query template system
looks for any included files.  The template system is described in the next
section.

### study-config.json Schema

The most important file for your study is the
[`study-config.json`](https://raw.githubusercontent.com/boalang/study-template/main/study-config.json) configuration file.  This file defines
all datasets, all queries (and their output file paths), and any template
substitutions needed to build the queries.

#### Defining Datasets

```json title="study-config.json" linenums="3"
--8<-- "docs/study-config.example.json:3:10"
```

The first thing to include is at least one dataset.  Datasets are listed in the
`datasets` object.  Each dataset must have a unique `custom_name`.  This is the
name used to reference the dataset in a query.  The value is the name of the
Boa dataset, as on the Boa website.  You can list as many datasets here as you
want.

Listing datasets here makes it easy to repeat a study on a new dataset, as you
only need to update a single entry in the JSON file and all queries will pick
up the change.

#### Defining Queries

The next object in the study config is the `queries` object:

```json title="study-config.json" linenums="11"
--8<-- "docs/study-config.example.json:11:55"
```

This object contains output filenames as keys.  Note that all output here is
coming from Boa queries, so they are always TXT files stored under
`data/txt/`.  You omit that prefix in the file paths listed here.
You can include sub-folders if you want.

The values must have, at a minimum, `query` and `dataset` keys listing the path
to the Boa query stored under `boa/` (again, you omit that prefix here,
but you can point to any path under that folder) and the name of a dataset
defined earlier.

If for some reason you don't want the Boa job to be marked public, you can set
the `public` key to `false`.  By default, all submitted jobs will be marked
public after submission.

A query can also indicate if it should be converted to CSV format.  The output
of most queries will probably need to be converted to CSV, so you can easily
load the data into Pandas for analysis. This is indicated by adding a `csv` key.
The value is either a string listing the output path for the CSV file (stored in
`data/csv/`, with the prefix omitted here) or an object listing the `output`
path and some optional parameters:

* `test` (can be repeated)
    * Add a `"column,test"` pair, where the given column keeps consuming the row
      until the given regex test matches. This is useful because the output from
      Boa does not escape, so if a column (other than the last) contains strings
      and if those strings wind up having `][` in them (as some filenames do),
      the conversion script might break and create a jagged CSV table.
* `drop` (can be repeated)
    * Drop a column (0-indexed) when converting.
* `header`
    * A header row to prepend to the CSV output.  Can be useful if you think
      others might use the generated CSV files outside your own analyses.
* `index`
    * Number of indices in the Boa output - if not given, infers from the first
      line.  This is usually not needed.

Finally, a query can also indicate if the `gendupes.py`
script should run on the output file.  This is used for queries that output
file hashes from Boa, to allow identifying duplicate files (based on matching
AST hashes) for later de-duplication during analysis.  The value takes the
`output` path where to store the generated TXT file with duplicate hash data
(here, you must provide the `data/txt/` prefix).  It can also
provide an optional `csv` key to convert the generated TXT file into CSV format
(with the prefix omitted).  An optional `cacheclean` key allows listing
additional cache (Parquet) files to clean up when re-generating this output.

#### Defining Substitutions

```json title="study-config.json" linenums="56"
--8<-- "docs/study-config.example.json:56:65"
```

The next object is the list of global template substitutions.  These
substitutions are available to every query, but can be overridden by specific
queries.  See [templates](templates.md) for more details.

#### Defining Analyses

```json title="study-config.json" linenums="66"
--8<-- "docs/study-config.example.json:66:73"
```

The last object is the list of analysis scripts you want to run.  See the
section on [adding an analysis](add-analysis.md) for more details.

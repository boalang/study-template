To build, run `make`.  This will submit all queries, download their outputs,
convert them (where necessary), and run all analysis tasks to generate the
output tables/figures.

As Boa queries are submitted, they are marked public (unless specified not to)
and details about the submitted Boa job are cached in `jobs.json`.
This file contains keys that are the name of an output TXT file (without the
`data/txt/` prefix).  The values are the `job` number and a
`sha256` hash of the source query (after running through the template engine).
The hash is used to determine if the source query has changed and trigger
re-submitted it.  Otherwise, the downloader will simply grab the output from
the `job` specified.

## Cleanup

There are several `make` targets to clean up:

- `make clean` cleans up some temporary files and analysis outputs
- `make clean-figures` removes generated figures (`.pdf` and .png anywhere in `figures/`)
- `make clean-tables` removes generated tables (`.tex` anywhere in `tables/`)
- `make clean-txt` removes downloaded TXT files
- `make clean-csv` removes generated CSV files
- `make clean-pq` removes cached/intermediate Parquet files
- `make clean-zip` removes generated ZIP files
- `make clean-all` runs all the clean targets

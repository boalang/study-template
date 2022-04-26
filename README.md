# boalang/study-template

A template for setting up an empirical study utilizing the Boa infrastructure.

Note that a username/password to the Boa website and API are required.

## Requirements

You need a GNU Make 3.81 compatible build system.

### Python Requirements

See `requirements.txt` for the official requirements.  There are also optional
packages you can install to improve the experience.

If you install `tqdm`, some of the scripts will display a progress bar.  This
can be very useful when processing extremely large (multi-GB) output files.

If you install `keyring`, you can store your API credentials in your OS's
keyring.  This is more secure than storing it in plaintext in the
`boa-credentials.txt` file.  If you don't utilize either of those options, it
will prompt you for your username/password (once for **each** file it tries to
download!).

## Adding Queries

All information about the queries to run and download output from is stored in
the `job-config.json` file.

TODO

## Adding Analyses

TODO

## Building

To build, run `make`.

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

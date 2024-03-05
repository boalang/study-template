## Adding a README.md file

Your replication package will need a README file.  We provide a template file,
[`sample-README.md`](https://raw.githubusercontent.com/boalang/study-template/main/sample-README.md), that you can use as a starting point
for your package.  Just rename the file to `README.md` and edit accordingly.
There are several places with "TODO" notices that you will definitely want to
change.  And we recommend also adding a section at the end that describes each
analysis in a bit more detail.

## *(optional)* Configuring Docker Support

The study template has a sample [`Dockerfile`](https://raw.githubusercontent.com/boalang/study-template/main/Dockerfile) to build a Python-based container
that is capable of building the study.  You will need to update two things.
First, update the version of Python used.  Currently, the Dockerfile is set to
Python 3.10, so if you used a newer version of Python be sure to update.  Try
to use a concrete version (e.g., `3.11.2`) rather than a generic version.
Second, you will want to edit the `Makefile` to change the name of the
generated Docker image.  By default, the image will be named "study-template".

## Packaging

If you run `make package`, replication package ZIP files will be generated.  It
generates three different ZIP files:

- `replication-pkg.zip`
    - The main replication package and should include all Boa queries, analysis scripts, support scripts, and additional things like the documentation and Makefile.
- `data-cache.zip`
    - The pre-processed Parquet files.  This is the cache of the raw data files, in a compressed binary format.
- `data.zip`
    - The contents of the `data/txt/` folder, which is the raw outputs from Boa.

Most people simply trying to regenerate the tables/figures will only need the
first and second files.  The file with the full data is typically quite large
and only needed if someone plans to extend/enhance the analyses somehow.

Note that the command updates existing ZIP files if they exist, so you can
simply re-run it after small changes to a few files and it will update.  It
will not, however, remove any files from the ZIP files so if you wind up
deleting a query/analysis you either need to remove the ZIPs with `make
clean-zip` and regenerate, or manually run the `zip` command and remove file(s)
from the generates ZIPs.

## Publishing the Package

Once you have build your replication package, you can also upload it to Zenodo.
To do so, you will need to create a `.env` file with the following
contents:

```sh title=".env"
ZENODO_API_TOKEN='<your API token here>'
ZENODO_API_ENDPOINT='https://zenodo.org'
# or for testing:
ZENODO_API_ENDPOINT='https://sandbox.zenodo.org'
```

This requires logging into Zenodo and creating an API token.  Be sure to not
share the `.env` file with anyone once you create it!  It will not be
placed into any ZIP files and is ignored by Git, but you will still want to be
careful with it.

Then select an API endpoint.  If you want to test creating a Zenodo record you
can utilize their sandbox server.  Otherwise, use the main server.  Note that
if you use the sandbox, you need to create a token *on that server*, as tokens
are not shared across the two servers.

To utilize the script, simply run `make zenodo`.

The metadata for the Zenodo record is stored in the
`.zenodo.json` file.  This file can be shared and by default is
stored in Git.  If one does not exist, the first time you run the command one
will be generated and it will stop processing to allow you time to edit it.
This file contains the metadata for your record, including things like the
title, description, creators, and license info.  By default, we selected
CC-By-4.0 as the license, so feel free to change it if needed.

For a double-blinded submission, you will want to ensure the creators are
listed as anonymous and the access rights set to "open":

```json title=".zenodo.json" linenums="15"
    "creators": [
        {
            "affiliation": "Anonymous",
            "name": "Anonymous"
        }
    ],
    "access_right": "open",
```

After your paper is published, you can update the metadata and re-run the
script to have it update the metadata with your actual author name(s).

For more details on the metadata JSON format, see this link:
[https://developers.zenodo.org/#representation](https://developers.zenodo.org/#representation)

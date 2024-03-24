# boalang/study-template

A template for setting up an empirical study utilizing the [Boa infrastructure](https://boa.cs.iastate.edu/).  Using this template provides several benefits:

- Automatic management of Boa scripts and data
- A template system for Boa queries
- A Docker-based environment for people to easily replicate your study
- Automated publishing to Zenodo, including handling of double-blinded submissions

See the [online documentation](https://boalang.github.io/study-template/v0.3.0/) for more details on how to use the study template.

- [Requirements](#requirements)
- [Performing Research With This Template](#performing-research-with-this-template)
- [Using a Replication Package Built With This Template](#using-a-replication-package-built-with-this-template)

## Requirements

You need a GNU Make compatible build system and Python.  See the [full requirements](https://boalang.github.io/study-template/v0.3.0/requirements/) for more details.

## Performing Research With This Template

Note that a username/password to the Boa website and API are required.  You
can request one here: https://boa.cs.iastate.edu/request/

See the [online documentation for Using the Template](https://boalang.github.io/study-template/v0.3.0/research/) for more details.

### Adding a README.md file

Your replication package will need a README file.  We provide a template file,
[`sample-README.md`](sample-README.md), that you can use as a starting point
for your package.  Just rename the file to `README.md` and edit accordingly.
There are several places with "TODO" notices that you will definitely want to
change.  And we recommend also adding a section at the end that describes each
analysis in a bit more detail.

## Using a Replication Package Built With This Template

See the [online documentation for Using a Replication](https://boalang.github.io/study-template/v0.3.0/replications/) for more details.

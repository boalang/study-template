You need a GNU Make compatible build system.  Tested on GNU Make 3.81.

## Boa API Access

A username/password to the Boa website and API are required to use the study template.  You can request one here:
[https://boa.cs.iastate.edu/request/](https://boa.cs.iastate.edu/request/)

## Python Requirements

Python 3 is required for all scripts.  Tested on Python 3.9.12.

See [`requirements.txt`](https://raw.githubusercontent.com/boalang/study-template/main/requirements.txt) for the package requirements.  To install them, run:

```sh linenums="0"
pip3 install -r requirements.txt
```

There are also optional packages you can install to improve the experience.

## Optional Python Requirements

If you install `tqdm`, some scripts will display a progress bar.  This
can be very useful when processing extremely large (multi-GB) output files.

If you install `keyring`, you can store your API credentials in your
OS's keyring.  This is more secure than storing it in plaintext in the
`.env` file.  If you don't utilize either of those options, it will
prompt you for your username/password (once for **each** output it tries to
download!).

See [`requirements-optional.txt`](https://raw.githubusercontent.com/boalang/study-template/main/requirements-optional.txt) for the package requirements.  To install them, run:

```sh linenums="0"
pip3 install -r requirements-optional.txt
```

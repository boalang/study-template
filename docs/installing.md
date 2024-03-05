## Boa API Credentials

/// admonition | Boa API Access for New Studies
    type: warning

If you are starting a new research study and utilizing Boa's study template,
a username/password to the Boa website and API are required.  See the
full [list of requirements](requirements.md) for more details.
///

/// admonition | Boa API Access for Replication Packages
    type: tip

If you are using a replication package that utilized Boa's study template,
you should not need any Boa API credentials (unless you wish to re-run the
Boa queries in the package or intend to make changes to the study).
///

Once you have a Boa API login, edit the file `.env` and enter your
username as `BOA_API_USER='<username here>'`, then save and close the file.

We recommend also setting your password in your OS keyring, so you are not
prompted to enter it each time a download triggers.  To do this, first install
the `keyring` Python package and then run:

```sh linenums="0"
keyring set boaapi <username>
```

where `<username>` is your Boa username.

If you are unable to use the keyring, you can also enter your password into the `.env` file as
`BOA_API_PW='<password here>'`.

Finally, if the script can't find your
username and/or password, it will prompt you for it.  Note however it will
prompt *for each file it downloads*.

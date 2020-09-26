# keepassx_pw_finder

## Overview
Password-management aid tool


Helps you find passwords matching a specific regex in your keepassx db. Useful
when you believe a shared pw or a pw root is compromised and you want to expire
said pw root/shared pw everywhere at once.

To avoid having to enter your password at every run, pass the `--timeout NUM` flag
to cache the unlocked db in a daemon process that will survive between runs.
Caching in memory is disabled by default.

Recommended: https://keepassxc.org/

## Build:
```
cd ./keepassx_pw_finder
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
make
```
You should now have a `.pex` file in `./build` that you can copy and run anywhere
without needing to activate the virtual environment. It should Just Work (TM)

## Run
```
usage: keepassx_pw_finder.py [-h] [-d] [-k KEY_FILE] [--no-regex]
                             [--re-flags [RE_FLAGS [RE_FLAGS ...]]]
                             [-t TIMEOUT] [--enable-history]
                             db needle

positional arguments:
  db                    db file to examine
  needle                password pattern to search for

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable debug logging information
  -k KEY_FILE, --key-file KEY_FILE
  --no-regex            use exact password matching instead of regex
  --re-flags [RE_FLAGS [RE_FLAGS ...]]
                        additional regex flags to pass to
                        `find_entries_by_password`
  -t TIMEOUT, --timeout TIMEOUT
                        cache the unlocked db for TIMEOUT seconds between
                        program runs, to allow for not having to reenter the
                        password at every run. Default is disabled
  --enable-history      display entries from history that are no longer being
                        used today
```

## Contributing
Don't forget to run the `black` auto-formatter before committing!
```
black src/keepassx_pw_finder.py
```

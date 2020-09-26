Password-management aid tool

Helps you find passwords matching a specific regex in your keepassx db. Useful
when you believe a shared pw or a pw root is compromised and you want to expire
said pw root/shared pw everywhere at once

Recommended: https://keepassxc.org/

Usage: keepassx_pw_finder.py [-h] [-d] [-k KEY_FILE] [--no-regex]
                             [--re-flags [RE_FLAGS [RE_FLAGS ...]]]
                             [-t TIMEOUT] [--enable-history]
                             db needle

positional arguments:
  db                    db file to examine
  needle                password PCRE pattern to search for

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable debug logging information
  -k KEY_FILE, --key-file KEY_FILE
  --no-regex            use exact password matching instead of regex
  --re-flags [RE_FLAGS [RE_FLAGS ...]]
                        additional regex flags to pass to
                        `find_entries_by_password`
  -t TIMEOUT, --timeout TIMEOUT
                        how long to cache the db in memory for (0 to disable)
  --enable-history      display entries from history that are no longer being
                        used today

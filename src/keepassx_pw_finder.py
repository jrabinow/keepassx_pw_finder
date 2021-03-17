#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Helps you find passwords matching a specific regex in your keepassx db. Useful
when you believe a shared pw or a pw root is compromised and you want to expire
it everywhere at once
"""

from typing import List, Optional
from pykeepass import PyKeePass as PyKeePassNoCache, entry
from pykeepass_cache import PyKeePass as PyKeePassWithCache, cached_databases
from pykeepass.exceptions import CredentialsError

import argparse
import getpass
import logging
import os
import stat

import rpyc

rpyc.core.vinegar._generic_exceptions_cache["pykeepass.exceptions.CredentialsError"] = CredentialsError

LOG: logging.Logger = logging.getLogger()
LOG.setLevel("INFO")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(formatter)
LOG.addHandler(ch)


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="enable debug logging information",
    )
    parser.add_argument(
        "-k",
        "--key-file",
        help="key file to unlock keypassx db",
    )
    parser.add_argument(
        "--no-regex",
        default=False,
        action="store_true",
        help="use exact password matching instead of regex",
    )
    parser.add_argument(
        "--re-flags",
        nargs="*",
        default="I",
        help="additional regex flags to pass to `find_entries_by_password`",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        default=0,
        type=int,
        help="cache the unlocked db for TIMEOUT seconds between program runs, to"
        " allow for not having to reenter the password at every run. Default is"
        " disabled",
    )
    parser.add_argument(
        "--enable-history",
        action="store_true",
        help="display entries from history that are no longer being used today",
    )
    parser.add_argument("db", help="db file to examine")
    parser.add_argument("needle", help="password pattern to search for")
    return parser.parse_args()


def is_dir_world_readable(directory: str = ".") -> bool:
    st: os.stat_result = os.stat(directory)
    return bool(st.st_mode & stat.S_IROTH)


def get_entries_from_db(
    db_file: str,
    key_file: str,
    needle: str,
    socket_path: str = "./pykeepass_socket",
    needle_is_regex: bool = True,
    re_flags: str = "I",
    enable_history_search: bool = False,
    timeout: int = 0,
) -> List[entry.Entry]:

    use_cache: bool = False
    if timeout > 0:
        if is_dir_world_readable():
            LOG.warning(
                "current dir is world-readable; you will have to enter your pw "
                "at every call to avoid security risks"
            )
        else:
            use_cache = True

    password: Optional[str] = None
    if use_cache:
        if db_file not in cached_databases(socket_path=socket_path):
            password = getpass.getpass()
        kp = PyKeePassWithCache(
            db_file,
            password=password,
            keyfile=key_file,
            timeout=timeout,
            socket_path=socket_path,
        )
    else:
        password = getpass.getpass()
        kp = PyKeePassNoCache(
            db_file,
            password=password,
            keyfile=key_file,
        )

    entries: List[entry.Entry] = kp.find_entries_by_password(
        needle,
        regex=needle_is_regex,
        flags=re_flags,
        history=enable_history_search,
    )
    return entries


def main():
    args = parse_args()
    args.re_flags = "|".join(args.re_flags)

    try:
        entries = get_entries_from_db(
            args.db,
            args.key_file,
            args.needle,
            needle_is_regex=not args.no_regex,
            re_flags=args.re_flags,
            enable_history_search=args.enable_history,
            timeout=args.timeout,
        )

        for e in entries:
            print(e)
    except CredentialsError as e:
        LOG.fatal("bad credentials")


if __name__ == "__main__":
    main()

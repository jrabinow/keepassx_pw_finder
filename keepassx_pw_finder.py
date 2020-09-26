#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Helps you find passwords matching a specific regex in your keepassx db. Useful
when you believe a shared pw or a pw root is compromised and you want to expire
it everywhere at once
"""

import argparse
import getpass
import logging
import os
import stat

LOG = logging.getLogger()
LOG.setLevel("INFO")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(formatter)
LOG.addHandler(ch)


def parse_args():
    parser = argparse.ArgumentParser(
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


def is_dir_world_readable(directory="."):
    st = os.stat(directory)
    return bool(st.st_mode & stat.S_IROTH)


def pykeepass_with_cache(args):
    from pykeepass_cache import PyKeePass, cached_databases

    socket_path = "./pykeepass_socket"

    if args.db not in cached_databases(socket_path=socket_path):
        pw = getpass.getpass()
    else:
        pw = None

    kp = PyKeePass(
        args.db,
        password=pw,
        keyfile=args.key_file,
        timeout=args.timeout,
        socket_path=socket_path,
    )
    entries = kp.find_entries_by_password(
        args.needle,
        regex=not args.no_regex,
        flags=args.re_flags,
        history=args.enable_history,
    )
    return entries


def pykeepass_nocache(args):
    from pykeepass import PyKeePass

    pw = getpass.getpass()
    kp = PyKeePass(
        args.db,
        password=pw,
        keyfile=args.key_file,
    )
    entries = kp.find_entries_by_password(
        args.needle,
        regex=not args.no_regex,
        flags=args.re_flags,
        history=args.enable_history,
    )
    return entries


def main():
    args = parse_args()
    args.re_flags = "|".join(args.re_flags)

    use_cache = False
    if args.timeout > 0:
        if is_dir_world_readable():
            LOG.warning(
                "current dir is world-readable; you will have to enter your pw "
                "at every call to avoid security risks"
            )
        else:
            use_cache = True

    if use_cache:
        entries = pykeepass_with_cache(args)
    else:
        entries = pykeepass_nocache(args)

    for e in entries:
        print(e)


if __name__ == "__main__":
    main()

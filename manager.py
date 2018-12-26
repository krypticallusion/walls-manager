#!/usr/bin/env python3
import argparse
import configparser

from stats import parse_and_display_stats
from sync import sync_to_remote, sync_to_local

config = configparser.ConfigParser()
config.read("config.ini")
remote_dirs = config["DEST"]["RSYNC_DIRS"]
local_dir = config["SOURCE"]["DIR"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sync", help="Set direction of sync, local for pull and remote for push", type=str)
    parser.add_argument("-d", "--details", help="List statistics of local directory", action="store_true")
    args = parser.parse_args()

    if args.sync and args.sync == "remote":
        sync_to_remote(remote_dirs, local_dir)
    elif args.sync and args.sync == "local":
        # The adjustments below are required to replicate the sync_to_remote
        # semantics when we do this reverse sync.
        # We choose the first in the remote_dirs to be our primary and reliable
        # mirror, then append a trailing slash, and remove the same slash
        # from the local directory. Gotta love rsync.
        sync_to_local(remote_dirs.split(",")[0] + '/', local_dir[0:-1])
    elif args.details:
        parse_and_display_stats(local_dir)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

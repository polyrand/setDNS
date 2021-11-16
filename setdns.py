#!/usr/bin/env python3

import sys
import subprocess
import argparse


servers = [
    "1.1.1.1",
    "1.0.0.1",
    "1.1.1.2",
    "1.0.0.2",
    "2606:4700:4700::1111",
    "2606:4700:4700::1001",
    "2606:4700:4700::1112",
    "2606:4700:4700::1002",
]  # cloudflare DNS servers


flush_1_cmd = ["sudo", "dscacheutil", "-flushcache"]
flush_2_cmd = ["sudo", "killall", "-HUP", "mDNSResponder"]
default_cmd = ["networksetup", "-setdnsservers", "Wi-Fi"] + servers
remove_cmd = ["networksetup", "-setdnsservers", "Wi-Fi", "Empty"]
check_cmd = ["networksetup", "-getdnsservers", "Wi-Fi"]


def process_or_error(cmd, err):
    print(cmd)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        p.check_returncode()
        print(p.stdout.strip())
    except subprocess.CalledProcessError:
        print(p.stderr, file=sys.stderr)
        if err:
            # this should use logging but ¯\_(ツ)_/¯
            print(err, file=sys.stderr)
        raise SystemExit


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--flush", action="store_true", help="Flush DNS cache")
    parser.add_argument(
        "-c", "--check", action="store_true", help="Check current settings"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d",
        "--default",
        action="store_true",
        help="Set DNS servers to 1.1.1.1 and/or 1.0.0.1",
    )
    group.add_argument(
        "-r", "--remove", action="store_true", help="Remove current DNS settings"
    )
    group.add_argument("--local", action="store_true", help="Use server in resolv.conf")

    args = parser.parse_args()

    if args.check:
        process_or_error(check_cmd, "Couldn't check default settings")

    if args.remove:
        process_or_error(remove_cmd, "Couldn't remove current DNS servers")

    if args.default:
        process_or_error(default_cmd, "Couldn't set default servers")

    if args.flush:
        process_or_error(flush_1_cmd, "Could not flush DNS cache")
        process_or_error(flush_2_cmd, "Could not flush DNS cache (2)")

    raise SystemExit

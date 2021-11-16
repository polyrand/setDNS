#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path
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
scutil_cmd = ["scutil", "--dns"]


def e(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def process_or_error(cmd, err):
    # print(cmd)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        p.check_returncode()
        return p.stdout.strip()
    except subprocess.CalledProcessError:
        e(p.stderr)
        if err:
            # this should use logging but ¯\_(ツ)_/¯
            e(err)
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
    parser.add_argument(
        "--local",
        action="store_true",
        help="Show DNS servers used as reported by scutil",
    )

    parser.add_argument(
        "--resolv", action="store_true", help="Show servers in /etc/resolv.conf"
    )

    args = parser.parse_args()

    if args.check:
        e("Checking default DNS settings")
        out = process_or_error(check_cmd, "Couldn't check default settings")
        print(out)

    if args.remove:
        e("Removing all DNS servers (empty'ing config)")
        out = process_or_error(remove_cmd, "Couldn't remove current DNS servers")
        print(out)

    if args.default:
        e("Setting default (cloudflare) dns servers")
        out = process_or_error(default_cmd, "Couldn't set default servers")
        print(out)

    if args.flush:
        e("Flushing DNS caches")
        out = process_or_error(flush_1_cmd, "Could not flush DNS cache")
        print(out)
        out = process_or_error(flush_2_cmd, "Could not flush DNS cache (2)")
        print(out)

    if args.resolv:
        e("Reading /etc/resolv.conf")
        data = Path("/etc/resolv.conf").read_text()
        for line in data.split("\n"):
            if "nameserver" in line:
                server_ip = line.strip().split()[1]
                print(server_ip)

    if args.local:
        e("Checking local DNS using scutil")
        scutil_dns_out = process_or_error(scutil_cmd, "Could run scutil --dns")

        main_resolver_group = None
        for group in scutil_dns_out.split("\n\n"):
            if "resolver #1" in group:
                main_resolver_group = group

        if not main_resolver_group:
            raise ValueError("No resolver group #1 found with scutil --dns")

        for line in main_resolver_group.split("\n"):
            line = line.strip()
            if "nameserver" in line:
                server_addr = line.split(" : ")[-1]
                print(server_addr)

    raise SystemExit

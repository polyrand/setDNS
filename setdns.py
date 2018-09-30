#!/usr/bin/env python3

import sys
import subprocess
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--flush", action="store_true",
    help="Flush DNS cache")
ap.add_argument("-d", "--default", action="store_true",
    help="Set DNS servers to 1.1.1.1 and/or 1.0.0.1")
ap.add_argument("-rm", "--remove", action="store_true",
    help="Remove current DNS settings")
ap.add_argument("-c", "--check", action="store_true",
    help="Check current settings")
args = vars(ap.parse_args())

servers = ["1.1.1.1", "1.0.0.1"] # cloudflare DNS servers

flush_1 = r"sudo dscacheutil -flushcache"
flush_2 = r"sudo killall -HUP mDNSResponder"

default = f"networksetup -setdnsservers Wi-Fi {servers[0]} {servers[1]}"

remove = r'networksetup -setdnsservers Wi-Fi "Empty"'

check = r"networksetup -getdnsservers Wi-Fi"

if args['remove'] is not False:
    try:
        subprocess.run(remove, shell=True, check=True)
    except:
        print("Error occurred, couldn't remove current DNS servers")
    if args['flush'] is not False:
        try:
            subprocess.run(flush_1, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Could not flush DNS cache")
            sys.exit(1)
        try:
            subprocess.run(flush_2, shell=True, check=True)
        except:
            print("Couldn't flush")
            sys.exit(1)


if args['flush'] is not False:
    try:
        subprocess.run(flush_1, shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Could not flush DNS cache")
        sys.exit(1)
    try:
        subprocess.run(flush_2, shell=True, check=True)
    except:
        print("Couldn't flush")
        sys.exit(1)
if args['default'] is not False:
    try:
        subprocess.run(default, shell=True, check=True)
    except:
        print("Couldn't set default servers")
        sys.exit(1)

if args['check'] is not False:
    try:
        subprocess.run(check, shell=True, check=True)
    except:
        print("Couldn't check default settinfs")
        sys.exit(1)

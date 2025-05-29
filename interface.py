#!/usr/bin/env python3
import argparse
from verifier import verify as verifyOnionUrls

parser = argparse.ArgumentParser(
    prog='dark web scraper',
    description="Cmd interface for the application"
    )

parser.add_argument('-d', '--domain', type=str, required=False)
parser.add_argument('-n', '--name', type=str, required=False)
parser.add_argument('-l', '--latest', type=bool, required=False, default=False)
parser.add_argument('-s', '--static', action='store_true', required=False, default=False)
parser.add_argument('-a', '--all', action='store_true', required=False, default=False)
parser.add_argument('--verify', action='store_true', required=False, default=False)
    
args = parser.parse_args()

if args.verify:
    verifyOnionUrls()
    print("Verification complete. Check 'onion-working.txt' for working URLs.")

if args.static:
    from scraper import static
    if args.domain:
        static(args.domain)
    elif args.name:
        static(args.name)
    else:
        parser.error("At least one of --domain or --name must be provided for static scraping.")


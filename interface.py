#!/usr/bin/env python3
import argparse
from verifier import verify as verifyOnionUrls

parser = argparse.ArgumentParser(
    prog='dark web scraper',
    description="Cmd interface for the application"
    )

parser.add_argument('-d', '--domain', type=str, required=False, description="Domain to search on the dark web")
parser.add_argument('-n', '--name', type=str, required=False, description="Name to search on the dark web")
parser.add_argument('-l', '--latest', type=bool, required=False, default=False, description="If some websites have a latest page, only that page will be scraped")
parser.add_argument('-s', '--static', action='store_true', required=False, default=False, description="Scrape static pages only")
parser.add_argument('-a', '--all', action='store_true', required=False, default=False, description="Scrape all pages, including dynamic ones")
parser.add_argument('-v', '--verbose', action='store_true', required=False, default=False, description="Enable verbose output")
parser.add_argument('--verify', action='store_true', required=False, default=False, description="Verify onion URLs for accessibility")
    
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


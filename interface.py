#!/usr/bin/env python3
import argparse
from verifier import verify as verifyOnionUrls

parser = argparse.ArgumentParser(
    prog='dark web scraper',
    description="Command interface for the scraper and verifier for the dark web",
)

parser.add_argument('-k', '--keyword', type=str, required=True, help="Keyword to search on the dark web")
parser.add_argument('-l', '--latest', type=bool, required=False, default=False, help="If some websites have a latest page, only that page will be scraped")
parser.add_argument('-s', '--static', action='store_true', required=False, default=False, help="Scrape static pages only")
parser.add_argument('-d', '--dynamic', action='store_true', required=False, default=False, help="Scrape dynamic pages only")
parser.add_argument('-a', '--all', action='store_true', required=False, default=False, help="Scrape all pages, including dynamic ones")
parser.add_argument('-v', '--verbose', action='store_true', required=False, default=False, help="Enable verbose output")
parser.add_argument('--verify', action='store_true', required=False, default=False, help="Verify onion URLs for accessibility")
    
args = parser.parse_args()

assert sum([args.static, args.dynamic, args.all]) == 1, "You must specify exactly one scraping mode: --static, --dynamic, or --all."

if args.verbose:
    print("Verbose mode enabled. All output will be printed to the console.")
    global VERBOSE
    VERBOSE = True

if args.verify:
    verifyOnionUrls()
    print("Verification complete. Check 'onion-working.txt' for working URLs.")
elif args.static:
    from scraper import static
    static(args.keyword)
elif args.dynamic:
    from scraper import dynamic
    dynamic(args.keyword)
elif args.all:
    from scraper import dynamic, static
    static(args.keyword)
    dynamic(args.keyword)
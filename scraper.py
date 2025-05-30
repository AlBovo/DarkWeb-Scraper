#!/usr/bin/env python3
import requests, tqdm, json

global VERBOSE
PROXIES = {
    'http':  'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

session = requests.Session()
session.proxies = PROXIES

# Test the connection to the Tor network
try:
    session.get('http://httpbin.org/ip')
except:
    print("Failed to connect to the Tor network. Ensure Tor is running and configured correctly. (sudo systemctl start tor)")
    exit(1)

def static(to_find: str):
    to_find = to_find.lower()
    
    urls = json.load(open('onion-list.json', 'r'))

    for url in tqdm.tqdm(urls, desc="Processing URLs"):
        try:
            res = session.get(url['url'], timeout=20).text
            if to_find in res.lower():
                with open('static-results.txt', 'w') as output_file:
                    if VERBOSE:
                        print(f"Found '{to_find}' in {url['url']}")
                    output_file.write(f"Found '{to_find}' in {url}\n")
        except TimeoutError:
            print(f"Connection to {url} timed out.")

def dynamic(to_find: str):
    to_find = to_find.lower()
    
    urls = json.load(open('onion-list.json', 'r'))

    for url in tqdm.tqdm(urls, desc="Processing URLs"):
        try:
            u = url['url']
            a = url['api']
            # TODO
        except TimeoutError:
            print(f"Connection to {url} timed out.")
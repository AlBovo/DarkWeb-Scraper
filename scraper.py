#!/usr/bin/env python3
import requests, tqdm, json

PROXIES = {
    'http':  'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

session = requests.Session()
session.proxies = PROXIES

def test_tor_connection():
    """
    Test the connection to the Tor network by making a request to a known URL.
    If the request fails, it indicates that the Tor service is not running or not configured correctly.
    """
    try:
        session.get('http://httpbin.org/ip')
    except:
        print("Failed to connect to the Tor network. Ensure Tor is running and configured correctly. (sudo systemctl start tor)")
        exit(1)

def save_status(file: str, status: str, verbose: bool = False):
    with open(file, 'w') as output_file:
        if verbose: print(status)
        output_file.write(status + '\n')

def static(to_find: str, verbose: bool = False):
    test_tor_connection()
    to_find = to_find.lower()
    
    urls = json.load(open('static.json', 'r'))

    for url in tqdm.tqdm(urls, desc="Processing URLs"):
        try:
            res = session.get(url['url'], timeout=20).text
            if to_find in res.lower(): save_status('static-results.txt', f"Found '{to_find}' in {url['url']}", verbose)
        except:
            print(f"Connection to {url['url']} timed out.")

def dynamic(to_find: str, verbose: bool = False):
    test_tor_connection()
    to_find = to_find.lower()
    
    urls = json.load(open('dynamic.json', 'r'))

    # TODO: Implement modular dynamic URL handling
    for i, url in enumerate(tqdm.tqdm(urls, desc="Processing URLs")):
        try:
            if url['captcha']:
                print(f"Skipping {url['url']} due to captcha requirement.")
                continue
            u = url['url']
            a = url['api']

            if i == 0:
                e = 0
                while True:
                    atemp = a.format(e)
                    try:
                        res = session.get(u + atemp, timeout=20).text
                        if "PUBLISHED" not in res:
                            break
                    except:
                        break
                    if to_find in res.lower(): 
                        save_status('dynamic-results.txt', f"Found '{to_find}' in {u + atemp}", verbose)
                    e += 30
            elif i == 1 or i == 4 or i == 5:
                e = 0
                while True:
                    atemp = a.format(e)
                    try:
                        res = session.get(u + atemp, timeout=20).text
                        if 'end":true' in res or 'Nothing here' in res:
                            break
                    except:
                        break
                    if to_find in res.lower():
                        save_status('dynamic-results.txt', f"Found '{to_find}' in {u + atemp}", verbose)
                    e += 1
            elif i == 2 or i == 3:
                try:
                    res = session.get(u + a, timeout=20).text
                    if to_find in res.lower():
                        save_status('dynamic-results.txt', f"Found '{to_find}' in {u + a}", verbose)
                except:
                    continue
            else:
                assert False, "Unexpected index in dynamic URLs"
        except TimeoutError:
            print(f"Connection to {url} timed out.")
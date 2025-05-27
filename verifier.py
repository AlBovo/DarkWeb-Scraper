#!/usr/bin/env python3
import requests, tqdm

PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def getOnionList():
    with open('onion-list.txt', 'r') as file:
        onion_list = file.readlines()
    return [url.strip() for url in onion_list]

def verifyOnionUrl(url):
    try:
        response = requests.get(url, proxies=PROXIES, timeout=10)
        if response.status_code == 200:
            with open('onion-working.txt', 'a') as output_file:
                output_file.write(url + "\n")
    except:
        pass

if __name__ == "__main__":
    onion_list = getOnionList()
    for onion_url in tqdm.tqdm(onion_list, desc="Verifying URLs", unit="url"):
        verifyOnionUrl(onion_url)
    print("Verification complete. Check 'onion-working.txt' for working URLs.")
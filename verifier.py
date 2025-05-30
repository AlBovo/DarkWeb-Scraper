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
        return response.status_code == 200
    except:
        pass

def verify(onion_list):
    verified_urls = []
    for onion_url in tqdm.tqdm(onion_list, desc="Verifying URLs", unit="url"):
        if verifyOnionUrl(onion_url):
            verified_urls.append(onion_url)
    return verified_urls
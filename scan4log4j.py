#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import concurrent.futures

default_headers = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
   "Cache-Control": "max-age=0",
   "Upgrade-Insecure-Requests": "1",
   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
   "Accept-Language": "en-GB,en-US;q=0.9,en"
}


def scan(url, payloads, headers, split_headers=False):
    for payload in payloads:
        if split_headers:
            for header in headers:
                send_request(url, payload, [header])
        else:
            send_request(url, payload, headers)


def send_request(url, payload, headers):
    all_headers = default_headers.copy()
    for header in headers:
        all_headers[header] = payload

    requests.get(url, headers=all_headers, allow_redirects=True, timeout=5)
    print('[x] Request send to %s' % url)


if __name__ == '__main__':
    split_headers = False

    urls = []
    payloads = []
    headers = []

    get_urls = open('urls.txt', 'r').readlines()
    get_payloads = open('payloads.txt', 'r').readlines()
    get_headers = open('headers.txt', 'r').readlines()

    for url in get_urls:
        urls.append(url.strip())
    for payload in get_payloads:
        payloads.append(payload.strip())
    for header in get_headers:
        headers.append(header.strip())

    executor = concurrent.futures.ProcessPoolExecutor(100)
    futures = [executor.submit(scan, url, payloads, headers, split_headers) for url in urls]
    concurrent.futures.wait(futures)

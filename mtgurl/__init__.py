#! /usr/bin/env python3

import grequests  # must be imported before requests
import requests

_BASE_URL = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?name='

class NotFound(Exception):
    pass

def _exception_handler(request, exception):
    print("request failed")

def make_unquoted_url(name):
    return _BASE_URL + ('+[%s]' % name)

def make_quoted_url(name):
    return _BASE_URL + ('+["%s"]' % name)

def make_vanilla_url(name):
    return _BASE_URL + name

def fetch_by_name(name, url_method):
    url = url_method(name)
    return fetch(url)

def _check_found(response):
    if response.url.find('multiverseid=') != -1:
        return

    if response.status_code != 200:
        raise NotFound

    if response.url.find('/Search/') != -1:
        raise NotFound

def fetch_by_url(url):
    response = requests.head(url, allow_redirects=True)
    print(f'\n{url} → {response.url}')
    _check_found(response)

def fetch_by_url_async(urls):
    reqs = (grequests.head(url, allow_redirects=True) for url in urls)
    responses = grequests.map(reqs, size=10, exception_handler=_exception_handler)
    cardset_found = {}

    for response in responses:
        card_found = True
        try:
            _check_found(response)
        except NotFound:
            card_found = False
        finally:
            cardset_found[response.url] = card_found

    return cardset_found

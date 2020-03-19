#! /usr/bin/env python3

import requests

_BASE_URL = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?name='

class NotFound(Exception):
    pass

def make_unquoted_url(name):
    return _BASE_URL + ('+[%s]' % name)

def make_quoted_url(name):
    return _BASE_URL + ('+["%s"]' % name)

def make_vanilla_url(name):
    return _BASE_URL + name

def fetch_by_name(name, url_method):
    url = url_method(name)
    return fetch(url)

def fetch_by_url(url):
    response = requests.head(url)
    response.connection.close()
    if response.status_code != 302:
        raise NotFound

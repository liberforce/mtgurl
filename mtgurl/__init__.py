#! /usr/bin/env python3

import requests

_BASE_URL = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?name='

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
    r = requests.head(url, allow_redirects=False)
    r.connection.close()
    return bool(r.status_code == 302)

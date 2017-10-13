#! /usr/bin/env python3
import requests

def url_from_card_name(name):
    base_url='http://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[%s]'
    url = base_url % name
    return url

def fetch_card(name):
    url = url_from_card_name(name)
    r = requests.get(url, allow_redirects=False)
    assert r.status_code == 302, name

    with open('toto.html', 'w') as file_:
        file_.write(r.text)

if __name__ == '__main__':
    cards = [
        'Synod Sanctum',
        'Lightning Bolt',
        'Foudre',
    ]

    for card in cards:
        fetch_card(card)

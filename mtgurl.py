#! /usr/bin/env python3
import requests

def fetch_card(url):
    r = requests.get(url)
    print(r.status_code)

    with open('toto.html', 'w') as file_:
        file_.write(r.text)

if __name__ == '__main__':
    url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx?name=%2b%5bSynod%20Sanctum%5d'
    fetch_card(url)

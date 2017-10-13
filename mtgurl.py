#! /usr/bin/env python3
import requests
import unittest

def url_from_card_name(name):
    base_url='http://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[%s]'
    url = base_url % name
    return url

def fetch_card(name):
    url = url_from_card_name(name)
    r = requests.get(url, allow_redirects=False)
    r.connection.close()

    with open('{}.html'.format(name), 'w') as file_:
        file_.write(r.text)

    return bool(r.status_code == 302)


class TestFetchCard(unittest.TestCase):
    CARDS = [
        'Synod Sanctum',
        'Lightning Bolt',
        'Foudre',
    ]

    def test_fetch_card(self):
        for card in self.CARDS:
            with self.subTest(i=card):
                self.assertTrue(fetch_card(card))


if __name__ == '__main__':
    unittest.main()

#! /usr/bin/env python3
import grequests
import unittest
import os.path


def make_url1(name):
    base_url='http://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[%s]'
    url = base_url % name
    return url

def make_url2(name):
    base_url='http://gatherer.wizards.com/Pages/Search/Default.aspx?name=+["%s"]'
    url = base_url % name
    return url

def fetch_card(name, make_url=make_url1):
    url = make_url(name)
    r = grequests.head(url, allow_redirects=False, verify=False)
    r.connection.close()
    return bool(r.status_code == 302)

def fetch_cards(names, make_url=make_url1):
    urls = []
    for name in names:
        urls.append(make_url(name))

    rs = [grequests.head(url) for url in urls]
    responses = grequests.map(rs, size=5)
    results = [bool(r.status_code == 302) for r in responses]
    return [tup for tup in zip(names, responses)]


class TestFetchCard(unittest.TestCase):
    CARDS = []

    @classmethod
    def setUpClass(cls):
        cards_db_path = os.path.join(os.path.dirname(__file__), 'cards.txt')
        with open(cards_db_path, 'r') as file_:
            for line in file_:
                cls.CARDS.append(line.strip())

        cls.RESULTS = fetch_cards(cls.CARDS)

    def test_fetch_card(self):
        for (card, result) in self.RESULTS:
            with self.subTest(i=card):
                print('{}'.format(card))
                self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

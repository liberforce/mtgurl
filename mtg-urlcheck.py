#! /usr/bin/env python3
import requests
import unittest
import os.path


def make_unquoted_url(name):
    base_url='http://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[%s]'
    url = base_url % name
    return url

def make_quoted_url(name):
    base_url='http://gatherer.wizards.com/Pages/Search/Default.aspx?name=+["%s"]'
    url = base_url % name
    return url

def fetch_card(name, make_url):
    url = make_url(name)
    r = requests.head(url, allow_redirects=False)
    r.connection.close()

    return bool(r.status_code == 302)


class TestFetchQuotedCard(unittest.TestCase):
    CARDS = []

    @classmethod
    def setUpClass(cls):
        cards_db_path = os.path.join(os.path.dirname(__file__), 'cards.txt')
        with open(cards_db_path, 'r') as file_:
            for line in file_:
                cls.CARDS.append(line.strip())

    def test_fetch_card(self):
        for card in self.CARDS:
            with self.subTest(i=card):
                print('{}'.format(card))
                self.assertTrue(fetch_card(card, make_quoted_url))

class TestFetchUnquotedCard(unittest.TestCase):
    CARDS = []

    @classmethod
    def setUpClass(cls):
        cards_db_path = os.path.join(os.path.dirname(__file__), 'cards.txt')
        with open(cards_db_path, 'r') as file_:
            for line in file_:
                cls.CARDS.append(line.strip())

    def test_fetch_card(self):
        for card in self.CARDS:
            with self.subTest(i=card):
                print('{}'.format(card))
                self.assertTrue(fetch_card(card, make_unquoted_url))


if __name__ == '__main__':
    unittest.main()

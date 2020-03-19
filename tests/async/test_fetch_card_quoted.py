#! /usr/bin/env python3
import os.path
from pprint import pprint as pp

import pytest

import mtgurl


def list_card_names(filepath):
    cards = []
    with open(filepath, 'r') as file_:
        for line in file_:
            cards.append(line.strip())

    return cards


CARDS = list_card_names(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'cardset-simple.txt',
    )
)


def test_fetch_card_quoted():
    urls = [mtgurl.make_quoted_url(cardname) for cardname in CARDS]
    pp(urls)
    statuses = mtgurl.fetch_by_url_async(urls)
    assert all(statuses.values())

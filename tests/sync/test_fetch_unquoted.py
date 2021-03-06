#! /usr/bin/env python3
import os.path

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


@pytest.mark.parametrize("cardname", CARDS)
def test_fetch_card_unquote(cardname):
    url = mtgurl.make_unquoted_url(cardname)
    mtgurl.fetch_by_url(url)

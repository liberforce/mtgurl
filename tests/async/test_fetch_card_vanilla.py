#! /usr/bin/env python3
import os.path
from pprint import pprint as pp

import grequests
import requests
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


def test_fetch_cards_sending_requests_all_at_once_blocking_for_responses():
    """
    Send requests blocking for the response.
    Block until all responses are received.
    """
    urls = [mtgurl.make_vanilla_url(cardname) for cardname in CARDS]
    pp(urls)
    statuses = mtgurl.fetch_by_url_async(urls)
    assert all(statuses.values())


def test_fetch_cards_sending_requests_by_batches_blocking_for_responses():
    """
    Send requests blocking for the response.
    Use a request pool to keep a threshold of maximum number of requests.
    Block until all responses are received.
    """
    import time
    start = time.time()
    urls = [mtgurl.make_vanilla_url(cardname) for cardname in CARDS]
    reqs = (grequests.head(url, allow_redirects=True) for url in urls)
    responses = grequests.imap(reqs, size=30)

    delay = 1
    time.sleep(delay)

    index = 0
    for response in responses:
        print(response.url)
        assert response
        assert response.status_code in [200]
        index += 1

    stop = time.time()
    print(stop - start - delay)


def _on_response(response, *args, **kwargs):
    print(response.url)
    assert response
    assert response.status_code in [200]


def test_fetch_cards_sending_requests_by_batches_not_blocking_for_responses():
    """
    Send requests but don't block for the response.
    Use a request pool to keep a threshold of maximum number of requests.
    Use a callback to get notified of the response.
    """
    urls = [mtgurl.make_vanilla_url(cardname) for cardname in CARDS]
    reqs = (grequests.head(url, allow_redirects=True, callback=_on_response) for url in urls)
    pool = grequests.Pool(30)
    for req in reqs:
        grequests.send(req, pool)

    # Don't exit until we received the responses, otherwise we may lose some of them
    import time
    time.sleep(20)

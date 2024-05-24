import pytest
from YahooFinClient import client
from datetime import datetime, timedelta


def test_getquote():
    print(client.get_live_quote("GOOG"))

    assert (client.get_live_quote("GOOG") > 1)

def test_get_historical_quote():
    assert client.get_historical_data("GOOG", 10) is not None

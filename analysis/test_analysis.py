import pytest
from YahooFinClient import client

def test_series_difference():
    days = 365
    ticker1 = "SPY"
    # Instantiate the classes to access the new instance methods
    stock1 = client.Stock(ticker1)
    series1 = stock1.get_historical_data(days)
    assert series1 is not None
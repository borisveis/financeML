import pytest
import time
from YahooFinClient import client

@pytest.fixture(autouse=True)
def rate_limit_buffer():
    """Adds a 1-second delay between tests to avoid Yahoo's rate limit"""
    yield
    time.sleep(1)

def test_smoke_client():
    # Retaining AAPL as used in your original test
    apple = client.Stock("AAPL")
    assert apple.get_live_quote() is not None

def test_live_quote():
    # Retaining GOOG as used in your original test
    google = client.Stock("GOOG")
    assert google.get_live_quote() > 1

def test_invalid_ticker_symbol():
    invalid_symbol = "ABCDEF"
    with pytest.raises(ValueError) as exc_info:
        client.Stock(invalid_symbol)
    assert f"Invalid ticker symbol: {invalid_symbol}" in str(exc_info.value)

def test_historical_quote():
    # Retaining AAPL as used in your original test
    apple = client.Stock("AAPL")
    assert apple is not None

def test_historical():
    # Retaining AMZN as used in your original test
    ticker_symbol = "AMZN"
    amazon = client.Stock(ticker_symbol)
    historical_data = amazon.get_historical_data(5)
    assert historical_data['Close'].notna().any(), "No valid close prices found"
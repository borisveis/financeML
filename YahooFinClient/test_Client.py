from datetime import datetime, timedelta
import pytest
import yfinance as yf
from YahooFinClient import client
def test_smoke_client():
    apple=client.Stock("AAPL")
    assert apple.get_live_quote() is not None
def test_live_quote():
    google=client.Stock("GOOG")
    assert google.get_live_quote()>1
def test_invalid_ticker_symbol():
    invalid_symbol = "ABCDEF"
    with pytest.raises(ValueError) as exc_info:
        client.Stock(invalid_symbol)
    assert f"Invalid ticker symbol: {invalid_symbol}" in str(exc_info.value)
def test_historical_quote():
        apple = client.Stock("AAPL")
def test_historical():
    ticker_symbol="AMZN"
    Amazon=client.Stock(ticker_symbol)
    historical_data=Amazon.get_historical_data(5)
    assert historical_data['Close'].notna().any(), "No valid close prices found"
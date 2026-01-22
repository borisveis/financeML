import pytest
import time
from YahooFinClient import client
from unittest.mock import patch, ANY
import pandas as pd


# --- New AH and Training Method Tests ---

@pytest.fixture
def mock_ah_data():
    """Generates synthetic minute-level data to simulate After-Hours action."""
    dates = pd.date_range(start="2026-01-20 09:30:00", periods=5, freq='min')
    return pd.DataFrame({
        "Close": [400.1, 400.5, 400.3, 401.0, 401.5]
    }, index=dates)


@patch('yfinance.download')
def test_get_full_day_data(mock_download, mock_ah_data):
    """Verifies retrieval of the final AH close for the daily cron job."""
    mock_download.return_value = mock_ah_data
    # Consistent with your test_smoke_client() style
    spy = client.Stock("SPY")

    result = spy.get_full_day_data()

    # ANY allows the Ticker object to pass while strictly checking params
    mock_download.assert_called_once_with(
        ANY,
        period="1d",
        interval="1m",
        prepost=True
    )

    # Ensure we only extract the final AH price point
    assert len(result) == 1
    assert result['Close'].iloc[0] == 401.5


@patch('yfinance.download')
def test_get_training_data(mock_download, mock_ah_data):
    """Verifies retrieval of AH-aware training data for JIT retraining."""
    mock_download.return_value = pd.DataFrame({"Close": mock_ah_data["Close"]})
    spy = client.Stock("SPY")

    result = spy.get_training_data(period="5y")

    # Verifies the 5y window and AH parameter are used
    mock_download.assert_called_once_with(
        ANY,
        period="5y",
        prepost=True
    )
    assert isinstance(result, pd.Series)
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
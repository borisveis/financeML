import pytest
import time
from YahooFinClient import client
from unittest.mock import patch, ANY, MagicMock
import pandas as pd


# ... [Keep your existing mock_ah_data fixture and previous tests] ...

@patch('yfinance.Ticker')
def test_get_audit_metrics(mock_ticker_class):
    """Verifies that audit metrics correctly map fundamental data."""
    # Setup mock info dictionary
    mock_ticker_instance = mock_ticker_class.return_value
    mock_ticker_instance.info = {
        "regularMarketPrice": 10.32,
        "targetMeanPrice": 12.00,
        "recommendationKey": "buy",
        "bookValue": 12.50,
        "numberOfAnalystOpinions": 9
    }
    mock_ticker_instance.fast_info = {'currency': 'USD'}

    agnc = client.Stock("AGNC")
    metrics = agnc.get_audit_metrics()

    assert metrics['symbol'] == "AGNC"
    assert metrics['target_mean'] == 12.00
    assert metrics['book_value'] == 12.50
    assert metrics['recommendation'] == "buy"


@patch('yfinance.download')
@patch('yfinance.Ticker')
def test_get_relationship_metrics(mock_ticker_class, mock_download):
    """Verifies the divergence calculation between stock and benchmark."""
    # Mocking the 5-day history for the stock
    mock_stock_instance = mock_ticker_class.return_value
    mock_stock_instance.fast_info = {'currency': 'USD'}

    # Simulate a 1% price increase for AGNC
    mock_stock_instance.history.return_value = pd.DataFrame({
        "Close": [10.0, 10.0, 10.0, 10.0, 10.1]
    })

    # Mocking the 5-day history for ^TNX (the benchmark)
    # Simulate a 1% price decrease for ^TNX
    mock_download.return_value = pd.DataFrame({
        "Close": [4.5, 4.5, 4.5, 4.5, 4.455]
    })

    agnc = client.Stock("AGNC")
    rel_metrics = agnc.get_relationship_metrics(benchmark_ticker="^TNX")

    # AGNC +1%, TNX -1% -> Divergence should be ~2% (0.02)
    assert rel_metrics['ticker_change'] > 0
    assert rel_metrics['benchmark_change'] < 0
    assert pytest.approx(rel_metrics['divergence'], 0.001) == 0.02


def test_audit_metrics_missing_data():
    """Defensive test: ensures code doesn't crash if Yahoo returns empty info."""
    with patch('yfinance.Ticker') as mock_ticker:
        inst = mock_ticker.return_value
        # FIX: Add 'last_price' to the mocked fast_info so the fallback works
        inst.fast_info = {'currency': 'USD', 'last_price': 10.32}
        inst.info = {}  # Empty info dict

        agnc = client.Stock("AGNC")
        metrics = agnc.get_audit_metrics()

        # Should return None for missing fields, not raise KeyError
        assert metrics['target_mean'] is None
        assert metrics['book_value'] is None
        # Verify the fallback to fast_info actually worked
        assert metrics['current_price'] == 10.32
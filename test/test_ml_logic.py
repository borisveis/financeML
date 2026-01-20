import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from ML_Stock_Movement import fetch_data, train_model, evaluate_model


@pytest.fixture
def mock_settings():
    return {
        "target_ticker": "SPY",
        "feature_tickers": ["AAPL", "GOOGL", "^TNX"]
    }


@pytest.fixture
def mock_market_data():
    # Create 100 days of synthetic data for testing
    dates = pd.date_range(start="2020-01-01", periods=100)
    data = pd.DataFrame({
        "SPY": np.linspace(300, 400, 100) + np.random.normal(0, 1, 100),
        "AAPL": np.linspace(100, 150, 100) + np.random.normal(0, 1, 100),
        "GOOGL": np.linspace(1000, 1200, 100) + np.random.normal(0, 1, 100),
        "^TNX": np.linspace(1.5, 4.5, 100) + np.random.normal(0, 0.1, 100)
    }, index=dates)
    return data


@patch('yfinance.download')
def test_fetch_data_logic(mock_download, mock_settings, mock_market_data):
    # yfinance returns a MultiIndex if multiple tickers are requested.
    # We simulate this by creating a DataFrame with a "Close" column level.
    mock_df = pd.concat({"Close": mock_market_data}, axis=1)
    mock_download.return_value = mock_df

    # Execute the function under test
    df, target, features = fetch_data(mock_settings)

    # Assertions
    assert target == "SPY"
    assert "AAPL" in features
    assert "^TNX" in features
    assert not df.empty
    # Ensure the returned df is the sliced 'Close' data
    assert list(df.columns).sort() == ["SPY", "AAPL", "GOOGL", "^TNX"].sort()


def test_model_training_and_evaluation(mock_market_data):
    X = mock_market_data[["AAPL", "GOOGL", "^TNX"]]
    y = mock_market_data["SPY"]

    model, X_test, y_test = train_model(X, y)
    mse, r2, y_pred = evaluate_model(model, X_test, y_test)

    # Basic sanity checks for regression metrics
    assert mse >= 0
    assert -1 <= r2 <= 1
    assert len(y_pred) == len(y_test)


def test_prediction_integrity(mock_market_data):
    X = mock_market_data[["AAPL", "GOOGL", "^TNX"]]
    y = mock_market_data["SPY"]
    model, _, _ = train_model(X, y)

    # Test a single prediction
    sample_input = pd.DataFrame([[150, 1200, 4.0]], columns=["AAPL", "GOOGL", "^TNX"])
    prediction = model.predict(sample_input)

    assert isinstance(prediction[0], (float, np.float64))
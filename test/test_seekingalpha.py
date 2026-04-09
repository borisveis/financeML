import pytest
from analysis.seeking_alpha_client import SeekingAlphaClient


@pytest.fixture(scope="module")
def sa_client():
    """Provides a single SeekingAlphaClient instance for the test session."""
    return SeekingAlphaClient()


def test_get_metrics(sa_client):
    """Verifies the /metrics endpoint returns historical return data."""
    print("\n--- Testing Metrics Endpoint ---")
    data = sa_client.get_metrics(["agnc", "aapl"])

    assert isinstance(data, list), "Expected a list of metrics"
    assert len(data) > 0, "No metrics returned"

    # Verify the structure matches the payload we discovered
    first_ticker_metrics = data[0]
    assert 'price_return_1m' in first_ticker_metrics, "Missing 1-month return data"
    assert 'price_close_1m' in first_ticker_metrics, "Missing 1-month close price"
    print(f"SUCCESS: Retrieved metrics for {len(data)} tickers.")


def test_get_analyst_summary(sa_client):
    """Verifies the /analyst-recommendation endpoint returns analyst volume."""
    print("\n--- Testing Analyst Summary Endpoint ---")
    data = sa_client.get_analyst_summary("agnc")

    assert isinstance(data, dict), "Expected a dictionary for analyst summary"
    assert 'tot_analysts_recommendations' in data, "Missing total analyst count"
    assert 'authors_count' in data, "Missing author count"
    print(f"SUCCESS: AGNC has {data['tot_analysts_recommendations']} analyst recommendations.")


def test_get_real_time_quote(sa_client):
    """Verifies the /recommendation endpoint returns current pricing."""
    print("\n--- Testing Real-Time Quote Endpoint ---")
    data = sa_client.get_real_time_quote("agnc")

    assert isinstance(data, dict), "Expected a dictionary for real-time quote"
    assert 'last' in data, "Missing last traded price"
    assert 'volume' in data, "Missing volume data"
    print(f"SUCCESS: AGNC last traded at ${data['last']}")
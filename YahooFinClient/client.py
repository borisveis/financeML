import pytest
import yfinance as yf
from datetime import datetime, timedelta


def get_live_quote(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    live_quote = ticker.history(period='1d')['Close'].iloc[-1]
    return live_quote
def get_historical_data(ticker_symbol,days):
    period = f"{days}d"
    ticker = yf.Ticker(ticker_symbol)
    historical_data = ticker.history(period=period)
    # print(historical_data)
    return historical_data
def get_historical_datafortickers(tickers,days):
    current_date = datetime.now()
    startdate = current_date - timedelta(days=365 * days)
    period = f"{days}d"
    data=yf.download(tickers, startdate, current_date)
    return data



def test_getquote():
    print(get_live_quote("GOOG"))
    assert (get_live_quote("GOOG") > 1)
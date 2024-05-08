import pytest
from YahooFinClient import client
from analysis import calculations as calc
def test_series_difference():
    days=365
    ticker1="SPY"
    ticker2="QQQ"
    series1=client.get_historical_data(ticker1,days)
    series2=client.get_historical_data(ticker2,days)
    difference= calc.series_difference(series1,series2)
    print(difference)

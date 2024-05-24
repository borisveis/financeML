import os
import pytest
from file_management import excel
from YahooFinClient import client


# def test_append_to_existing_excel():
#     target_file = "/Users/borvei01/source/personal/financeML/data/5yr/tickersdatefile.csv"
#     assert (excel.create_excel_sheet(target_file, ""))=="File exists"
#
# def test_create_new_file():
#     target_file = "/Users/borvei01/source/personal/financeML/data/testdata.xlsx"
#     ticker="SPY"
#     excel.create_excel_sheet(target_file,ticker, client.get_historical_data(ticker,1))
#     assert True==os.path.exists(target_file)
# os.remove(target_file)

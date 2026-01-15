import os
import pytest
from file_management import excel
from YahooFinClient import client


def test_create_new_file(tmp_path):
    # tmp_path is a pathlib object provided by pytest
    # It creates a temporary directory unique to this test run
    temp_dir = tmp_path / "data"
    temp_dir.mkdir()

    target_file = str(temp_dir / "testdata.xlsx")
    ticker = "SPY"

    # Fetch a small amount of data for the test
    test_data = client.Stock(ticker).get_historical_data(1)

    # Execute the function
    excel.create_excel_sheet(target_file, test_data, ticker)

    # Assertions
    assert os.path.exists(target_file) is True
    assert target_file.endswith(".xlsx")

    # No manual os.remove() needed! pytest handles cleanup of tmp_path
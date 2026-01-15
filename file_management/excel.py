import os
import pandas as pd
from openpyxl import load_workbook


def create_excel_sheet(target_file, dataframe, ticker):
    if os.path.exists(target_file):
        print("file exists")
        return "file exists"
    else:
        # FIX: Remove timezone information from the index to support Excel format
        if dataframe.index.tz is not None:
            dataframe.index = dataframe.index.tz_localize(None)

        with pd.ExcelWriter(target_file, engine='openpyxl') as writer:
            # Use ticker as sheet_name so the later workbook[ticker] call works
            dataframe.to_excel(writer, sheet_name=ticker, index=True)

        print(f"Excel file {target_file} has been created successfully.")

        # Reload to ensure visibility (optional)
        workbook = load_workbook(target_file)
        sheet = workbook[ticker]
        sheet.sheet_state = 'visible'
        workbook.save(target_file)
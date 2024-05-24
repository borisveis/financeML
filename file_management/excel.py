import os
import pandas as pd
import openpyxl
from openpyxl import load_workbook


def create_excel_sheet(target_file, dataframe, ticker):
    if os.path.exists(target_file):
        print("file exists")
        return "file exists"
    else:
        with pd.ExcelWriter(target_file, engine='openpyxl') as writer:
            # Write DataFrame to an Excel sheet
            dataframe.to_excel(writer, sheet_name='Stock Data', index=True)

        print(f"Excel file {target_file} has been created successfully.")
        workbook = load_workbook(target_file)
        sheet = workbook[ticker]
        sheet.sheet_state = 'visible'
        workbook.save(target_file)

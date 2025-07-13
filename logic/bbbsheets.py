# File: logic/sheets_bbb.py

import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1RGa0tgTNUtwLjAoeIyZNYrjG-afS7_rA8d1Amh70P-0'  # To be provided by user
SHEET_NAME = 'Sheet1'

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


def get_next_business():
    data = sheet.get_all_records()
    for index, row in enumerate(data):
        if row.get("Status") != "Success":
            row["RowID"] = index + 2  # Account for header row
            return row
    return None


def update_submission_result(row_id, status, details):
    sheet.update_cell(row_id, find_column_index("Status"), status)
    sheet.update_cell(row_id, find_column_index("Result URL"), details)


def has_more_data():
    data = sheet.get_all_records()
    return any(row.get("Status") != "Success" for row in data)


def find_column_index(header):
    headers = sheet.row_values(1)
    return headers.index(header) + 1

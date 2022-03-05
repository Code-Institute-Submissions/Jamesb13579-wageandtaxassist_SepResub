import gspread
from google.oauth2.service_account import Credentials
import pandas

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('employeedetails')

print('                         Welcome to Wage and Tax assist')
print('                         ******************************')

def new_employee():
    """
    Function to enter employee details to spreadsheet
    """
    newemployee = []
    print("Please input employee details")
    name = input("Enter employee name: ")
    tax_credits = int(input("Enter employees tax Credits:"))
    wage = input("Enter employees hourly wage:")
    newemployee = name, tax_credits, wage
    worksheet_to_update = SHEET.worksheet("Sheet1")
    worksheet_to_update.append_row(newemployee)
    print(newemployee)

new_employee()
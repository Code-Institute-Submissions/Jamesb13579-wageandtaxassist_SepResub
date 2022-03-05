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

print(' '*25 + "Welcome to Wage and Tax assist")
print(' '*25 + "******************************")

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

#new_employee()

def choose_option():
    """
    Function to choose between entering new employee and working out wages
    """
    print(' '*13 + "Type 1 if you would like to enter new employee details")
    print(' '*9 + "Type 2 if you would like you work out existing employee wages")

    userinput = int(input())

    if userinput == 1:
        print("You have chosen enter employee details")
        new_employee()
    elif userinput == 2:
        print("You have chosen existing employee wages")

    elif userinput > 2:
        raise ValueError("Please enter 1 or 2")


choose_option()
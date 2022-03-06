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

def choose_option():
    """
    Function to choose between entering new employee and working out wages
    """
    print(' '*13 + "Type 1 if you would like to enter new employee details")
    print(' '*9 + "Type 2 if you would like you work out existing employee wages")

    userinput = int(input("Type choice here please:"))

    if userinput == 1:
        print("You have chosen enter employee details")
        new_employee()
    elif userinput == 2:
        print("You have chosen existing employee wages")
        wages_taxes()
    elif userinput > 2:
        raise ValueError("Please enter 1 or 2")

#def wages_taxes():
    """
    function to work out and return wages and taxes owed
    """
    print("Enter employee and and hours worked this week")
    name = input("Enter name here:")
    hours = input("Hours worked this week:")
    wage = name, hours
    return wage
    wages = SHEET.worksheet("Sheet1").get_all_values()
    print(wages)


def prsi():
    """
    function to work out prsi charge for employee
    """
    wage = 374
    if wage < 352:
        prsi_owed = 0
    elif wage < 424:
        one_sixth = (wage - 352)/6
        prsi_credit = 12 - one_sixth
        taxable_pay = (wage * 0.04)
        prsi_owed = taxable_pay - prsi_credit
        
    elif wage > 424.01:
        prsi_owed = (wage * 0.04)
        
    print(prsi_owed)


prsi()


#choose_option()
import gspread
from google.oauth2.service_account import Credentials
from decimal import Decimal as D

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('employeedetails')

print(' '*25 + "Welcome to wage and Tax assist")
print(' '*25 + "******************************")


def choose_option():
    """
    Function to choose between entering new employee and working out wages
    """
    print(' '*13 + "Type 1 if you would like to enter new employee details")
    print(' '*10 + "*" * 60)
    print(' '*9 + "Type 2 if you would like you work out employee wages")
    print(' '*10 + "*" * 60)

    userinput = int(input("Type choice here please:\n"))

    if userinput == 1:
        print("You have chosen enter employee details")
        new_employee()
    elif userinput == 2:
        print("You have chosen existing employee wages")
        main()
    elif userinput > 2:
        raise ValueError("Please enter 1 or 2")


def new_employee():
    """
    Function to enter employee details to spreadsheet
    """
    newemployee = []
    print("Please input employee details")
    name = input("Enter employee name: \n")
    tax_credits = int(input("Enter employees tax Credits:\n"))
    wage = input("Enter employees hourly wage:\n")
    newemployee = name, tax_credits, wage
    worksheet_to_update = SHEET.worksheet("Sheet1")
    worksheet_to_update.append_row(newemployee)
    print("Information added to spreadsheet")
    restart()


def employee_name():
    """
    input for employee name
    """
    employee_name = input("Please enter employees name:\n")
    return employee_name
    

def weekly_hours():
    """
    input for hours worked
    """
    weekly_hours = int(input("Hours worked this week:\n"))
    return weekly_hours



def hourly_wage(employeeName):
    """
    test
    """    
    for i in range(1, SHEET.sheet1.row_count + 1):
        row = SHEET.sheet1.row_values(i)
        if row[0] == employeeName:
            return row[2]


def tax_credits(employeeName):
    """
    test
    """
    for i in range(1, SHEET.sheet1.row_count + 1):
        row = SHEET.sheet1.row_values(i)
        if row[0] == employeeName:
            return row[1]


def restart():
    """
    function to allow user to restart to enter new data.
    or to exit the program.
    """
    print("Would you like to start the process again")
    print("Type 1 for yes or 2 for no")
    userinput = int(input("Type choice here please:\n"))

    if userinput == 1:
        print("You have chosen yes")
        choose_option()
    elif userinput == 2:
        print("You have chosen no program will end now")
        exit()
    elif userinput > 2:
        raise ValueError("Please enter 1 or 2")




def prsi(wage):
    """
    function to work out prsi charge for employee
    """
    if wage < 352:
        prsi_owed = 0
    elif wage < 424:
        one_sixth = (int(wage) - 352)/6
        prsi_credit = 12 - one_sixth
        taxable_pay = (int(wage) * 0.04)
        prsi_owed = round(taxable_pay - prsi_credit, 2)
    elif wage > 424.01:
        prsi_owed = round(int(wage) * 0.04, 2)
    return prsi_owed


def usc(wage):
    """
    function to work out usc charge for employee
    """
    if wage < 231:
        usc_owed = round(int(wage) * 0.005, 2)
    elif wage < 409.5:
        low_rate = (231 * 0.005)
        mid_rate = (int(wage) - 231)*0.02
        usc_owed = round(low_rate + mid_rate, 2)
    elif wage < 1347:
        low_rate = (231 * 0.005)
        mid_rate = (178.5 * 0.02)
        high_rate = (int(wage) - 409.5)*0.045
        usc_owed = round(low_rate + mid_rate + high_rate, 2)
    elif wage > 1347.01:
        low_rate = (231 * 0.005)
        mid_rate = (178.5 * 0.02)
        high_rate = (937.5 * 0.04)
        highest_rate = (int(wage) - 1347)*0.08
        usc_owed = round(low_rate + mid_rate + high_rate + highest_rate, 2)
    return usc_owed


def tax(wage, weeklyTaxCredits):
    """
    function to work out tax charge for employee
    """

    
    if wage < 707.69:
        tax_owed = round(int(wage) * 0.2 - int(weeklyTaxCredits), 2)
    elif wage > 707.7:
        low_rate = (707.69 * 0.2)
        high_rate = (int(wage) - 707.69)*0.4
        tax_owed = round(low_rate + high_rate - weeklyTaxCredits, 2)

    return tax_owed

def main():
    """
    test
    """
    employeeName = employee_name()
    weeklyHours = weekly_hours()
    hourlyWage = hourly_wage(employeeName)
    taxCredits = tax_credits(employeeName)
    weeklyTaxCredits = D(taxCredits) / 52
    wage = D(hourlyWage) * D(weeklyHours)
    print(wage)
    taxowed = tax(wage, weeklyTaxCredits)
    prsiowed = prsi(wage)
    useowed = usc(wage)
    print(' '*21 + "Hi wage details for this employee are:")
    print(' '*25 + f"Gross Weekly wage: {wage}")
    print(' '*32 + f"Tax Owed: {taxowed}")
    print(' '*32 + f"PRSI owed: {prsiowed}")
    print(' '*32 + f"USC owed: {useowed}")
    print(' '*29 + f"total tax owed {taxowed+prsiowed+useowed}")
    print(' '*29+f"Net wage for this week {int(wage)-taxowed-prsiowed-useowed}")
    restart()


choose_option()

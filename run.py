from decimal import Decimal
import gspread
from google.oauth2.service_account import Credentials


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
    print(' '*13 + "*" * 54)
    print(' '*14 + "Type 2 if you would like you work out employee wages")
    print(' '*14 + "*" * 52)
    print(' '*16 + "Type 3 if you would like to list employee names")
    print(' '*16 + "*" * 48)
    print(' '*33 + "Type 0 to exit")
    print(' '*33 + "*" * 14)

    userinput = int(input("Type choice here please:\n"))
    if userinput == 1:
        print("You have chosen enter employee details.")
    elif userinput == 2:
        print("You have chosen existing employee wages.")
    elif userinput == 3:
        print("You have chosen list employee names.")
    elif userinput == 0:
        print("Exiting.")
    else:
        print("Invalid option.")
    return userinput


def new_employee():
    """
    Function to enter employee details to spreadsheet
    """
    newemployee = []
    print("Please input employee details")
    name = input("Enter employee name: \n")
    try:
        credits_tax = int(input("Enter employees Tax Credits:\n"))
    except error:
        print("Please only enter numbers in to the Tax Credits input")        
        print("Would you like to start the process again")
        print("Type 1 for yes or 2 for no")
        employeeinput = input("Type choice here please:\n")

        if employeeinput == "1":
            print("You have chosen try again")
            new_employee()
        elif employeeinput == "2":
            print("You have chosen no program will now go back to main menu")
            main()
        else:
            print("Please enter 1 or 2")
            restart()

    try:
        wage = int(input("Enter employees hourly wage:\n"))
    except:
        print("Please only enter numbers in to the Tax Credits input")        
        print("Would you like to start the process again")
        print("Type 1 for yes or 2 for no")
        employeeinput = input("Type choice here please:\n")

        if employeeinput == "1":
            print("You have chosen try again")
            new_employee()
        elif employeeinput == "2":
            print("You have chosen no program will now go back to main menu")
            main()
        else:
            print("Please enter 1 or 2")
            restart()
        
    if (name != "" and wage != "" and credits_tax != ""):
        newemployee = name, credits_tax, wage
        worksheet_to_update = SHEET.worksheet("Sheet1")
        worksheet_to_update.append_row(newemployee)
        print("Information added to spreadsheet")
    else:
        print("You have entered no details for a field, restarting....")
    restart()


def employee_name_hours():
    """
    Input for employee name
    """
    list_names()
    name = input("Please choose and enter employees name:\n")
    week_hours = int(input("Hours worked this week:\n"))
    return (name, week_hours)


def list_names():
    """
    bring up list of screen of all employees in spread sheet
    """
    names = SHEET.sheet1.col_values(1)
    for name in names:
        print(name)


def wage_credits(name):
    """
    returns employees hourly wage from the spreedsheet
    """
    for i in range(1, SHEET.sheet1.row_count + 1):
        row = SHEET.sheet1.row_values(i)
        if row[0].lower() == name.lower():
            return (row[2], row[1])


def restart():
    """
    function to allow user to restart to enter new data.
    or to exit the program.
    """
    print("Would you like to start the process again")
    print("Type 1 for yes or 2 for no")
    userinput = input("Type choice here please:\n")

    if userinput == "1":
        print("You have chosen yes")
        main()
    elif userinput == "2":
        print("You have chosen no program will end now")
        exit()
    else:
        print("Please enter 1 or 2")
        restart()


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


def tax(wage, weekly_tax_credits):
    """
    function to work out tax charge for employee
    """
    taxes = int(weekly_tax_credits)
    if wage < 707.69:
        tax_owed = round(int(wage) * 0.2 - int(weekly_tax_credits), 2)
    elif wage > 707.7:
        low_rate = (707.69 * 0.2)
        high_rate = (int(wage) - 707.69)*0.4
        tax_owed = low_rate + high_rate - taxes
    return tax_owed


def main():
    """
    this runs when option 2 is chosen to bring together all the functions
    """
    i = 0
    while i <= 0:
        try:
            user_input = choose_option()
            if user_input in [1, 2, 3, 0]:
                i = + 1
        except ValueError:
            print("Please enter a valid option")

    if user_input == 1:
        new_employee()
    elif user_input == 2:
        try:
            name, hours = employee_name_hours()
            hourly_rate, credits_tax = wage_credits(name)
            weekly_tax_credits = Decimal(credits_tax) / 52
            wage = (Decimal(hourly_rate) * Decimal(hours))
            taxowed = tax(wage, weekly_tax_credits)
            prsio = prsi(wage)
            useowed = usc(wage)
            print(' '*21 + "Hi wage details for this employee are:")
            print(' '*25 + f"Gross Weekly wage: {wage}")
            print(' '*32 + f"Tax Owed: {taxowed}")
            print(' '*32 + f"PRSI owed: {prsio}")
            print(' '*32 + f"USC owed: {useowed}")
            print(' '*29 + f"Total tax owed: {round(taxowed+prsio+useowed,3)}")
            print(' '*32+f"Net wage: {int(wage)-taxowed-prsio-useowed}")
            restart()
        finally:
            print("Incorrect entry, please try again")
            restart()
    elif user_input == 3:
        list_names()
        restart()
    elif user_input == 0:
        exit()


if __name__ == "__main__":
    main()

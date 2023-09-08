import datetime
import re
from utilities import is_valid_email, is_valid_password
from google.oauth2.service_account import Credentials
import gspread

# Google Sheets authentication
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fishing_tackle')
users_sheet = SHEET.worksheet('user')

def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    user_data = users_sheet.get_all_records()

    for user in user_data:
        if user['User'] == email and user['Password'] == password:
            last_login = user['Last Login']
            print(f"\nWelcome {email}! You are now logged in.")
            if last_login:
                print(f"Your last login was on {last_login}.")
            update_last_login(email)
            return True
    print("\nInvalid email or password.")
    return False

def signup():
    while True:
        email = input("Enter your email: ")
        if not is_valid_email(email):
            print("Invalid email! Please adhere to the requirements.")
            print("- Contains one '@' symbol.")
            print("- Has a domain name after the '@' symbol.")
            print("- Ends with a domain extension like .com, .org, etc.")
            continue
        user_data = users_sheet.col_values(1)  # Get all emails
        if email in user_data:
            print("Email already exists! Please try another one or log in.")
            continue
        break

    while True:
        print("\nPassword requirements:")
        print("- At least 8 characters")
        print("- At least one uppercase letter")
        print("- At least one lowercase letter")
        print("- At least one digit")
        print("- At least one special character (e.g., !, @, #, $, etc.)")
        print("- No spaces at the beginning or end")
        password = input("\nEnter a password: ")

        if not is_valid_password(password):
            print("Invalid password! Please adhere to the requirements.")
            continue

        confirm_password = input("Re-enter password to confirm: ")
        if password != confirm_password:
            print("\nPasswords do not match! Please try again.")
            continue
        else:
            break

    # Append the new user data
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users_sheet.append_row([email, password, current_time])
    print(f"\nUser with email {email} successfully signed up!")
    return True

def update_last_login(email):
    cell = users_sheet.find(email)
    row_num = cell.row
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users_sheet.update_cell(row_num, 3, current_time)

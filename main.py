import logging
from getpass import getpass
from banking_tools import (
    create_account,
    validate_login,
    get_account_balance,
    transfer_funds,
    get_transaction_history,
    get_loan_information,
    get_investment_advice,
    schedule_appointment,
)

# Configure logging
logging.basicConfig(
    filename="user_activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def display_header(title):
    print("\n" + "=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)

def main_menu(account_number):
    while True:
        display_header("SecureBank International - Main Menu")
        print("1. 📊 Check Account Balance")
        print("2. 💸 Transfer Funds")
        print("3. 🧾 View Transaction History")
        print("4. 🏠 Loan Information")
        print("5. 📈 Investment Advice")
        print("6. 📅 Schedule Appointment")
        print("7. 🔒 Logout")

        choice = input("\nPlease select an option (1-7): ").strip()

        if choice == '1':
            response = get_account_balance(account_number)
            logging.info(f"{account_number} viewed account balance")
            print(f"\n✅ Account Balance Details:\n{response}")

        elif choice == '2':
            to_account = input("Enter the recipient's account number: ").strip()
            try:
                amount = float(input("Enter the amount to transfer: "))
                logging.info(f"{account_number} attempted transfer of {amount} to {to_account}")
                response = transfer_funds(account_number, to_account, amount)
                print(f"\n✅ Transfer Status:\n{response}")
            except ValueError:
                logging.warning(f"{account_number} entered invalid amount for transfer")
                print("❌ Invalid amount entered. Please enter a numeric value.")

        elif choice == '3':
            logging.info(f"{account_number} accessed transaction history")
            print(f"\n📄 Transaction History:\n{get_transaction_history(account_number)}")

        elif choice == '4':
            logging.info(f"{account_number} requested loan information")
            print(f"\n🏠 Loan Information:\n{get_loan_information()}")

        elif choice == '5':
            logging.info(f"{account_number} requested investment advice")
            print(f"\n📈 Investment Advice:\n{get_investment_advice()}")

        elif choice == '6':
            logging.info(f"{account_number} scheduled an appointment")
            print(f"\n📅 Appointment Scheduling:\n{schedule_appointment()}")

        elif choice == '7':
            logging.info(f"{account_number} logged out")
            print("\n🔒 You have been successfully logged out. Thank you for banking with us.")
            break

        else:
            print("⚠️ Invalid selection. Please choose a valid option (1-7).")

def welcome():
    display_header("Welcome to SecureBank International")
    while True:
        print("1. 📝 Register a New Account")
        print("2. 🔐 Login to Existing Account")
        print("3. ❎ Exit Application")

        option = input("\nPlease choose an option (1-3): ").strip()

        if option == '1':
            name = input("Enter your full name: ").strip()
            password = getpass("Create a secure password (input hidden): ")
            result = create_account(name, password)
            logging.info(f"New account registered for {name}")
            print(f"\n✅ Registration Successful:\n{result}")

        elif option == '2':
            account_number = input("Enter your account number: ").strip()
            password = getpass("Enter your password (input hidden): ")

            if validate_login(account_number, password):
                logging.info(f"{account_number} logged in successfully")
                print(f"\n🔓 Login Successful. Welcome back, {account_number}!")
                main_menu(account_number)
            else:
                logging.warning(f"Failed login attempt for account {account_number}")
                print("❌ Invalid credentials. Please try again.")

        elif option == '3':
            print("\n👋 Thank you for choosing SecureBank International.")
            break

        else:
            print("⚠️ Invalid selection. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    welcome()

# This helper will be imported by server.py
def run_banking_agent(user_input: str) -> str:
    return f"Agent received: {user_input}"

# banking_tools.py

import random
import string
from datetime import datetime

# In-memory database substitute
users_db = {}
transactions_db = {}

def generate_account_number():
    return "SBI" + ''.join(random.choices(string.digits, k=6))

def create_account(name, password):
    account_number = generate_account_number()
    users_db[account_number] = {
        "name": name,
        "password": password,
        "balance": 5000.0,
        "created_at": datetime.now(),
    }
    transactions_db[account_number] = []
    return f"✅ Account created successfully!\nAccount Number: {account_number}"

def validate_login(account_number, password):
    user = users_db.get(account_number)
    if user and user["password"] == password:
        return True
    return False

def get_account_balance(account_number):
    user = users_db.get(account_number)
    if user:
        return f"💰 Balance for {account_number}: ${user['balance']:.2f}"
    return "❌ Account not found."

def get_transaction_history(account_number):
    txs = transactions_db.get(account_number, [])
    if not txs:
        return "📭 No transactions found."
    history = "\n".join([f"{t['type']} ${t['amount']:.2f} on {t['date']}" for t in txs])
    return f"📄 Transaction History:\n{history}"

def transfer_funds(from_acc, to_acc, amount):
    sender = users_db.get(from_acc)
    receiver = users_db.get(to_acc)

    if not sender:
        return "❌ Sender account not found."
    if not receiver:
        return "❌ Recipient account not found."
    if sender["balance"] < amount:
        return "❌ Insufficient funds."

    sender["balance"] -= amount
    receiver["balance"] += amount

    tx = {
        "type": "Sent",
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    transactions_db[from_acc].append(tx)

    tx_receiver = {
        "type": "Received",
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    transactions_db[to_acc].append(tx_receiver)

    return f"✅ ${amount:.2f} transferred from {from_acc} to {to_acc}."

# Placeholder functions for next phase
def get_loan_information():
    return "📄 Loan options: Home Loan (5%), Car Loan (7%), Personal Loan (10%)"

def get_investment_advice():
    return "📊 Consider diversifying into mutual funds, ETFs, and fixed deposits."

def schedule_appointment():
    return "📅 Appointment scheduled with banking advisor."

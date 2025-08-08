from fastapi import FastAPI
from pydantic import BaseModel
import logging
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

app = FastAPI()

logging.basicConfig(
    filename="user_activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class ChatRequest(BaseModel):
    action: str
    params: dict

@app.get("/")
def home():
    return {"message": "SecureBank International API is running."}

@app.post("/chat")
def chat_endpoint(data: ChatRequest):
    action = data.action.lower()

    if action == "create_account":
        name = data.params.get("name")
        password = data.params.get("password")
        result = create_account(name, password)
        return {"response": result}

    elif action == "login":
        account_number = data.params.get("account_number")
        password = data.params.get("password")
        if validate_login(account_number, password):
            return {"response": f"Welcome back, {account_number}!"}
        return {"response": "Invalid credentials."}

    elif action == "check_balance":
        account_number = data.params.get("account_number")
        return {"response": get_account_balance(account_number)}

    elif action == "transfer_funds":
        account_number = data.params.get("account_number")
        to_account = data.params.get("to_account")
        amount = float(data.params.get("amount", 0))
        return {"response": transfer_funds(account_number, to_account, amount)}

    elif action == "transaction_history":
        account_number = data.params.get("account_number")
        return {"response": get_transaction_history(account_number)}

    elif action == "loan_info":
        return {"response": get_loan_information()}

    elif action == "investment_advice":
        return {"response": get_investment_advice()}

    elif action == "schedule_appointment":
        return {"response": schedule_appointment()}

    else:
        return {"response": "Unknown action."}

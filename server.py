from flask import Flask, request, jsonify
import banking_tools

app = Flask(__name__)

def run_banking_agent(user_input: str) -> str:
    """
    Simple logic to interpret commands from user_input.
    This is where you can replace with your AI/agent logic later.
    """
    text = user_input.lower()

    if "balance" in text:
        # For now, using a dummy account number
        return banking_tools.get_account_balance("1001")
    elif "transfer" in text:
        return "Please provide the recipient account number and amount."
    elif "loan" in text:
        return banking_tools.get_loan_information()
    elif "investment" in text:
        return banking_tools.get_investment_advice()
    elif "history" in text:
        return banking_tools.get_transaction_history("1001")
    else:
        return "Sorry, I didn’t understand that. Try: balance, transfer, loan, investment, history."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = run_banking_agent(user_input)
    return jsonify({"response": response})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "SecureBank API is running."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

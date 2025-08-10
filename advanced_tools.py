# advanced_tools.py
import random
from datetime import datetime, timedelta
from typing import Dict, Any

# Safe function_tool import with fallback
try:
    from agents import function_tool
except ImportError:
    def function_tool(func):
        """Fallback decorator if agents library not available"""
        func._is_tool = True
        return func

@function_tool
def check_account_status(account_number: str) -> Dict[str, Any]:
    """
    Check comprehensive account status including holds, restrictions, and alerts.
    """
    try:
        if not account_number or len(account_number.strip()) == 0:
            return {
                "error": "Invalid account number",
                "message": "Please provide a valid account number."
            }
        
        statuses = ["Active", "Restricted", "On Hold", "Frozen", "Closed"]
        alerts = ["Low Balance", "Unusual Activity", "Payment Due", "Document Required"]
        
        account_status = random.choice(statuses)
        has_alerts = random.choice([True, False])
        
        return {
            "account_number": f"****{account_number[-4:]}" if len(account_number) >= 4 else "****XXXX",
            "status": account_status,
            "status_since": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "has_restrictions": account_status in ["Restricted", "On Hold", "Frozen"],
            "active_alerts": [random.choice(alerts)] if has_alerts else [],
            "next_statement_date": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "last_login": (datetime.now() - timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "error": f"Status check failed: {str(e)}",
            "message": "Please contact customer service."
        }

@function_tool
def calculate_interest_earned(principal: float, rate: float, days: int) -> Dict[str, Any]:
    """
    Calculate interest earned on savings accounts and deposits.
    """
    try:
        # Input validation
        if principal <= 0:
            return {
                "error": "Invalid principal amount",
                "message": "Principal must be positive."
            }
        
        if rate < 0 or rate > 50:
            return {
                "error": "Invalid interest rate",
                "message": "Interest rate must be between 0% and 50%."
            }
        
        if days <= 0 or days > 3650:
            return {
                "error": "Invalid time period",
                "message": "Days must be between 1 and 3650 (10 years)."
            }
        
        daily_rate = rate / 100 / 365
        interest_earned = principal * daily_rate * days
        final_balance = principal + interest_earned
        
        return {
            "principal_amount": principal,
            "interest_rate": rate,
            "calculation_period_days": days,
            "daily_interest_rate": round(daily_rate * 100, 6),
            "interest_earned": round(interest_earned, 2),
            "final_balance": round(final_balance, 2),
            "annualized_yield": round((interest_earned / principal) * (365 / days) * 100, 2),
            "calculation_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"Interest calculation failed: {str(e)}",
            "message": "Please verify your input and try again."
        }

@function_tool
def get_exchange_rates(base_currency: str = "USD") -> Dict[str, Any]:
    """
    Get current exchange rates for international transfers.
    (Mock implementation - in production, this would connect to a real exchange rate API)
    """
    try:
        # Validate base currency
        valid_currencies = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CHF", "CNY", "INR", "MXN"]
        
        if base_currency not in valid_currencies:
            return {
                "error": "Invalid base currency",
                "message": f"Base currency must be one of: {', '.join(valid_currencies)}"
            }
        
        # Mock exchange rates (in production, fetch from real API)
        rates = {
            "EUR": round(random.uniform(0.82, 0.88), 4),
            "GBP": round(random.uniform(0.70, 0.76), 4),
            "CAD": round(random.uniform(1.20, 1.30), 4),
            "AUD": round(random.uniform(1.30, 1.40), 4),
            "JPY": round(random.uniform(105.0, 115.0), 2),
            "CHF": round(random.uniform(0.88, 0.96), 4),
            "CNY": round(random.uniform(6.20, 6.70), 4),
            "INR": round(random.uniform(72.0, 76.0), 2),
            "MXN": round(random.uniform(18.0, 22.0), 2)
        }
        
        # Remove base currency from rates if present
        if base_currency in rates:
            del rates[base_currency]
        
        return {
            "base_currency": base_currency,
            "rates": rates,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rate_source": "SecureBank International Exchange Desk",
            "disclaimer": "Rates are indicative and subject to change. Contact us for real-time rates."
        }
        
    except Exception as e:
        return {
            "error": f"Exchange rate retrieval failed: {str(e)}",
            "message": "Please try again later or contact customer service."
        }

@function_tool
def schedule_appointment(service_type: str, preferred_date: str, preferred_time: str) -> Dict[str, Any]:
    """
    Schedule an appointment with a banking specialist.
    """
    # Validate inputs
    if not service_type or len(service_type.strip()) == 0:
        return {
            "error": "Service type is required",
            "message": "Please specify the type of service you need."
        }
    
    if not preferred_date or len(preferred_date.strip()) == 0:
        return {
            "error": "Preferred date is required",
            "message": "Please provide your preferred appointment date."
        }
    
    if not preferred_time or len(preferred_time.strip()) == 0:
        return {
            "error": "Preferred time is required", 
            "message": "Please provide your preferred appointment time."
        }
    
    # Validate date format (basic validation)
    try:
        appointment_date = datetime.strptime(preferred_date, "%Y-%m-%d")
    except ValueError:
        return {
            "error": "Invalid date format",
            "message": "Please use YYYY-MM-DD format for the date."
        }
    if appointment_date < datetime.now():
        return {
            "error": "Invalid date",
            "message": "Appointment date cannot be in the past."
        }
    
    appointment_id = f"APT{random.randint(10000, 99999)}"
    
    specialists = {
        "loan_service": "Senior Loan Officer",
        "investment_service": "Investment Advisor", 
        "account_service": "Account Manager",
        "business_banking": "Business Banking Specialist",
        "general": "Customer Service Representative"
    }
    
    specialist = specialists.get(service_type.lower(), "Customer Service Representative")
    
    return {
        "appointment_id": appointment_id,
        "service_type": service_type,
        "specialist": specialist,
        "scheduled_date": preferred_date,
        "scheduled_time": preferred_time,
        "duration": "30 minutes",
        "location": "SecureBank International Main Branch",
        "preparation_required": "Please bring valid ID and relevant account documents",
        "confirmation_sent": True,
        "cancellation_policy": "24-hour advance notice required",
        "contact_number": "1-800-SECURE-BANK",
    }
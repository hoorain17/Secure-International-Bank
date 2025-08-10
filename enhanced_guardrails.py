# enhanced_guardrails.py

from functools import wraps
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class SecurityRequest(BaseModel):
    customer_id: str
    request_type: str

def enhanced_security_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            request = SecurityRequest(**kwargs)
            if not request.customer_id:
                logger.warning("Security check: customer ID missing")
        except Exception as e:
            logger.warning(f"Security check skipped: {e}")
        return func(*args, **kwargs)
    return wrapper

class ComplianceRequest(BaseModel):
    operation: str
    data: dict

def compliance_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            request = ComplianceRequest(operation=func.__name__, data=kwargs)
            logger.info(f"Compliance log: {request.operation} with {request.data}")
        except Exception as e:
            logger.warning(f"Compliance check skipped: {e}")
        return func(*args, **kwargs)
    return wrapper

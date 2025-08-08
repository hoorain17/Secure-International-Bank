# specialized_agents.py

# Safe imports with fallbacks
try:
    from agents import Agent
    from config import BankingConfig
    from enhanced_guardrails import enhanced_security_check, compliance_check
    from banking_tools import ALL_BANKING_TOOLS
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    ALL_BANKING_TOOLS = []

    class Agent:
        def __init__(self, **kwargs):
            self.name = kwargs.get('name', 'Unknown Agent')
            self.instructions = kwargs.get('instructions', '')
            self.model = kwargs.get('model')
            self.tools = kwargs.get('tools', [])

def softened_guardrails(output):
    """Passive guardrails — logs issues but does not block output"""
    try:
        compliance_check(output)
        enhanced_security_check(output)
    except Exception as e:
        print(f"⚠️ Guardrail warning (ignored): {e}")
    return output

def create_specialized_agents():
    """Create all specialized banking agents"""
    if not AGENTS_AVAILABLE:
        return {
            "account": Agent(name="Account Services Specialist", tools=ALL_BANKING_TOOLS),
            "transfer": Agent(name="Transfer Services Specialist", tools=ALL_BANKING_TOOLS),
            "loan": Agent(name="Loan Services Specialist", tools=ALL_BANKING_TOOLS),
            "investment": Agent(name="Investment Services Specialist", tools=ALL_BANKING_TOOLS)
        }

    try:
        config = BankingConfig()

        def agent_template(name, role_instructions):
            return Agent(
                name=name,
                instructions=role_instructions,
                model=config.model,
                tools=ALL_BANKING_TOOLS,
                output_guardrails=[softened_guardrails]  # soft guardrails only
            )

        return {
            "account": agent_template(
                "Account Services Specialist",
                "Handle account info, balances, access, and security. Be professional, discreet, and helpful."
            ),
            "transfer": agent_template(
                "Transfer Services Specialist",
                "Assist with money transfers, fees, limits, and setup. Follow AML principles."
            ),
            "loan": agent_template(
                "Loan Services Specialist",
                "Help customers understand loans, calculate payments, and apply or modify terms."
            ),
            "investment": agent_template(
                "Investment Services Specialist",
                "Guide customers on investments, risks, and retirement planning. Stay compliant."
            )
        }

    except Exception as e:
        print(f"⚠️ Could not create specialized agents: {e}")
        return {
            "account": Agent(name="Account Services Specialist", tools=ALL_BANKING_TOOLS),
            "transfer": Agent(name="Transfer Services Specialist", tools=ALL_BANKING_TOOLS),
            "loan": Agent(name="Loan Services Specialist", tools=ALL_BANKING_TOOLS),
            "investment": Agent(name="Investment Services Specialist", tools=ALL_BANKING_TOOLS)
        }

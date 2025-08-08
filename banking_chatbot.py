# banking_chatbot.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from specialized_agents import create_specialized_agents
import logging

# Initialize app
app = FastAPI(title="SecureBank Chatbot API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize logging
logging.basicConfig(filename="chatbot.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize agents
agents = create_specialized_agents()

# Request schema
class ChatRequest(BaseModel):
    user_id: str
    agent_type: str  # 'account', 'transfer', 'loan', 'investment'
    message: str

# Response schema
class ChatResponse(BaseModel):
    agent_name: str
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    agent = agents.get(request.agent_type)
    if not agent:
        return {"agent_name": "System", "response": "❌ Invalid service type."}

    # For now, the response is mocked (replace with actual agent call)
    mock_response = f"Thank you for your query: '{request.message}'. We are processing it."

    # Log conversation
    logging.info(f"UserID: {request.user_id} | Agent: {request.agent_type} | Msg: {request.message}")

    return ChatResponse(agent_name=agent.name, response=mock_response)

@app.get("/")
def root():
    return {"message": "✅ SecureBank Chatbot is live!"}

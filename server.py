from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import run_banking_agent  # Import your function from main.py

# Define request body structure
class ChatRequest(BaseModel):
    message: str

app = FastAPI()

# Allow calls from anywhere (for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    reply_text = run_banking_agent(request.message)
    return {"reply": reply_text}

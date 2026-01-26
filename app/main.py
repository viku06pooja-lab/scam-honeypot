from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
def root():
    return {"status": "ok", "message": "Scam Honeypot API is running"}

# API Key
API_KEY = "test123"

# Wrapper model matching platform input
class WrappedInput(BaseModel):
    audioBase64: str

# Message endpoint
app.post("/message")
def receive_message(data: WrappedInput, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    payload = json.loads(data.audioBase64)

    conversation_id = payload["conversation_id"]
    message = payload["message"]
scam_keywords = ["lottery", "investment", "bank account", "urgent", "prize"]
    is_scam = any(word in message.lower() for word in scam_keywords)

    reply = "Scam intent detected." if is_scam else "No scam intent detected."

    return {
        "reply": reply,
        "conversation_id": conversation_id
    }

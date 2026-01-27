from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

API_KEY = "test123"

# Health check
@app.get("/")
def root():
    return {"status": "ok"}

# Input model expected by GUVI honeypot tester
class WrappedInput(BaseModel):
    audioBase64: str

# Message endpoint
@app.post("/message")
def receive_message(data: WrappedInput, x_api_key: str = Header(None)):
    # API Key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Decode wrapped JSON string
    payload = json.loads(data.audioBase64)

    conversation_id = payload["conversation_id"]
    message = payload["message"]

    # Simple scam detection
    scam_keywords = ["lottery", "investment", "bank account", "urgent", "prize"]

    is_scam = any(word in message.lower() for word in scam_keywords)

    reply = "Scam intent detected." if is_scam else "No scam intent detected."

    return {
        "reply": reply,
        "conversation_id": conversation_id
    }

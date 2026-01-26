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

# === Input Models ===

# For GUVI platform request
class WrappedInput(BaseModel):
    audioBase64: str

# For Hoppscotch manual request
class DirectInput(BaseModel):
    conversation_id: str
    message: str


# === Unified Scam Detection Logic ===

def detect_scam(conversation_id: str, message: str):
    scam_keywords = ["lottery", "investment", "bank account", "urgent", "prize", "double money"]

    is_scam = any(word in message.lower() for word in scam_keywords)

    reply = "Scam intent detected." if is_scam else "No scam intent detected."

    return {
        "reply": reply,
        "conversation_id": conversation_id
    }


# === Endpoint ===

@app.post("/message")
def receive_message(data: dict, x_api_key: str = Header(None)):
    # API Key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Case 1: GUVI format → audioBase64 wrapper
    if "audioBase64" in data:
        try:
            payload = json.loads(data["audioBase64"])
            conversation_id = payload["conversation_id"]
            message = payload["message"]
            return detect_scam(conversation_id, message)
        except:
            raise HTTPException(status_code=400, detail="Invalid GUVI request body")

    # Case 2: Hoppscotch direct JSON
    elif "conversation_id" in data and "message" in data:
        return detect_scam(data["conversation_id"], data["message"])

    # Invalid body
    else:
        raise HTTPException(status_code=422, detail="Invalid request body")

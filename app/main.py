from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# Allow all CORS (required for GUVI tester)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class RequestModel(BaseModel):
    language: str
    audio_format: str
    audio_base64: str
# Health check
@app.get("/")
def root():
    return {"status": "ok"}

# API Key
API_KEY = "test123"

# ---- Input model expected by GUVI platform ----
class WrappedInput(BaseModel):
    audioBase64: str

# ---- Honeypot Endpoint ----
@app.post("/message")
def receive_message(data: WrappedInput, x_api_key: str = Header(None)):

    # API Key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Decode wrapped payload
    try:
        payload = json.loads(data.audioBase64)
        conversation_id = payload["conversation_id"]
        message = payload["message"]
    except:
        raise HTTPException(status_code=422, detail="Invalid Request Body")

    # ---- Scam detection logic ----
    scam_keywords = [
        "lottery", "investment", "bank", "account",
        "urgent", "otp", "prize", "suspended"
    ]

    is_scam = any(word in message.lower() for word in scam_keywords)

    if is_scam:
        reply_text = "SCAM DETECTED"
    else:
        reply_text = "NORMAL MESSAGE"

    # ---- Response format required by GUVI ----
    return {
        "reply": {
            "role": "assistant",
            "content": reply_text
        },
        "conversation_id": conversation_id
    }

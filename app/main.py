from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ======================
# Root Health Check
# ======================

@app.get("/")
def root():
    return {"status": "ok", "message": "Scam Honeypot API is running"}


# ======================
# API Key Setup
# ======================

API_KEY = "test123"   # You will submit this in GUVI form


# ======================
# Request Body Model
# ======================

class MessageIn(BaseModel):
    conversation_id: str
    message: str


# ======================
# Honeypot Message Endpoint
# ======================

@app.post("/message")
def receive_message(data: MessageIn, x_api_key: str = Header(None)):

    # --- API Key Validation ---
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # --- Simple Scam Detection Demo Logic ---
    user_message = data.message.lower()

    if "lottery" in user_message or "bank account" in user_message or "upi" in user_message:
        reply = "Oh really? Can you tell me more details?"
    else:
        reply = "I see. Please continue."

    # --- Mandatory Response Format ---
    return {"reply": reply}

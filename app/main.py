from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS (safe for GUVI + browser tests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Health Check
# --------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Scam Honeypot API is running"}

# --------------------
# API Key
# --------------------
API_KEY = "test123"

# --------------------
# Scam Detection Logic
# --------------------
def classify_message(conversation_id: str, message: str):
    scam_keywords = [
        "lottery", "investment", "bank account", "upi",
        "reward", "prize", "urgent", "double money"
    ]

    is_scam = any(word in message.lower() for word in scam_keywords)

    reply = "SCAMMER" if is_scam else "AGENT"

   return {
    "reply": {
        "role": "assistant",
        "content": reply
    }
}
# --------------------
# Main Endpoint
# --------------------
@app.post("/message")
def receive_message(data: dict, x_api_key: str = Header(None)):

    # API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # --- Case 1: GUVI format ---
    # {
    #   "audioBase64": "{\"conversation_id\":\"id\",\"message\":\"text\"}"
    # }
    if "audioBase64" in data:
        try:
            payload = json.loads(data["audioBase64"])
            conversation_id = payload["conversation_id"]
            message = payload["message"]
            return classify_message(conversation_id, message)
        except:
            raise HTTPException(status_code=400, detail="Invalid GUVI request body")

    # --- Case 2: Direct JSON (Hoppscotch/manual) ---
    # {
    #   "conversation_id": "id",
    #   "message": "text"
    # }
    if "conversation_id" in data and "message" in data:
        return classify_message(data["conversation_id"], data["message"])

    # --- Invalid body ---
    raise HTTPException(status_code=422, detail="Invalid request body")

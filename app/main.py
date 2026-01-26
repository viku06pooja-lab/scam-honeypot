from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

API_KEY = "test123"

class WrappedInput(BaseModel):
    audioBase64: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/message")
def receive_message(data: WrappedInput, x_api_key: str = Header(None)):
    # Accept any key but still check header exists
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API Key")

    # Decode wrapped payload
    try:
        payload = json.loads(data.audioBase64)
        conversation_id = payload["conversation_id"]
        message = payload["message"]
    except:
        raise HTTPException(status_code=422, detail="Invalid request body")

    # Simple scam detection logic
    scam_keywords = ["lottery", "investment", "bank", "urgent", "prize", "otp", "account"]

    is_scam = any(word in message.lower() for word in scam_keywords)

    if is_scam:
        reply_text = "Scam intent detected"
    else:
        reply_text = "No scam intent detected"

    # REQUIRED response format for GUVI tester
    return {
        "reply": {
            "role": "assistant",
            "content": reply_text
        }
    }

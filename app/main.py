from fastapi import FastAPI, Header, HTTPException, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

API_KEY = "test123"

class MessageIn(BaseModel):
    conversation_id: str
    message: str

@app.get("/")
def root():
    return {"status": "ok", "message": "Scam Honeypot API is running"}

@app.post("/message")
def receive_message(
    x_api_key: str = Header(None),
    data: Optional[MessageIn] = Body(None)
):
    # API Key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # GUVI sometimes sends empty body → handle fallback
    if data is None:
        raise HTTPException(status_code=422, detail="Missing request body")

    # Simple scam-detection demo reply
    text = data.message.lower()

    if "lottery" in text or "bank" in text or "account" in text:
        reply = "Oh really? Can you share more details?"
    else:
        reply = "Hello. How can I help you?"

    return {"reply": reply}

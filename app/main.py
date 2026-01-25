from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.store import (
    get_conversation, save_message,
    set_mode, get_mode,
    save_extracted, get_extracted
)

from app.detector import detect_scam_intent
from app.agent import agent_reply
from app.extractor import extract_intel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"status": "ok", "message": "Scam Honeypot API is running"}
API_KEY = "test123"  # Change this later

class MessageIn(BaseModel):
    conversation_id: str
    message: str
from fastapi import Body

@app.post("/guvi/message")
def guvi_entry(
    payload: dict = Body(...),
    x_api_key: str = Header(None)
):
    # Extract fields from GUVI format
    try:
        inner = payload["audioBase64"]
        # inner is a JSON string → convert to dict
        import json
        inner_data = json.loads(inner)

        conversation_id = inner_data["conversation_id"]
        message = inner_data["message"]

    except Exception:
        raise HTTPException(status_code=422, detail="Invalid GUVI payload")

    # Reuse your existing logic
    data = MessageIn(conversation_id=conversation_id, message=message)
    return receive_message(data, x_api_key)
@app.post("/message")
def receive_message(data: MessageIn, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    convo = get_conversation(data.conversation_id)

    # Save incoming message
    save_message(data.conversation_id, "user", data.message)

    mode = get_mode(data.conversation_id)

    # Detect scam if still normal
    if mode == "NORMAL":
        if detect_scam_intent(data.message):
            set_mode(data.conversation_id, "AGENT")
            mode = "AGENT"

    # If agent mode, generate agent reply
    if mode == "AGENT":
        # Extract intel
        extracted = extract_intel(data.message)
        save_extracted(data.conversation_id, extracted)

        reply = agent_reply(data.message)
    else:
        reply = "Hello! How can I help you?"

    # Save agent reply
    save_message(data.conversation_id, "agent", reply)

    return {
        "conversation_id": data.conversation_id,
        "reply": reply,
        "mode": mode,
        "extracted_intel": get_extracted(data.conversation_id)
    }

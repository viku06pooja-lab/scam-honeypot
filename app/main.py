from fastapi import FastAPI, Header, HTTPException,Request
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
async def receive_message(request: Request, x_api_key: str = Header(None)):

    raw = await request.body()

    if x_api_key != API_KEY:
        return {"error": "Invalid API Key"}

    try:
        body = json.loads(raw)
    except:
        return {"error": "Invalid JSON"}

    # --- Case 1: Agentic Honeypot direct format ---
    if "conversation_id" in body and "message" in body:
        conversation_id = body["conversation_id"]
        message = body["message"]

    # --- Case 2: Voice Detection wrapped format ---
    elif "audio_base64" in body:
        try:
            inner = json.loads(body["audio_base64"])
            conversation_id = inner.get("conversation_id","no_id")
            message = inner.get("message","")
        except:
            return {"error": "Bad audio_base64 format"}

    else:
        return {"error": "Unknown request schema", "received": body}

    # --- Scam detection ---
    scam_keywords = ["lottery","investment","bank account","urgent","prize"]
    is_scam = any(word in message.lower() for word in scam_keywords)

    result_text = "SCAM DETECTED" if is_scam else "NORMAL MESSAGE"

    return {
        "reply": {
            "role": "assistant",
            "content": result_text
        },
        "conversation_id": conversation_id
    }

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

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

API_KEY = "test123"

class MessageIn(BaseModel):
    conversation_id: str
    message: str

@app.post("/message")
def receive_message(data: MessageIn, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "reply": "Scam intent detected. Conversation logged.",
        "conversation_id": data.conversation_id
    }

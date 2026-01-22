# Scam Honeypot – Autonomous Scam Detection API

## Objective
This project exposes a public API that receives incoming chat messages, detects scam intent, activates an autonomous conversational agent, and extracts scam-related intelligence such as bank accounts, UPI IDs, and phishing URLs.

## Live API Endpoint
Base URL:
https://scam-honeypott.onrender.com

Message Endpoint:
POST /message

## Authentication
All requests must include an API key.

Header:
X-API-Key: test123

## Request Format

POST https://scam-honeypott.onrender.com/message

Headers:
Content-Type: application/json  
X-API-Key: test123  

Body:
{
  "conversation_id": "unique-id-001",
  "message": "Your incoming chat message"
}

## Response Format

{
  "conversation_id": "unique-id-001",
  "reply": "Autonomous agent response",
  "scam_detected": true,
  "extracted": {
    "bank_accounts": [],
    "upi_ids": [],
    "urls": []
  }
}

## Example Test

Request message:
"Send ₹5000 to UPI: demo@upi immediately"

Response:
scam_detected: true  
extracted.upi_ids: ["demo@upi"]

## Features Implemented
- Scam intent detection
- Autonomous conversational agent handoff
- Multi-turn conversation handling
- Structured intelligence extraction
- API key secured endpoint

## Tech Stack
Python, FastAPI, Uvicorn, Render Cloud

## How to Test
Use Hoppscotch or Postman to send POST requests to the /message endpoint with the provided format and API key.

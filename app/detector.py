SCAM_KEYWORDS = [
    "investment", "crypto", "profit", "transfer",
    "bank", "upi", "account", "lottery", "reward",
    "otp", "verification", "payment", "deposit"
]

def detect_scam_intent(message: str) -> bool:
    text = message.lower()
    for word in SCAM_KEYWORDS:
        if word in text:
            return True
    return False

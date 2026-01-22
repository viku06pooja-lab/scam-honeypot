# Autonomous scam engagement agent (simple scripted version)

def agent_reply(user_message: str):
    # Simple human-like baiting responses
    prompts = [
        "Oh really? Can you explain more?",
        "That sounds interesting. How does the payment work?",
        "Okay, what details do you need from me?",
        "Can you send me the account or payment link?"
    ]

    # Rotate reply based on message length
    index = len(user_message) % len(prompts)
    return prompts[index]

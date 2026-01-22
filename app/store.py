conversation_db = {}

def get_conversation(conversation_id):
    if conversation_id not in conversation_db:
        conversation_db[conversation_id] = {
            "history": [],
            "mode": "NORMAL",
            "extracted": {
                "bank_accounts": [],
                "upi_ids": [],
                "urls": []
            }
        }
    return conversation_db[conversation_id]

def save_message(conversation_id, role, message):
    convo = get_conversation(conversation_id)
    convo["history"].append({"role": role, "message": message})

def set_mode(conversation_id, mode):
    convo = get_conversation(conversation_id)
    convo["mode"] = mode

def get_mode(conversation_id):
    convo = get_conversation(conversation_id)
    return convo["mode"]

def save_extracted(conversation_id, extracted):
    convo = get_conversation(conversation_id)
    for key in convo["extracted"]:
        convo["extracted"][key].extend(extracted.get(key, []))

def get_extracted(conversation_id):
    convo = get_conversation(conversation_id)
    return convo["extracted"]

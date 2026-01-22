import re

BANK_REGEX = re.compile(r"\b\d{9,18}\b")
UPI_REGEX = re.compile(r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b")
URL_REGEX = re.compile(r"https?://[^\s]+")

def extract_intel(message: str):
    bank_accounts = BANK_REGEX.findall(message)
    upi_ids = UPI_REGEX.findall(message)
    urls = URL_REGEX.findall(message)

    return {
        "bank_accounts": bank_accounts,
        "upi_ids": upi_ids,
        "urls": urls
    }

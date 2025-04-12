
import re
import json
import time
from iraq import message
from datetime import datetime

def extract_email(output):
    try:
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', output)
        if email_match:
            return email_match.group(0)
    except Exception as e:
        print(f"Extract email error: {e}")
    return None

def wait_for_verification_code(email, timeout=120):
    print(f"⏳ Waiting for code at {email}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            _, out = message(EmailCheck=email)
            text = out.strip()
            code = extract_code_from_text(text)
            if code:
                return code
        except Exception as e:
            print(f"Error checking email: {e}")
        time.sleep(5)
    return None

def extract_code_from_text(text):
    match = re.search(r'\b(\d{4,8})\b', text)
    if match:
        return match.group(1)
    link_match = re.search(r'(https?://[^\s]+)', text)
    if link_match:
        return link_match.group(1)
    return None

def log_account(platform, email, password, username=None):
    entry = {
        "platform": platform,
        "email": email,
        "password": password,
        "username": username,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        with open("logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(entry)

    with open("logs.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

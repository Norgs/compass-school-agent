import os
import json
from pathlib import Path
import subprocess

GAPI = ["python3", os.path.expanduser("~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")]
DATA_DIR = Path.expanduser(Path("~/.hermes/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "compass_todo.json"

def fetch_compass_emails():
    res = subprocess.run(GAPI + ["gmail", "search", "compass", "--max", "10"], capture_output=True, text=True)
    if res.returncode != 0:
        print("Error searching Gmail:", res.stderr)
        return []
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print("Failed to parse JSON:", e, res.stdout)
        return []

def get_message_body(msg_id):
    res = subprocess.run(GAPI + ["gmail", "get", msg_id], capture_output=True, text=True)
    if res.returncode != 0:
        return ""
    try:
        data = json.loads(res.stdout)
        return data.get("body", "")
    except Exception:
        return ""

def process_emails():
    emails = fetch_compass_emails()
    items = []
    
    for i, mail in enumerate(emails):
        subject = mail.get("subject", "No Subject")
        sender = mail.get("from", "")
        date = mail.get("date", "")
        body = get_message_body(mail["id"])
        
        # Simple heuristic classification
        category = "Informational"
        cost = None
        deadline = None
        
        sub_lower = subject.lower()
        body_lower = body.lower()
        
        if "payment" in sub_lower or "cost" in body_lower or "$" in body:
            category = "Payment Needed"
        elif "consent" in sub_lower or "slip" in sub_lower or "booking" in sub_lower or "interview" in sub_lower:
            category = "Action Required"
        elif "excursion" in sub_lower or "camp" in sub_lower:
            category = "Excursion"

        # Determine child based on sender/content keywords and correct family baseline
        child = "Kids"
        text_blob = (sender + " " + subject + " " + body).lower()
        if "melbourne girls" in text_blob or "mgc" in text_blob:
            child = "Brae"
        elif "deepdene" in text_blob:
            child = "Ivy"
        elif "kew high" in text_blob or "jy" in text_blob or "quade" in text_blob:
            child = "Jy & Quade"

        items.append({
            "id": mail["id"],
            "child": child,
            "date": date[:16],
            "title": subject.replace("News: ", ""),
            "category": category,
            "deadline": deadline,
            "cost": cost,
            "summary": mail.get("snippet", "")[:150] + "..."
        })
    
    DB_PATH.write_text(json.dumps(items, indent=2))
    print(f"Processed {len(items)} Compass emails into dashboard store.")

if __name__ == "__main__":
    process_emails()

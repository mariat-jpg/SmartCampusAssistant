import json
from datetime import datetime, timedelta
import os
import re

os.makedirs("storage", exist_ok=True)

REMINDER_FILE = "storage/reminders.json"

def load_reminders():
    try:
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=2)

def add_reminder(text):
    reminders = load_reminders()

    # Try to extract a date from the text
    reminder = {
        "id": int(datetime.now().timestamp() * 1000),
        "text": text,
        "created": datetime.now().isoformat(),
        "due": None,
        "recurring": None,
        "type": "general"
    }

    # Detect type
    text_lower = text.lower()
    if any(word in text_lower for word in ["assignment", "submit", "deadline", "due"]):
        reminder["type"] = "deadline"
    elif any(word in text_lower for word in ["every monday", "every tuesday", "every wednesday",
                                               "every thursday", "every friday", "weekly"]):
        reminder["type"] = "recurring"
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
            if day in text_lower:
                reminder["recurring"] = day
    elif any(word in text_lower for word in ["hackathon", "seminar", "workshop", "fest", "event"]):
        reminder["type"] = "event"

    # Try to extract date (formats: April 5, Apr 5, 2025-04-05)
    months = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
              "july":7,"august":8,"september":9,"october":10,"november":11,"december":12,
              "jan":1,"feb":2,"mar":3,"apr":4,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
    
    if "tonight" in text_lower or "today" in text_lower:
        reminder["due"] = datetime.now().replace(hour=23, minute=59).isoformat()
    elif "tomorrow" in text_lower:
        reminder["due"] = (datetime.now() + timedelta(days=1)).isoformat()
    elif re.search(r'in (\d+) hour', text_lower):
        hours = int(re.search(r'in (\d+) hour', text_lower).group(1))
        reminder["due"] = (datetime.now() + timedelta(hours=hours)).isoformat()
    elif re.search(r'in (\d+) minute', text_lower):
        minutes = int(re.search(r'in (\d+) minute', text_lower).group(1))
        reminder["due"] = (datetime.now() + timedelta(minutes=minutes)).isoformat()
    elif re.search(r'in (\d+) day', text_lower):
        days = int(re.search(r'in (\d+) day', text_lower).group(1))
        reminder["due"] = (datetime.now() + timedelta(days=days)).isoformat()
    elif re.search(r'in (\d+) week', text_lower):
        weeks = int(re.search(r'in (\d+) week', text_lower).group(1))
        reminder["due"] = (datetime.now() + timedelta(weeks=weeks)).isoformat()
    
    pattern = r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2})'
    match = re.search(pattern, text_lower)
    if match:
        month = months[match.group(1)]
        day = int(match.group(2))
        year = datetime.now().year
        try:
            reminder["due"] = datetime(year, month, day).isoformat()
        except:
            pass

    reminders.append(reminder)
    save_reminders(reminders)
    return f"Reminder set: '{text}'"

def get_due_reminders():
    reminders = load_reminders()
    now = datetime.now()
    due = []
    for r in reminders:
        if r.get("due"):
            due_date = datetime.fromisoformat(r["due"])
            days_left = (due_date - now).days
            r["days_left"] = days_left
            due.append(r)
    return sorted(due, key=lambda x: x["days_left"])

def get_all_reminders():
    return load_reminders()

def delete_reminder(reminder_id):
    reminders = load_reminders()
    reminders = [r for r in reminders if r.get("id") != reminder_id]
    save_reminders(reminders)
    return "Reminder deleted."
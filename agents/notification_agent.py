import json

REMINDER_FILE = "storage/reminders.json"

def get_reminders():

    try:
        with open(REMINDER_FILE, "r") as f:
            reminders = json.load(f)
    except:
        reminders = []

    if not reminders:
        return "No reminders available."

    return "\n".join(reminders)
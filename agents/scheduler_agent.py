import json

REMINDER_FILE = "storage/reminders.json"

def add_reminder(text):

    try:
        with open(REMINDER_FILE, "r") as f:
            reminders = json.load(f)
    except:
        reminders = []

    reminders.append(text)

    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f)

    return "Reminder added successfully."
from agents.scheduler_agent import get_due_reminders, get_all_reminders
from datetime import datetime

def get_notifications():
    reminders = get_due_reminders()
    notifications = []

    for r in reminders:
        days_left = r.get("days_left", 0)
        if days_left < 0:
            status = "overdue"
        elif days_left == 0:
            status = "today"
        elif days_left <= 3:
            status = "soon"
        else:
            status = "upcoming"

        notifications.append({
            "text": r["text"],
            "days_left": days_left,
            "status": status,
            "type": r.get("type", "general"),
            "due": r.get("due"),
            "id": r.get("id")
        })

    return notifications
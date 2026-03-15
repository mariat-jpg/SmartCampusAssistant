from agents.query_agent import handle_query
from agents.scheduler_agent import add_reminder, get_all_reminders
from agents.notification_agent import get_notifications
from datetime import datetime

def route_query(query):
    q = query.lower()

    if "remind" in q or "reminder" in q:
        return add_reminder(query)

    elif "show reminders" in q or "my reminders" in q:
        reminders = get_all_reminders()
        if not reminders:
            return "No reminders saved yet."
        return "\n".join(f"- {r['text']}" for r in reminders)

    elif "notifications" in q:
        notifications = get_notifications()
        if not notifications:
            return "No upcoming notifications."
        return "\n".join(f"- {n['text']} ({n['status']})" for n in notifications)

    elif any(word in q for word in ["when is", "when's", "due", "deadline", "assignment"]):
        reminders = get_all_reminders()
        matches = []
        for r in reminders:
            if any(word in r["text"].lower() for word in q.split() if len(word) > 3):
                if r.get("due"):
                    due_date = datetime.fromisoformat(r["due"])
                    days_left = (due_date - datetime.now()).days
                    if days_left < 0:
                        timing = f"was due {abs(days_left)} day(s) ago"
                    elif days_left == 0:
                        timing = "is due today"
                    else:
                        timing = f"is due in {days_left} day(s) on {due_date.strftime('%B %d')}"
                    matches.append(f"'{r['text']}' {timing}")
        
        if matches:
            return "\n".join(matches)
        else:
            return handle_query(query)  # fall back to RAG if nothing found

    else:
        return handle_query(query)
from agents.query_agent import handle_query
from agents.scheduler_agent import add_reminder
from agents.notification_agent import get_reminders

def route_query(query):

    q = query.lower()

    if "remind" in q or "reminder" in q:
        return add_reminder(query)

    elif "show reminders" in q:
        return get_reminders()

    else:
        return handle_query(query)
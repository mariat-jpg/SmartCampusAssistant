import streamlit as st
import json
from backend import process_query
from agents.notification_agent import get_notifications
from agents.scheduler_agent import get_all_reminders, delete_reminder
from datetime import datetime

st.set_page_config(page_title="AI Smart Campus Assistant", layout="wide")

col_main, col_notif = st.columns([2, 1])

with col_main:
    st.title("AI Smart Campus Assistant")

    query = st.text_input("Ask your campus assistant", placeholder="e.g. when is the next hackathon?")

    if st.button("Submit"):
        if query:
            with st.spinner("Thinking..."):
                answer = process_query(query)
            st.success(answer)

            if "remind" in query.lower():
                notifications = get_notifications()
                just_added = [n for n in notifications if query in n["text"] or n["text"] == query]
                if just_added:
                    n = just_added[-1]
                    notif_list = json.dumps([{"text": n["text"], "status": n["status"]}])
                    st.components.v1.html(f"""
                        <script>
                        const n = {notif_list}[0];
                        const fire = () => new Notification("Reminder Set!", {{
                            body: n.text,
                            icon: "https://cdn-icons-png.flaticon.com/512/2232/2232688.png"
                        }});
                        if (Notification.permission === "granted") {{
                            fire();
                        }} else if (Notification.permission !== "denied") {{
                            Notification.requestPermission().then(p => {{ if (p === "granted") fire(); }});
                        }}
                        </script>
                    """, height=0)

    st.markdown("---")
    st.markdown("**Try asking:**")
    examples = [
        "When is the next hackathon?",
        "Who teaches AI?",
        "What is my Monday timetable?",
        "Remind me about the ML assignment due April 10",
        "Remind me every Monday about AI class",
    ]
    for ex in examples:
        if st.button(ex, key=ex):
            with st.spinner("Thinking..."):
                answer = process_query(ex)
            st.success(answer)

with col_notif:
    st.markdown("### Notifications")

    notifications = get_notifications()

    if not notifications:
        st.info("No upcoming reminders.")
    else:
        for n in notifications:
            days = n["days_left"]

            if n["status"] == "overdue":
                color = "🔴"
                label = f"Overdue by {abs(days)} day(s)"
            elif n["status"] == "today":
                color = "🟠"
                label = "Due today!"
            elif n["status"] == "soon":
                color = "🟡"
                label = f"Due in {days} day(s)"
            else:
                color = "🟢"
                label = f"Due in {days} day(s)"

            with st.expander(f"{color} {n['text'][:40]}..."):
                st.write(f"**Status:** {label}")
                st.write(f"**Type:** {n['type'].capitalize()}")
                if n.get("due"):
                    due_date = datetime.fromisoformat(n["due"]).strftime("%B %d, %Y")
                    st.write(f"**Due:** {due_date}")
                if st.button("Delete", key=f"del_{n['id']}"):
                    delete_reminder(n["id"])
                    st.rerun()

    st.markdown("---")
    st.markdown("### All Reminders")
    all_reminders = get_all_reminders()
    recurring = [r for r in all_reminders if r.get("type") == "recurring"]

    if recurring:
        st.markdown("**Recurring:**")
        for r in recurring:
            st.write(f"🔁 {r['text']}")

    if not all_reminders:
        st.write("No reminders saved yet.")
    else:
        st.write(f"Total: {len(all_reminders)} reminder(s)")
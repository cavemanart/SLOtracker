import streamlit as st
from core.storage import load_json, save_json, POSTMORTEM_FILE
import datetime

def render_postmortem_tracker():
    st.title("Postmortem Tracker")

    pms = load_json(POSTMORTEM_FILE)

    with st.expander("➕ Add Postmortem Action"):
        title = st.text_input("Action Item")
        due = st.date_input("Due Date", value=datetime.date.today())
        status = st.selectbox("Status", ["Open", "Closed"])

        if st.button("Save Action Item"):
            pms.append({
                "title": title,
                "due": str(due),
                "status": status
            })
            save_json(POSTMORTEM_FILE, pms)
            st.success("Saved.")

    overdue = [
        pm for pm in pms
        if pm["status"] != "Closed" and datetime.date.fromisoformat(pm["due"]) < datetime.date.today()
    ]

    st.metric("Open Items", sum(1 for pm in pms if pm["status"] == "Open"))
    st.metric("Overdue", len(overdue))
    st.metric("Closed in Time %", f"{100 * sum(1 for pm in pms if pm['status'] == 'Closed') / len(pms):.0f}%" if pms else "N/A")

    for pm in pms[::-1]:
        st.markdown(f"- **{pm['title']}** – `{pm['status']}` – _Due: {pm['due']}_")

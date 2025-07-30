import streamlit as st
from core.storage import load_json, save_json, INCIDENT_FILE
import datetime

def render_incident_tracker():
    st.title("Incident & MTTR Tracker")

    incidents = load_json(INCIDENT_FILE)

    with st.expander("➕ Add Incident"):
        sev = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        ack = st.time_input("Acknowledged At", value=datetime.datetime.now())
        res = st.time_input("Resolved At", value=datetime.datetime.now())

        if st.button("Log Incident"):
            duration = (res - ack).total_seconds() / 60
            incidents.append({
                "severity": sev,
                "ack": str(ack),
                "res": str(res),
                "duration_min": duration
            })
            save_json(INCIDENT_FILE, incidents)
            st.success(f"Logged with MTTR: {duration:.1f} mins")

    if incidents:
        df = pd.DataFrame(incidents)
        st.dataframe(df)

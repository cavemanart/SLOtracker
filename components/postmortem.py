import streamlit as st
import pandas as pd

# This will be passed from the incident CSV upload
INCIDENT_CACHE_KEY = "incident_data"


def render_postmortem_log():
    st.title("🧠 Postmortem Log")

    if INCIDENT_CACHE_KEY not in st.session_state:
        st.info("Please upload an incident CSV file from the Incident Log first.")
        return

    df = st.session_state[INCIDENT_CACHE_KEY]

    st.subheader("📋 Incident Overview")
    st.dataframe(df, use_container_width=True)

    st.subheader("🔍 High Severity Postmortems")
    if "severity" in df.columns:
        high_sev = df[df["severity"].astype(str).str.lower().isin(["1", "2"])]
        st.write(high_sev[["incident number", "short description", "assigned to", "severity", "state"]])
    else:
        st.warning("'severity' column not found in incident data.")

    st.subheader("📌 SLA Breach Summary")
    if "made sla" in df.columns:
        breached = df[df["made sla"].astype(str).str.lower() == "false"]
        st.write(breached[["incident number", "short description", "assignment group", "made sla"]])

    st.subheader("🕵️ Manual Postmortem Notes")
    for i in range(min(3, len(df))):
        with st.expander(f"Postmortem for Incident #{df.iloc[i]['incident number']}"):
            st.text_area("Root Cause Analysis", key=f"rca_{i}")
            st.text_area("Lessons Learned", key=f"lessons_{i}")
            st.text_area("Preventative Actions", key=f"actions_{i}")

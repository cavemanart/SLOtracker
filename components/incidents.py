import streamlit as st

def render_incident_log():
    st.subheader("🛠️ Incident Log")
    st.text_area("Describe the incident", key="incident_desc")
    st.date_input("Date of Incident", key="incident_date")
    st.button("Log Incident", key="log_incident")

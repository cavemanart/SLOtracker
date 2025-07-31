import streamlit as st
from components.incidents import render_incident_log
from components.slo_dashboard import render_dashboard
from components.input_slo import render_input_slo
from components.postmortem import render_postmortem

st.set_page_config(layout="wide")
tabs = st.tabs(["SLO Dashboard", "Input SLOs", "Incident Log", "Postmortems"])

with tabs[0]:
    render_dashboard()

with tabs[1]:
    render_input_slo()

with tabs[2]:
    render_incident_log()

with tabs[3]:
    render_postmortem()

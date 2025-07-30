import streamlit as st
from components.incidents import render_incident_log
from components.postmortem import render_postmortem_log
from components.input_slo import render_slo_input
from components.slo_dashboard import render_slo_dashboard
from components.trends import render_trends
from core.utils import load_styles

st.set_page_config(page_title="SLO Tracker", layout="wide")
load_styles()

st.title("📊 SLO Tracker")

tabs = st.tabs(["SLO Dashboard", "Input SLOs", "Incident Log", "Postmortem Log", "Trends"])

with tabs[0]:
    render_slo_dashboard()

with tabs[1]:
    render_slo_input()

with tabs[2]:
    render_incident_log()

with tabs[3]:
    render_postmortem_log()

with tabs[4]:
    render_trends()

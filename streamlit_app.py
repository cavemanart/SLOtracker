import streamlit as st
from components.dashboard import render_dashboard
from components.input_slo import render_slo_input
from components.trends import render_trend_charts
from components.postmortems import render_postmortem_tracker
from components.incidents import render_incident_tracker
from core.utils import load_styles

st.set_page_config(page_title="SLOTracker Pro", layout="wide")
load_styles()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "SLO Dashboard",
    "Add / Evaluate SLOs",
    "Trends & History",
    "Incident & MTTR",
    "Postmortems",
])

if page == "SLO Dashboard":
    render_dashboard()
elif page == "Add / Evaluate SLOs":
    render_slo_input()
elif page == "Trends & History":
    render_trend_charts()
elif page == "Incident & MTTR":
    render_incident_tracker()
elif page == "Postmortems":
    render_postmortem_tracker()

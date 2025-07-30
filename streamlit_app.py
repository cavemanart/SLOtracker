# slotracker/streamlit_app.py

import streamlit as st
from components.incidents import render_incident_tracker
from components.postmortems import render_postmortem_tracker
from components.slo_dashboard import render_slo_dashboard
from core.utils import load_styles

# Load custom CSS
load_styles()

# Sidebar navigation
st.sidebar.title("SLO Tracker Navigation")
page = st.sidebar.radio("Go to", ["SLO Dashboard", "Incidents", "Postmortems"])

# Routing
if page == "SLO Dashboard":
    render_slo_dashboard()
elif page == "Incidents":
    render_incident_tracker()
elif page == "Postmortems":
    render_postmortem_tracker()

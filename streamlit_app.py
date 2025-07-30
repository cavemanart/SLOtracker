import streamlit as st
from core.utils import load_styles
from components.input_slo import show_slo_input
from components.dashboard import show_dashboard
from components.trends import show_trends
from components.incidents import show_incidents
from components.postmortems import show_postmortems

load_styles()

st.sidebar.title("SLOTracker Pro")
tab = st.sidebar.radio("Navigate", [
    "SLO Input",
    "Dashboard",
    "Trends",
    "Incidents",
    "Postmortems"
])

if tab == "SLO Input":
    show_slo_input()
elif tab == "Dashboard":
    show_dashboard()
elif tab == "Trends":
    show_trends()
elif tab == "Incidents":
    show_incidents()
elif tab == "Postmortems":
    show_postmortems()

slotracker/streamlit_app.py

import streamlit as st from core.utils import load_styles from components.input_slo import render_slo_input from components.dashboard import render_dashboard from components.trends import render_trend_charts from components.incidents import render_incident_tracker from components.postmortems import render_postmortem_tracker

st.set_page_config(page_title="SLOTracker Pro", layout="wide") load_styles()

st.title("📈 SLOTracker Pro")

menu = st.sidebar.radio("Navigate", [ "SLO & SLI Input", "Dashboard", "Trends", "Incidents", "Postmortems"])

if menu == "SLO & SLI Input": render_slo_input() elif menu == "Dashboard": render_dashboard() elif menu == "Trends": render_trend_charts() elif menu == "Incidents": render_incident_tracker() elif menu == "Postmortems": render_postmortem_tracker()


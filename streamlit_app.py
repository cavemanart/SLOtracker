import streamlit as st
from dashboards.slo_dashboard import render_slo_dashboard
from dashboards.metrics_upload import render_metrics_upload
from dashboards.appdynamics_dashboard import render_appdynamics_dashboard

st.set_page_config(page_title="SLO Tracker", layout="wide")

st.sidebar.title("SLO Tracker Navigation")
page = st.sidebar.selectbox("Select a view", [
    "📊 SLO Dashboard",
    "⬆️ Upload & Analyze Metrics",
    "📈 AppDynamics Insights"
])

if page == "📊 SLO Dashboard":
    render_slo_dashboard()
elif page == "⬆️ Upload & Analyze Metrics":
    render_metrics_upload()
elif page == "📈 AppDynamics Insights":
    render_appdynamics_dashboard()

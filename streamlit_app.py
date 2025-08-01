import streamlit as st
from dashboards.slo_dashboard import render_slo_dashboard
from dashboards.metrics_upload import render_metrics_upload
from dashboards.appdynamics_dashboard import render_appdynamics_dashboard
from dashboards.sre_csv_insights import render_appd_csv_insights, render_bt_csv_insights

st.set_page_config(page_title="SLO Tracker", layout="wide")

st.sidebar.title("SLO Tracker Navigation")
page = st.sidebar.selectbox("Select a view", [
    "📊 SLO Dashboard",
    "⬆️ Upload & Analyze Metrics",
    "📈 AppDynamics Insights",
    "📊 AppD CSV Insights",
    "🧠 BT Insights"
])

if page == "📊 SLO Dashboard":
    render_slo_dashboard()
elif page == "⬆️ Upload & Analyze Metrics":
    render_metrics_upload()
elif page == "📈 AppDynamics Insights":
    render_appdynamics_dashboard()
elif page == "📊 AppD CSV Insights":
    render_appd_csv_insights()
elif page == "🧠 BT Insights":
    render_bt_csv_insights()

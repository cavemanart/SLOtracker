import streamlit as st
from components import input_slo, dashboard, trends, incidents, postmortems
from core.utils import load_styles

load_styles()

st.set_page_config(page_title="SLOTracker Pro", layout="wide")

st.title("📊 SLOTracker Pro")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📥 Input SLOs", "📈 Dashboard", "📉 Trends", "🚨 Incidents", "📜 Postmortems"])

with tab1:
    input_slo.render()

with tab2:
    dashboard.render()

with tab3:
    trends.render()

with tab4:
    incidents.render()

with tab5:
    postmortems.render()

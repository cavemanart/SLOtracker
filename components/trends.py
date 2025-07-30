import streamlit as st
import pandas as pd
import plotly.express as px
from core.storage import load_metrics

def render():
    st.subheader("📉 Historical Trends")
    st.markdown("This will chart SLI/SLO performance over time.")

    slo_data = load_metrics("slo_data.json")
    if not slo_data:
        st.info("No data to visualize yet.")
        return

    sample = pd.DataFrame({
        "date": pd.date_range(end=pd.Timestamp.today(), periods=7),
        "availability": [99.1, 99.3, 99.7, 99.8, 99.5, 99.6, 99.9]
    })
    fig = px.line(sample, x="date", y="availability", title="Availability Trend")
    st.plotly_chart(fig, use_container_width=True)

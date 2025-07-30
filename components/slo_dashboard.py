import streamlit as st
import pandas as pd
from core.storage import load_data

def render_slo_dashboard():
    st.subheader("📈 SLO Dashboard")

    data = load_data()

    if data.empty:
        st.info("No SLO data available. Use the 'Input SLOs' tab to get started.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Uptime %", f"{data['availability'].mean():.2f}%")
        st.metric("Error Budget Remaining", f"{100 - data['error_rate'].mean():.2f}%")
        st.metric("Avg Latency (ms)", f"{data['latency'].mean():.0f}")

    with col2:
        st.metric("SLI Target (%)", f"{data['sli_target'].mean():.2f}%")
        st.metric("SLO Achieved", f"{(data['availability'] > data['sli_target']).mean() * 100:.2f}%")
        st.metric("Total Records", len(data))

    st.dataframe(data)

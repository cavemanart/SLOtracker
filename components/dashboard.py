import streamlit as st
from core.storage import load_metrics
from core.compute import calculate_sli

def render():
    st.subheader("📈 Real-Time SLI Dashboard")
    data = load_metrics("slo_data.json")
    if not data:
        st.info("No data to visualize.")
        return

    for entry in data:
        st.metric(label=f"{entry['service']} - {entry['metric']}",
                  value=entry['target'],
                  delta="Live SLI placeholder")

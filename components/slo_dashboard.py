import streamlit as st
import json
import pandas as pd
from pathlib import Path

def render_dashboard():
    st.title("📈 SLO Dashboard")
    slo_file = Path("data/slo_data.json")

    if not slo_file.exists():
        st.warning("No SLO data found.")
        return

    with open(slo_file) as f:
        slo_data = json.load(f)

    if not slo_data:
        st.warning("No SLOs defined.")
        return

    st.subheader("📋 Current SLOs and SLIs")

    for entry in slo_data:
        with st.container():
            st.markdown(f"### {entry['service']}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Target (%)", entry["target"])
            with col2:
                st.metric("SLI (%)", entry.get("sli", "N/A"))
            with col3:
                st.write(f"Description: {entry['description']}")

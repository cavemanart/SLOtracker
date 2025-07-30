import streamlit as st
import pandas as pd
from core.data import get_sample_data
from core.metrics import evaluate_status

def render_dashboard():
    st.title("📊 SLA / SLO / SLI Tracker Dashboard")

    st.markdown("Use this dashboard to input and track SLAs and SLOs for your services.")

    df = get_sample_data()
    df["Status"] = df.apply(
        lambda row: evaluate_status(row["SLO Target"], row["Current Value"], "latency" in row["SLI (Metric)"].lower() or "error" in row["SLI (Metric)"].lower()),
        axis=1
    )

    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="main_editor")

    if st.button("🔁 Recalculate Status"):
        edited_df["Status"] = edited_df.apply(
            lambda row: evaluate_status(row["SLO Target"], row["Current Value"], "latency" in row["SLI (Metric)"].lower() or "error" in row["SLI (Metric)"].lower()),
            axis=1
        )
        st.success("Statuses updated!")

    st.markdown("### 📋 Current SLOs Overview")
    st.dataframe(edited_df, use_container_width=True)

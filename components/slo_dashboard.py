import streamlit as st
import json
import os
import pandas as pd

SLO_DATA_FILE = "core/storage/slo_data.json"

def load_slo_data():
    if not os.path.exists(SLO_DATA_FILE) or os.path.getsize(SLO_DATA_FILE) == 0:
        return []
    with open(SLO_DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def render_slo_dashboard():
    st.header("📊 SLO Dashboard")

    slo_data = load_slo_data()
    if not slo_data:
        st.info("No SLOs found. Add some in the 'Input SLOs' tab.")
        return

    df = pd.DataFrame(slo_data)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df = df.sort_values("created_at", ascending=False)

    st.dataframe(df, use_container_width=True)

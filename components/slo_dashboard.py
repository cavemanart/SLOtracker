import streamlit as st
import json
import os
import pandas as pd

SLO_DATA_PATH = "core/storage/slo_data.json"

def load_slo_data():
    if os.path.exists(SLO_DATA_PATH):
        with open(SLO_DATA_PATH, "r") as f:
            return json.load(f)
    return []

def render_slo_dashboard():
    st.title("📊 SLO Dashboard")

    slo_entries = load_slo_data()
    if not slo_entries:
        st.info("No SLO data available. Please input some SLOs first.")
        return

    df = pd.DataFrame(slo_entries)
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Aggregated SLO Insights")
    if "Objective" in df.columns and "Success Rate" in df.columns:
        df["Met Objective"] = df["Success Rate"] >= df["Objective"]
        met_count = df["Met Objective"].sum()
        total = len(df)
        st.metric("SLOs Met", f"{met_count} / {total}")

        category_breakdown = df["Category"].value_counts()
        st.bar_chart(category_breakdown)

        if "Success Rate" in df.columns:
            st.line_chart(df.set_index("Service")["Success Rate"])
    else:
        st.warning("Missing required fields for insights.")

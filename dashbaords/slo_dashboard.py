import streamlit as st
import pandas as pd
from utils.storage import save_custom_metrics, load_custom_metrics
from utils.graphs import render_trend_graphs
from utils.metric_logic import compute_threshold_violations

def render_slo_dashboard():
    st.title("📊 SLO/SLI/KPI Dashboard")

    st.subheader("Custom Metrics")
    metrics = load_custom_metrics()

    if metrics:
        df = pd.DataFrame(metrics)
        st.dataframe(df)

        st.download_button("📥 Export CSV", df.to_csv(index=False), "custom_metrics.csv", "text/csv")

        render_trend_graphs(df)

        with st.expander("🔍 Auto-Threshold Logic"):
            result = compute_threshold_violations(df)
            st.write(result)
    else:
        st.info("No custom metrics loaded yet.")

    with st.expander("💾 Save / Load"):
        if st.button("💾 Save Current Metrics"):
            save_custom_metrics()
            st.success("Metrics saved.")
        if st.button("📤 Load Saved Metrics"):
            st.experimental_rerun()

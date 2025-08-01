import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from utils.csv_utils import parse_appdynamics_csv
from datetime import datetime

DATA_DIR = "data"
SAVED_METRICS_FILE = os.path.join(DATA_DIR, "saved_metrics.json")

def load_saved_metrics():
    if os.path.exists(SAVED_METRICS_FILE):
        with open(SAVED_METRICS_FILE, "r") as f:
            return json.load(f)
    return []

def save_metrics(metrics):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SAVED_METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

def calculate_thresholds(df, column, threshold_factor=1.5):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + threshold_factor * iqr
    return upper_bound

def render_custom_metrics_section():
    st.header("📊 Custom SLO Metrics")
    metrics = load_saved_metrics()

    with st.expander("➕ Add New Metric"):
        name = st.text_input("Metric Name")
        value = st.number_input("Value", step=0.01)
        target = st.number_input("Target (optional)", step=0.01, value=0.0)
        unit = st.text_input("Unit (e.g. %, ms, count)")
        save_btn = st.button("Save Metric")

        if save_btn and name:
            metrics.append({
                "name": name,
                "value": value,
                "target": target,
                "unit": unit,
                "timestamp": datetime.utcnow().isoformat()
            })
            save_metrics(metrics)
            st.success(f"Saved metric '{name}'.")

    if metrics:
        df = pd.DataFrame(metrics)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Export CSV", csv, file_name="custom_slo_metrics.csv", mime="text/csv")

        # Placeholder for anomaly detection & trends
        st.subheader("📈 Historical View & Trends")
        fig = px.line(df, x="timestamp", y="value", color="name", markers=True)
        st.plotly_chart(fig, use_container_width=True)

def render_appdynamics_upload_section():
    st.header("📥 Upload AppDynamics Application CSV")
    uploaded_file = st.file_uploader("Upload Application Export CSV", type=["csv"])
    if uploaded_file:
        df = parse_appdynamics_csv(uploaded_file)
        if df is not None:
            st.success("CSV parsed successfully.")
            st.dataframe(df)

            # Threshold-based alert
            if "Response Time (ms)" in df.columns:
                rt_threshold = calculate_thresholds(df, "Response Time (ms)")
                st.info(f"Auto-calculated response time threshold: {rt_threshold:.2f} ms")

                high_latency = df[df["Response Time (ms)"] > rt_threshold]
                if not high_latency.empty:
                    st.warning(f"⚠️ {len(high_latency)} transactions exceed response time threshold.")
                    st.dataframe(high_latency)

            # Graphs
            st.subheader("📊 Application Metrics Overview")
            if "Calls / min" in df.columns and "Errors / min" in df.columns:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df["Name"], y=df["Calls / min"], name="Calls / min"))
                fig.add_trace(go.Bar(x=df["Name"], y=df["Errors / min"], name="Errors / min"))
                fig.update_layout(barmode='stack', xaxis_title="Transaction", yaxis_title="Rate")
                st.plotly_chart(fig, use_container_width=True)

def render_slo_dashboard():
    st.title("🎯 SLO/SLI/KPI Tracker")
    st.caption("Flexible dashboard for SREs to track service level metrics, business transaction health, and trends.")
    
    render_custom_metrics_section()
    st.markdown("---")
    render_appdynamics_upload_section()

import sys
import os

# Add 'core' folder to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from parser import parse_excel
from calculator import evaluate_slos
from visualizer import plot_sli_trends

import streamlit as st
import pandas as pd
import yaml

st.set_page_config(page_title="SLO Dashboard", layout="wide")
st.title("📊 SLO Compliance Dashboard")

mode = st.radio("Select input mode:", ["Upload Excel file", "Manual Data Input"])

df = None

if mode == "Upload Excel file":
    uploaded_file = st.file_uploader("Upload your Excel metrics file", type=[".xlsx"])
    if uploaded_file is not None:
        df = parse_excel(uploaded_file)

elif mode == "Manual Data Input":
    default_data = {
        "timestamp": ["2025-07-01 00:00:00", "2025-07-02 00:00:00"],
        "metric_name": ["auth_api_availability", "auth_api_availability"],
        "success_count": [995, 997],
        "total_count": [1000, 1000],
        "latency_p95": [280, 290],
    }
    df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

if df is not None:
    # Ensure 'timestamp' column is datetime dtype
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    st.subheader("Raw Metrics Preview")
    st.dataframe(df.head())

    with open("config/slo_definitions.yaml", "r") as f:
        slo_config = yaml.safe_load(f)

    results = evaluate_slos(df, slo_config)

    st.subheader("SLO Evaluation Results")
    for service_result in results:
        st.markdown(f"### {service_result['service']}")
        for slo in service_result['slos']:
            col1, col2 = st.columns([1, 3])
            with col1:
                status = "✅ PASS" if slo['compliant'] else "❌ FAIL"
                st.metric(label=slo['name'], value=status)
            with col2:
                plot_sli_trends(df, slo)

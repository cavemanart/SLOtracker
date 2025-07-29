import sys
import os

# Add 'core' folder to Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from parser import parse_excel
from calculator import evaluate_slos
from visualizer import plot_sli_trends

import streamlit as st
import pandas as pd
import yaml

st.set_page_config(page_title="SLO Dashboard", layout="wide")
st.title("📊 SLO Compliance Dashboard")

uploaded_file = st.file_uploader("Upload your Excel metrics file", type=[".xlsx"])

if uploaded_file:
    df = parse_excel(uploaded_file)

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

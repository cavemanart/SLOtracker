import streamlit as st
import json
import os
from datetime import datetime

SLO_DATA_FILE = "core/storage/slo_data.json"

def load_slo_data():
    if not os.path.exists(SLO_DATA_FILE):
        return []
    with open(SLO_DATA_FILE, "r") as f:
        return json.load(f)

def save_slo_data(data):
    with open(SLO_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def render_slo_input():
    st.title("📈 Input Service Level Objectives (SLOs)")

    with st.form("slo_input_form", clear_on_submit=True):
        service_name = st.text_input("Service Name")
        slo_description = st.text_area("SLO Description")
        objective_percent = st.slider("Objective % (e.g. 99.9)", 90.0, 100.0, 99.9)
        measurement_window = st.selectbox("Measurement Window", ["7 days", "30 days", "90 days"])
        sli_metric = st.text_input("SLI Metric (e.g. request latency < 300ms)")

        submit = st.form_submit_button("Submit SLO")

    if submit:
        if not service_name or not slo_description or not sli_metric:
            st.warning("Please fill in all fields.")
        else:
            slo_data = load_slo_data()
            slo_data.append({
                "service_name": service_name,
                "description": slo_description,
                "objective": objective_percent,
                "window": measurement_window,
                "sli_metric": sli_metric,
                "timestamp": datetime.utcnow().isoformat()
            })
            save_slo_data(slo_data)
            st.success(f"SLO for '{service_name}' saved.")

    st.markdown("---")
    if st.checkbox("Show Current SLOs"):
        data = load_slo_data()
        if data:
            for slo in data[::-1]:
                st.markdown(f"**{slo['service_name']}** — {slo['objective']}% over {slo['window']}<br><small>{slo['description']}</small>", unsafe_allow_html=True)
        else:
            st.info("No SLOs saved yet.")

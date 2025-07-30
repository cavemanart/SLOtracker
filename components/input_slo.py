import streamlit as st
from core.storage import save_metrics, load_metrics
from core.suggestions import suggest_slo_targets

def render():
    st.subheader("📥 Define New SLO")
    service = st.text_input("Service Name")
    metric = st.selectbox("Metric Type", ["Availability", "Latency", "Error Rate", "Throughput"])
    target = st.text_input("SLO Target", placeholder=suggest_slo_targets(metric))

    if st.button("➕ Add SLO"):
        entry = {"service": service, "metric": metric, "target": target}
        data = load_metrics("slo_data.json")
        data.append(entry)
        save_metrics("slo_data.json", data)
        st.success("SLO added successfully!")

    st.markdown("---")
    st.subheader("📋 Current SLOs")
    data = load_metrics("slo_data.json")
    if data:
        st.table(data)
    else:
        st.info("No SLOs defined yet.")

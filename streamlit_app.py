import streamlit as st
import pandas as pd
from core.metrics_loader import load_metrics, get_health_score
from core.suggestions import suggest_improvements
from core.storage import save_metrics
from core.config import DEFAULT_SLO

st.set_page_config(page_title="SLA/SLO Dashboard", layout="wide")

st.title("📊 SLA/SLO Dashboard for SREs")

metrics = load_metrics()

with st.expander("➕ Add New Service Metric"):
    service = st.text_input("Service Name")
    sli = st.text_input("SLI Description (e.g., p95 latency < 300ms)")
    slo_target = st.text_input("SLO Target (e.g., 99.9%)")
    current_value = st.text_input("Current Value (e.g., 99.5%)")

    if st.button("Add Metric"):
        metrics.append({
            "Service": service,
            "SLI": sli,
            "SLO Target": slo_target,
            "Current Value": current_value,
            "Status": "Met" if current_value >= slo_target else "Not Met"
        })
        save_metrics(metrics)
        st.success("Metric added!")

st.subheader("📋 Current SLA/SLO Tracking")

if metrics:
    df = pd.DataFrame(metrics)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No metrics added yet.")

health_score = get_health_score(metrics)
st.metric("🔧 Overall SRE Health Score", f"{health_score}%")

st.subheader("💡 Suggestions")
for tip in suggest_improvements(metrics):
    st.markdown(f"✅ {tip}")

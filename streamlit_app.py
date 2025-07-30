import streamlit as st
from core.storage import save_metrics, load_metrics
from core.suggestions import suggest_improvements
from core.metrics import calculate_status

st.set_page_config(page_title="SLO Tracker", layout="wide")
st.title("📊 SLO/SLA Tracker for SREs")

if "metrics" not in st.session_state:
    st.session_state["metrics"] = load_metrics()

st.sidebar.header("Add New Metric")
with st.sidebar.form("metric_form"):
    service = st.text_input("Service/Component", placeholder="e.g., API Gateway")
    sli = st.text_input("SLI (Metric)", placeholder="e.g., % of HTTP 200s")
    slo_target = st.text_input("SLO Target", placeholder="e.g., 99.9%")
    current_value = st.text_input("Current Value", placeholder="e.g., 99.95%")
    submitted = st.form_submit_button("Add Metric")

if submitted:
    new_entry = {
        "service": service,
        "sli": sli,
        "slo_target": slo_target,
        "current_value": current_value,
        "status": calculate_status(slo_target, current_value)
    }
    st.session_state["metrics"].append(new_entry)
    save_metrics(st.session_state["metrics"])
    st.success(f"Added metric for {service}")

st.subheader("🗂️ Metrics Overview")

if not st.session_state["metrics"]:
    st.info("No metrics added yet.")
else:
    st.dataframe(st.session_state["metrics"])
    st.subheader("🧠 Suggestions")
    suggestions = suggest_improvements(st.session_state["metrics"])
    for s in suggestions:
        st.markdown(f"- {s}")

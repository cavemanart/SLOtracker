# slotracker/components/slo_dashboard.py

import streamlit as st

def render_slo_dashboard():
    st.title("📊 SLO Dashboard")

    # Manual input
    st.subheader("📌 SLO Metrics Input")
    service_name = st.text_input("Service Name", "Authentication API")
    slo_target = st.number_input("SLO Target (%)", min_value=0.0, max_value=100.0, value=99.9)
    actual_sli = st.number_input("Current SLI (%)", min_value=0.0, max_value=100.0, value=99.2)
    uptime = st.number_input("Current Uptime (%)", min_value=0.0, max_value=100.0, value=99.8)
    latency_ms = st.number_input("Avg. Latency (ms)", min_value=0.0, value=120.0)
    error_rate = st.number_input("Error Rate (%)", min_value=0.0, max_value=100.0, value=0.8)

    # Suggestions
    st.markdown("### 🔍 Suggestions")
    if actual_sli < slo_target:
        st.error(f"⚠️ SLI is below target! Investigate {service_name}'s recent errors or outages.")
    else:
        st.success("✅ You're meeting your SLO target. Great job!")

    if uptime < 99.9:
        st.warning("🕒 Uptime could be improved. Consider reviewing recent incident logs.")

    if latency_ms > 200:
        st.warning("🐢 Latency is high. Look into performance bottlenecks or traffic spikes.")

    if error_rate > 1.0:
        st.warning("❌ Error rate is elevated. Check alerting rules and deploy health.")

    # Summary
    st.markdown("### 📈 Summary Report")
    st.metric(label="Service", value=service_name)
    st.metric(label="SLI", value=f"{actual_sli}%", delta=f"{actual_sli - slo_target:.2f}%")
    st.metric(label="Uptime", value=f"{uptime}%")
    st.metric(label="Latency", value=f"{latency_ms} ms")
    st.metric(label="Error Rate", value=f"{error_rate}%")

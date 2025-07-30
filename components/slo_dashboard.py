# components/slo_dashboard.py

import streamlit as st
import plotly.graph_objects as go

def render_slo_dashboard():
    st.title("📊 SLO Dashboard")

    st.subheader("Service Level Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        slo_target = st.number_input("🎯 SLO Target (%)", min_value=90.0, max_value=100.0, value=99.9, step=0.1)
    with col2:
        sli_actual = st.number_input("📈 Actual SLI (%)", min_value=90.0, max_value=100.0, value=99.5, step=0.1)
    with col3:
        error_budget_minutes = st.number_input("🧮 Error Budget (minutes/month)", min_value=0, value=43)

    st.divider()

    # Error Budget Used
    error_budget_used = max(0, ((slo_target - sli_actual) / 100.0) * 30 * 24 * 60)
    budget_remaining = max(0, error_budget_minutes - error_budget_used)
    budget_percent_used = round((error_budget_used / error_budget_minutes) * 100, 2) if error_budget_minutes else 0

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("SLO Target", f"{slo_target:.2f}%")
    with col5:
        st.metric("Current SLI", f"{sli_actual:.2f}%", delta=f"{sli_actual - slo_target:.2f}%")
    with col6:
        st.metric("Error Budget Used", f"{budget_percent_used:.1f}%", delta=f"-{budget_remaining:.0f} min remaining")

    st.divider()

    st.subheader("📉 Error Budget Gauge")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=budget_percent_used,
        delta={"reference": 100, "increasing": {"color": "red"}},
        gauge={
            "axis": {"range": [None, 100]},
            "bar": {"color": "green" if budget_percent_used < 50 else "orange" if budget_percent_used < 80 else "red"},
            "steps": [
                {"range": [0, 50], "color": "#d4f8e8"},
                {"range": [50, 80], "color": "#fff3cd"},
                {"range": [80, 100], "color": "#f8d7da"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 100
            }
        },
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Error Budget Used (%)"}
    ))

    st.plotly_chart(gauge, use_container_width=True)

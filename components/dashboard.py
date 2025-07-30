import streamlit as st
import pandas as pd
from core.utils import load_json, save_json

SLO_FILE = "data/slo.json"

def calculate_error_budget(slo_target, sli_actual, total_minutes=43200):
    # Default total minutes = 30 days of monitoring
    allowed_downtime = total_minutes * ((100 - slo_target) / 100)
    actual_downtime = total_minutes * ((100 - sli_actual) / 100)
    budget_remaining = allowed_downtime - actual_downtime
    return {
        "allowed_downtime": allowed_downtime,
        "actual_downtime": actual_downtime,
        "budget_remaining": max(0, budget_remaining),
        "budget_used_percent": min(100, (actual_downtime / allowed_downtime) * 100 if allowed_downtime else 0)
    }

def render_slo_dashboard():
    st.subheader("📊 SLO Dashboard")

    slo_data = load_json(SLO_FILE)

    with st.expander("➕ Add New SLO Metric"):
        date = st.date_input("Date")
        slo_target = st.number_input("SLO Target (%)", min_value=90.0, max_value=100.0, value=99.9)
        sli_actual = st.number_input("Observed SLI (%)", min_value=0.0, max_value=100.0, value=99.2)
        notes = st.text_area("Notes", placeholder="Outage due to database maintenance")

        if st.button("Save SLO Entry"):
            slo_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "slo_target": slo_target,
                "sli_actual": sli_actual,
                "notes": notes
            })
            save_json(SLO_FILE, slo_data)
            st.success("SLO entry saved!")

    if not slo_data:
        st.info("No SLO data available.")
        return

    df = pd.DataFrame(slo_data)

    # Sort by date descending
    df = df.sort_values(by="date", ascending=False)

    latest = df.iloc[0]
    slo_target = latest["slo_target"]
    sli_actual = latest["sli_actual"]
    error_metrics = calculate_error_budget(slo_target, sli_actual)

    st.markdown("### 🧮 Current SLO Summary")
    col1, col2, col3 = st.columns(3)

    col1.metric("🎯 SLO Target", f"{slo_target:.2f}%")
    col2.metric("📡 Current SLI", f"{sli_actual:.2f}%")
    col3.metric("📉 Error Budget Used", f"{error_metrics['budget_used_percent']:.1f}%")

    st.progress(min(1.0, sli_actual / slo_target))

    col4, col5 = st.columns(2)
    col4.metric("🕒 Budget Remaining (min)", f"{error_metrics['budget_remaining']:.1f}")
    col5.metric("❌ Downtime So Far (min)", f"{error_metrics['actual_downtime']:.1f}")

    if error_metrics['budget_remaining'] <= 0:
        st.error("🚨 Error budget exhausted! Investigate issues and consider triggering incident response.")
    elif error_metrics['budget_used_percent'] > 80:
        st.warning("⚠️ SLO at risk: more than 80% of error budget used.")
    else:
        st.success("✅ SLO within acceptable range.")

    st.markdown("### 📅 Historical SLO Data")
    st.dataframe(df, use_container_width=True)

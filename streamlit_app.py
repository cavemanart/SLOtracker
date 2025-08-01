import streamlit as st
import pandas as pd

st.set_page_config(page_title="SLO Tracker", layout="wide")

def load_bt_csv(file):
    df = pd.read_csv(file)
    df.columns = [col.strip() for col in df.columns]
    return df

def analyze_bt_data(df, slo_targets):
    insights = []

    for _, row in df.iterrows():
        name = row.get("Name", "Unnamed")
        resp_time = row.get("Response Time (ms)", 0)
        calls_per_min = row.get("Calls / min", 0)
        errors_per_min = row.get("Errors / min", 0)
        error_pct = row.get("% Errors", 0)
        very_slow_pct = row.get("% Very Slow Transactions", 0)
        max_resp_time = row.get("Max Response Time (ms)", 0)
        wait_time = row.get("Wait Time (ms)", 0)

        slo = slo_targets.get(name, {"target_ms": 400, "target_pct": 95})

        slo_target_ms = slo["target_ms"]
        slo_target_pct = slo["target_pct"]

        slo_violated = resp_time > slo_target_ms
        recommendations = []

        if slo_violated:
            recommendations.append(f"🔴 Avg response time {resp_time:.0f}ms > SLO of {slo_target_ms}ms.")
        if error_pct > 1:
            recommendations.append(f"⚠️ High error rate: {error_pct:.2f}%. Investigate upstream services.")
        if very_slow_pct > (100 - slo_target_pct):
            recommendations.append(f"⚠️ {very_slow_pct:.2f}% very slow transactions exceed SLO target.")
        if wait_time > 100:
            recommendations.append(f"🕒 High wait time: {wait_time}ms. Consider threadpool tuning or DB optimization.")
        if max_resp_time > 2 * resp_time:
            recommendations.append(f"📈 Max response time {max_resp_time}ms is much higher than avg. Look into outliers.")

        insights.append({
            "Transaction": name,
            "Response Time (ms)": resp_time,
            "Calls / min": calls_per_min,
            "Errors / min": errors_per_min,
            "% Errors": error_pct,
            "% Very Slow Transactions": very_slow_pct,
            "Max Response Time (ms)": max_resp_time,
            "SLO Target (ms)": slo_target_ms,
            "SLO Violated": "✅" if not slo_violated else "❌",
            "Recommendations": recommendations or ["✅ No major issues detected."],
        })

    return pd.DataFrame(insights)


def render_slo_dashboard(bt_df):
    st.header("📊 SLO Dashboard")

    with st.expander("🔧 Define SLO Targets Per Transaction", expanded=False):
        slo_targets = {}
        for name in bt_df["Name"].dropna().unique():
            col1, col2 = st.columns(2)
            with col1:
                ms = st.number_input(f"{name} - Target ms", value=400, key=f"{name}_ms")
            with col2:
                pct = st.number_input(f"{name} - Target %", value=95, min_value=80, max_value=100, key=f"{name}_pct")
            slo_targets[name] = {"target_ms": ms, "target_pct": pct}
    st.divider()

    result_df = analyze_bt_data(bt_df, slo_targets)

    st.dataframe(result_df[[
        "Transaction", "Response Time (ms)", "SLO Target (ms)", "SLO Violated", "% Errors",
        "% Very Slow Transactions", "Max Response Time (ms)"
    ]], use_container_width=True)

    st.subheader("📌 Recommendations")
    for _, row in result_df.iterrows():
        st.markdown(f"**{row['Transaction']}**")
        for r in row["Recommendations"]:
            st.markdown(f"- {r}")
        st.markdown("---")


def render_bt_insights():
    st.header("🔍 Business Transaction Insights")
    uploaded_file = st.file_uploader("Upload BT CSV", type=["csv"])
    if uploaded_file:
        bt_df = load_bt_csv(uploaded_file)
        st.subheader("Raw Preview")
        st.dataframe(bt_df.head(20), use_container_width=True)

        render_slo_dashboard(bt_df)


def main():
    st.title("📈 SLO Tracker + AppDynamics BT Analyzer")

    tab1, tab2 = st.tabs(["📊 SLO Dashboard", "🔍 BT Insights"])

    with tab1:
        st.info("Load BT data from the BT Insights tab to populate SLO Dashboard.")
        st.markdown("➡️ Go to **BT Insights** tab to upload a Business Transaction CSV and view analysis.")
    
    with tab2:
        render_bt_insights()


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd

def render_bt_csv_insights():
    st.header("📊 Business Transactions Insights")
    st.write("Upload a Business Transactions CSV from AppDynamics.")

    # Let engineer set the SLO threshold and target dynamically:
    slo_threshold_ms = st.number_input(
        "Set SLO Threshold (ms)",
        min_value=1,
        max_value=10000,
        value=400,
        step=10,
        help="Response time threshold (in ms) for SLO"
    )
    slo_target_pct = st.number_input(
        "Set SLO Target (%)",
        min_value=0,
        max_value=100,
        value=95,
        step=1,
        help="Percentage of transactions that should meet the SLO threshold"
    )

    uploaded_file = st.file_uploader("Upload BT CSV", type="csv", key="bt_csv")
    if not uploaded_file:
        return

    try:
        df = pd.read_csv(uploaded_file)

        # Normalize column names
        df.columns = [col.strip() for col in df.columns]
        required_cols = [
            "Name", "Response Time (ms)", "Calls / min", "Errors / min",
            "% Errors", "% Slow Transactions", "% Very Slow Transactions",
            "Max Response Time (ms)", "End to End Latency Time (ms)", "Transaction Type"
        ]

        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
            return

        # Clean & convert
        df["Response Time (ms)"] = pd.to_numeric(df["Response Time (ms)"], errors='coerce')
        df["Max Response Time (ms)"] = pd.to_numeric(df["Max Response Time (ms)"], errors='coerce')
        df["Calls / min"] = pd.to_numeric(df["Calls / min"], errors='coerce')
        df["Errors / min"] = pd.to_numeric(df["Errors / min"], errors='coerce')
        df["% Errors"] = pd.to_numeric(df["% Errors"].str.replace('%', ''), errors='coerce')
        df["% Slow Transactions"] = pd.to_numeric(df["% Slow Transactions"].str.replace('%', ''), errors='coerce')
        df["% Very Slow Transactions"] = pd.to_numeric(df["% Very Slow Transactions"].str.replace('%', ''), errors='coerce')
        df["End to End Latency Time (ms)"] = pd.to_numeric(df["End to End Latency Time (ms)"], errors='coerce')

        st.subheader("📌 High-Level Summary")

        total_calls = df["Calls / min"].sum()
        avg_resp = df["Response Time (ms)"].mean()
        slow_txns = df[df["Response Time (ms)"] > slo_threshold_ms]
        slow_pct = 100 * slow_txns["Calls / min"].sum() / total_calls if total_calls else 0

        st.metric("Avg Response Time", f"{avg_resp:.1f} ms")
        st.metric("Total Calls/min", f"{total_calls:.1f}")
        st.metric("SLO Target", f"{slo_threshold_ms}ms @ {slo_target_pct}%")
        st.metric("SLO Compliance", f"{100 - slow_pct:.2f}%")

        slo_compliant = (100 - slow_pct) >= slo_target_pct
        st.success("✅ SLO target met!") if slo_compliant else st.error("❌ SLO target NOT met")

        st.subheader("🚦 Problematic Transactions")
        outliers = df[
            (df["Response Time (ms)"] > slo_threshold_ms) |
            (df["% Errors"] > 1) |
            (df["% Very Slow Transactions"] > 5)
        ].sort_values(by="Response Time (ms)", ascending=False)

        if not outliers.empty:
            st.dataframe(outliers[[
                "Transaction Type", "Name", "Response Time (ms)", "% Errors",
                "% Slow Transactions", "% Very Slow Transactions", "Max Response Time (ms)"
            ]])
        else:
            st.success("No problematic transactions detected.")

        st.subheader("🛠 Recommendations for SREs")

        for _, row in outliers.iterrows():
            st.markdown(f"""
            - 🔍 **{row['Name']}**  
              • Response Time: {row['Response Time (ms)']} ms  
              • Errors: {row['% Errors']}%  
              • Very Slow: {row['% Very Slow Transactions']}%  
              👉 *Consider reviewing backend dependencies, increasing resource allocation, or optimizing logic.*
            """)

        if not slo_compliant:
            st.warning(f"⚠️ Over {100 - slo_target_pct}% of transactions are above {slo_threshold_ms}ms. Investigate key offenders above.")
#
        st.subheader("📎 Raw Data (Filtered)")
        st.dataframe(df.sort_values("Response Time (ms)", ascending=False))

    except Exception as e:
        st.error(f"Failed to parse CSV: {e}")

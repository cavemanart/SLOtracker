import streamlit as st
import pandas as pd

st.set_page_config(page_title="SLO Tracker", layout="wide")

st.title("📊 SLO Tracker Dashboard")

tab1, tab2, tab3 = st.tabs(["SLO Dashboard", "AppD CSV Insights", "BT Insights"])

# ---- TAB 1: Placeholder for SLO Dashboard ----
with tab1:
    st.subheader("SLO Dashboard (coming soon)")
    st.markdown("This will visualize and summarize service level objectives using real metrics.")

# ---- TAB 2: AppDynamics CSV Insights ----
with tab2:
    st.subheader("📥 Upload AppDynamics CSV")
    uploaded_appd = st.file_uploader("Upload AppDynamics Summary CSV", type=["csv"], key="appd")

    if uploaded_appd:
        try:
            df = pd.read_csv(uploaded_appd)

            st.markdown("### ✅ Raw Data Preview")
            st.dataframe(df.head(20))

            if "Response Time (ms)" in df.columns and "Call / min" in df.columns:
                df["Response Time (ms)"] = pd.to_numeric(df["Response Time (ms)"], errors="coerce")
                df["Call / min"] = pd.to_numeric(df["Call / min"], errors="coerce")

                high_latency = df[df["Response Time (ms)"] > 400]
                error_prone = df[df["Errors"] > 0]

                st.markdown("### 📈 Key Insights")
                st.markdown(f"- Total services: **{len(df)}**")
                st.markdown(f"- Services over 400ms (SLO violation): **{len(high_latency)}**")
                st.markdown(f"- Services with errors: **{len(error_prone)}**")

                worst_latency = df.sort_values("Response Time (ms)", ascending=False).head(5)
                st.markdown("#### 🚨 Top 5 Slowest Services")
                st.dataframe(worst_latency[["Summary", "Response Time (ms)", "Call / min", "Errors"]])

                most_errors = df.sort_values("Errors", ascending=False).head(5)
                st.markdown("#### ❌ Top 5 Most Error-Prone Services")
                st.dataframe(most_errors[["Summary", "Errors", "Errors / min", "Call / min"]])

                st.markdown("#### 🛠️ Recommendations")
                if not high_latency.empty:
                    st.markdown("- Investigate services with response time consistently over 400ms.")
                if not error_prone.empty:
                    st.markdown("- Review error logs or implement retries for error-prone calls.")
                st.markdown("- Consider scaling high-traffic services or load-testing slow endpoints.")

        except Exception as e:
            st.error(f"Failed to read AppDynamics CSV: {e}")

# ---- TAB 3: Business Transaction Insights ----
with tab3:
    st.subheader("📥 Upload Business Transactions CSV")
    uploaded_bt = st.file_uploader("Upload Business Transactions CSV", type=["csv"], key="bt")

    if uploaded_bt:
        try:
            df = pd.read_csv(uploaded_bt)

            st.markdown("### ✅ Raw Data Preview")
            st.dataframe(df.head(20))

            required_cols = ["Name", "Health", "Response Time (ms)", "Calls / min", "Errors / min", "% Errors", "% Slow Transactions", "% Very Slow Transactions"]

            if all(col in df.columns for col in required_cols):
                for col in ["Response Time (ms)", "Calls / min", "Errors / min", "% Errors", "% Slow Transactions", "% Very Slow Transactions"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

                slo_violations = df[df["Response Time (ms)"] > 400]
                error_transactions = df[df["% Errors"] > 0]

                st.markdown("### 📈 BT Key Insights")
                st.markdown(f"- Total BTs: **{len(df)}**")
                st.markdown(f"- Violating SLO (400ms): **{len(slo_violations)}**")
                st.markdown(f"- With any errors: **{len(error_transactions)}**")

                st.markdown("#### 🚨 Worst 5 Response Times")
                st.dataframe(df.sort_values("Response Time (ms)", ascending=False).head(5)[["Name", "Response Time (ms)", "Health", "% Errors"]])

                st.markdown("#### ❌ Highest Error %")
                st.dataframe(df.sort_values("% Errors", ascending=False).head(5)[["Name", "% Errors", "Errors / min", "Calls / min"]])

                st.markdown("#### 🛠️ BT Recommendations")
                st.markdown("- Prioritize remediation for transactions with both high response time and high error %.")
                st.markdown("- Consider alerting on % very slow and stalled transactions.")
                st.markdown("- Review backend service health where BTs repeatedly show poor performance.")
            else:
                st.warning("CSV missing one or more required columns.")

        except Exception as e:
            st.error(f"Failed to read Business Transactions CSV: {e}")

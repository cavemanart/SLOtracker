import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SLO Tracker", layout="wide")
st.title("📊 SLO Tracker Dashboard")

# Helper function to extract prefix from transaction name
def extract_prefix(name):
    if isinstance(name, str):
        parts = name.strip("/").split("/")
        if len(parts) > 0:
            return parts[0]
    return name

tab1, tab2, tab3 = st.tabs(["SLO Dashboard", "AppD CSV Insights", "BT Insights"])

# ---- TAB 1: Smart SLO Tracker Dashboard ----
with tab1:
    st.subheader("📈 SLO Tracker Dashboard")

    # Try to get BT data from session or ask user to upload
    df_bt = st.session_state.get("bt_data")

    if df_bt is None:
        uploaded_bt = st.file_uploader(
            "Upload Business Transactions CSV for SLO analysis (or upload in BT Insights tab)",
            type=["csv"],
            key="bt_dash_upload"
        )
        if uploaded_bt:
            try:
                df_bt = pd.read_csv(uploaded_bt)
                st.session_state["bt_data"] = df_bt
                st.success("Business Transactions data loaded.")
            except Exception as e:
                st.error(f"Failed to load CSV: {e}")
        else:
            st.info("Please upload a Business Transactions CSV on this tab or the BT Insights tab.")
    else:
        st.success("Business Transactions data loaded from session.")

    if df_bt is not None:
        # Clean columns
        required_cols = [
            "Name", "Response Time (ms)", "Calls / min",
            "Errors / min", "% Errors", "% Slow Transactions", "% Very Slow Transactions"
        ]
        if not all(col in df_bt.columns for col in required_cols):
            st.error(f"CSV missing one or more required columns: {required_cols}")
        else:
            # Clean & convert types
            for col in [
                "Response Time (ms)", "Calls / min", "Errors / min",
                "% Errors", "% Slow Transactions", "% Very Slow Transactions"
            ]:
                if col == "% Errors" and df_bt[col].dtype == "object":
                    df_bt[col] = pd.to_numeric(df_bt[col].str.replace("%", ""), errors="coerce")
                else:
                    df_bt[col] = pd.to_numeric(df_bt[col], errors="coerce")

            # Granularity selector
            granularity = st.selectbox(
                "Select Granularity Level for Transaction Names",
                options=["Exact", "By Path Prefix"],
                index=0
            )

            if granularity == "By Path Prefix":
                df_bt["GroupName"] = df_bt["Name"].apply(extract_prefix)
            else:
                df_bt["GroupName"] = df_bt["Name"]

            # Aggregate by GroupName
            grouped = df_bt.groupby("GroupName").agg({
                "Response Time (ms)": "mean",
                "Calls / min": "sum",
                "% Errors": "mean",
                "% Slow Transactions": "mean",
                "% Very Slow Transactions": "mean"
            }).reset_index()

            # SLO inputs
            slo_response_time = st.number_input(
                "SLO Response Time Threshold (ms)",
                min_value=1,
                max_value=10000,
                value=400,
                step=10
            )
            slo_error_pct = st.number_input(
                "SLO Error Rate Threshold (%)",
                min_value=0.0,
                max_value=100.0,
                value=1.0,
                format="%.2f"
            )

            # Find violating groups
            violating_resp = grouped[grouped["Response Time (ms)"] > slo_response_time]
            violating_error = grouped[grouped["% Errors"] > slo_error_pct]

            st.markdown(f"### Services violating Response Time SLO (> {slo_response_time} ms): {len(violating_resp)}")
            st.dataframe(violating_resp[["GroupName", "Response Time (ms)", "Calls / min"]].sort_values("Response Time (ms)", ascending=False))

            st.markdown(f"### Services violating Error Rate SLO (> {slo_error_pct} %): {len(violating_error)}")
            st.dataframe(violating_error[["GroupName", "% Errors", "Calls / min"]].sort_values("% Errors", ascending=False))

            if len(violating_resp) > 0 or len(violating_error) > 0:
                st.warning("⚠️ Some services are violating your SLOs. Consider investigating these to improve system health.")
            else:
                st.success("✅ All services meet current SLO targets!")

            # Visualization: Response Time distribution histogram
            st.markdown("### Response Time Distribution")
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(grouped["Response Time (ms)"].dropna(), bins=30, color="skyblue", edgecolor="black")
            ax.axvline(slo_response_time, color="red", linestyle="--", label="SLO Threshold")
            ax.set_xlabel("Response Time (ms)")
            ax.set_ylabel("Number of Groups")
            ax.legend()
            st.pyplot(fig)

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

    # Adjustable SLO inputs
    slo_threshold_ms = st.number_input(
        "Set SLO Threshold (ms)",
        min_value=1,
        max_value=10000,
        value=400,
        step=10,
        key="bt_slo_threshold"
    )
    slo_target_pct = st.number_input(
        "Set SLO Target (%)",
        min_value=0,
        max_value=100,
        value=95,
        step=1,
        key="bt_slo_target"
    )

    granularity = st.selectbox(
        "Select Granularity Level for Transaction Names",
        options=["Exact", "By Path Prefix"],
        index=0,
        key="bt_granularity"
    )

    uploaded_bt = st.file_uploader("Upload Business Transactions CSV", type=["csv"], key="bt")

    if uploaded_bt:
        try:
            df = pd.read_csv(uploaded_bt)
            st.session_state["bt_data"] = df  # persist for tab1 reuse

            st.markdown("### ✅ Raw Data Preview")
            st.dataframe(df.head(20))

            required_cols = [
                "Name", "Health", "Response Time (ms)", "Calls / min",
                "Errors / min", "% Errors", "% Slow Transactions", "% Very Slow Transactions"
            ]

            if all(col in df.columns for col in required_cols):
                for col in [
                    "Response Time (ms)", "Calls / min", "Errors / min",
                    "% Errors", "% Slow Transactions", "% Very Slow Transactions"
                ]:
                    if col == "% Errors" and df[col].dtype == "object":
                        df[col] = pd.to_numeric(df[col].str.replace("%", ""), errors="coerce")
                    else:
                        df[col] = pd.to_numeric(df[col], errors="coerce")

                # Apply granularity grouping
                if granularity == "By Path Prefix":
                    df["GroupName"] = df["Name"].apply(extract_prefix)
                else:
                    df["GroupName"] = df["Name"]

                grouped = df.groupby("GroupName").agg({
                    "Response Time (ms)": "mean",
                    "Calls / min": "sum",
                    "% Errors": "mean",
                    "% Slow Transactions": "mean",
                    "% Very Slow Transactions": "mean"
                }).reset_index()

                # Compute SLO compliance
                slo_violations = grouped[grouped["Response Time (ms)"] > slo_threshold_ms]
                total_calls = grouped["Calls / min"].sum()
                slow_calls_sum = slo_violations["Calls / min"].sum()
                slow_pct = 100 * slow_calls_sum / total_calls if total_calls else 0
                slo_compliant = (100 - slow_pct) >= slo_target_pct

                error_transactions = grouped[grouped["% Errors"] > 0]

                st.markdown("### 📈 BT Key Insights")
                st.markdown(f"- Total BT groups: **{len(grouped)}**")
                st.markdown(f"- Violating SLO ({slo_threshold_ms}ms): **{len(slo_violations)}**")
                st.markdown(f"- With any errors: **{len(error_transactions)}**")
                st.markdown(f"- SLO Compliance: **{100 - slow_pct:.2f}%** (target: {slo_target_pct}%)")

                st.markdown("#### 🚨 Worst 5 Response Times")
                st.dataframe(grouped.sort_values("Response Time (ms)", ascending=False).head(5)[
                    ["GroupName", "Response Time (ms)", "% Errors"]
                ])

                st.markdown("#### ❌ Highest Error %")
                st.dataframe(grouped.sort_values("% Errors", ascending=False).head(5)[
                    ["GroupName", "% Errors", "Calls / min"]
                ])

                st.markdown("#### 🛠️ BT Recommendations")
                st.markdown("- Prioritize remediation for transactions with both high response time and high error %.")
                st.markdown("- Consider alerting on % very slow and stalled transactions.")
                st.markdown("- Review backend service health where BTs repeatedly show poor performance.")

                if slo_compliant:
                    st.success("✅ SLO target met!")
                else:
                    st.error("❌ SLO target NOT met!")

            else:
                st.warning("CSV missing one or more required columns.")

        except Exception as e:
            st.error(f"Failed to read Business Transactions CSV: {e}")

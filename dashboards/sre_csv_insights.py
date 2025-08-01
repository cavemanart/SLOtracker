import streamlit as st
import pandas as pd

def render_appd_csv_insights():
    st.title("📊 AppDynamics CSV Insights")
    uploaded_file = st.file_uploader("Upload AppDynamics Application Dashboard CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        expected_cols = ['Type', 'Call Type', 'Summary', 'Response Time (ms)', 'Calls', 
                         'Calls / min', 'Errors', 'Errors / min']
        if not all(col in df.columns for col in expected_cols):
            st.error("CSV format doesn't match expected structure.")
            return

        st.subheader("Raw Data")
        st.dataframe(df)

        st.subheader("🔍 Top 5 Slowest Endpoints")
        st.dataframe(df.sort_values(by='Response Time (ms)', ascending=False).head(5))

        st.subheader("🚨 Top 5 Error-Prone Endpoints")
        st.dataframe(df.sort_values(by='Errors / min', ascending=False).head(5))

        st.subheader("✅ Cleanest High-Volume Endpoints")
        clean = df[(df['Errors'] == 0) & (df['Calls'] > df['Calls'].median())]
        st.dataframe(clean.sort_values(by='Calls', ascending=False).head(5))

        st.subheader("📈 SLO Suggestions")
        avg_response = df['Response Time (ms)'].mean()
        high_latency = df[df['Response Time (ms)'] > 500]
        error_rate = df['Errors'].sum() / max(df['Calls'].sum(), 1)

        st.markdown(f"""
- 📌 **Average response time:** {avg_response:.2f} ms  
- ⚠️ **Endpoints > 500ms:** {len(high_latency)} / {len(df)}  
- ❗ **Overall error rate:** {error_rate:.2%}  
- ✅ Suggest target SLO: 95% of endpoints under 500ms  
        """)

def render_bt_csv_insights():
    st.title("🧠 Business Transaction Insights")
    uploaded_file = st.file_uploader("Upload Business Transactions CSV", type="csv")
    if not uploaded_file:
        return

    df = pd.read_csv(uploaded_file)

    required_cols = ['Business Transaction', 'Calls', 'Response Time (ms)', 'Errors']
    if not all(col in df.columns for col in required_cols):
        st.error(f"CSV is missing required columns. Expected: {required_cols}")
        return

    df['Error Rate'] = df['Errors'] / df['Calls'].replace(0, 1)
    call_median = df['Calls'].median()

    st.subheader("📊 Summary")
    st.markdown(f"""
    - Total Transactions: **{len(df)}**  
    - Total Calls: **{df['Calls'].sum():,.0f}**  
    - Average Latency: **{df['Response Time (ms)'].mean():.2f} ms**  
    - Total Errors: **{df['Errors'].sum():,.0f}**  
    - BTs Meeting SLO (≤ 400ms): **{(df['Response Time (ms)'] <= 400).mean() * 100:.2f}%**
    """)

    needs_tuning = df[(df['Calls'] > call_median) & (df['Response Time (ms)'] > 400)]
    monitor = df[(df['Error Rate'] > 0.01) | ((df['Response Time (ms)'] > 350) & (df['Response Time (ms)'] <= 450))]
    stale = df[(df['Calls'] < call_median) & (df['Response Time (ms)'] > 1000)]
    healthy = df[(df['Response Time (ms)'] <= 400) & (df['Error Rate'] <= 0.01)]

    st.subheader("🚨 Needs Tuning")
    st.dataframe(needs_tuning[['Business Transaction', 'Calls', 'Response Time (ms)', 'Error Rate']])

    st.subheader("🧪 Monitor Closely")
    st.dataframe(monitor[['Business Transaction', 'Calls', 'Response Time (ms)', 'Error Rate']])

    st.subheader("💤 Possibly Stale")
    st.dataframe(stale[['Business Transaction', 'Calls', 'Response Time (ms)', 'Error Rate']])

    st.subheader("✅ Healthy")
    st.dataframe(healthy[['Business Transaction', 'Calls', 'Response Time (ms)', 'Error Rate']])

    st.subheader("📌 Recommendations")
    def recommend(row):
        name = row['Business Transaction']
        latency = row['Response Time (ms)']
        calls = row['Calls']
        err = row['Error Rate']

        if name in needs_tuning['Business Transaction'].values:
            return f"Tune '{name}': high volume + latency {latency:.0f}ms."
        elif name in monitor['Business Transaction'].values:
            return f"Monitor '{name}': err rate {err:.2%}, latency {latency:.0f}ms."
        elif name in stale['Business Transaction'].values:
            return f"Review '{name}': low usage + slow response ({latency:.0f}ms)."
        elif name in healthy['Business Transaction'].values:
            return f"'{name}' looks healthy."
        return ""

    df['Recommendation'] = df.apply(recommend, axis=1)
    st.dataframe(df[['Business Transaction', 'Recommendation']])

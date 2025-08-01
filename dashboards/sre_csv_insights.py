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
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Raw Business Transactions Data")
        st.dataframe(df)

        if 'Response Time (ms)' in df.columns and 'Calls' in df.columns:
            st.subheader("📉 Rarely Used Transactions")
            st.dataframe(df[df['Calls'] < df['Calls'].median()].sort_values(by='Calls').head(5))

            st.subheader("🚨 High Latency Transactions")
            st.dataframe(df[df['Response Time (ms)'] > 500].sort_values(by='Response Time (ms)', ascending=False).head(5))

            st.subheader("📌 Recommendations for SRE")
            st.markdown("""
- Consider **deprecating** low-call transactions if they are stale.  
- Set **alerts** on BTs with high error or response time.  
- Prioritize tuning BTs > 500ms response.  
- Use these for **SLI/SLO tracking** and error budgeting.  
            """)

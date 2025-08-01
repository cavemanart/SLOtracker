import streamlit as st
import pandas as pd

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

    # Summary stats
    st.subheader("📊 Summary")
    st.markdown(f"""
    - Total Transactions: **{len(df)}**  
    - Total Calls: **{df['Calls'].sum():,.0f}**  
    - Average Latency: **{df['Response Time (ms)'].mean():.2f} ms**  
    - Total Errors: **{df['Errors'].sum():,.0f}**  
    - BTs Meeting SLO (≤ 400ms): **{(df['Response Time (ms)'] <= 400).mean() * 100:.2f}%**
    """)

    # Categorize BTs
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

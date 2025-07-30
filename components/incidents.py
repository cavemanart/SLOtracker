import streamlit as st
import pandas as pd
import datetime

def render_incident_tracker():
    st.subheader("🛠️ Incident Tracker")

    # Upload Incident CSV
    uploaded_file = st.file_uploader("Upload Incident CSV", type="csv", key="incident_upload")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("🔍 Raw Incident Data", df)

            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                df["date"] = df["timestamp"].dt.date

                daily_counts = df.groupby("date").size()
                st.line_chart(daily_counts)
            else:
                st.warning("⚠️ CSV is missing 'timestamp' column.")
        except Exception as e:
            st.error(f"❌ Failed to process CSV: {e}")
    else:
        st.info("📄 Upload a CSV file to view incident trends.")

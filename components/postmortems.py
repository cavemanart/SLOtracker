import streamlit as st
import pandas as pd
import datetime

def render_postmortem_tracker():
    st.subheader("📋 Postmortems")

    uploaded_file = st.file_uploader("Upload Postmortems CSV", type="csv", key="postmortem_upload")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("🔍 Raw Postmortem Data", df)

            required_columns = {"status", "due"}
            if not required_columns.issubset(df.columns):
                st.warning(f"⚠️ CSV must include these columns: {', '.join(required_columns)}")
                return

            df["due"] = pd.to_datetime(df["due"], errors="coerce")
            overdue = df[
                (df["status"].str.lower() != "closed") &
                (df["due"].dt.date < datetime.date.today())
            ]

            st.error(f"🚨 {len(overdue)} postmortems overdue")
            st.write(overdue)

        except Exception as e:
            st.error(f"❌ Failed to process postmortem CSV: {e}")
    else:
        st.info("📄 Upload a CSV to track postmortem follow-ups.")

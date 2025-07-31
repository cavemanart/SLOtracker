import streamlit as st
import pandas as pd
from datetime import datetime

REQUIRED_COLUMNS = ["date", "system", "impact", "duration_minutes", "description"]

def parse_dates_if_possible(df):
    if "start_time" in df.columns and "end_time" in df.columns:
        try:
            df["start_time"] = pd.to_datetime(df["start_time"])
            df["end_time"] = pd.to_datetime(df["end_time"])
            df["duration_minutes"] = (df["end_time"] - df["start_time"]).dt.total_seconds() / 60
        except Exception as e:
            st.warning(f"Failed to calculate 'duration_minutes' from start/end times: {e}")
    return df

def validate_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"CSV is missing required columns: {', '.join(missing)}")
        return False
    return True

def render_incident_log():
    st.header("📉 Incident Log")

    uploaded_file = st.file_uploader("Upload Incident Log CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df = parse_dates_if_possible(df)

            if not validate_columns(df):
                return

            st.success("CSV successfully loaded and validated.")
            st.dataframe(df)

            # Key stats
            st.subheader("📊 Key Stats")
            avg_duration = df["duration_minutes"].mean()
            total_incidents = df.shape[0]
            high_impact = df[df["impact"].str.lower() == "high"].shape[0]

            st.metric("Total Incidents", total_incidents)
            st.metric("Average Duration (min)", round(avg_duration, 2))
            st.metric("High Impact Incidents", high_impact)

            # Change Management Suggestions
            st.subheader("🔧 Change Management Suggestions")
            st.markdown("- Review root causes for high-duration or frequent incidents.")
            st.markdown("- Prioritize automation or alerting for top impacted systems.")
            st.markdown("- Schedule postmortems for high-impact incidents.")
            st.markdown("- Allocate team capacity for incident response training.")

            # Show top affected systems
            st.subheader("💥 Most Affected Systems")
            system_counts = df["system"].value_counts().head(5)
            st.bar_chart(system_counts)

        except Exception as e:
            st.error(f"Could not read or process file: {e}")

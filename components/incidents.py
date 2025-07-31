import streamlit as st
import pandas as pd

REQUIRED_COLUMNS = {
    "Number": "incident_id",
    "Short description": "short_description",
    "Service": "system",
    "Impact Issue Code": "impact",
    "Duration": "duration_minutes",
    "Description": "description",
    "Created": "date"
}

def map_incident_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"CSV is missing required columns: {', '.join(missing)}")
        return None

    mapped_df = df.rename(columns=REQUIRED_COLUMNS)
    
    # Ensure 'duration_minutes' is numeric
    mapped_df["duration_minutes"] = pd.to_numeric(mapped_df["duration_minutes"], errors="coerce")

    # Ensure date column is datetime
    mapped_df["date"] = pd.to_datetime(mapped_df["date"], errors="coerce")

    return mapped_df

def render_incident_log():
    st.title("📉 Incident Log & Change Management Planner")
    uploaded_file = st.file_uploader("Upload Incident CSV", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df = map_incident_columns(df_raw)

        if df is None:
            return

        # Key stats
        st.subheader("📊 Key Incident Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Incidents", len(df))
        with col2:
            st.metric("Average Duration (min)", round(df["duration_minutes"].mean(), 2))
        with col3:
            st.metric("Most Impacted System", df["system"].mode().iloc[0])

        # Change Planner
        st.subheader("🛠️ Change Management Planner")
        systems = df["system"].value_counts().reset_index()
        systems.columns = ["System", "Incident Count"]
        st.dataframe(systems)

        st.subheader("📋 Full Incident Table")
        st.dataframe(df)

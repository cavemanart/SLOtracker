import streamlit as st
import pandas as pd

REQUIRED_COLUMNS = ["date", "system", "impact", "duration_minutes", "description"]

def render_incident_log():
    st.header("Incident Log & Change Planner")
    uploaded_file = st.file_uploader("Upload your incident CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Check if all required columns exist
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                st.error(f"CSV is missing required columns: {', '.join(missing_cols)}")
                show_sample_csv()
                return

            st.success("CSV uploaded successfully.")
            st.subheader("Raw Incident Log")
            st.dataframe(df)

            # Convert date column to datetime if needed
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            # Incident Summary
            st.subheader("📊 Incident Summary")
            st.metric("Total Incidents", len(df))
            st.metric("Avg Duration (min)", round(df["duration_minutes"].mean(), 2))
            st.metric("Total Duration (hrs)", round(df["duration_minutes"].sum() / 60, 2))
            st.metric("Impacted Systems", df["system"].nunique())

            st.subheader("Top Impacted Systems")
            top_systems = df["system"].value_counts().head(5)
            st.bar_chart(top_systems)

            # Change Management Planner (Simple Rule-of-Thumb)
            st.subheader("🛠️ Change Management Suggestions")
            for system, count in top_systems.items():
                if count >= 3:
                    st.warning(f"⚠️ System '{system}' had {count} incidents. Consider a change review or reliability improvement sprint.")

        except Exception as e:
            st.error(f"An error occurred while processing the CSV: {e}")
            show_sample_csv()
    else:
        st.info("Please upload a CSV to begin analysis.")
        show_sample_csv()

def show_sample_csv():
    st.subheader("📋 Sample CSV Format")
    st.markdown("""
    Please upload a CSV file with the following **columns**:
    - `date`: (e.g., 2025-07-15)
    - `system`: System or service affected
    - `impact`: Brief description of user/business impact
    - `duration_minutes`: How long the incident lasted (numeric)
    - `description`: More detailed notes or findings
    """)
    sample_data = {
        "date": ["2025-07-15", "2025-07-20"],
        "system": ["Login API", "Database"],
        "impact": ["Login failure", "Read timeout"],
        "duration_minutes": [25, 60],
        "description": ["Token service misconfigured", "Connection pool exhausted"]
    }
    st.dataframe(pd.DataFrame(sample_data))

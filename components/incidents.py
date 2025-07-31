import streamlit as st
import pandas as pd

def render_incident_log():
    st.subheader("Incident Log Analysis")
    st.write("Upload your incident CSV to view key metrics and planning suggestions.")

    uploaded_file = st.file_uploader("Upload Incident CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            required_columns = [
                "Number", "Short description", "Caller", "Priority", "State", "Service",
                "Assignment group", "Assigned to", "Created", "Actions taken",
                "Business duration", "Business resolve time", "Caused by Change",
                "Description", "Time worked", "Impact", "Issue Code", "Made SLA",
                "SLA due", "Severity"
            ]

            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                st.error(f"CSV is missing required columns: {', '.join(missing)}")
                return

            # Clean and derive needed fields
            df["Time worked"] = pd.to_numeric(df["Time worked"], errors="coerce")
            df["duration_minutes"] = df["Time worked"]  # Assuming it's in minutes already

            avg_duration = df["duration_minutes"].mean()
            total_incidents = len(df)
            high_impact = df[df["Impact"].str.contains("High", case=False, na=False)]
            changes_linked = df[df["Caused by Change"].notna() & (df["Caused by Change"] != "")]

            st.metric("Total Incidents", total_incidents)
            st.metric("Average Duration (min)", round(avg_duration, 2) if not pd.isna(avg_duration) else "N/A")
            st.metric("High Impact Incidents", len(high_impact))
            st.metric("Linked to Change", len(changes_linked))

            st.markdown("---")
            st.subheader("Change Management Planning")
            if len(changes_linked) > 0:
                top_change_causes = changes_linked["Caused by Change"].value_counts().head(3)
                st.write("Top changes associated with incidents:")
                st.write(top_change_causes)
            else:
                st.info("No change-related incidents found.")

            st.markdown("---")
            if st.checkbox("Show full incident table"):
                st.dataframe(df)

        except Exception as e:
            st.error(f"Error processing file: {e}")

import streamlit as st
import pandas as pd
import io

def render_incident_log():
    st.header("Incident Log Analyzer")
    
    uploaded_file = st.file_uploader("Upload Incident Log CSV", type="csv")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            st.subheader("Raw Data Preview")
            st.dataframe(df.head())

            # Key stats
            st.subheader("Key Stats")
            total_incidents = len(df)
            sev_counts = df['severity'].value_counts()
            avg_resolution_time = df['resolution_time_minutes'].mean()
            top_causes = df['root_cause'].value_counts().head(3)

            st.markdown(f"**Total Incidents:** {total_incidents}")
            st.markdown("**Severity Breakdown:**")
            st.dataframe(sev_counts)
            st.markdown(f"**Average Resolution Time (mins):** {avg_resolution_time:.2f}")
            st.markdown("**Top 3 Root Causes:**")
            st.dataframe(top_causes)

            # Change Management Plan Output
            st.subheader("Change Management Planner")
            for cause in top_causes.index:
                st.markdown(f"### Root Cause: {cause}")
                st.text_area(f"Remediation plan for {cause}", key=cause)

        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("Upload a CSV file to begin analysis.")

# Example expected CSV format:
# incident_id,timestamp,severity,resolution_time_minutes,root_cause
# 123,2024-07-01 08:00,P1,55,DB outage

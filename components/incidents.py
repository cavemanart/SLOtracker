import streamlit as st
import pandas as pd

def render_incident_log():
    st.subheader("📂 Upload Incident Log CSV")
    uploaded_file = st.file_uploader("Upload a CSV file with incident data", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if df.empty:
            st.warning("CSV file is empty.")
            return

        # Display raw table
        st.dataframe(df)

        # --- Key Stats ---
        st.markdown("## 📊 Key Incident Stats")

        total_incidents = len(df)
        avg_duration = df["duration_minutes"].mean()
        services_affected = df["service"].value_counts()
        mttr = avg_duration

        st.metric("Total Incidents", total_incidents)
        st.metric("Average Duration (min)", f"{avg_duration:.1f}")
        st.metric("MTTR", f"{mttr:.1f} minutes")

        st.markdown("### Top 5 Affected Services")
        st.bar_chart(services_affected.head(5))

        st.markdown("### Most Common Root Causes")
        st.table(df["root_cause"].value_counts().head(5))

        # --- Change Management Suggestions ---
        st.markdown("## 🛠️ Change Management Planner")

        high_incident_services = services_affected[services_affected > 2]

        if high_incident_services.empty:
            st.success("No services flagged for change planning 🎉")
        else:
            for service, count in high_incident_services.items():
                st.markdown(f"### 🔧 {service}")
                st.write("- 📌 Incident Count:", count)
                st.write("- 🔁 Consider load balancing, caching, or scaling policies")
                st.write("- 🔔 Review alert thresholds and reduce false positives")
                st.write("- 🔒 Check dependency resilience (DBs, APIs, etc.)")

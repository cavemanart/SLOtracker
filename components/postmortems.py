import streamlit as st
import pandas as pd
import datetime

def render_incident_tracker():
    st.subheader("🛠️ Incident Tracker")

    tab1, tab2 = st.tabs(["📄 Upload CSV", "✍️ Manual Entry"])

    with tab1:
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

    with tab2:
        st.markdown("**Suggested Fields:** `timestamp`, `service`, `impact`, `description`")

        incident_data = []
        with st.form("manual_incident_form"):
            num_rows = st.number_input("How many incidents do you want to input?", 1, 10, 1)
            for i in range(num_rows):
                st.markdown(f"**Incident {i+1}**")
                timestamp = st.date_input(f"Timestamp", key=f"ts_{i}")
                service = st.text_input("Service affected", key=f"svc_{i}")
                impact = st.selectbox("Impact level", ["Low", "Medium", "High", "Critical"], key=f"imp_{i}")
                description = st.text_area("Description", key=f"desc_{i}")
                incident_data.append({
                    "timestamp": pd.to_datetime(timestamp),
                    "service": service,
                    "impact": impact,
                    "description": description
                })
            submitted = st.form_submit_button("Submit")

        if submitted:
            df = pd.DataFrame(incident_data)
            st.success("✅ Incidents recorded")
            st.write(df)

            df["date"] = df["timestamp"].dt.date
            daily_counts = df.groupby("date").size()
            st.line_chart(daily_counts)

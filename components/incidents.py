import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime

REQUIRED_COLUMNS = [
    "Number", "Short description", "Caller", "Priority", "State", "Service",
    "Assignment group", "Assigned to", "Created", "Actions taken",
    "Business duration", "Business resolve time", "Description", "Duration",
    "Escalation", "Impact", "Issue Code", "Made SLA", "SLA due", "Severity", "Time worked"
]

def parse_business_duration(duration_str):
    match = re.match(r"(?:(\d+)d)?\s*(?:(\d+)h)?\s*(?:(\d+)m)?", str(duration_str))
    if not match:
        return 0
    days, hours, minutes = match.groups()
    total_minutes = int(days or 0) * 1440 + int(hours or 0) * 60 + int(minutes or 0)
    return total_minutes

def render_incident_log():
    st.header("📉 Incident Log & Change Management Planner")
    uploaded_file = st.file_uploader("Upload Incident CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.error(f"CSV is missing required columns: {', '.join(missing_cols)}")
            return

        df['Created'] = pd.to_datetime(df['Created'], errors='coerce')
        df['Business duration (mins)'] = df['Business duration'].apply(parse_business_duration)

        # Business resolve time is already in seconds - convert to mins
        df['Business resolve time (mins)'] = df['Business resolve time'].apply(pd.to_numeric, errors='coerce') / 60

        df['Duration (mins)'] = df['Duration'].apply(pd.to_numeric, errors='coerce')

        mttr = df['Duration (mins)'].mean()
        avg_business_duration = df['Business duration (mins)'].mean()
        avg_resolve = df['Business resolve time (mins)'].mean()

        st.subheader("📊 Key Metrics")
        st.metric("Mean Time To Resolve (MTTR)", f"{mttr:.2f} minutes")
        st.metric("Avg. Business Duration", f"{avg_business_duration:.2f} minutes")
        st.metric("Avg. Business Resolve Time", f"{avg_resolve:.2f} minutes")

        st.subheader("📌 Avg Resolution by Incident Type")
        if 'Issue Code' in df.columns:
            grouped = df.groupby('Issue Code').agg({
                'Duration (mins)': 'mean',
                'Business duration (mins)': 'mean',
                'Business resolve time (mins)': 'mean',
                'Number': 'count'
            }).rename(columns={
                'Duration (mins)': 'MTTR (mins)',
                'Business duration (mins)': 'Biz Duration (mins)',
                'Business resolve time (mins)': 'Biz Resolve (mins)',
                'Number': 'Incident Count'
            }).sort_values(by='Incident Count', ascending=False)

            st.dataframe(grouped.style.format({
                'MTTR (mins)': '{:.1f}',
                'Biz Duration (mins)': '{:.1f}',
                'Biz Resolve (mins)': '{:.1f}'
            }))

        st.subheader("🔍 Incident Insights")

        df_filtered = df.dropna(subset=['Short description'])
        keyword_counts = df_filtered['Short description'].str.lower().str.extractall(r'(?P<keyword>\b\w{4,}\b)')['keyword'].value_counts().head(10)

        st.write("Top Keywords in Short Descriptions:")
        st.bar_chart(keyword_counts)

        st.write("Incidents Breakdown by State:")
        st.bar_chart(df['State'].value_counts())

        st.write("Incidents by Priority:")
        st.bar_chart(df['Priority'].value_counts())

        st.subheader("📁 Full Incident Table")
        st.dataframe(df)

        st.download_button("Download Enhanced Incident Data", data=df.to_csv(index=False), file_name="enhanced_incidents.csv")

import streamlit as st
import pandas as pd
import re
from collections import Counter

def extract_keywords(text_series, top_n=10):
    all_words = []
    for desc in text_series.dropna():
        words = re.findall(r"\b\w{4,}\b", str(desc).lower())  # 4+ character words
        all_words.extend(words)
    common_words = Counter(all_words).most_common(top_n)
    return pd.DataFrame(common_words, columns=["Keyword", "Count"])

def convert_to_minutes(time_series):
    if pd.api.types.is_numeric_dtype(time_series):
        return time_series
    try:
        # Handle HH:MM:SS or D-HH:MM:SS formats
        return pd.to_timedelta(time_series, errors="coerce").dt.total_seconds() / 60
    except:
        return pd.Series([None] * len(time_series))

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

            # Convert time fields
            df["duration_minutes"] = pd.to_numeric(df["Time worked"], errors="coerce")
            df["business_duration_min"] = convert_to_minutes(df["Business duration"])
            df["business_resolve_min"] = convert_to_minutes(df["Business resolve time"])

            # Basic metrics
            total_incidents = len(df)
            avg_duration = df["duration_minutes"].mean()
            avg_resolve = df["business_resolve_min"].mean()
            worst_resolve = df["business_resolve_min"].max()
            high_impact = df[df["Impact"].str.contains("High", case=False, na=False)]
            changes_linked = df[df["Caused by Change"].notna() & (df["Caused by Change"].str.strip() != "")]

            st.metric("Total Incidents", total_incidents)
            st.metric("Average Time Worked (min)", round(avg_duration, 2) if not pd.isna(avg_duration) else "N/A")
            st.metric("MTTR (Mean Time to Resolve)", round(avg_resolve, 2) if not pd.isna(avg_resolve) else "N/A")
            st.metric("Longest Resolution (min)", round(worst_resolve, 2) if not pd.isna(worst_resolve) else "N/A")
            st.metric("High Impact Incidents", len(high_impact))

            # Keyword frequency
            st.markdown("### 🔍 Top Keywords in Incident Descriptions")
            keyword_df = extract_keywords(df["Short description"], top_n=10)
            st.dataframe(keyword_df)

            # Optional: Show top issue codes
            if "Issue Code" in df.columns:
                st.markdown("### 🧩 Top Issue Codes")
                top_issues = df["Issue Code"].value_counts().head(5)
                st.bar_chart(top_issues)

            # Optional: Changes linked
            if not changes_linked.empty:
                st.markdown("### 🔗 Incidents Linked to Change")
                top_change_causes = changes_linked["Caused by Change"].value_counts().head(3)
                st.dataframe(top_change_causes.rename("Count"))

            st.markdown("---")
            if st.checkbox("Show full incident table"):
                st.dataframe(df)

        except Exception as e:
            st.error(f"Error processing file: {e}")

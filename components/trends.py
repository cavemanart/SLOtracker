import streamlit as st
import pandas as pd
import altair as alt

INCIDENT_CACHE_KEY = "incident_data"


def render_trends():
    st.title("📈 Incident Trends & Analytics")

    if INCIDENT_CACHE_KEY not in st.session_state:
        st.info("Upload an incident CSV in the Incident Log tab.")
        return

    df = st.session_state[INCIDENT_CACHE_KEY]

    st.subheader("📊 Issues by Assignment Group")
    if "assignment group" in df.columns:
        group_counts = df["assignment group"].value_counts().reset_index()
        group_counts.columns = ["assignment group", "count"]
        chart = alt.Chart(group_counts).mark_bar().encode(
            x=alt.X("count:Q", title="Incident Count"),
            y=alt.Y("assignment group:N", sort="-x", title="Group"),
            tooltip=["assignment group", "count"]
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

    st.subheader("🔥 Top Repeated Issues")
    if "short description" in df.columns:
        top_issues = df["short description"].value_counts().head(10).reset_index()
        top_issues.columns = ["issue", "count"]
        st.write(top_issues)

    st.subheader("⏱️ Average Business Resolve Time by Severity")
    if "severity" in df.columns and "business resolve time" in df.columns:
        try:
            df["business resolve time"] = pd.to_numeric(df["business resolve time"], errors="coerce")
            avg_times = df.groupby("severity")["business resolve time"].mean().reset_index()
            chart = alt.Chart(avg_times).mark_bar().encode(
                x="severity:N",
                y=alt.Y("business resolve time:Q", title="Avg Resolve Time (hrs)"),
                tooltip=["severity", "business resolve time"]
            )
            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error plotting average resolve time: {e}")

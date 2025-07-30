import streamlit as st
import pandas as pd
import altair as alt
from collections import Counter

def render_incident_log():
    st.title("📋 Incident Log & Response Optimizer")

    st.markdown("Upload your **incident CSV** below to analyze patterns, improve response times, and support change management planning.")

    uploaded_file = st.file_uploader("Upload Incident CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully.")
        st.subheader("🧾 Incident Table Preview")
        st.dataframe(df.head(20))

        st.subheader("📊 Key Stats")

        if "state" in df.columns:
            state_counts = df["state"].value_counts()
            st.metric("Open Incidents", state_counts.get("open", 0))
            st.metric("Closed Incidents", state_counts.get("closed", 0))

        if "severity" in df.columns:
            st.write("**Severity Breakdown:**")
            st.bar_chart(df["severity"].value_counts())

        if "issue code" in df.columns:
            top_issues = df["issue code"].value_counts().head(5)
            st.write("**Top 5 Issue Codes:**")
            st.bar_chart(top_issues)

        if "made sla" in df.columns:
            breached = df[df["made sla"] == False]
            st.metric("SLA Breaches", len(breached))
            if len(breached) > 0 and "assignment group" in breached.columns:
                st.write("**Most SLA Breached Groups:**")
                st.bar_chart(breached["assignment group"].value_counts().head(5))

        if "assignment group" in df.columns:
            st.write("**Top Assignment Groups:**")
            st.bar_chart(df["assignment group"].value_counts().head(5))

        st.markdown("---")
        st.subheader("🛠️ Change Management Planner")
        if "description" in df.columns:
            keyword_counts = Counter(" ".join(df["description"].astype(str)).lower().split())
            st.write("**Common Incident Keywords (from description):**")
            common_words = pd.DataFrame(keyword_counts.most_common(10), columns=["Word", "Count"])
            st.dataframe(common_words)

        st.markdown("---")
        st.subheader("🧭 Link to SLO & Service")

        service = st.text_input("Enter the service this incident data relates to (used for SLO tracking):", "")
        if service:
            st.success(f"✅ Service '{service}' mapped successfully to incident log.")
            # Optionally store in session_state for later reuse
            st.session_state['mapped_service'] = service

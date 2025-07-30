import streamlit as st
import pandas as pd
import datetime

def render_postmortem_tracker():
    st.subheader("📋 Postmortems")

    tab1, tab2 = st.tabs(["📄 Upload CSV", "✍️ Manual Entry"])

    with tab1:
        uploaded_file = st.file_uploader("Upload Postmortems CSV", type="csv", key="postmortem_upload")

        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("🔍 Raw Postmortem Data", df)

                required_columns = {"status", "due"}
                if not required_columns.issubset(df.columns):
                    st.warning(f"⚠️ CSV must include these columns: {', '.join(required_columns)}")
                    return

                df["due"] = pd.to_datetime(df["due"], errors="coerce")
                overdue = df[
                    (df["status"].str.lower() != "closed") &
                    (df["due"].dt.date < datetime.date.today())
                ]

                st.error(f"🚨 {len(overdue)} postmortems overdue")
                st.write(overdue)

            except Exception as e:
                st.error(f"❌ Failed to process postmortem CSV: {e}")
        else:
            st.info("📄 Upload a CSV to track postmortem follow-ups.")

    with tab2:
        st.markdown("**Suggested Fields:** `title`, `owner`, `status`, `due`")

        postmortem_data = []
        with st.form("manual_pm_form"):
            num_rows = st.number_input("How many postmortems to enter?", 1, 10, 1)
            for i in range(num_rows):
                st.markdown(f"**Postmortem {i+1}**")
                title = st.text_input("Title", key=f"title_{i}")
                owner = st.text_input("Owner", key=f"owner_{i}")
                status = st.selectbox("Status", ["Open", "In Progress", "Closed"], key=f"status_{i}")
                due = st.date_input("Due Date", key=f"due_{i}")
                postmortem_data.append({
                    "title": title,
                    "owner": owner,
                    "status": status,
                    "due": pd.to_datetime(due)
                })
            submitted = st.form_submit_button("Submit")

        if submitted:
            df = pd.DataFrame(postmortem_data)
            st.success("✅ Postmortems recorded")
            st.write(df)

            overdue = df[
                (df["status"].str.lower() != "closed") &
                (df["due"].dt.date < datetime.date.today())
            ]
            st.error(f"🚨 {len(overdue)} postmortems overdue")
            st.write(overdue)

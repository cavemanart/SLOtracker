def render_incident_tracker():
    st.subheader("🛠️ Incident Tracker")

    incidents = load_data("incidents")  # FIX: Make sure this loads a list
    if incidents is None or not isinstance(incidents, list):
        incidents = []

    if incidents:
        df = pd.DataFrame(incidents)
        st.dataframe(df)
    else:
        st.info("No incidents recorded yet.")

    with st.form("incident_form"):
        st.write("Log a new incident")
        title = st.text_input("Title")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        reported_by = st.text_input("Reported By")
        description = st.text_area("Description")

        submitted = st.form_submit_button("Log Incident")
        if submitted:
            new_incident = {
                "title": title,
                "severity": severity,
                "reported_by": reported_by,
                "description": description,
                "timestamp": datetime.datetime.now().isoformat()
            }
            incidents.append(new_incident)
            save_data("incidents", incidents)
            st.success("Incident logged!")

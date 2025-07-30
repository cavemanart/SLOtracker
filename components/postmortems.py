def render_postmortem_tracker():
    st.subheader("📋 Postmortems")

    postmortems = load_data("postmortems")
    if postmortems is None or not isinstance(postmortems, list):
        postmortems = []

    if postmortems:
        open_pms = []
        for pm in postmortems:
            if (
                isinstance(pm, dict) and
                "status" in pm and "due" in pm and
                pm["status"] != "Closed" and
                datetime.date.fromisoformat(pm["due"]) < datetime.date.today()
            ):
                open_pms.append(pm)

        if open_pms:
            st.warning(f"⚠️ You have {len(open_pms)} overdue postmortems")
        st.dataframe(pd.DataFrame(postmortems))
    else:
        st.info("No postmortems yet.")

    with st.form("postmortem_form"):
        st.write("Submit Postmortem")
        incident = st.text_input("Related Incident")
        summary = st.text_area("Summary")
        root_cause = st.text_area("Root Cause")
        action_items = st.text_area("Action Items")
        due_date = st.date_input("Due Date")

        submitted = st.form_submit_button("Submit Postmortem")
        if submitted:
            new_pm = {
                "incident": incident,
                "summary": summary,
                "root_cause": root_cause,
                "action_items": action_items,
                "due": due_date.isoformat(),
                "status": "Open",
                "created_at": datetime.datetime.now().isoformat()
            }
            postmortems.append(new_pm)
            save_data("postmortems", postmortems)
            st.success("Postmortem submitted.")

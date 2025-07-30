import streamlit as st
from core.storage import load_metrics, save_metrics
from core.compute import mttr_mttd

def render():
    st.subheader("🚨 Incident Tracker")
    with st.form("incident_form"):
        summary = st.text_input("Incident Summary")
        detected = st.number_input("Time to Detect (min)", 0)
        resolved = st.number_input("Time to Resolve (min)", 0)
        submitted = st.form_submit_button("Add Incident")

        if submitted:
            data = load_metrics("incidents.json")
            data.append({"summary": summary, "detected_in_minutes": detected, "resolved_in_minutes": resolved})
            save_metrics("incidents.json", data)
            st.success("Incident recorded!")

    incidents = load_metrics("incidents.json")
    if incidents:
        mttr, mttd = mttr_mttd(incidents)
        st.metric("🛠️ MTTR", f"{mttr} min")
        st.metric("🔍 MTTD", f"{mttd} min")
        st.table(incidents)
    else:
        st.info("No incidents logged yet.")

import streamlit as st

def render_postmortem_log():
    st.subheader("📋 Postmortem Log")
    st.text_area("Postmortem Summary", key="pm_summary")
    st.text_input("Key Learnings", key="pm_learnings")
    st.button("Save Postmortem", key="save_pm")

# streamlit_app.py

import streamlit as st
from components.slo_dashboard import render_slo_dashboard
from components.incidents import render_incident_log
from components.postmortems import render_postmortems
from core.utils import show_header, get_active_tab

st.set_page_config(page_title="SLO Tracker", layout="wide")

def main():
    show_header()

    tab = get_active_tab()

    if tab == "SLO Dashboard":
        render_slo_dashboard()
    elif tab == "Incident Log":
        render_incident_log()
    elif tab == "Postmortems":
        render_postmortems()
    else:
        st.warning("Tab not found.")

if __name__ == "__main__":
    main()

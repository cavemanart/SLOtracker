import streamlit as st
from core.storage import load_json, SLO_FILE

def render_dashboard():
    st.title("SLO Dashboard")
    data = load_json(SLO_FILE)
    if not data:
        st.info("No SLO records found.")
        return

    for entry in data[::-1]:
        st.markdown(f"**{entry['desc']}** ({entry['service']})")
        st.markdown(f"SLI: `{entry['sli']:.2f}%` based on {entry['success']}/{entry['total']} requests")
        st.markdown("---")

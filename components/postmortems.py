import streamlit as st
from core.storage import load_metrics, save_metrics

def render():
    st.subheader("📜 Postmortems")
    title = st.text_input("Postmortem Title")
    notes = st.text_area("Summary and Learnings")

    if st.button("📝 Add Postmortem"):
        data = load_metrics("postmortems.json")
        data.append({"title": title, "notes": notes})
        save_metrics("postmortems.json", data)
        st.success("Postmortem added.")

    posts = load_metrics("postmortems.json")
    if posts:
        for p in posts:
            st.markdown(f"### {p['title']}")
            st.markdown(p['notes'])
            st.markdown("---")
    else:
        st.info("No postmortems available.")

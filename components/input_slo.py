import streamlit as st
from core.storage import load_json, save_json, SLO_FILE
from core.suggestions import suggest_targets, evaluate_target

def render_slo_input():
    st.title("Add or Evaluate SLO")

    service = st.selectbox("Service Type", ["API", "Database", "Auth", "Other"])
    description = st.text_input("Short description of the service")
    success = st.number_input("Successful Requests", min_value=0)
    total = st.number_input("Total Requests", min_value=1)

    if st.button("Calculate & Suggest"):
        percent = (success / total) * 100
        suggested, reason = suggest_targets(service)
        evaluation = evaluate_target(percent)

        st.markdown(f"### ✅ Calculated SLI: `{percent:.2f}%`")
        st.markdown(f"Suggested Target: `{suggested}%` – _{reason}_")
        st.info(evaluation)

        # Save SLO entry
        data = load_json(SLO_FILE)
        data.append({
            "service": service,
            "desc": description,
            "success": success,
            "total": total,
            "sli": percent
        })
        save_json(SLO_FILE, data)
        st.success("Saved to SLO records.")

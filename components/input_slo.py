import streamlit as st
import pandas as pd
from core.storage import save_data, load_data
from core.suggestions import suggest_sli_inputs

def render_slo_input():
    st.subheader("📥 Input SLIs/SLOs")

    with st.expander("💡 Suggestions"):
        st.write(suggest_sli_inputs())

    input_mode = st.radio("Input method", ["Manual", "Upload CSV"])

    if input_mode == "Manual":
        with st.form("manual_input"):
            availability = st.number_input("Availability (%)", min_value=0.0, max_value=100.0, value=99.9)
            latency = st.number_input("Latency (ms)", min_value=0.0, value=200.0)
            error_rate = st.number_input("Error Rate (%)", min_value=0.0, max_value=100.0, value=0.5)
            sli_target = st.number_input("SLI Target (%)", min_value=0.0, max_value=100.0, value=99.0)
            submitted = st.form_submit_button("Save Entry")

            if submitted:
                new_row = pd.DataFrame([{
                    "availability": availability,
                    "latency": latency,
                    "error_rate": error_rate,
                    "sli_target": sli_target
                }])
                existing = load_data()
                save_data(pd.concat([existing, new_row], ignore_index=True))
                st.success("SLO entry saved!")

    elif input_mode == "Upload CSV":
        uploaded = st.file_uploader("Upload CSV", type="csv")
        if uploaded:
            new_data = pd.read_csv(uploaded)
            existing = load_data()
            save_data(pd.concat([existing, new_data], ignore_index=True))
            st.success("CSV data uploaded.")

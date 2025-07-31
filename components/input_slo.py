import streamlit as st
import json
from pathlib import Path

def render_input_slo():
    st.title("📝 Input SLOs")
    slo_file = Path("data/slo_data.json")

    with st.form("slo_form"):
        service = st.text_input("Service Name")
        description = st.text_input("SLO Description")
        target = st.slider("SLO Target (%)", min_value=1.0, max_value=99.9, step=0.1)
        submitted = st.form_submit_button("Add SLO")

        if submitted:
            if slo_file.exists():
                with open(slo_file) as f:
                    slo_data = json.load(f)
            else:
                slo_data = []

            slo_data.append({
                "service": service,
                "description": description,
                "target": target,
                "sli": None
            })

            slo_file.parent.mkdir(parents=True, exist_ok=True)
            with open(slo_file, "w") as f:
                json.dump(slo_data, f, indent=2)

            st.success("SLO added.")

    st.subheader("💡 Suggested SRE SLOs")
    st.markdown("""
    - **Availability**: 99.9% uptime for production API
    - **Latency**: 95% of requests under 200ms
    - **Error Rate**: Less than 0.1% of failed requests
    - **Durability**: Zero data loss incidents per quarter
    - **Throughput**: Sustain 1000 requests/sec
    """)


import streamlit as st import json import os

SLO_FILE_PATH = "core/storage/slo_data.json"

SERVICES = [ "Authentication", "Payments", "Search", "User Profile", "Notifications" ]

SLI_OPTIONS = [ "Availability", "Latency", "Error Rate", "Throughput" ]

def load_slos(): if os.path.exists(SLO_FILE_PATH): with open(SLO_FILE_PATH, "r") as f: return json.load(f) return []

def save_slos(slos): with open(SLO_FILE_PATH, "w") as f: json.dump(slos, f, indent=2)

def render_input_slo(): st.header("📈 Input SLO Definitions")

slos = load_slos()

with st.form("slo_form"):
    service = st.selectbox("Service", SERVICES)
    sli = st.selectbox("SLI Type", SLI_OPTIONS)
    objective = st.number_input("Objective % (e.g. 99.9)", min_value=90.0, max_value=100.0, value=99.0, step=0.1)
    period = st.selectbox("Evaluation Period", ["7 days", "30 days", "90 days"])
    notes = st.text_area("Notes", "")
    submit = st.form_submit_button("Save SLO")

    if submit:
        slos.append({
            "service": service,
            "sli": sli,
            "objective": objective,
            "period": period,
            "notes": notes
        })
        save_slos(slos)
        st.success("✅ SLO saved.")

if slos:
    st.subheader("📋 Existing SLOs")
    for slo in slos:
        st.markdown(f"**Service:** {slo['service']} | **SLI:** {slo['sli']} | **Target:** {slo['objective']}% | **Period:** {slo['period']}")
        if slo['notes']:
            st.markdown(f"_Notes:_ {slo['notes']}")
        st.markdown("---")


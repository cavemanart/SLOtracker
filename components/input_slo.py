import streamlit as st
import json
import os
from datetime import datetime

SLO_DATA_FILE = "core/storage/slo_data.json"

def load_slo_data():
    if not os.path.exists(SLO_DATA_FILE) or os.path.getsize(SLO_DATA_FILE) == 0:
        return []
    with open(SLO_DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_slo_data(data):
    os.makedirs(os.path.dirname(SLO_DATA_FILE), exist_ok=True)
    with open(SLO_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def render_slo_input():
    st.header("🎯 Input New SLO")

    service = st.text_input("Service Name")
    objective = st.text_input("Objective Description")
    target = st.slider("Target %", 80, 100, 99)
    timeframe = st.selectbox("Timeframe", ["7d", "30d", "90d", "180d", "365d"])
    notes = st.text_area("Notes (Optional)")

    if st.button("➕ Add SLO"):
        if service and objective:
            new_slo = {
                "service": service,
                "objective": objective,
                "target": target,
                "timeframe": timeframe,
                "notes": notes,
                "created_at": datetime.utcnow().isoformat()
            }

            slo_data = load_slo_data()
            slo_data.append(new_slo)
            save_slo_data(slo_data)

            st.success("SLO added successfully!")
            st.experimental_rerun()
        else:
            st.warning("Please fill out all required fields.")

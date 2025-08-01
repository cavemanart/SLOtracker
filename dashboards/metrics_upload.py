import streamlit as st
import pandas as pd
from utils.storage import store_uploaded_file

def render_metrics_upload():
    st.title("⬆️ Upload Custom Metric Data")

    uploaded_file = st.file_uploader("Upload a CSV with your SLO/SLI/KPI data", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())

        store_uploaded_file(uploaded_file, subdir="custom")
        st.success("File stored and ready for analysis!")

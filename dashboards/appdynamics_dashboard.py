import streamlit as st
import pandas as pd
from utils.xml_parser import parse_appdynamics_xml
from utils.graphs import render_appdynamics_graphs
from utils.storage import store_uploaded_file

def render_appdynamics_dashboard():
    st.title("📈 AppDynamics XML and Business Transaction CSV Viewer")

    xml_file = st.file_uploader("Upload AppDynamics XML export", type=["xml"])
    if xml_file:
        data = parse_appdynamics_xml(xml_file)
        st.subheader("Parsed Summary")
        st.dataframe(data)
        render_appdynamics_graphs(data)
        store_uploaded_file(xml_file, subdir="xml")

    st.subheader("Business Transaction CSV")
    bt_file = st.file_uploader("Upload BT Data CSV", type=["csv"])
    if bt_file:
        df = pd.read_csv(bt_file)
        st.write(df.head())
        store_uploaded_file(bt_file, subdir="bt")

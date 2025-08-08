import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from io import BytesIO

DATA_FILE = "metrics_data.csv"

def get_data_file_path():
    # Make sure file path is absolute relative to this script
    return os.path.join(os.path.dirname(__file__), DATA_FILE)

def load_data():
    path = get_data_file_path()
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(columns=["Service", "Metric Type", "Metric Name", "Definition", "Target", "Current Value", "Owner", "Last Updated"])

def save_data(df):
    path = get_data_file_path()
    df.to_csv(path, index=False)

def export_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="SRE Metrics Report", ln=True, align='C')
    for index, row in df.iterrows():
        for col in df.columns:
            pdf.cell(200, 10, txt=f"{col}: {row[col]}", ln=True)
        pdf.cell(200, 10, txt="-----------------------------", ln=True)
    # Save PDF to bytes buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

st.title("SRE Metrics Analyzer")

df = load_data()

st.subheader("Define New Metric")
with st.form("metric_form"):
    service = st.text_input("Service/Component")
    metric_type = st.selectbox("Metric Type", ["SLA", "SLO", "SLI", "KPI", "KPR"])
    metric_name = st.text_input("Metric Name")
    definition = st.text_area("Definition")
    target = st.text_input("Target/Threshold")
    current_value = st.text_input("Current Value")
    owner = st.text_input("Owner")
    last_updated = st.date_input("Last Updated")
    submitted = st.form_submit_button("Add Metric")
    if submitted:
        new_row = {
            "Service": service,
            "Metric Type": metric_type,
            "Metric Name": metric_name,
            "Definition": definition,
            "Target": target,
            "Current Value": current_value,
            "Owner": owner,
            "Last Updated": last_updated.strftime("%Y-%m-%d")  # convert to string
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Metric added successfully!")
        st.experimental_rerun()  # reload the app to show updated table

st.subheader("Current Metrics")
st.dataframe(df)

st.subheader("Export Options")
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", data=csv_data, file_name="SRE_Metrics_Export.csv", mime='text/csv')

pdf_buffer = export_pdf(df)
st.download_button("Download PDF Report", data=pdf_buffer, file_name="SRE_Metrics_Report.pdf", mime='application/pdf')

st.subheader("Dashboard View")
metric_counts = df["Metric Type"].value_counts()
fig, ax = plt.subplots()
ax.pie(metric_counts, labels=metric_counts.index, autopct='%1.1f%%')
st.pyplot(fig)

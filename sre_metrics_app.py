
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

DATA_FILE = "metrics_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Service", "Metric Type", "Metric Name", "Definition", "Target", "Current Value", "Owner", "Last Updated"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def export_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="SRE Metrics Report", ln=True, align='C')
    for index, row in df.iterrows():
        for col in df.columns:
            pdf.cell(200, 10, txt=f"{col}: {row[col]}", ln=True)
        pdf.cell(200, 10, txt="-----------------------------", ln=True)
    pdf.output("SRE_Metrics_Report.pdf")

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
            "Last Updated": last_updated
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Metric added successfully!")

st.subheader("Current Metrics")
st.dataframe(df)

st.subheader("Export Options")
if st.button("Download CSV"):
    df.to_csv("SRE_Metrics_Export.csv", index=False)
    st.success("CSV file exported.")

if st.button("Download PDF Report"):
    export_pdf(df)
    st.success("PDF report generated.")

st.subheader("Dashboard View")
metric_counts = df["Metric Type"].value_counts()
fig, ax = plt.subplots()
ax.pie(metric_counts, labels=metric_counts.index, autopct='%1.1f%%')
st.pyplot(fig)

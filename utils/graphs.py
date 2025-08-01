import streamlit as st
import pandas as pd
import plotly.express as px

def render_trend_graphs(df):
    if "Time" in df.columns and "Value" in df.columns:
        fig = px.line(df, x="Time", y="Value", color="Metric", title="Custom Metric Trends")
        st.plotly_chart(fig, use_container_width=True)

def render_appdynamics_graphs(df):
    if "Transaction Name" in df.columns and "Response Time (ms)" in df.columns:
        fig = px.bar(df, x="Transaction Name", y="Response Time (ms)", title="Response Time by Transaction")
        st.plotly_chart(fig, use_container_width=True)

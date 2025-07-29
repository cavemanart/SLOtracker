import plotly.express as px
import streamlit as st

def plot_sli_trends(df, slo):
    df_plot = slo['data'].copy()
    df_plot = df_plot.sort_values('timestamp')

    if slo['name'].lower().startswith('availability'):
        df_plot['sli'] = (df_plot[df_plot.columns[2]] / df_plot[df_plot.columns[3]]) * 100
    elif slo['name'].lower().startswith('latency'):
        df_plot['sli'] = df_plot[df_plot.columns[4]]

    fig = px.line(df_plot, x='timestamp', y='sli', title=f"SLI: {slo['name']}")
    fig.add_hline(y=slo['target'], line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
from core.storage import load_json, SLO_FILE
import pandas as pd

def render_trend_charts():
    st.title("Historical Trends")

    data = load_json(SLO_FILE)
    if not data:
        st.warning("No historical data.")
        return

    df = pd.DataFrame(data)
    df["index"] = range(1, len(df)+1)

    st.line_chart(df[["index", "sli"]].set_index("index"))

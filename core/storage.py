import pandas as pd
import os

DATA_FILE = "data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["availability", "latency", "error_rate", "sli_target"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

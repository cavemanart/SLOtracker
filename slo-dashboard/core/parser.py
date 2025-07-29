import pandas as pd

def parse_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

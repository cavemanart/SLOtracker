# utils/csv_utils.py

import pandas as pd

def parse_appdynamics_csv(file):
    df = pd.read_csv(file)
    # Normalize headers
    df.columns = [col.strip() for col in df.columns]
    return df

def normalize_appd_bt_csv(df):
    rename_map = {
        "Transaction Type": "transaction_type",
        "Name": "name",
        "Health": "health",
        "Response Time (ms)": "response_time_ms",
        "End to End Latency Time (ms)": "latency_ms",
        "Max Response Time (ms)": "max_response_time_ms",
        "Calls / min": "calls_per_min",
        "Errors / min": "errors_per_min",
        "% Errors": "percent_errors",
        "% Slow Transactions": "percent_slow",
        "Very Slow Transactions": "very_slow",
        "% Very Slow Transactions": "percent_very_slow",
        "% Stalled Transactions": "percent_stalled",
        "Wait Time (ms)": "wait_time_ms"
    }
    df = df.rename(columns=rename_map)
    return df

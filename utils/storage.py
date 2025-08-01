import os
import json
import pandas as pd

METRIC_FILE = "data/saved_metrics.json"

def save_custom_metrics():
    df = pd.DataFrame({
        "Metric": ["MTTR", "Availability", "Latency"],
        "Value": [4200, 99.95, 250],
        "Unit": ["seconds", "%", "ms"]
    })
    df.to_json(METRIC_FILE, orient="records")

def load_custom_metrics():
    if os.path.exists(METRIC_FILE):
        with open(METRIC_FILE) as f:
            return json.load(f)
    return []

def store_uploaded_file(file, subdir="custom"):
    os.makedirs(f"data/uploads/{subdir}", exist_ok=True)
    with open(f"data/uploads/{subdir}/{file.name}", "wb") as f:
        f.write(file.read())

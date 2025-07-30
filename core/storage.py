import json
import os

DATA_FILE = "data/sample_metrics.json"

def load_metrics():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_metrics(metrics):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

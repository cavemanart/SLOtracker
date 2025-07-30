import json
import os

DATA_FILE = "data/sample_metrics.json"

def load_metrics():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_metrics(metrics):
    with open(DATA_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

def get_health_score(metrics):
    if not metrics:
        return 0
    met_count = sum(1 for m in metrics if m.get("Status") == "Met")
    return round((met_count / len(metrics)) * 100, 1)

import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def save_metrics(file, data):
    with open(DATA_DIR / file, "w") as f:
        json.dump(data, f)

def load_metrics(file):
    try:
        with open(DATA_DIR / file) as f:
            return json.load(f)
    except FileNotFoundError:
        return []

import json
import os

DATA_DIR = "data"
SLO_FILE = os.path.join(DATA_DIR, "slo_data.json")
INCIDENT_FILE = os.path.join(DATA_DIR, "incidents.json")
POSTMORTEM_FILE = os.path.join(DATA_DIR, "postmortems.json")

def load_json(file_path, default=[]):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return default

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

import pandas as pd

def get_sample_data():
    return pd.DataFrame([
        {
            "Service/Component": "API Gateway",
            "SLI (Metric)": "% of successful HTTP 200 responses",
            "SLO Target": 99.9,
            "Current Value": 99.95
        },
        {
            "Service/Component": "User Login",
            "SLI (Metric)": "p95 latency < 300ms",
            "SLO Target": 95,
            "Current Value": 92
        },
        {
            "Service/Component": "Database",
            "SLI (Metric)": "Error rate < 0.1%",
            "SLO Target": 0.1,
            "Current Value": 0.05
        }
    ])

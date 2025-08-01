import pandas as pd

def compute_threshold_violations(df):
    violations = []
    for _, row in df.iterrows():
        metric = row.get("Metric", "")
        value = row.get("Value", 0)

        if "MTTR" in metric and float(value) > 3600:
            violations.append(f"⚠️ High MTTR Detected: {value} seconds")

        if "Error Rate" in metric and float(value) > 5.0:
            violations.append(f"⚠️ Error rate > 5% on {metric}")

    return violations if violations else "✅ All thresholds healthy."

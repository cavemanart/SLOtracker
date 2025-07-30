# For future expansion: store snapshots, export reports, cloud sync, etc.
def save_snapshot_to_markdown(metrics, filename="reports/snapshot.md"):
    with open(filename, "w") as f:
        for m in metrics:
            f.write(f"- {m['Service']}: {m['SLI']} - {m['Current Value']} (Target: {m['SLO Target']}) - {m['Status']}\n")

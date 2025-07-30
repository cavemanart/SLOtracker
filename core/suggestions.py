def suggest_improvements(metrics):
    suggestions = []
    for m in metrics:
        if m.get("Status") == "Not Met":
            if "latency" in m["SLI"].lower():
                suggestions.append(f"{m['Service']}: Investigate API optimization or cache issues.")
            elif "error" in m["SLI"].lower():
                suggestions.append(f"{m['Service']}: Check logs for 5xx trends or error spikes.")
            else:
                suggestions.append(f"{m['Service']}: Review SLI definition and incident reports.")
    if not suggestions:
        suggestions.append("All systems look good! Maintain observability and incident readiness.")
    return suggestions

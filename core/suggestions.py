def suggest_improvements(metrics):
    suggestions = []
    for m in metrics:
        if m["status"] == "Not Met":
            suggestions.append(
                f"🔧 {m['service']}: Consider investigating why {m['sli']} is below the target of {m['slo_target']}. "
                f"Current: {m['current_value']}"
            )
        elif m["status"] == "Unknown":
            suggestions.append(
                f"❓ {m['service']}: Unable to determine status. Check format of target/current values."
            )
    if not suggestions:
        suggestions.append("✅ All tracked metrics are meeting their SLOs.")
    return suggestions

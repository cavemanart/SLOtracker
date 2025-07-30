def suggest_targets(service_type):
    if service_type == "API":
        return 99.9, "Common SLO target for APIs"
    elif service_type == "Database":
        return 99.95, "Typical for backend DBs"
    elif service_type == "Auth":
        return 99.99, "Critical path SLO target"
    else:
        return 99.0, "Default baseline"

def evaluate_target(slo):
    if slo >= 99.99:
        return "⚠️ Aggressive SLO"
    elif slo < 95:
        return "⚠️ Weak SLO"
    return "✅ Reasonable"

def suggest_slo_targets(metric_type):
    suggestions = {
        "availability": "99.9%",
        "latency": "< 300ms",
        "error_rate": "< 0.1%",
        "throughput": ">= 1000 req/min"
    }
    return suggestions.get(metric_type.lower(), "Review your baseline")

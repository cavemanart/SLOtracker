import statistics

def calculate_sli(data, key="success", total="total"):
    if not data:
        return 0.0
    try:
        return round(100 * sum(d[key] for d in data) / sum(d[total] for d in data), 2)
    except ZeroDivisionError:
        return 0.0

def mttr_mttd(incidents):
    if not incidents:
        return 0, 0
    mttrs = [i["resolved_in_minutes"] for i in incidents if "resolved_in_minutes" in i]
    mttds = [i["detected_in_minutes"] for i in incidents if "detected_in_minutes" in i]
    return round(statistics.mean(mttrs), 2), round(statistics.mean(mttds), 2)

def calculate_status(slo_target, current_value):
    try:
        target = float(slo_target.strip('%'))
        current = float(current_value.strip('%'))
        return "Met" if current >= target else "Not Met"
    except:
        return "Unknown"

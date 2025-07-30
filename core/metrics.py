def evaluate_status(target, current, reverse=False):
    try:
        if reverse:
            return "Met" if current <= target else "Not Met"
        else:
            return "Met" if current >= target else "Not Met"
    except Exception:
        return "N/A"

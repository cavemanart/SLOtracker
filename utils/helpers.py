def percent_format(value):
    try:
        return f"{value:.2f}%"
    except:
        return value

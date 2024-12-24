import math


def sanitize_event(event):
    sanitized_event = {}
    for key, value in event.items():
        if isinstance(value, float) and math.isnan(value):
            sanitized_event[key] = None
        else:
            sanitized_event[key] = value
    return sanitized_event
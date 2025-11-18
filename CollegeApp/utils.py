"""
Utility functions for parsing and converting schedule data.

Functions:
    time_str_to_minutes: Convert "HH:MM" to minutes since midnight.
    minutes_to_slot_index: Convert minutes since midnight to grid row index.
    parse_schedule_input: Parse input like "M W F 10:30-11:20" into days list and start/end times in minutes.
"""


import re

DAY_MAP = {
    'M': 0, 'MON': 0,
    'T': 1, 'TU': 1, 'TUE': 1,
    'W': 2, 'WED': 2,
    'R': 3, 'TH': 3, 'THU': 3,
    'F': 4, 'FRI': 4
}

START_HOUR = 8
SLOT_MINUTES = 30  


def time_str_to_minutes(s):
    """
    Convert HH:MM string to minutes since midnight.
    Accepts 1 or 2 digit hour.
    """
    s = s.strip()
    m = re.match(r"^(\d{1,2}):(\d{2})$", s)
    if not m:
        raise ValueError(f"Invalid time format: {s}")
    h, mm = int(m.group(1)), int(m.group(2))
    if not (0 <= mm < 60):
        raise ValueError(f"Invalid minutes in time: {s}")
    return h * 60 + mm


def minutes_to_slot_index(minutes):
    """Convert minutes since midnight to grid row index."""
    start = START_HOUR * 60
    if minutes < start:
        return None
    return (minutes - start) // SLOT_MINUTES


def parse_schedule_input(text):
    """
    Parse input like 'M W F 10:30-11:20' -> (days_list, start_min, end_min)
    Days may be letters or full names (Mon, Tue, etc.)
    """
    tokens = text.strip().upper().split()
    if len(tokens) < 2:
        raise ValueError("Input must include days and a time range")

    day_tokens = tokens[:-1]
    time_range = tokens[-1]

    match = re.match(r"^(\d{1,2}:\d{2})-(\d{1,2}:\d{2})$", time_range)
    if not match:
        raise ValueError("Time range must be like 10:30-11:20")

    start_min = time_str_to_minutes(match.group(1))
    end_min = time_str_to_minutes(match.group(2))
    if end_min <= start_min:
        raise ValueError("End time must be after start time")

    days = []
    for d in day_tokens:
        if len(d) > 1 and re.match(r"^[MTWRF]{2,}$", d):
            for ch in d:
                if ch in DAY_MAP:
                    days.append(DAY_MAP[ch])
                else:
                    raise ValueError(f"Unknown day: {ch}")
        else:
            if d in DAY_MAP:
                days.append(DAY_MAP[d])
            elif d[:3] in DAY_MAP:
                days.append(DAY_MAP[d[:3]])
            else:
                raise ValueError(f"Unknown day token: {d}")
    return sorted(set(days))
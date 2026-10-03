from __future__ import annotations

import pandas as pd


def ensure_utc(value):
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        return ts.tz_localize("UTC")
    return ts.tz_convert("UTC")


def floor_minutes(value, minutes: int):
    return ensure_utc(value).floor(f"{minutes}min")


def elapsed_minutes(a, b) -> float:
    return float((ensure_utc(b) - ensure_utc(a)).total_seconds() / 60.0)

from __future__ import annotations

import numpy as np
import pandas as pd


def add_risk_velocity(frame: pd.DataFrame, periods: int = 1) -> pd.DataFrame:
    out = frame.copy().sort_values("window_end")
    out["velocity"] = out["smoothed_probability"].diff(periods=periods)
    return out


def trend_label(velocity: float, fast: float = 0.12, slow: float = 0.04) -> str:
    if not np.isfinite(velocity):
        return "stable"
    if velocity >= fast:
        return "rising_fast"
    if velocity >= slow:
        return "rising"
    if velocity <= -fast:
        return "falling_fast"
    if velocity <= -slow:
        return "falling"
    return "stable"


def annotate_trends(frame: pd.DataFrame, periods: int = 1) -> pd.DataFrame:
    out = add_risk_velocity(frame, periods=periods)
    out["trend"] = out["velocity"].map(trend_label)
    return out

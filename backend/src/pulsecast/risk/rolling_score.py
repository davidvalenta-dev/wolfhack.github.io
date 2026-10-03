from __future__ import annotations

import numpy as np
import pandas as pd


def ewma_risk(probabilities, halflife_windows: float = 3.0) -> np.ndarray:
    s = pd.Series(np.asarray(probabilities, dtype=float))
    return s.ewm(halflife=halflife_windows, adjust=False, min_periods=1).mean().to_numpy()


def confidence_adjusted_risk(probability, confidence, floor: float = 0.5):
    p = np.asarray(probability, dtype=float)
    c = np.clip(np.asarray(confidence, dtype=float), 0.0, 1.0)
    return floor + (p - floor) * c


def compute_risk_stream(
    frame: pd.DataFrame,
    halflife_windows: float = 3.0,
    suppress_below_confidence: float = 0.30,
) -> pd.DataFrame:
    out = frame.copy().sort_values("window_end")
    adjusted = confidence_adjusted_risk(out["raw_probability"], out["signal_confidence"])
    out["adjusted_probability"] = adjusted
    out["smoothed_probability"] = ewma_risk(adjusted, halflife_windows=halflife_windows)
    out["suppressed"] = out["signal_confidence"] < suppress_below_confidence
    out.loc[out["suppressed"], "smoothed_probability"] = np.nan
    return out

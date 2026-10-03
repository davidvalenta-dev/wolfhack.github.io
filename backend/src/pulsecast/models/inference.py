from __future__ import annotations

import numpy as np
import pandas as pd


def predict_windows(model, windows: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    out = windows[[c for c in ["subject_id", "window_start", "window_end", "signal_confidence"] if c in windows]].copy()
    p = model.predict_proba(windows[feature_columns])[:, 1]
    out["raw_probability"] = np.clip(p, 0.0, 1.0)
    return out

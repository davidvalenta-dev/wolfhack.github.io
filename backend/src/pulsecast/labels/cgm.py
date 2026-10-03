from __future__ import annotations

import numpy as np
import pandas as pd


def cgm_metrics(dexcom: pd.DataFrame) -> dict[str, float]:
    if dexcom.empty:
        return {k: np.nan for k in [
            "cgm_mean", "cgm_std", "cgm_cv", "cgm_p95", "cgm_max",
            "cgm_time_gt_140", "cgm_time_gt_180", "cgm_mean_abs_delta"
        ]}
    g = pd.to_numeric(dexcom["Value"], errors="coerce").dropna()
    if g.empty:
        return {}
    mean = float(g.mean())
    std = float(g.std(ddof=1))
    return {
        "cgm_mean": mean,
        "cgm_std": std,
        "cgm_cv": std / mean if mean else np.nan,
        "cgm_p95": float(g.quantile(0.95)),
        "cgm_max": float(g.max()),
        "cgm_time_gt_140": float((g > 140).mean()),
        "cgm_time_gt_180": float((g > 180).mean()),
        "cgm_mean_abs_delta": float(g.diff().abs().mean()),
    }


def future_rise_labels(dexcom: pd.DataFrame, horizon_minutes: int = 30, rise_mg_dl: float = 20.0) -> pd.DataFrame:
    if dexcom.empty:
        return pd.DataFrame(columns=["timestamp", "future_glucose", "future_change", "future_rise"])
    d = dexcom[["timestamp", "Value"]].copy().sort_values("timestamp")
    d = d.rename(columns={"Value": "glucose"}).set_index("timestamp")
    grid = d.resample("5min").mean().interpolate(limit=2)
    steps = max(1, horizon_minutes // 5)
    grid["future_glucose"] = grid["glucose"].shift(-steps)
    grid["future_change"] = grid["future_glucose"] - grid["glucose"]
    grid["future_rise"] = (grid["future_change"] >= rise_mg_dl).astype("Int64")
    return grid.reset_index()

from __future__ import annotations

import numpy as np
import pandas as pd
from pulsecast.features.common import safe_mean, safe_std, safe_iqr, linear_slope, quantile


def accel_features(frame: pd.DataFrame) -> dict[str, float]:
    if frame.empty or not {"X", "Y", "Z"}.issubset(frame.columns):
        return {k: np.nan for k in [
            "acc_mag_mean", "acc_mag_std", "acc_mag_iqr", "acc_mag_p95",
            "acc_mag_slope", "acc_jerk_mean", "acc_jerk_p95", "acc_active_fraction"
        ]}
    xyz = frame[["X", "Y", "Z"]].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    mag = np.sqrt(np.nansum(np.square(xyz), axis=1))
    jerk = np.abs(np.diff(mag))
    rolling_baseline = pd.Series(mag).rolling(64, min_periods=8, center=True).median().to_numpy()
    residual = np.abs(mag - rolling_baseline)
    finite_residual = residual[np.isfinite(residual)]
    if finite_residual.size:
        residual_median = np.median(finite_residual)
        threshold = residual_median + 2.0 * np.median(np.abs(finite_residual - residual_median))
        active = residual > threshold
    else:
        active = np.zeros_like(residual, dtype=bool)
    return {
        "acc_mag_mean": safe_mean(mag),
        "acc_mag_std": safe_std(mag),
        "acc_mag_iqr": safe_iqr(mag),
        "acc_mag_p95": quantile(mag, 0.95),
        "acc_mag_slope": linear_slope(mag),
        "acc_jerk_mean": safe_mean(jerk),
        "acc_jerk_p95": quantile(jerk, 0.95),
        "acc_active_fraction": float(np.mean(active)) if active.size else np.nan,
    }

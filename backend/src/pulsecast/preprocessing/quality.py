from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import welch


def acceleration_magnitude(acc: pd.DataFrame) -> pd.Series:
    xyz = acc[["X", "Y", "Z"]].astype(float).to_numpy()
    return pd.Series(np.sqrt(np.square(xyz).sum(axis=1)), index=acc.index)


def motion_score(acc: pd.DataFrame) -> float:
    if acc.empty or not {"X", "Y", "Z"}.issubset(acc.columns):
        return 0.0
    mag = acceleration_magnitude(acc)
    centered = mag - mag.rolling(32, min_periods=1).median()
    return float(np.nanmedian(np.abs(centered)))


def bvp_spectral_quality(values: np.ndarray, sample_rate_hz: float = 64.0) -> float:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < int(sample_rate_hz * 10):
        return 0.0
    f, pxx = welch(x - np.mean(x), fs=sample_rate_hz, nperseg=min(len(x), 1024))
    total = float(np.trapezoid(pxx, f))
    band = (f >= 0.7) & (f <= 3.5)
    pulse = float(np.trapezoid(pxx[band], f[band])) if band.any() else 0.0
    if total <= 0:
        return 0.0
    return float(np.clip(pulse / total, 0.0, 1.0))


def combined_signal_confidence(
    bvp_quality: float,
    motion: float,
    missing_fraction: float,
    motion_reference: float = 0.15,
) -> float:
    motion_penalty = np.exp(-max(0.0, motion) / max(motion_reference, 1e-6))
    missing_penalty = 1.0 - np.clip(missing_fraction, 0.0, 1.0)
    score = 0.55 * bvp_quality + 0.30 * motion_penalty + 0.15 * missing_penalty
    return float(np.clip(score, 0.0, 1.0))

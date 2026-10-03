from __future__ import annotations

import numpy as np


def finite(x) -> np.ndarray:
    arr = np.asarray(x, dtype=float)
    return arr[np.isfinite(arr)]


def safe_mean(x) -> float:
    a = finite(x)
    return float(np.mean(a)) if a.size else np.nan


def safe_std(x) -> float:
    a = finite(x)
    return float(np.std(a, ddof=1)) if a.size > 1 else np.nan


def safe_median(x) -> float:
    a = finite(x)
    return float(np.median(a)) if a.size else np.nan


def safe_iqr(x) -> float:
    a = finite(x)
    if not a.size:
        return np.nan
    q1, q3 = np.quantile(a, [0.25, 0.75])
    return float(q3 - q1)


def linear_slope(x) -> float:
    a = np.asarray(x, dtype=float)
    mask = np.isfinite(a)
    if mask.sum() < 3:
        return np.nan
    y = a[mask]
    t = np.arange(a.size, dtype=float)[mask]
    t = t - t.mean()
    denom = float(np.dot(t, t))
    return float(np.dot(t, y - y.mean()) / denom) if denom > 0 else np.nan


def quantile(x, q: float) -> float:
    a = finite(x)
    return float(np.quantile(a, q)) if a.size else np.nan


def coefficient_of_variation(x) -> float:
    a = finite(x)
    if a.size < 2:
        return np.nan
    m = np.mean(a)
    return float(np.std(a, ddof=1) / m) if abs(m) > 1e-12 else np.nan

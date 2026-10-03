from __future__ import annotations

import numpy as np
import pandas as pd


def winsorize_series(s: pd.Series, low: float = 0.005, high: float = 0.995) -> pd.Series:
    numeric = pd.to_numeric(s, errors="coerce")
    lo, hi = numeric.quantile([low, high])
    return numeric.clip(lower=lo, upper=hi)


def interpolate_short_gaps(s: pd.Series, limit: int = 5) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").interpolate(limit=limit, limit_direction="both")


def clean_hr(s: pd.Series) -> pd.Series:
    out = pd.to_numeric(s, errors="coerce")
    out = out.where(out.between(30, 220))
    return interpolate_short_gaps(out, limit=10)


def clean_eda(s: pd.Series) -> pd.Series:
    out = pd.to_numeric(s, errors="coerce")
    out = out.where(out >= 0)
    return winsorize_series(out.fillna(out.median()))


def clean_temperature(s: pd.Series) -> pd.Series:
    out = pd.to_numeric(s, errors="coerce")
    out = out.where(out.between(20, 45))
    return interpolate_short_gaps(out, limit=20)


def robust_zscore(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    med = x.median()
    mad = np.median(np.abs(x.dropna().to_numpy() - med)) if x.notna().any() else np.nan
    if not np.isfinite(mad) or mad <= 1e-12:
        return pd.Series(np.zeros(len(x)), index=x.index, dtype=float)
    return 0.67448975 * (x - med) / mad

from __future__ import annotations

import numpy as np
from pulsecast.features.common import finite, safe_mean, safe_std, safe_median, linear_slope


def rmssd(ibi_seconds) -> float:
    x = finite(ibi_seconds)
    if x.size < 3:
        return np.nan
    d = np.diff(x)
    return float(np.sqrt(np.mean(np.square(d))))


def sdnn(ibi_seconds) -> float:
    return safe_std(ibi_seconds)


def pnn50(ibi_seconds) -> float:
    x = finite(ibi_seconds)
    if x.size < 3:
        return np.nan
    return float(np.mean(np.abs(np.diff(x)) > 0.050))


def ibi_features(values) -> dict[str, float]:
    x = finite(values)
    plausible = x[(x >= 0.25) & (x <= 2.5)]
    return {
        "ibi_mean": safe_mean(plausible),
        "ibi_median": safe_median(plausible),
        "ibi_sdnn": sdnn(plausible),
        "ibi_rmssd": rmssd(plausible),
        "ibi_pnn50": pnn50(plausible),
        "ibi_slope": linear_slope(plausible),
        "ibi_count": float(plausible.size),
    }

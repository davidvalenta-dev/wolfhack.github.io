from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks
from pulsecast.features.common import finite, safe_mean, safe_std, safe_iqr, linear_slope, quantile


def eda_features(values, fs: float = 4.0) -> dict[str, float]:
    x = finite(values)
    if x.size < 4:
        return {k: np.nan for k in [
            "eda_mean", "eda_std", "eda_iqr", "eda_slope", "eda_p95", "eda_peak_rate"
        ]}
    prominence = max(np.std(x) * 0.25, 1e-4)
    peaks, _ = find_peaks(x, distance=max(1, int(fs)), prominence=prominence)
    duration_min = x.size / fs / 60.0
    return {
        "eda_mean": safe_mean(x),
        "eda_std": safe_std(x),
        "eda_iqr": safe_iqr(x),
        "eda_slope": linear_slope(x),
        "eda_p95": quantile(x, 0.95),
        "eda_peak_rate": float(len(peaks) / duration_min) if duration_min > 0 else np.nan,
    }

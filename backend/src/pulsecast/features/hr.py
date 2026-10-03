from __future__ import annotations

import numpy as np
import pandas as pd
from pulsecast.features.common import safe_mean, safe_std, safe_median, safe_iqr, linear_slope, quantile


def hr_features(values) -> dict[str, float]:
    x = pd.to_numeric(pd.Series(values), errors="coerce").to_numpy(dtype=float)
    return {
        "hr_mean": safe_mean(x),
        "hr_std": safe_std(x),
        "hr_median": safe_median(x),
        "hr_iqr": safe_iqr(x),
        "hr_min": quantile(x, 0.02),
        "hr_max": quantile(x, 0.98),
        "hr_slope": linear_slope(x),
        "hr_p10": quantile(x, 0.10),
        "hr_p90": quantile(x, 0.90),
        "hr_range_80": quantile(x, 0.90) - quantile(x, 0.10),
    }

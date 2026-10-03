from __future__ import annotations

import numpy as np
from pulsecast.features.common import finite, safe_mean, safe_std, safe_iqr, linear_slope, quantile


def temp_features(values) -> dict[str, float]:
    x = finite(values)
    return {
        "temp_mean": safe_mean(x),
        "temp_std": safe_std(x),
        "temp_iqr": safe_iqr(x),
        "temp_slope": linear_slope(x),
        "temp_p10": quantile(x, 0.10),
        "temp_p90": quantile(x, 0.90),
    }

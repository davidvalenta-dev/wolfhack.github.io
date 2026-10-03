from __future__ import annotations

import numpy as np


def confidence_band(value: float) -> str:
    if not np.isfinite(value):
        return "unknown"
    if value >= 0.80:
        return "high"
    if value >= 0.55:
        return "medium"
    return "low"


def should_suppress(confidence: float, threshold: float = 0.30) -> bool:
    return not np.isfinite(confidence) or confidence < threshold

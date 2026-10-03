from __future__ import annotations

import numpy as np


def sigmoid(x):
    x = np.asarray(x, dtype=float)
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def logit(p):
    p = np.clip(np.asarray(p, dtype=float), 1e-8, 1 - 1e-8)
    return np.log(p / (1 - p))


def nan_weighted_mean(values, weights):
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    mask = np.isfinite(v) & np.isfinite(w) & (w > 0)
    if not mask.any():
        return np.nan
    return float(np.average(v[mask], weights=w[mask]))


def clamp01(x):
    return np.clip(np.asarray(x, dtype=float), 0.0, 1.0)

from __future__ import annotations

import numpy as np
import pandas as pd


def zscore_against_reference(
    subject_row: pd.Series,
    reference: pd.DataFrame,
    feature_columns: list[str],
) -> pd.Series:
    out = {}
    for c in feature_columns:
        ref = pd.to_numeric(reference[c], errors="coerce")
        mu, sd = ref.mean(), ref.std(ddof=1)
        value = float(subject_row[c]) if pd.notna(subject_row[c]) else np.nan
        out[c] = (value - mu) / sd if np.isfinite(sd) and sd > 1e-12 else 0.0
    return pd.Series(out)


def centroid_distance(
    row: pd.Series,
    group: pd.DataFrame,
    feature_columns: list[str],
) -> float:
    x = pd.to_numeric(row[feature_columns], errors="coerce").to_numpy(dtype=float)
    centroid = group[feature_columns].apply(pd.to_numeric, errors="coerce").median(axis=0).to_numpy(dtype=float)
    mask = np.isfinite(x) & np.isfinite(centroid)
    if not mask.any():
        return np.nan
    scale = group[feature_columns].apply(pd.to_numeric, errors="coerce").std(axis=0).to_numpy(dtype=float)
    scale = np.where(np.isfinite(scale) & (scale > 1e-9), scale, 1.0)
    return float(np.sqrt(np.mean(np.square((x[mask] - centroid[mask]) / scale[mask]))))

from __future__ import annotations

import numpy as np
import pandas as pd


def numeric_feature_columns(df: pd.DataFrame) -> list[str]:
    blocked = {"subject_id", "window_start", "window_end", "target", "hba1c", "metabolic_class"}
    return [c for c in df.select_dtypes(include=[np.number]).columns if c not in blocked]


def aggregate_subject_features(windows: pd.DataFrame) -> pd.DataFrame:
    if windows.empty:
        return pd.DataFrame()
    features = numeric_feature_columns(windows)
    parts = []
    for subject_id, group in windows.groupby("subject_id"):
        row: dict[str, object] = {"subject_id": subject_id}
        for c in features:
            s = pd.to_numeric(group[c], errors="coerce")
            row[f"{c}__median"] = s.median()
            row[f"{c}__mean"] = s.mean()
            row[f"{c}__std"] = s.std()
            row[f"{c}__p10"] = s.quantile(0.10)
            row[f"{c}__p90"] = s.quantile(0.90)
        parts.append(row)
    return pd.DataFrame(parts)

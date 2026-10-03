from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import rankdata


def _percentile_rank(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    valid = x.notna()
    out = pd.Series(np.nan, index=s.index, dtype=float)
    if valid.any():
        out.loc[valid] = (rankdata(x.loc[valid], method="average") - 1) / max(valid.sum() - 1, 1)
    return out


def score_demo_candidates(subjects: pd.DataFrame) -> pd.DataFrame:
    out = subjects.copy()
    components = []
    for column, weight in [
        ("probability", 0.45),
        ("hba1c", 0.25),
        ("cgm_time_gt_140", 0.15),
        ("cgm_cv", 0.10),
        ("signal_confidence", 0.05),
    ]:
        if column in out.columns:
            rank = _percentile_rank(out[column])
            out[f"candidate_component_{column}"] = rank
            components.append((rank.fillna(0.5), weight))
    if not components:
        out["candidate_score"] = 0.0
        return out
    denom = sum(w for _, w in components)
    out["candidate_score"] = sum(s * w for s, w in components) / denom
    return out.sort_values("candidate_score", ascending=False).reset_index(drop=True)

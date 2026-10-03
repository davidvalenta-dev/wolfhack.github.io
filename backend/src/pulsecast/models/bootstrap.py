from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def bootstrap_subject_auc(subject_predictions: pd.DataFrame, n_boot: int = 2000, seed: int = 42) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    df = subject_predictions[["subject_id", "target", "probability"]].dropna().reset_index(drop=True)
    aucs = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(df), len(df))
        sample = df.iloc[idx]
        if sample["target"].nunique() < 2:
            continue
        aucs.append(roc_auc_score(sample["target"], sample["probability"]))
    if not aucs:
        return {"auc_bootstrap_median": float("nan"), "auc_ci_low": float("nan"), "auc_ci_high": float("nan")}
    return {
        "auc_bootstrap_median": float(np.median(aucs)),
        "auc_ci_low": float(np.quantile(aucs, 0.025)),
        "auc_ci_high": float(np.quantile(aucs, 0.975)),
    }

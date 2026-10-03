from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss
from sklearn.model_selection import LeaveOneGroupOut


@dataclass
class FoldResult:
    subject_id: str
    target: int
    probability: float
    n_windows: int


def leave_one_subject_out_predict(
    estimator,
    windows: pd.DataFrame,
    feature_columns: list[str],
    target_col: str = "target",
    group_col: str = "subject_id",
) -> tuple[pd.DataFrame, list[object]]:
    logo = LeaveOneGroupOut()
    X = windows[feature_columns]
    y = windows[target_col].astype(int).to_numpy()
    groups = windows[group_col].astype(str).to_numpy()
    oof = np.full(len(windows), np.nan, dtype=float)
    models = []
    for train_idx, test_idx in logo.split(X, y, groups):
        model = clone(estimator)
        model.fit(X.iloc[train_idx], y[train_idx])
        oof[test_idx] = model.predict_proba(X.iloc[test_idx])[:, 1]
        models.append(model)
    pred = windows[[group_col, target_col]].copy()
    pred["window_probability"] = oof
    subject = (
        pred.groupby(group_col, as_index=False)
        .agg(
            target=(target_col, "first"),
            probability=("window_probability", "median"),
            probability_mean=("window_probability", "mean"),
            probability_p90=("window_probability", lambda s: s.quantile(0.90)),
            n_windows=("window_probability", "size"),
        )
    )
    return subject, models


def subject_metrics(subject_predictions: pd.DataFrame) -> dict[str, float]:
    y = subject_predictions["target"].astype(int).to_numpy()
    p = subject_predictions["probability"].astype(float).clip(1e-6, 1 - 1e-6).to_numpy()
    out = {
        "subject_log_loss": float(log_loss(y, p, labels=[0, 1])),
        "subject_brier": float(np.mean(np.square(p - y))),
    }
    if len(np.unique(y)) == 2:
        out["subject_roc_auc"] = float(roc_auc_score(y, p))
        out["subject_pr_auc"] = float(average_precision_score(y, p))
    return out

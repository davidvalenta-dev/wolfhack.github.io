from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import confusion_matrix, balanced_accuracy_score


def threshold_metrics(y_true, probabilities, threshold: float = 0.5) -> dict[str, float]:
    y = np.asarray(y_true, dtype=int)
    p = np.asarray(probabilities, dtype=float)
    pred = (p >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "sensitivity": float(tp / (tp + fn)) if tp + fn else np.nan,
        "specificity": float(tn / (tn + fp)) if tn + fp else np.nan,
        "ppv": float(tp / (tp + fp)) if tp + fp else np.nan,
        "npv": float(tn / (tn + fn)) if tn + fn else np.nan,
    }


def phenotype_correlations(subject_predictions: pd.DataFrame) -> dict[str, float]:
    out = {}
    for metric in ["hba1c", "cgm_mean", "cgm_std", "cgm_cv", "cgm_time_gt_140"]:
        if metric not in subject_predictions.columns:
            continue
        clean = subject_predictions[["probability", metric]].dropna()
        if len(clean) < 3:
            continue
        rho, p = spearmanr(clean["probability"], clean[metric])
        out[f"spearman_{metric}"] = float(rho)
        out[f"spearman_{metric}_p"] = float(p)
    return out

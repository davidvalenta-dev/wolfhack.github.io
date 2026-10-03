from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from pulsecast.features.aggregate import numeric_feature_columns
from pulsecast.models.pipeline import build_xgb_pipeline
from pulsecast.models.cv import leave_one_subject_out_predict, subject_metrics
from pulsecast.models.evaluate import threshold_metrics


@dataclass
class TrainingResult:
    model: object
    feature_columns: list[str]
    subject_predictions: pd.DataFrame
    metrics: dict[str, float]


def train_window_model(windows: pd.DataFrame, random_state: int = 42) -> TrainingResult:
    features = numeric_feature_columns(windows)
    blocked = {"signal_confidence"}
    features = [c for c in features if c not in blocked]
    model = build_xgb_pipeline(features, random_state=random_state)
    subject_pred, _ = leave_one_subject_out_predict(model, windows, features)
    metrics = subject_metrics(subject_pred)
    metrics.update(threshold_metrics(subject_pred["target"], subject_pred["probability"]))
    model.fit(windows[features], windows["target"].astype(int))
    return TrainingResult(model=model, feature_columns=features, subject_predictions=subject_pred, metrics=metrics)

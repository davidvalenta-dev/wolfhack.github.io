from __future__ import annotations

import joblib
import pandas as pd

from pulsecast.analysis.cgm_validation import build_cgm_validation_table
from pulsecast.analysis.cohort import cohort_feature_comparison
from pulsecast.config import get_settings
from pulsecast.features.aggregate import aggregate_subject_features
from pulsecast.io.physionet import PhysioNetRepository
from pulsecast.labels.hba1c import build_hba1c_labels
from pulsecast.models.inference import predict_windows
from pulsecast.models.train import train_window_model
from pulsecast.pipeline.build_features import build_all_windows
from pulsecast.risk.candidate import score_demo_candidates
from pulsecast.risk.rolling_score import compute_risk_stream
from pulsecast.risk.trend import annotate_trends


def run_pipeline() -> dict[str, object]:
    s = get_settings()
    repo = PhysioNetRepository(s.data_root)
    labels = build_hba1c_labels(repo.load_demographics(), threshold=s.hba1c_threshold)
    windows = build_all_windows(repo, window_minutes=s.window_minutes, step_minutes=s.step_minutes)
    windows = windows.merge(labels, on="subject_id", how="inner")
    train = train_window_model(windows, random_state=s.random_state)

    pred = predict_windows(train.model, windows, train.feature_columns)
    risk_frames = []
    for subject_id, group in pred.groupby("subject_id"):
        r = compute_risk_stream(group)
        r = annotate_trends(r)
        risk_frames.append(r)
    risk = pd.concat(risk_frames, ignore_index=True)

    subject_windows = aggregate_subject_features(windows)
    comparison = cohort_feature_comparison(subject_windows, labels, top_k=40)
    cgm = build_cgm_validation_table(repo)
    oof = train.subject_predictions.merge(labels, on=["subject_id", "target"], how="left")
    confidence = risk.groupby("subject_id", as_index=False)["signal_confidence"].median()
    summary = oof.merge(cgm, on="subject_id", how="left").merge(confidence, on="subject_id", how="left")
    summary = score_demo_candidates(summary)

    artifact = s.artifact_path
    artifact.mkdir(parents=True, exist_ok=True)
    windows.to_parquet(artifact / "windows.parquet", index=False)
    risk.to_parquet(artifact / "risk.parquet", index=False)
    summary.to_parquet(artifact / "subject_summary.parquet", index=False)
    comparison.to_parquet(artifact / "feature_comparison.parquet", index=False)
    joblib.dump({"model": train.model, "features": train.feature_columns}, artifact / "model.joblib")
    return {"metrics": train.metrics, "summary": summary, "comparison": comparison}


if __name__ == "__main__":
    result = run_pipeline()
    print(result["metrics"])
    print(result["summary"].head(5).to_string(index=False))

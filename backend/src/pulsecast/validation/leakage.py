from __future__ import annotations

import pandas as pd


def assert_subject_disjoint(train: pd.DataFrame, test: pd.DataFrame, subject_col: str = "subject_id") -> None:
    train_ids = set(train[subject_col].astype(str))
    test_ids = set(test[subject_col].astype(str))
    overlap = train_ids & test_ids
    if overlap:
        raise AssertionError(f"Subject leakage detected: {sorted(overlap)}")


def assert_no_cgm_predictors(feature_columns: list[str]) -> None:
    bad = [c for c in feature_columns if any(token in c.lower() for token in ["glucose", "dexcom", "cgm", "hba1c", "a1c"])]
    if bad:
        raise AssertionError(f"Outcome leakage columns present: {bad}")

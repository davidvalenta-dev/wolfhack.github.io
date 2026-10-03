from __future__ import annotations

import pandas as pd


def cohort_feature_comparison(
    subject_features: pd.DataFrame,
    labels: pd.DataFrame,
    top_k: int = 20,
) -> pd.DataFrame:
    joined = subject_features.merge(labels, on="subject_id", how="inner")
    numeric = [c for c in subject_features.columns if c != "subject_id"]
    rows = []
    for c in numeric:
        low = pd.to_numeric(joined.loc[joined["target"] == 0, c], errors="coerce")
        high = pd.to_numeric(joined.loc[joined["target"] == 1, c], errors="coerce")
        pooled = pd.concat([low, high]).std(ddof=1)
        delta = high.median() - low.median()
        effect = delta / pooled if pd.notna(pooled) and pooled > 1e-12 else 0.0
        rows.append({
            "feature": c,
            "normal_median": low.median(),
            "prediabetes_median": high.median(),
            "median_delta": delta,
            "standardized_delta": effect,
            "abs_standardized_delta": abs(effect),
        })
    return pd.DataFrame(rows).sort_values("abs_standardized_delta", ascending=False).head(top_k)

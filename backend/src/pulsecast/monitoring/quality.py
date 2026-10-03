from __future__ import annotations

import pandas as pd


def quality_summary(risk: pd.DataFrame) -> pd.DataFrame:
    return (
        risk.groupby("subject_id", as_index=False)
        .agg(
            median_signal_confidence=("signal_confidence", "median"),
            p10_signal_confidence=("signal_confidence", lambda s: s.quantile(0.10)),
            suppressed_fraction=("suppressed", "mean"),
            observations=("window_end", "size"),
        )
        .sort_values("median_signal_confidence", ascending=False)
    )

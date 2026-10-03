from __future__ import annotations

import pandas as pd
from pulsecast.schemas import SubjectLabel


def build_hba1c_labels(demographics: pd.DataFrame, threshold: float = 5.7) -> pd.DataFrame:
    df = demographics[["subject_id", "hba1c"]].copy()
    df["hba1c"] = pd.to_numeric(df["hba1c"], errors="coerce")
    df = df.dropna(subset=["hba1c"])
    df["target"] = (df["hba1c"] >= threshold).astype(int)
    df["metabolic_class"] = df["target"].map({0: "elevated_normal", 1: "prediabetes"})
    return df.reset_index(drop=True)


def as_models(labels: pd.DataFrame) -> list[SubjectLabel]:
    return [SubjectLabel(**row) for row in labels.to_dict(orient="records")]

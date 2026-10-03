from __future__ import annotations

import numpy as np
import pandas as pd


def require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")


def finite_fraction(df: pd.DataFrame, columns: list[str]) -> float:
    if not columns or df.empty:
        return 0.0
    arr = df[columns].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    return float(np.isfinite(arr).mean())


def safe_records(df: pd.DataFrame) -> list[dict]:
    copy = df.copy()
    for c in copy.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
        copy[c] = copy[c].astype(str)
    return copy.replace({np.nan: None}).to_dict(orient="records")

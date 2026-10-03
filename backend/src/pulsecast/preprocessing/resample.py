from __future__ import annotations

import pandas as pd


def resample_numeric(
    df: pd.DataFrame,
    freq: str,
    columns: list[str] | None = None,
    agg: str = "mean",
) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    columns = columns or [c for c in df.columns if c != "timestamp"]
    indexed = df.set_index("timestamp")[columns]
    if agg == "mean":
        out = indexed.resample(freq).mean()
    elif agg == "median":
        out = indexed.resample(freq).median()
    elif agg == "max":
        out = indexed.resample(freq).max()
    else:
        out = indexed.resample(freq).agg(agg)
    return out.reset_index()


def merge_on_minute(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    merged: pd.DataFrame | None = None
    for name, frame in frames.items():
        if frame.empty:
            continue
        renamed = frame.rename(columns={c: f"{name}_{c}" for c in frame.columns if c != "timestamp"})
        merged = renamed if merged is None else merged.merge(renamed, on="timestamp", how="outer")
    if merged is None:
        return pd.DataFrame(columns=["timestamp"])
    return merged.sort_values("timestamp").reset_index(drop=True)

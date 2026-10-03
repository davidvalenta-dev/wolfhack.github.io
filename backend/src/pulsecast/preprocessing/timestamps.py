from __future__ import annotations

import pandas as pd


def normalize_timestamp(df: pd.DataFrame, column: str = "timestamp") -> pd.DataFrame:
    out = df.copy()
    out[column] = pd.to_datetime(out[column], errors="coerce", utc=True)
    out = out.dropna(subset=[column]).sort_values(column)
    return out.drop_duplicates(subset=[column], keep="last").reset_index(drop=True)


def crop_overlap(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    valid = {k: v for k, v in frames.items() if not v.empty and "timestamp" in v.columns}
    if not valid:
        return frames
    starts = [v["timestamp"].min() for v in valid.values()]
    ends = [v["timestamp"].max() for v in valid.values()]
    start, end = max(starts), min(ends)
    if start >= end:
        return {k: v.iloc[0:0].copy() for k, v in frames.items()}
    return {
        k: v[(v["timestamp"] >= start) & (v["timestamp"] <= end)].copy()
        if "timestamp" in v.columns else v.copy()
        for k, v in frames.items()
    }

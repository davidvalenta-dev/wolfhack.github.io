from __future__ import annotations

from pathlib import Path
from typing import Iterable
import pandas as pd


def read_sensor_csv(path: str | Path, value_columns: Iterable[str] | None = None) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]
    ts_candidates = [c for c in df.columns if c.lower() in {"timestamp", "time", "datetime"}]
    if not ts_candidates:
        raise ValueError(f"No timestamp column in {path}")
    ts_col = ts_candidates[0]
    df["timestamp"] = pd.to_datetime(df[ts_col], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
    if value_columns is not None:
        keep = ["timestamp"] + [c for c in value_columns if c in df.columns]
        df = df[keep]
    return df.reset_index(drop=True)


def read_food_log(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]
    for c in ["time_begin", "time_end"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", utc=True)
    return df

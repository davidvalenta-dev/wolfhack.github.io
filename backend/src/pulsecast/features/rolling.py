from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import numpy as np
import pandas as pd

from pulsecast.features.accel import accel_features
from pulsecast.features.bvp import bvp_features
from pulsecast.features.eda import eda_features
from pulsecast.features.hr import hr_features
from pulsecast.features.ibi import ibi_features
from pulsecast.features.temp import temp_features
from pulsecast.preprocessing.quality import bvp_spectral_quality, motion_score, combined_signal_confidence


@dataclass(frozen=True)
class RollingFeatureConfig:
    window_minutes: int = 15
    step_minutes: int = 5


def _slice(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    if df.empty:
        return df
    return df[(df["timestamp"] > start) & (df["timestamp"] <= end)]


def extract_rolling_features(
    subject_id: str,
    streams: dict[str, pd.DataFrame],
    config: RollingFeatureConfig = RollingFeatureConfig(),
) -> pd.DataFrame:
    nonempty = [v for v in streams.values() if not v.empty and "timestamp" in v.columns]
    if not nonempty:
        return pd.DataFrame()
    start = max(v["timestamp"].min() for v in nonempty) + timedelta(minutes=config.window_minutes)
    end = min(v["timestamp"].max() for v in nonempty)
    if start >= end:
        return pd.DataFrame()
    times = pd.date_range(start=start.ceil(f"{config.step_minutes}min"), end=end, freq=f"{config.step_minutes}min")
    rows: list[dict[str, float | str | pd.Timestamp]] = []
    window_delta = timedelta(minutes=config.window_minutes)
    for t in times:
        ws = t - window_delta
        acc = _slice(streams.get("acc", pd.DataFrame()), ws, t)
        bvp = _slice(streams.get("bvp", pd.DataFrame()), ws, t)
        hr = _slice(streams.get("hr", pd.DataFrame()), ws, t)
        ibi = _slice(streams.get("ibi", pd.DataFrame()), ws, t)
        eda = _slice(streams.get("eda", pd.DataFrame()), ws, t)
        temp = _slice(streams.get("temp", pd.DataFrame()), ws, t)
        row: dict[str, float | str | pd.Timestamp] = {
            "subject_id": subject_id,
            "window_start": ws,
            "window_end": t,
        }
        row.update(accel_features(acc))
        row.update(bvp_features(bvp.get("Value", pd.Series(dtype=float)).to_numpy()))
        row.update(hr_features(hr.get("Value", pd.Series(dtype=float)).to_numpy()))
        row.update(ibi_features(ibi.get("Value", pd.Series(dtype=float)).to_numpy()))
        row.update(eda_features(eda.get("Value", pd.Series(dtype=float)).to_numpy()))
        row.update(temp_features(temp.get("Value", pd.Series(dtype=float)).to_numpy()))
        bq = bvp_spectral_quality(bvp.get("Value", pd.Series(dtype=float)).to_numpy()) if not bvp.empty else 0.0
        ms = motion_score(acc)
        total_expected = config.window_minutes * 60
        hr_missing = 1.0 - min(1.0, len(hr) / max(total_expected, 1))
        row["bvp_quality"] = bq
        row["motion_score"] = ms
        row["signal_confidence"] = combined_signal_confidence(bq, ms, hr_missing)
        rows.append(row)
    return pd.DataFrame(rows)

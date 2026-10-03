from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticSubjectConfig:
    subject_id: str = "999"
    hours: int = 12
    seed: int = 42
    phenotype_strength: float = 0.7


def _time_index(start: str, hz: float, seconds: int) -> pd.DatetimeIndex:
    n = int(seconds * hz)
    return pd.date_range(start, periods=n, freq=pd.to_timedelta(1 / hz, unit="s"), tz="UTC")


def generate_subject(config: SyntheticSubjectConfig) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(config.seed)
    seconds = config.hours * 3600
    start = "2026-01-01T08:00:00"
    hr_t = _time_index(start, 1, seconds)
    phase = np.linspace(0, 8 * np.pi, len(hr_t))
    activity = np.maximum(0, np.sin(phase) + 0.3 * rng.normal(size=len(hr_t)))
    hr = 62 + 13 * activity + 5 * config.phenotype_strength + rng.normal(0, 2, len(hr_t))
    hr_df = pd.DataFrame({"timestamp": hr_t, "Value": hr})

    acc_t = _time_index(start, 32, seconds)
    acc_activity = np.interp(np.arange(len(acc_t)), np.linspace(0, len(acc_t)-1, len(activity)), activity)
    acc = pd.DataFrame({
        "timestamp": acc_t,
        "X": rng.normal(0, 0.02 + 0.08 * acc_activity),
        "Y": rng.normal(0, 0.02 + 0.08 * acc_activity),
        "Z": 1 + rng.normal(0, 0.02 + 0.08 * acc_activity),
    })

    bvp_t = _time_index(start, 64, seconds)
    hr_bvp = np.interp(np.arange(len(bvp_t)), np.linspace(0, len(bvp_t)-1, len(hr)), hr)
    phase_bvp = np.cumsum(2 * np.pi * hr_bvp / 60 / 64)
    bvp = np.sin(phase_bvp) + 0.15 * rng.normal(size=len(bvp_t))
    bvp_df = pd.DataFrame({"timestamp": bvp_t, "Value": bvp})

    eda_t = _time_index(start, 4, seconds)
    eda = 0.7 + 0.2 * config.phenotype_strength + 0.05 * rng.normal(size=len(eda_t))
    eda_df = pd.DataFrame({"timestamp": eda_t, "Value": np.maximum(0, eda)})

    temp_t = _time_index(start, 4, seconds)
    temp = 33.1 + 0.3 * np.sin(np.linspace(0, 2*np.pi, len(temp_t))) + rng.normal(0, 0.05, len(temp_t))
    temp_df = pd.DataFrame({"timestamp": temp_t, "Value": temp})

    ibi_t = hr_t[::2]
    ibi_hr = hr[::2]
    ibi = 60 / ibi_hr + rng.normal(0, 0.025, len(ibi_hr))
    ibi_df = pd.DataFrame({"timestamp": ibi_t, "Value": ibi})

    dex_t = pd.date_range(start, periods=max(2, seconds // 300), freq="5min", tz="UTC")
    dex_phase = np.linspace(0, 6*np.pi, len(dex_t))
    glucose = 102 + 12 * config.phenotype_strength + 18 * np.maximum(0, np.sin(dex_phase)) + rng.normal(0, 4, len(dex_t))
    dex_df = pd.DataFrame({"timestamp": dex_t, "Value": glucose})
    return {"acc": acc, "bvp": bvp_df, "hr": hr_df, "ibi": ibi_df, "eda": eda_df, "temp": temp_df, "dexcom": dex_df}

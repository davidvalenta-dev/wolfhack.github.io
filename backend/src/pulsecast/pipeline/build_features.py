from __future__ import annotations

import pandas as pd
from pulsecast.features.rolling import RollingFeatureConfig, extract_rolling_features
from pulsecast.pipeline.load_subject import load_subject_streams


def build_all_windows(repository, window_minutes: int = 15, step_minutes: int = 5) -> pd.DataFrame:
    frames = []
    cfg = RollingFeatureConfig(window_minutes=window_minutes, step_minutes=step_minutes)
    for subject_id in repository.subjects():
        streams = load_subject_streams(repository, subject_id)
        frame = extract_rolling_features(subject_id, streams, cfg)
        if not frame.empty:
            frames.append(frame)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

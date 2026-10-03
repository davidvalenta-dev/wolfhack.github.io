import numpy as np
import pandas as pd
from pulsecast.risk.rolling_score import ewma_risk, confidence_adjusted_risk, compute_risk_stream
from pulsecast.risk.trend import trend_label, annotate_trends


def test_ewma_is_smooth():
    raw = np.array([0.2, 0.2, 0.9, 0.9])
    smooth = ewma_risk(raw, halflife_windows=2)
    assert smooth[2] < raw[2]
    assert smooth[-1] > smooth[1]


def test_confidence_adjustment_moves_to_half():
    p = confidence_adjusted_risk([0.9], [0.0])
    assert np.isclose(p[0], 0.5)


def test_stream_suppression():
    frame = pd.DataFrame({
        "window_end": pd.date_range("2026-01-01", periods=3, freq="5min", tz="UTC"),
        "raw_probability": [0.2, 0.8, 0.9],
        "signal_confidence": [0.9, 0.2, 0.9],
    })
    out = compute_risk_stream(frame, suppress_below_confidence=0.3)
    assert pd.isna(out.loc[1, "smoothed_probability"])


def test_trend_labels():
    assert trend_label(0.20) == "rising_fast"
    assert trend_label(0.06) == "rising"
    assert trend_label(0.00) == "stable"
    assert trend_label(-0.06) == "falling"

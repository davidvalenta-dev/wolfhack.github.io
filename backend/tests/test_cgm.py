import pandas as pd
from pulsecast.labels.cgm import cgm_metrics, future_rise_labels


def test_cgm_metrics():
    df = pd.DataFrame({"Value": [100, 120, 150, 160]})
    m = cgm_metrics(df)
    assert m["cgm_mean"] == 132.5
    assert m["cgm_time_gt_140"] == 0.5


def test_future_rise_labels():
    ts = pd.date_range("2026-01-01", periods=12, freq="5min", tz="UTC")
    df = pd.DataFrame({"timestamp": ts, "Value": list(range(100, 160, 5))})
    out = future_rise_labels(df, horizon_minutes=30, rise_mg_dl=20)
    assert out["future_rise"].dropna().iloc[0] == 1

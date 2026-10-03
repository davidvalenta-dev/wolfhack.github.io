import numpy as np
import pandas as pd
from pulsecast.features.hr import hr_features
from pulsecast.features.ibi import rmssd, pnn50
from pulsecast.features.accel import accel_features
from pulsecast.features.bvp import bvp_features


def test_hr_features():
    f = hr_features([60, 61, 62, 63, 64])
    assert np.isclose(f["hr_mean"], 62.0)
    assert f["hr_slope"] > 0


def test_rmssd():
    value = rmssd([1.0, 1.1, 1.0, 1.1])
    assert value > 0


def test_pnn50():
    assert pnn50([1.0, 1.1, 1.0]) == 1.0


def test_accel_features():
    frame = pd.DataFrame({"X": [0, 1, 0], "Y": [0, 0, 1], "Z": [1, 1, 1]})
    f = accel_features(frame)
    assert f["acc_mag_mean"] > 0


def test_bvp_features_smoke():
    fs = 64
    t = np.arange(fs * 20) / fs
    signal = np.sin(2 * np.pi * 1.2 * t)
    f = bvp_features(signal, fs=fs)
    assert 1.0 < f["bvp_peak_frequency"] < 1.4

from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks, welch
from scipy.stats import skew, kurtosis
from pulsecast.features.common import finite, safe_mean, safe_std, safe_iqr, quantile, linear_slope


def _peak_rate(x: np.ndarray, fs: float) -> float:
    if x.size < int(fs * 8):
        return np.nan
    distance = max(1, int(fs * 0.30))
    prominence = max(np.std(x) * 0.2, 1e-6)
    peaks, _ = find_peaks(x, distance=distance, prominence=prominence)
    duration_minutes = x.size / fs / 60.0
    return float(len(peaks) / duration_minutes) if duration_minutes > 0 else np.nan


def _spectral_features(x: np.ndarray, fs: float) -> tuple[float, float, float]:
    if x.size < int(fs * 10):
        return np.nan, np.nan, np.nan
    f, pxx = welch(x - np.mean(x), fs=fs, nperseg=min(2048, x.size))
    band = (f >= 0.6) & (f <= 4.0)
    if not band.any():
        return np.nan, np.nan, np.nan
    fb = f[band]
    pb = pxx[band]
    peak_f = float(fb[np.argmax(pb)])
    total = float(np.trapezoid(pxx, f))
    pulse_power = float(np.trapezoid(pb, fb))
    ratio = pulse_power / total if total > 0 else np.nan
    return peak_f, pulse_power, ratio


def bvp_features(values, fs: float = 64.0) -> dict[str, float]:
    x = finite(values)
    if x.size:
        x = x - np.median(x)
    peak_f, pulse_power, band_ratio = _spectral_features(x, fs)
    return {
        "bvp_mean": safe_mean(x),
        "bvp_std": safe_std(x),
        "bvp_iqr": safe_iqr(x),
        "bvp_p05": quantile(x, 0.05),
        "bvp_p95": quantile(x, 0.95),
        "bvp_slope": linear_slope(x),
        "bvp_skew": float(skew(x, bias=False)) if x.size > 8 else np.nan,
        "bvp_kurtosis": float(kurtosis(x, bias=False)) if x.size > 8 else np.nan,
        "bvp_peak_rate": _peak_rate(x, fs),
        "bvp_peak_frequency": peak_f,
        "bvp_pulse_power": pulse_power,
        "bvp_band_power_ratio": band_ratio,
    }

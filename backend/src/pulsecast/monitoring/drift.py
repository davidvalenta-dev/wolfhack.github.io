from __future__ import annotations

import numpy as np
import pandas as pd


def population_stability_index(reference, current, bins: int = 10) -> float:
    ref = pd.to_numeric(pd.Series(reference), errors="coerce").dropna().to_numpy()
    cur = pd.to_numeric(pd.Series(current), errors="coerce").dropna().to_numpy()
    if len(ref) < bins or len(cur) < bins:
        return np.nan
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return 0.0
    r, _ = np.histogram(ref, bins=edges)
    c, _ = np.histogram(cur, bins=edges)
    rp = np.clip(r / max(r.sum(), 1), 1e-6, 1)
    cp = np.clip(c / max(c.sum(), 1), 1e-6, 1)
    return float(np.sum((cp - rp) * np.log(cp / rp)))


def drift_report(reference: pd.DataFrame, current: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for c in columns:
        psi = population_stability_index(reference[c], current[c])
        rows.append({"feature": c, "psi": psi, "drift": bool(np.isfinite(psi) and psi >= 0.2)})
    return pd.DataFrame(rows).sort_values("psi", ascending=False)

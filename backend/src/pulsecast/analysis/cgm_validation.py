from __future__ import annotations

import pandas as pd
from pulsecast.labels.cgm import cgm_metrics


def build_cgm_validation_table(repository) -> pd.DataFrame:
    rows = []
    for subject_id in repository.subjects():
        path = repository.subject_paths(subject_id).sensor("dexcom")
        from pulsecast.io.csv_reader import read_sensor_csv
        d = read_sensor_csv(path, ["Value"])
        row = {"subject_id": subject_id}
        row.update(cgm_metrics(d))
        rows.append(row)
    return pd.DataFrame(rows)

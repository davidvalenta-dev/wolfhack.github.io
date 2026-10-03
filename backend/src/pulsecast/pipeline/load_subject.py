from __future__ import annotations

import pandas as pd
from pulsecast.constants import SENSOR_VALUE_COLUMNS
from pulsecast.io.csv_reader import read_sensor_csv


def load_subject_streams(repository, subject_id: str) -> dict[str, pd.DataFrame]:
    paths = repository.subject_paths(subject_id)
    streams = {}
    for sensor in ["acc", "bvp", "hr", "ibi", "eda", "temp", "dexcom"]:
        path = paths.sensor(sensor)
        streams[sensor] = read_sensor_csv(path, SENSOR_VALUE_COLUMNS.get(sensor))
    return streams

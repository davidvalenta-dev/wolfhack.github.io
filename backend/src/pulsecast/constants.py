from __future__ import annotations

SENSOR_FILES = {
    "acc": "ACC_{subject_id}.csv",
    "bvp": "BVP_{subject_id}.csv",
    "dexcom": "Dexcom_{subject_id}.csv",
    "eda": "EDA_{subject_id}.csv",
    "hr": "HR_{subject_id}.csv",
    "ibi": "IBI_{subject_id}.csv",
    "temp": "TEMP_{subject_id}.csv",
    "food": "Food_Log_{subject_id}.csv",
}

SENSOR_VALUE_COLUMNS = {
    "acc": ["X", "Y", "Z"],
    "bvp": ["Value"],
    "dexcom": ["Value"],
    "eda": ["Value"],
    "hr": ["Value"],
    "ibi": ["Value"],
    "temp": ["Value"],
}

RAW_SAMPLE_RATES_HZ = {
    "acc": 32.0,
    "bvp": 64.0,
    "eda": 4.0,
    "hr": 1.0,
    "temp": 4.0,
}

PREDIABETES_HBA1C_THRESHOLD = 5.7
MAX_HBA1C = 6.4
MIN_HBA1C = 5.2
DEFAULT_WINDOW_MINUTES = 15
DEFAULT_STEP_MINUTES = 5
DEFAULT_RISK_HALFLIFE_WINDOWS = 3.0
DEFAULT_HIGH_RISK_THRESHOLD = 0.70
DEFAULT_LOW_CONFIDENCE_THRESHOLD = 0.45
EPS = 1e-9

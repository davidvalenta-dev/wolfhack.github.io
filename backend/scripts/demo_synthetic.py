from __future__ import annotations

import pandas as pd
from pulsecast.features.rolling import RollingFeatureConfig, extract_rolling_features
from pulsecast.synthetic.generator import SyntheticSubjectConfig, generate_subject

streams = generate_subject(SyntheticSubjectConfig(hours=2))
features = extract_rolling_features("999", streams, RollingFeatureConfig(window_minutes=15, step_minutes=5))
print(features.tail().to_string(index=False))

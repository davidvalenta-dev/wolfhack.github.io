import pandas as pd
from pulsecast.labels.hba1c import build_hba1c_labels


def test_hba1c_threshold():
    df = pd.DataFrame({"subject_id": ["001", "002", "003"], "hba1c": [5.6, 5.7, 6.0]})
    out = build_hba1c_labels(df)
    assert out["target"].tolist() == [0, 1, 1]
    assert out["metabolic_class"].tolist() == ["elevated_normal", "prediabetes", "prediabetes"]

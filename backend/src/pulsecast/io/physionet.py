from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
import pandas as pd

from pulsecast.constants import SENSOR_FILES


@dataclass(frozen=True)
class SubjectPaths:
    subject_id: str
    root: Path

    def sensor(self, sensor: str) -> Path:
        pattern = SENSOR_FILES[sensor]
        return self.root / self.subject_id / pattern.format(subject_id=self.subject_id)


class PhysioNetRepository:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    @property
    def demographics_path(self) -> Path:
        return self.root / "Demographics.csv"

    def subjects(self) -> list[str]:
        ids = []
        for child in self.root.iterdir():
            if child.is_dir() and child.name.isdigit() and len(child.name) == 3:
                ids.append(child.name)
        return sorted(ids)

    def subject_paths(self, subject_id: str) -> SubjectPaths:
        return SubjectPaths(subject_id=subject_id, root=self.root)

    def iter_subject_paths(self) -> Iterator[SubjectPaths]:
        for subject_id in self.subjects():
            yield self.subject_paths(subject_id)

    def load_demographics(self) -> pd.DataFrame:
        df = pd.read_csv(self.demographics_path)
        df.columns = [str(c).strip() for c in df.columns]
        lower = {c.lower(): c for c in df.columns}
        id_col = lower.get("id") or lower.get("subject") or lower.get("subject_id")
        a1c_col = lower.get("hba1c") or lower.get("a1c") or lower.get("hba1c (%)")
        if id_col is None or a1c_col is None:
            raise ValueError(f"Unsupported demographics columns: {df.columns.tolist()}")
        df = df.rename(columns={id_col: "subject_id", a1c_col: "hba1c"})
        df["subject_id"] = df["subject_id"].astype(str).str.extract(r"(\d+)")[0].str.zfill(3)
        df["hba1c"] = pd.to_numeric(df["hba1c"], errors="coerce")
        return df.dropna(subset=["subject_id", "hba1c"]).reset_index(drop=True)

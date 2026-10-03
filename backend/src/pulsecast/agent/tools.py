from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable
import pandas as pd


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    fn: Callable[..., Any]

    def spec(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class DataTools:
    def __init__(self, risk: pd.DataFrame, subject_summary: pd.DataFrame, feature_comparison: pd.DataFrame):
        self.risk = risk.copy()
        self.subject_summary = subject_summary.copy()
        self.feature_comparison = feature_comparison.copy()

    def get_current_risk(self, subject_id: str) -> dict[str, Any]:
        g = self.risk[self.risk["subject_id"].astype(str) == str(subject_id)].sort_values("window_end")
        if g.empty:
            return {"subject_id": subject_id, "status": "missing"}
        row = g.iloc[-1]
        keys = ["window_end", "raw_probability", "smoothed_probability", "signal_confidence", "velocity", "trend"]
        return {k: (row[k].isoformat() if hasattr(row[k], "isoformat") else row[k]) for k in keys if k in row}

    def get_risk_history(self, subject_id: str, n: int = 12) -> list[dict[str, Any]]:
        g = self.risk[self.risk["subject_id"].astype(str) == str(subject_id)].sort_values("window_end").tail(int(n))
        cols = [c for c in ["window_end", "smoothed_probability", "signal_confidence", "velocity", "trend"] if c in g]
        rows = g[cols].copy()
        if "window_end" in rows:
            rows["window_end"] = rows["window_end"].astype(str)
        return rows.to_dict(orient="records")

    def get_subject_summary(self, subject_id: str) -> dict[str, Any]:
        g = self.subject_summary[self.subject_summary["subject_id"].astype(str) == str(subject_id)]
        return g.iloc[0].to_dict() if not g.empty else {"subject_id": subject_id, "status": "missing"}

    def compare_cohorts(self, top_k: int = 10) -> list[dict[str, Any]]:
        return self.feature_comparison.head(int(top_k)).to_dict(orient="records")

    def registry(self) -> dict[str, Tool]:
        return {
            "get_current_risk": Tool(
                "get_current_risk",
                "Return current rolling phenotype-risk estimate and signal confidence.",
                {"type": "object", "properties": {"subject_id": {"type": "string"}}, "required": ["subject_id"]},
                self.get_current_risk,
            ),
            "get_risk_history": Tool(
                "get_risk_history",
                "Return recent rolling risk points for trend analysis.",
                {"type": "object", "properties": {"subject_id": {"type": "string"}, "n": {"type": "integer"}}, "required": ["subject_id"]},
                self.get_risk_history,
            ),
            "get_subject_summary": Tool(
                "get_subject_summary",
                "Return HbA1c, held-out risk, CGM validation metrics, and cohort metadata.",
                {"type": "object", "properties": {"subject_id": {"type": "string"}}, "required": ["subject_id"]},
                self.get_subject_summary,
            ),
            "compare_cohorts": Tool(
                "compare_cohorts",
                "Return wearable metrics with the largest standardized differences between cohorts.",
                {"type": "object", "properties": {"top_k": {"type": "integer"}}},
                self.compare_cohorts,
            ),
        }

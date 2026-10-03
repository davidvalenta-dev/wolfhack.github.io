from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator


class SubjectLabel(BaseModel):
    subject_id: str
    hba1c: float
    metabolic_class: Literal["elevated_normal", "prediabetes"]
    target: int


class WindowKey(BaseModel):
    subject_id: str
    window_start: datetime
    window_end: datetime


class RiskPoint(BaseModel):
    subject_id: str
    timestamp: datetime
    raw_probability: float = Field(ge=0.0, le=1.0)
    smoothed_probability: float = Field(ge=0.0, le=1.0)
    signal_confidence: float = Field(ge=0.0, le=1.0)
    velocity_5m: float = 0.0
    trend: Literal["falling_fast", "falling", "stable", "rising", "rising_fast"]


class ToolCall(BaseModel):
    type: Literal["tool"] = "tool"
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class FinalAnswer(BaseModel):
    type: Literal["final"] = "final"
    content: str


class AgentEnvelope(BaseModel):
    type: Literal["tool", "final"]
    name: str | None = None
    arguments: dict[str, Any] | None = None
    content: str | None = None

    @model_validator(mode="after")
    def validate_shape(self) -> "AgentEnvelope":
        if self.type == "tool" and not self.name:
            raise ValueError("tool envelope requires name")
        if self.type == "final" and not self.content:
            raise ValueError("final envelope requires content")
        return self

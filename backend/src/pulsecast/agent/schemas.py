from __future__ import annotations

from typing import Any
from typing import Literal
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    subject_id: str
    question: str
    max_steps: int = Field(default=6, ge=1, le=12)
    audience: Literal["doctor", "patient"] = "doctor"


class AgentResult(BaseModel):
    answer: str
    tool_trace: list[dict[str, Any]] = Field(default_factory=list)
    model_endpoint: str

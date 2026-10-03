from __future__ import annotations

from functools import lru_cache
import pandas as pd

from pulsecast.agent.client import DatabricksChatClient
from pulsecast.agent.orchestrator import WearableAgent
from pulsecast.agent.tools import DataTools
from pulsecast.config import get_settings


@lru_cache(maxsize=1)
def get_agent() -> WearableAgent:
    settings = get_settings()
    risk = pd.read_parquet(f"{settings.artifact_root}/risk.parquet")
    summary = pd.read_parquet(f"{settings.artifact_root}/subject_summary.parquet")
    comparison = pd.read_parquet(f"{settings.artifact_root}/feature_comparison.parquet")
    tools = DataTools(risk, summary, comparison).registry()
    client = DatabricksChatClient(settings.llm_endpoint)
    return WearableAgent(client, tools)

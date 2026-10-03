from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PULSECAST_", env_file=".env", extra="ignore")

    data_root: str = "/Volumes/wolfhacks/pulsecast/raw"
    artifact_root: str = "/Volumes/wolfhacks/pulsecast/artifacts"
    catalog: str = "wolfhacks"
    schema_name: str = Field(default="pulsecast", alias="schema")
    llm_endpoint: str = "system.ai.claude-sonnet-4-5"
    sql_warehouse_id: str = ""
    window_minutes: int = 15
    step_minutes: int = 5
    hba1c_threshold: float = 5.7
    min_signal_confidence: float = 0.45
    random_state: int = 42
    model_name: str = "metabolic_risk_xgb"

    @property
    def model_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_name}.{self.model_name}"

    @property
    def data_path(self) -> Path:
        return Path(self.data_root)

    @property
    def artifact_path(self) -> Path:
        return Path(self.artifact_root)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

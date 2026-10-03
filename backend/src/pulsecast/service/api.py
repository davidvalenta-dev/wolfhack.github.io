from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pulsecast.agent.orchestrator import WearableAgent
from pulsecast.agent.schemas import AgentRequest, AgentResult
from pulsecast.service.dependencies import get_agent

app = FastAPI(title="PulseCast API", version="0.1.0")
origins = [v.strip() for v in os.environ.get("PULSECAST_ALLOWED_ORIGINS", "").split(",") if v.strip()]
if origins:
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/agent", response_model=AgentResult)
def agent_query(request: AgentRequest, agent: WearableAgent = Depends(get_agent)) -> AgentResult:
    if request.audience == "patient":
        if request.subject_id != "004":
            raise HTTPException(status_code=403, detail="Patient demo is assigned to participant 004")
        scoped = WearableAgent(agent.client, {k: v for k, v in agent.tools.items() if k != "compare_cohorts"})
        return scoped.run(request)
    return agent.run(request)

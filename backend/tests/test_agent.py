import json
import pandas as pd
from pulsecast.agent.orchestrator import WearableAgent
from pulsecast.agent.schemas import AgentRequest
from pulsecast.agent.tools import DataTools


class FakeClient:
    endpoint = "fake"
    def __init__(self):
        self.calls = 0
    def complete(self, messages, max_tokens=700, temperature=0.1):
        self.calls += 1
        if self.calls == 1:
            return json.dumps({"type": "tool", "name": "get_current_risk", "arguments": {}})
        return json.dumps({"type": "final", "content": "The research risk score is elevated."})


def test_agent_tool_loop():
    risk = pd.DataFrame({
        "subject_id": ["001"],
        "window_end": pd.to_datetime(["2026-01-01T00:00:00Z"]),
        "raw_probability": [0.8],
        "smoothed_probability": [0.75],
        "signal_confidence": [0.9],
        "velocity": [0.1],
        "trend": ["rising"],
    })
    summary = pd.DataFrame({"subject_id": ["001"], "hba1c": [5.8]})
    comparison = pd.DataFrame({"feature": ["hr_mean"], "standardized_delta": [0.8]})
    agent = WearableAgent(FakeClient(), DataTools(risk, summary, comparison).registry())
    result = agent.run(AgentRequest(subject_id="001", question="Why?"))
    assert len(result.tool_trace) == 1
    assert "research prototype" in result.answer.lower()

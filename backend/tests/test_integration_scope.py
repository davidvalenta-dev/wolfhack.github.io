import json
from fastapi.testclient import TestClient
from pulsecast.agent.orchestrator import WearableAgent
from pulsecast.agent.schemas import AgentRequest
from pulsecast.agent.tools import Tool
from pulsecast.service.api import app
from pulsecast.service.dependencies import get_agent

class Client:
    endpoint = "test"
    def __init__(self, tool, arguments):
        self.tool, self.arguments, self.calls = tool, arguments, 0
    def complete(self, messages):
        self.calls += 1
        if self.calls == 1:
            return json.dumps({"type": "tool", "name": self.tool, "arguments": self.arguments})
        return json.dumps({"type": "final", "content": "Research result"})

def test_agent_cannot_redirect_subject():
    seen = []
    tool = Tool("get_current_risk", "", {"properties": {"subject_id": {"type": "string"}}}, lambda subject_id: seen.append(subject_id) or {})
    agent = WearableAgent(Client(tool.name, {"subject_id": "016"}), {tool.name: tool})
    agent.run(AgentRequest(subject_id="004", question="Explain"))
    assert seen == ["004"]

def test_cohort_tool_does_not_receive_subject_argument():
    tool = Tool("compare_cohorts", "", {"properties": {"top_k": {"type": "integer"}}}, lambda top_k=10: [])
    result = WearableAgent(Client(tool.name, {}), {tool.name: tool}).run(AgentRequest(subject_id="004", question="Compare"))
    assert result.tool_trace[0]["arguments"] == {}

def test_patient_api_rejects_other_participant():
    app.dependency_overrides[get_agent] = lambda: WearableAgent(Client("", {}), {})
    try:
        response = TestClient(app).post("/agent", json={"subject_id": "016", "audience": "patient", "question": "Explain"})
        assert response.status_code == 403
    finally:
        app.dependency_overrides.clear()

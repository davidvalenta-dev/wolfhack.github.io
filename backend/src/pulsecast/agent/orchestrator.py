from __future__ import annotations

import json
from pydantic import ValidationError

from pulsecast.agent.client import DatabricksChatClient
from pulsecast.agent.guardrails import sanitize_answer
from pulsecast.agent.prompts import SYSTEM_PROMPT, tool_catalog_prompt, subject_context_prompt
from pulsecast.agent.schemas import AgentRequest, AgentResult
from pulsecast.schemas import AgentEnvelope


class WearableAgent:
    def __init__(self, client: DatabricksChatClient, tools: dict):
        self.client = client
        self.tools = tools

    def _specs(self) -> list[dict]:
        return [tool.spec() for tool in self.tools.values()]

    def _parse(self, text: str) -> AgentEnvelope:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.removeprefix("json").strip()
        try:
            return AgentEnvelope.model_validate(json.loads(cleaned))
        except (json.JSONDecodeError, ValidationError):
            return AgentEnvelope(type="final", content=cleaned)

    def run(self, request: AgentRequest) -> AgentResult:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": tool_catalog_prompt(self._specs())},
            {"role": "system", "content": subject_context_prompt(request.subject_id)},
            {"role": "user", "content": request.question},
        ]
        trace = []
        for _ in range(request.max_steps):
            raw = self.client.complete(messages)
            envelope = self._parse(raw)
            if envelope.type == "final":
                return AgentResult(
                    answer=sanitize_answer(envelope.content or ""),
                    tool_trace=trace,
                    model_endpoint=self.client.endpoint,
                )
            name = envelope.name or ""
            if name not in self.tools:
                messages.append({"role": "assistant", "content": raw})
                messages.append({"role": "user", "content": json.dumps({"error": f"unknown tool {name}"})})
                continue
            args = dict(envelope.arguments or {})
            if "subject_id" in self.tools[name].parameters.get("properties", {}):
                args["subject_id"] = request.subject_id
            result = self.tools[name].fn(**args)
            trace.append({"tool": name, "arguments": args, "result": result})
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": "TOOL_RESULT=" + json.dumps(result, default=str)})
        return AgentResult(
            answer=sanitize_answer("Unable to complete the analysis within the configured tool-step limit."),
            tool_trace=trace,
            model_endpoint=self.client.endpoint,
        )

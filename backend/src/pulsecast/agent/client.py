from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from databricks.sdk import WorkspaceClient


class DatabricksChatClient:
    def __init__(self, endpoint: str, workspace: "WorkspaceClient | None" = None):
        self.endpoint = endpoint
        if workspace is None:
            from databricks.sdk import WorkspaceClient
            workspace = WorkspaceClient()
        self.workspace = workspace

    def complete(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 700,
        temperature: float = 0.1,
    ) -> str:
        from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

        role_map = {
            "system": ChatMessageRole.SYSTEM,
            "user": ChatMessageRole.USER,
            "assistant": ChatMessageRole.ASSISTANT,
        }
        mapped = [
            ChatMessage(role=role_map[m["role"]], content=m["content"])
            for m in messages
        ]
        response = self.workspace.serving_endpoints.query(
            name=self.endpoint,
            messages=mapped,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

"""Server-only Gemini adapter for the supplied agent's JSON tool loop."""
import os
import requests

class GeminiClient:
    def __init__(self):
        self.key = os.environ.get("GEMINI_API_KEY", "")
        self.endpoint = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
        if not self.key:
            raise RuntimeError("GEMINI_API_KEY is not configured on the server")

    def complete(self, messages, max_tokens=700, temperature=0.1):
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")
        conversation = "\n".join(m["role"].upper() + ": " + m["content"] for m in messages if m["role"] != "system")
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/interactions",
            headers={"x-goog-api-key": self.key, "Content-Type": "application/json"},
            json={"model": self.endpoint, "system_instruction": system, "input": conversation,
                  "store": False, "generation_config": {"max_output_tokens": max_tokens, "temperature": temperature}},
            timeout=25,
        )
        response.raise_for_status()
        payload = response.json()
        text = payload.get("output_text") or "".join(
            output.get("text", "") if output.get("type") == "text" else
            "".join(part.get("text", "") for part in output.get("content", []) if part.get("type") == "text")
            for output in payload.get("outputs", [])
        )
        if not text:
            raise RuntimeError("The model returned no text")
        return text

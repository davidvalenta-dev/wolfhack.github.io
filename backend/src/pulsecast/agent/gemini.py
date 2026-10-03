"""Server-only Gemini adapter for the supplied agent's JSON tool loop."""
import os
import requests

class GeminiClient:
    def __init__(self):
        self.key = os.environ.get("GEMINI_API_KEY", "")
        self.endpoint = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
        if not self.key:
            raise RuntimeError("GEMINI_API_KEY is not configured on the server")

    def complete(self, messages, max_tokens=700, temperature=0.1):
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")
        contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]} for m in messages if m["role"] != "system"]
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.endpoint}:generateContent",
            headers={"x-goog-api-key": self.key, "Content-Type": "application/json"},
            json={"systemInstruction": {"parts": [{"text": system}]}, "contents": contents,
                  "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature, "responseMimeType": "application/json"}},
            timeout=25,
        )
        response.raise_for_status()
        payload = response.json()
        text = "".join(part.get("text", "") for candidate in payload.get("candidates", [])[:1] for part in candidate.get("content", {}).get("parts", []) if not part.get("thought"))
        if not text:
            raise RuntimeError("The model returned no text")
        return text

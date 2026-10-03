from __future__ import annotations

import requests


class PulseCastClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health(self) -> dict:
        r = requests.get(f"{self.base_url}/health", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def ask(self, subject_id: str, question: str, max_steps: int = 6) -> dict:
        r = requests.post(
            f"{self.base_url}/agent",
            json={"subject_id": subject_id, "question": question, "max_steps": max_steps},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

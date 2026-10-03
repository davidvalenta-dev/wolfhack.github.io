from __future__ import annotations

import re

FORBIDDEN_DIAGNOSTIC_PATTERNS = [
    r"\byou have diabetes\b",
    r"\byou are diabetic\b",
    r"\byou have prediabetes\b",
    r"\bdiagnos(?:e|ed|is)\b",
]


def sanitize_answer(text: str) -> str:
    out = text.strip()
    for pattern in FORBIDDEN_DIAGNOSTIC_PATTERNS:
        out = re.sub(pattern, "the research score is elevated", out, flags=re.IGNORECASE)
    if "research prototype" not in out.lower():
        out += " This is a research prototype score, not a diagnosis."
    return out

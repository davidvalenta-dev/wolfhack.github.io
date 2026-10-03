from __future__ import annotations

from pulsecast.pipeline.end_to_end import run_pipeline

result = run_pipeline()
print(result["metrics"])

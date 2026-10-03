from pulsecast.logging_utils import configure_logging
from pulsecast.pipeline.end_to_end import run_pipeline

configure_logging()
result = run_pipeline()
print(result["metrics"])

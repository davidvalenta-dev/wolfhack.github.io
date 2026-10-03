from __future__ import annotations

import argparse
import time
import pandas as pd
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--speed", type=float, default=120.0)
    args = p.parse_args()
    src = pd.read_parquet(args.input).sort_values("window_end")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    previous = None
    for _, row in src.iterrows():
        current = pd.Timestamp(row["window_end"])
        if previous is not None:
            dt = max(0.0, (current - previous).total_seconds() / args.speed)
            time.sleep(min(dt, 2.0))
        pd.DataFrame([row]).to_json(out, orient="records", lines=True, mode="a")
        previous = current


if __name__ == "__main__":
    main()

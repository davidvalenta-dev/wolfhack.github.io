from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", required=True)
    p.add_argument("--version", default="1.1.3")
    args = p.parse_args()
    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)
    url = f"https://physionet.org/files/big-ideas-glycemic-wearable/{args.version}/"
    subprocess.run(["wget", "-r", "-N", "-c", "-np", "-nH", "--cut-dirs=3", "-P", str(dest), url], check=True)


if __name__ == "__main__":
    main()

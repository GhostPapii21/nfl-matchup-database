#!/usr/bin/env python3
"""Poll CHI@DET official inactives until both clubs OK or near kickoff."""
from __future__ import annotations

import datetime as dt
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEADLINE = dt.datetime(2026, 11, 26, 17, 55, tzinfo=dt.timezone.utc)
OUT = Path(__file__).resolve().parent / "CHI_DET_inactives_poll.log"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    while dt.datetime.now(tz=dt.timezone.utc) < DEADLINE:
        now = dt.datetime.now(tz=dt.timezone.utc).isoformat()
        r = subprocess.run(
            ["python3", "-m", "phase15.official_inactives", "--game", "2026_12_CHI_DET"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        text = (r.stdout or "") + (r.stderr or "")
        line = f"{now} exit={r.returncode}\n{text}\n"
        with OUT.open("a") as f:
            f.write(line)
        print(line, flush=True)
        if "CHI: OK" in text and "DET: OK" in text and "INCOMPLETE" not in text:
            print("BOTH_OK", flush=True)
            return 0
        if "CHI: OK" in text:
            print("CHI_OK_DETECTED", flush=True)
            return 0
        time.sleep(90)
    print("POLL_DONE", dt.datetime.now(tz=dt.timezone.utc).isoformat(), flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

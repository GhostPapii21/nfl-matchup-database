"""Shared fixtures for the postgame grading audit tests. Read-only: nothing here writes inside the repository."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
for p in (str(ROOT), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

GAME = "2026_12_DEN_PIT"
RUN_DIR = ROOT / "runs" / "2026-11-27_DEN@PIT"
ESPN_FINAL = RUN_DIR / "pbp" / "summary_FINAL.json"
LOCK_DIR = ROOT / "snapshots" / GAME / "20261127T111648Z"
PACKET_REL = f"pregame/packets/{GAME}/packet.json"
FIXED_NOW = datetime(2026, 11, 28, 1, 0, tzinfo=timezone.utc)


def git_history_available() -> bool:
    """CI checks out with depth 1; tests that walk packet history skip there instead of failing."""
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "log", "--format=%H", "--", PACKET_REL],
                             capture_output=True, text=True, check=True).stdout.split()
    except Exception:
        return False
    return len(out) >= 2


def denpit_actuals():
    """ESPNActuals built from the FINAL ESPN summary committed in PR #146 (no network)."""
    from grading import espn as E
    d = json.loads(ESPN_FINAL.read_text())
    rec = {"url": str(ESPN_FINAL.relative_to(ROOT)), "retrieved_utc": "2026-11-27T23:06:58+00:00",
           "sha256_full_response": "unknown", "header": d["header"], "boxscore": d["boxscore"]}
    return E.ESPNActuals(GAME, rec, str(ESPN_FINAL.relative_to(ROOT)))

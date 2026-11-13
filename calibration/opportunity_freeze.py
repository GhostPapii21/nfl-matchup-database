"""NFL-75 Phase 2: holdout freeze manifest for the opportunity model (Ghost6 review item: freeze before W10-12).

Before ANY Weeks 10-12 grading of the opportunity model, the exact model code and the frozen parameters must be
recorded in a committed manifest:

    python3 -m calibration.opportunity_freeze freeze       # writes HOLDOUT_MANIFEST (then commit it)
    python3 -m calibration.opportunity_freeze check 10     # exit 0 only if code + params match the manifest

`check_freeze(week)` is called first by calibration/opportunity_holdout_grade.py and refuses (raises FreezeError) if
the manifest is absent, the week is not covered, or any recorded code file / params file sha256 differs. Any change to
the model (e.g. new depth signals) therefore needs a NEW freeze, committed before Weeks 10-12 actuals are read.

Params for Weeks 10, 11 and 12 are all the Week-10 fit (2024-2025 + 2026 Weeks 1-9): no Week >= 10 data is read to
fit anything. Candidate lists for a holdout game are still built point in time at grading (prior weeks' PBP,
that week's injury report and pre-game-day depth chart). This module never reads Week 10-12 actuals.
Research only. projection_ready stays false."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Phase 2b (refs NFL-75): the frozen holdout model is now the Phase 2b model (depth signal + opt-in INT pooling).
# The Phase 2 manifest (research/runs/2026-11-13_opportunity_phase2/holdout_freeze_manifest.json, model b6e955c)
# is superseded (marked status SUPERSEDED in the file): its code hashes no longer match (simulate.py, opportunity_fit.py
# and opportunity_backtest.py changed), so it would refuse.
RUN = ROOT / "research/runs/2026-11-13_opportunity_phase2b"
HOLDOUT_MANIFEST = RUN / "holdout_freeze_manifest.json"
HOLDOUT_WEEKS = (10, 11, 12)
CODE_FILES = ("core/possession_engine_v0/opportunity.py", "core/possession_engine_v0/player_box.py",
              "core/possession_engine_v0/simulate.py", "core/possession_engine_v0/state.py",
              "calibration/opportunity_fit.py", "calibration/opportunity_backtest.py",
              "calibration/opportunity_report.py",
              "core/possession_engine_v0/int_pool.py", "calibration/opportunity_intcap.py",
              "calibration/opportunity_fit2b.py", "calibration/opportunity_report_2b.py",
              "data/historical/nflverse/derived_pit/depth_skill_snapshots_2025_2026.csv.gz",
              "research/runs/2026-11-13_opportunity_phase2b/int_pool/int_pool_2026_w10.json")  # INT-pool spec (W10 fit)
PARAMS = {w: "research/runs/2026-11-13_opportunity_phase2b/params/params_2026_w10.json" for w in HOLDOUT_WEEKS}


class FreezeError(RuntimeError):
    pass


def _sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build_manifest(root: Path = ROOT) -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *CODE_FILES, *set(PARAMS.values())], cwd=root,
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        raise FreezeError(f"refuse to freeze uncommitted model code/params:\n{dirty}")
    params = {str(w): {"path": p, "sha256": _sha(root / p)} for w, p in PARAMS.items()}
    for w, p in PARAMS.items():
        meta = json.loads((root / p).read_text())
        if meta["data_max_week_used"]["season"] != 2026 or meta["data_max_week_used"]["week"] >= 10:
            raise FreezeError(f"params for week {w} were fit with data from week >= 10")
    ip = json.loads((root / CODE_FILES[-1]).read_text())
    if ip["meta"]["eval_week"] != 10 or "weeks 4..9" not in ip["meta"]["fitted_on"]:
        raise FreezeError("INT-pool spec must be the week-10 fit on data through week 9")
    return {"schema": "nfl75-opportunity-holdout-freeze/1", "model_commit": head, "model": "phase2b",
            "frozen_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "holdout_weeks": list(HOLDOUT_WEEKS), "params": params,
            "code_sha256": {f: _sha(root / f) for f in CODE_FILES},
            "data_max_week_used_for_fit": {"season": 2026, "week": 9},
            "rule": "grading of weeks 10-12 refuses unless every code/params sha256 here matches the tree",
            "week10_note": "W10 TNF (WAS@NYG, Nov 12) was already played when this was frozen; its actuals were "
                           "never read by the fit or this manifest", "projection_ready": False}


def check_freeze(week: int, root: Path = ROOT, manifest: Path | None = None) -> dict:
    mp = manifest or (root / HOLDOUT_MANIFEST.relative_to(ROOT))
    if not mp.exists():
        raise FreezeError(f"no holdout freeze manifest at {mp}; freeze and commit before grading weeks 10-12")
    m = json.loads(mp.read_text())
    if int(week) not in m.get("holdout_weeks", []):
        raise FreezeError(f"week {week} is not covered by the freeze manifest")
    bad = [f for f, h in m["code_sha256"].items() if not (root / f).exists() or _sha(root / f) != h]
    p = m["params"].get(str(int(week)))
    if p is None or not (root / p["path"]).exists() or _sha(root / p["path"]) != p["sha256"]:
        bad.append(p["path"] if p else f"params week {week}")
    if bad:
        raise FreezeError(f"model/params differ from the freeze manifest ({m['model_commit'][:7]}): {bad}; re-freeze")
    return m


if __name__ == "__main__":
    if sys.argv[1:2] == ["freeze"]:
        HOLDOUT_MANIFEST.write_text(json.dumps(build_manifest(), indent=1) + "\n")
        print("wrote", HOLDOUT_MANIFEST)
    elif sys.argv[1:2] == ["check"]:
        print(json.dumps(check_freeze(int(sys.argv[2]))["model_commit"]))
    else:
        raise SystemExit("usage: freeze | check WEEK")

"""NFL-75 Phase 4: freeze manifest for the selective-edge classifier.

    python3 -m calibration.selective_edge_run fit          # writes PARAMS_FILE from Weeks 4-7 only (commit it)
    python3 -m calibration.selective_edge_freeze freeze    # writes MANIFEST (commit it BEFORE scoring Weeks 8-9)
    python3 -m calibration.selective_edge_freeze check 10  # exit 0 only if code + params match the manifest

Weeks 8-9 evaluation (`selective_edge_run eval`) and Weeks 10-12 live grading (`selective_edge_live`) both call
`verify_hashes` / `check_freeze` first and refuse on any difference. Any change to the classifier needs a new fit on
Weeks 4-7 and a new freeze. Research only; projection_ready stays false."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "research/runs/2026-11-13_selective_edge_phase4"
MANIFEST = RUN / "freeze_manifest.json"
PARAMS_FILE = "research/runs/2026-11-13_selective_edge_phase4/params_w4_7.json"
CODE_FILES = ("calibration/selective_edge.py", "calibration/selective_edge_live.py",
              "calibration/selective_edge_run.py", "calibration/selective_edge_freeze.py")  # checker hashes itself
FIT_WEEKS, EVAL_WEEKS, HOLDOUT_WEEKS = (4, 5, 6, 7), (8, 9), (10, 11, 12)


class FreezeError(RuntimeError):
    pass


def sha256(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build_manifest(root: Path = ROOT, inputs: dict | None = None) -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *CODE_FILES, PARAMS_FILE], cwd=root,
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        raise FreezeError(f"refuse to freeze uncommitted classifier code/params:\n{dirty}")
    params = json.loads((root / PARAMS_FILE).read_text())
    if params.get("train_weeks") != list(FIT_WEEKS):
        raise FreezeError(f"params were not fit on Weeks 4-7 only: {params.get('train_weeks')}")
    return {"schema": "nfl75-selective-edge-freeze/1", "classifier_commit": head,
            "frozen_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fit_weeks": list(FIT_WEEKS), "eval_weeks": list(EVAL_WEEKS), "holdout_weeks": list(HOLDOUT_WEEKS),
            "params": {"path": PARAMS_FILE, "sha256": sha256(root / PARAMS_FILE)},
            "code_sha256": {f: sha256(root / f) for f in CODE_FILES},
            "inputs_sha256": inputs or {},
            "rule": "Weeks 8-9 eval and Weeks 10-12 live grading refuse unless every code/params sha256 matches",
            "projection_ready": False}


def verify_hashes(root: Path = ROOT, manifest: Path | None = None) -> dict:
    mp = manifest or (root / MANIFEST.relative_to(ROOT))
    if not mp.exists():
        raise FreezeError(f"no freeze manifest at {mp}; fit W4-7, freeze and commit first")
    m = json.loads(mp.read_text())
    bad = [f for f, h in m["code_sha256"].items() if not (root / f).exists() or sha256(root / f) != h]
    p = m["params"]
    if not (root / p["path"]).exists() or sha256(root / p["path"]) != p["sha256"]:
        bad.append(p["path"])
    if bad:
        raise FreezeError(f"classifier/params differ from the freeze manifest ({m['classifier_commit'][:7]}): {bad}")
    return m


def check_freeze(week: int, root: Path = ROOT, manifest: Path | None = None) -> dict:
    mp = manifest or (root / MANIFEST.relative_to(ROOT))
    if not mp.exists():
        raise FreezeError(f"no freeze manifest at {mp}; fit W4-7, freeze and commit first")
    m = json.loads(mp.read_text())
    if int(week) not in m.get("holdout_weeks", []) + m.get("eval_weeks", []):
        raise FreezeError(f"week {week} is not covered by the freeze manifest")
    return verify_hashes(root, mp)


def load_params(root: Path = ROOT) -> dict:
    return json.loads((root / PARAMS_FILE).read_text())


if __name__ == "__main__":
    if sys.argv[1:2] == ["freeze"]:
        inputs = json.loads(Path(sys.argv[2]).read_text()) if len(sys.argv) > 2 else {}
        MANIFEST.write_text(json.dumps(build_manifest(inputs=inputs), indent=1) + "\n")
        print("wrote", MANIFEST, sha256(MANIFEST))
    elif sys.argv[1:2] == ["check"]:
        print(check_freeze(int(sys.argv[2]))["classifier_commit"])
    else:
        raise SystemExit("usage: freeze [inputs.json] | check WEEK")

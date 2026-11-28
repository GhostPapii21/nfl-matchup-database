"""Public sim_v6 contract for the Sunday run.

The recovered algorithm is ``tools/sim_v6_historical.py`` (blob
``ab2144f03f6ca3b57950a1f2528e305193e723cd``). It samples three methods,
``mc``, ``bias``, and ``gr``. It does not take the three game scripts. This
module refuses a 3 x 3 x 100000 claim instead of running a smaller count or
another engine under that name.

Bias stays refused unless a calibration artifact carries a dated holdout or
walk-forward scorecard. A missing artifact is not replaced with multiplier 1.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

BLOB = "ab2144f03f6ca3b57950a1f2528e305193e723cd"
METHODS = ("mc", "bias", "gr")
SCRIPTS = ("favorite_controls", "competitive", "underdog_chases")
TRIALS = 100_000
HISTORICAL = Path(__file__).with_name("sim_v6_historical.py")


def historical_sha256() -> str | None:
    try:
        return hashlib.sha256(HISTORICAL.read_bytes()).hexdigest()
    except OSError:
        return None


def bias_status(calib: dict | None) -> dict:
    """Refuse Bias when the calibration cannot support a non-neutral multiplier."""
    if not isinstance(calib, dict) or not calib:
        return {
            "status": "REFUSED",
            "calibration_status": "MISSING",
            "multiplier_applied": None,
            "reason": "Bias calibration artifact is missing. No neutral multiplier was applied.",
        }
    scorecard = calib.get("holdout_scorecard") or calib.get("walk_forward")
    if not isinstance(scorecard, dict) or not scorecard.get("as_of"):
        return {
            "status": "REFUSED",
            "calibration_status": "EXPERIMENTAL_UNVALIDATED",
            "multiplier_applied": None,
            "reason": "Bias calibration has no dated holdout or walk-forward scorecard. The fitted multiplier was not applied.",
        }
    return {
        "status": "READY",
        "calibration_status": "HOLDOUT_PRESENT",
        "multiplier_applied": None,
        "reason": "A dated scorecard is present. This contract still does not run Bias inside a script cell.",
    }


def acceptance_receipt() -> dict:
    """The nine-cell 100k script run. Refused when the recovered engine has no script axis."""
    text = HISTORICAL.read_text() if HISTORICAL.is_file() else ""
    methods_present = [name for name in METHODS if f"'{name}'" in text or f'"{name}"' in text]
    scripts_present = [name for name in SCRIPTS if name in text]
    refused = len(scripts_present) != len(SCRIPTS) or len(methods_present) != len(METHODS)
    return {
        "schema": "sim-v6-acceptance-receipt/1",
        "engine_id": "sim_v6",
        "entrypoint": "tools/sim_v6.py",
        "recovered_file": "tools/sim_v6_historical.py",
        "provenance_blob": BLOB,
        "recovered_sha256": historical_sha256(),
        "methods": list(METHODS),
        "methods_in_recovered_source": methods_present,
        "scripts": list(SCRIPTS),
        "scripts_in_recovered_source": scripts_present,
        "trials_required_per_cell": TRIALS,
        "cells_required": len(METHODS) * len(SCRIPTS),
        "trials_required": TRIALS * len(METHODS) * len(SCRIPTS),
        "trials_executed": 0,
        "status": "REFUSED" if refused else "NOT_RUN",
        "fallback_used": False,
        "not_used": [
            "pipeline.sim100k",
            "core.possession_engine_v0",
            "core.period_engine_v0",
            "calibration.simv56",
        ],
        "bias": bias_status(None),
        "projection_ready": False,
        "reason": (
            "The recovered sim_v6 source has mc, bias, and gr and no game-script argument. "
            "Three methods times three scripts at 100000 trials were not run. "
            "The count was not reduced, and no other engine was labeled sim_v6."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(acceptance_receipt(), indent=2))

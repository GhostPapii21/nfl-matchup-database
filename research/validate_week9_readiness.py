#!/usr/bin/env python3
"""Integrity/fail-closed audit for the frozen Week 9 research snapshot."""
import csv
import hashlib
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "research" else SCRIPT_DIR
RESEARCH = ROOT / "research"
LOCK = RESEARCH / "WEEK9_PROSPECTIVE_EVAL_LOCK_20261108_0856ET.json"
SNAPSHOT = RESEARCH / "WEEK9_READINESS_SNAPSHOT_20261108_0856ET.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    assert len(snapshot["phases"]) == 15, "phase ledger must enumerate all 15 phases"
    assert [row["phase"] for row in snapshot["phases"]] == list(range(1, 16)), "phase IDs must be complete and ordered"
    assert snapshot["readiness"]["projection_ready"] is False, "this snapshot is not production accepted"
    assert snapshot["readiness"]["full_integration_acceptance"] is False, "do not promote a partial audit"
    assert snapshot["readiness"]["calibration_status"] == "PROSPECTIVE_LOCKED_OUTCOMES_PENDING"
    assert lock["calibration_claim"] is False
    assert lock["status"] == "FROZEN_PENDING_OUTCOMES"

    for item in lock["artifacts"]:
        path = ROOT / item["path"]
        assert path.is_file(), f"missing frozen artifact: {item['path']}"
        actual = sha256(path)
        assert actual == item["sha256"], f"hash mismatch: {item['path']} expected {item['sha256']} got {actual}"

    simulation = RESEARCH / "WEEK9_DAY1_MODEL_SIMULATION_20261108.csv"
    with simulation.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == lock["forecast_population"]["simulation_rows"] == 471
    assert {r["model"] for r in rows} == set(lock["forecast_population"]["models"])
    assert {int(r["simulations"]) for r in rows} == {100000}
    assert len({(r["player"], r["market"], r["book"], r["line"]) for r in rows}) == 157
    assert not any(r["kickoff_et"] == "9:30 AM ET" for r in rows), "9:30 game is intentionally out of current simulation coverage"

    overlay = RESEARCH / "WEEK9_DAY1_REFRESHED_PROJECTION_OVERLAY_20261108_0823ET.csv"
    with overlay.open(newline="", encoding="utf-8") as stream:
        overlay_rows = list(csv.DictReader(stream))
    exact = sum(str(r["exact_threshold"]).lower() == "true" for r in overlay_rows)
    assert exact == lock["forecast_population"]["exact_threshold_current_line_rows"] == 139
    assert len(overlay_rows) - exact == lock["forecast_population"]["changed_threshold_rows_unscorable"] == 18

    print("PASS: 15 phase IDs, frozen artifact hashes, 471 x 100000 simulations, 157 lines, and 139 exact-threshold rows verified.")
    print("FAIL-CLOSED: production readiness and calibration remain false; outcomes are pending; CIN-ATL 09:30 is uncovered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

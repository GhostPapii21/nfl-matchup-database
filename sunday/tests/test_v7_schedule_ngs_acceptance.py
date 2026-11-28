"""Regression tests for sourced kickoff, optional aggregate NGS, and V7-only acceptance."""
import json
from pathlib import Path

from sunday.kickoff import nfl_official_kickoff, resolve
from sunday.ngs_verify import verify
from sunday.stack import ORDER, acceptance_result


def test_official_schedule_capture_is_authoritative(tmp_path):
    dest = tmp_path / "data/schedule/nfl_official_schedule.json"
    dest.parent.mkdir(parents=True)
    dest.write_text(json.dumps({
        "source": "https://www.nfl.com/schedules/2026/by-week/week-12",
        "retrieved_utc": "2026-11-28T06:15:09Z",
        "as_of": "2026-11-28T06:15:09Z",
        "games": {"2026_12_NO_CIN": "2026-11-29T18:00:00Z"}
    }))
    row = nfl_official_kickoff(tmp_path, "2026_12_NO_CIN")
    assert row["status"] == "OK"
    assert row["kickoff_utc"].isoformat() == "2026-11-29T18:00:00+00:00"
    out = resolve(tmp_path, "2026_12_NO_CIN")
    assert out["verification"] == "VERIFIED"
    assert out["capture_before_this_kickoff"] is True


def test_ngs_aggregate_does_not_require_charts(tmp_path):
    import pandas as pd
    from sunday.ngs_verify import FILES
    for path in FILES.values():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame([{"season": 2026, "week": 9}]).to_csv(target, index=False, compression="gzip")
    out = verify(tmp_path)
    assert out["aggregate_usable"] is True
    assert out["chart_images_required_for_aggregates"] is False
    assert "route" in out["unavailable_play_level_fields"]
    assert out["certification"] is False


def test_legacy_refusal_not_disguised_or_required_for_v7():
    rows = [{"id": x, "kind": "analytical", "status": "EXECUTED",
             "analytical_execution": True} for x in ORDER]
    rows[0]["kind"] = "identity"
    rows[4].update(status="REFUSED", analytical_execution=False, required_for_v7=False)
    rows[6].update(status="REFUSED", analytical_execution=False, required_for_v7=False)
    assert acceptance_result(rows) == "PASS"
    rows[5]["status"] = "FAILED"
    assert acceptance_result(rows) == "PARTIAL"
    rows[5]["status"] = "EXECUTED"
    rows[0]["status"] = "BLOCKED"
    assert acceptance_result(rows) == "BLOCKED"

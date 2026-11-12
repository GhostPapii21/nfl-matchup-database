"""rocket: fail-closed behaviour of each check (pytest suites skipped here to avoid recursion)."""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from rocket_gate import cli


def test_repo_as_committed_passes_r2_after_nfl43_review_accepted():
    """NFL-43 bounds accepted at 32b9b92 (Nov 12 ~3:05 PM ET): R2 passes; rocket still never sets projection_ready."""
    r = cli.run(None, skip_pytest=True)
    by = {c["check"]: c for c in r["checks"]}
    assert by["R1_nfl42_entrypoint"]["status"] == "PASS" and by["R3_safety"]["status"] == "PASS"
    assert by["R2_nfl43_semantics"]["status"] == "PASS"
    assert r["projection_ready"] is False


def _accepted_repo(tmp_path, review="ACCEPTED", edit=False):
    import hashlib
    root = _fake_repo(tmp_path)
    (root / "known_flags/KNOWN_LIMITATIONS.json").write_text(json.dumps(
        {"projection_ready": False, "unsupported_semantics": [], "DEFERRED_100K": False,
         "nfl43": {"still_unsupported": [
             "kick-play fouls", "joint_producer penalties/return yards", "blocked kicks/onside/fakes"]}}))
    b = root / "core/possession_engine_v0/SEMANTICS_BOUNDS.md"
    b.write_text("bounds v1")
    (root / "core/possession_engine_v0/semantics.py").write_text("official_2025_regular_season")
    (root / "known_flags/NFL43_REVIEW.json").write_text(json.dumps(
        {"status": review, "accepted_bounds_sha256": hashlib.sha256(b"bounds v1").hexdigest()}))
    if edit:
        b.write_text("bounds v2")
    return root


def test_r2_passes_only_when_review_accepted_for_current_bounds(tmp_path):
    r = cli.r2_semantics(_accepted_repo(tmp_path / "ok"))
    assert r["status"] == "PASS"
    assert r["detail"]["still_unsupported"] == [
        "kick-play fouls", "joint_producer penalties/return yards", "blocked kicks/onside/fakes"]
    assert cli.r2_semantics(_accepted_repo(tmp_path / "pend", review="PENDING"))["status"] == "FAIL"
    assert cli.r2_semantics(_accepted_repo(tmp_path / "edit", edit=True))["status"] == "FAIL"


def test_r2_fails_when_still_unsupported_missing(tmp_path):
    root = _accepted_repo(tmp_path)
    (root / "known_flags/KNOWN_LIMITATIONS.json").write_text(json.dumps(
        {"projection_ready": False, "unsupported_semantics": [], "DEFERRED_100K": False}))
    r = cli.r2_semantics(root)
    assert r["status"] == "FAIL"
    assert any("STILL_UNSUPPORTED" in str(x) or "still_unsupported" in str(x) for x in r["detail"])


def test_r2_fails_when_a_config_enables_still_unsupported(tmp_path):
    root = _accepted_repo(tmp_path)
    d = root / "core/possession_engine_v0/config"
    d.mkdir(parents=True, exist_ok=True)
    (d / "bad.json").write_text(json.dumps({
        "config_id": "bad", "semantics": {"penalties": "canonical_log_v1", "kick_play_fouls": True}
    }))
    r = cli.r2_semantics(root)
    assert r["status"] == "FAIL"
    blob = json.dumps(r["detail"])
    assert "kick-play fouls" in blob and "STILL_UNSUPPORTED" in blob


def test_r5_flags_locks_made_before_review(tmp_path):
    locks = sorted((ROOT / "snapshots").glob("*/*/LOCK.json"))
    if not locks:
        import pytest
        pytest.skip("no locked snapshot in repo")
    gid = locks[-1].parent.parent.name
    r = cli.r5_snapshot(gid)
    assert r["status"] == "FAIL"
    assert any("KNOWN_MODEL_ERROR_UNREVIEWED_BOUNDS" in p for p in r["detail"]["problems"])


def test_skip_pytest_can_never_exit_zero():
    assert cli.main(["--skip-pytest"]) == 1


def test_missing_snapshot_fails():
    r = cli.r5_snapshot("2026_99_XXX_YYY")
    assert r["status"] == "FAIL" and "no snapshots" in r["detail"]


def _fake_repo(tmp_path):
    for rel in ("known_flags", "core/possession_engine_v0", "pregame/packets/G", "snapshots", "phase15"):
        (tmp_path / rel).mkdir(parents=True, exist_ok=True)
    (tmp_path / "known_flags/KNOWN_LIMITATIONS.json").write_text(json.dumps({"projection_ready": False, "unsupported_semantics": []}))
    (tmp_path / "pregame/packets/G/packet.json").write_text(json.dumps({"projection_ready": False}))
    return tmp_path


def test_projection_ready_true_anywhere_fails(tmp_path):
    root = _fake_repo(tmp_path)
    assert cli.r3_safety(root)["status"] == "PASS"
    (root / "pregame/packets/G/packet.json").write_text(json.dumps({"projection_ready": True}))
    assert cli.r3_safety(root)["status"] == "FAIL"


def test_money_keys_fail(tmp_path):
    root = _fake_repo(tmp_path)
    (root / "snapshots/x.json").write_text(json.dumps({"stake": 5}))
    assert cli.r3_safety(root)["status"] == "FAIL"


def test_semantics_unsupported_fails(tmp_path):
    root = _fake_repo(tmp_path)
    (root / "known_flags/KNOWN_LIMITATIONS.json").write_text(json.dumps({"projection_ready": False, "unsupported_semantics": ["penalties"]}))
    assert cli.r2_semantics(root)["status"] == "FAIL"


def test_tampered_snapshot_fails(tmp_path):
    locks = sorted((ROOT / "snapshots").glob("*/*/LOCK.json"))
    if not locks:
        import pytest
        pytest.skip("no locked snapshot in repo yet")
    src = locks[-1].parent
    gid = src.parent.name
    root = _fake_repo(tmp_path)
    dst = root / "snapshots" / gid / src.name
    shutil.copytree(src, dst)
    # git ancestry is checked against the real repo HEAD, so only test the hash path here
    (dst / "summary.json").write_text("{}")
    r = cli.r5_snapshot(gid, root)
    assert r["status"] == "FAIL" and any("hash mismatch" in p for p in r["detail"]["problems"])


def test_r3_rejects_player_numbers_in_snapshot(tmp_path):
    from rocket_gate.cli import r3_safety
    (tmp_path / "known_flags").mkdir()
    (tmp_path / "known_flags/KNOWN_LIMITATIONS.json").write_text(json.dumps({"projection_ready": False}))
    d = tmp_path / "snapshots/G/20260101T000000Z"
    (d / "inputs").mkdir(parents=True)
    (d / "LOCK.json").write_text(json.dumps({"projection_ready": False}))
    (d / "summary.json").write_text(json.dumps({"n": 1}))
    (d / "inputs/team_prices.json").write_text(json.dumps({"meta": {}, "rows": [{"market": "h2h", "player": None}]}))
    assert r3_safety(tmp_path)["status"] == "PASS"
    (d / "inputs/team_prices.json").write_text(json.dumps({"rows": [{"market": "player_rush_yds", "player": "X"}]}))
    assert r3_safety(tmp_path)["status"] == "FAIL"
    (d / "inputs/team_prices.json").unlink()
    (d / "summary.json").write_text(json.dumps({"player_mean_yards_top": {}}))
    assert r3_safety(tmp_path)["status"] == "FAIL"


def test_r1_passes_on_repo_and_reports_g0_enforcement():
    r = cli.r1_entrypoint()
    assert r["status"] == "PASS" and r["detail"]["enforced_g0"] == "OK"


def test_r1_fails_when_entrypoint_enforcement_fails(monkeypatch):
    sys.path.insert(0, str(cli.ROOT))
    from pipeline import hooks
    monkeypatch.setattr(hooks, "nfl42_entrypoint", lambda *a, **k: {"status": "FAILED", "reason": "deny list empty"})
    r = cli.r1_entrypoint()
    assert r["status"] == "FAIL" and r["detail"]["enforced_g0"]["status"] == "FAILED"

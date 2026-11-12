"""rocket: fail-closed behaviour of each check (pytest suites skipped here to avoid recursion)."""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from rocket_gate import cli


def test_repo_checks_pass_in_selftest_mode():
    r = cli.run(None, skip_pytest=True)
    assert r["status"] == "PASS_SELFTEST", r
    assert r["projection_ready"] is False


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

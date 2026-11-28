"""`python -m sunday sim`: fails closed without calibration or validation, never claims sim_v6 for the replacement,
and writes only under its output directory."""
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from sunday import cli, sim_triad

ROOT = Path(__file__).resolve().parents[2]


def test_missing_calibration_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(sim_triad, "CALIB_R1", tmp_path / "absent.json")
    with pytest.raises(sim_triad.Blocked):
        sim_triad.load_calib(sim_triad.CALIB_R1)


def test_missing_validation_blocks(tmp_path):
    with pytest.raises(sim_triad.Blocked):
        sim_triad.accepted_methods(tmp_path / "absent.json")


def test_unaccepted_method_is_refused(tmp_path, monkeypatch):
    v = tmp_path / "validation.json"
    v.write_text(json.dumps({"verdict": {"sim_v6r1": {"sim_v6r1:mc_nb": {"accepted": True, "reasons": []},
                                                      "sim_v6r1:eb_boot": {"accepted": False, "reasons": ["x"]}}}}))
    monkeypatch.setattr(sim_triad, "VALIDATION", v)
    with pytest.raises(sim_triad.Blocked):
        sim_triad.run_slate([], repo=ROOT, out=tmp_path / "o", as_of=datetime.now(timezone.utc), methods=["eb_boot"])


def test_cli_has_sim_command():
    a = cli.parser().parse_args(["sim", "--date", "2026-11-29", "--trials", "100000"])
    assert a.cmd == "sim" and a.trials == 100000


@pytest.mark.skipif(not sim_triad.VALIDATION.exists() or not sim_triad.CALIB_R1.exists(), reason="no validation yet")
def test_one_game_small_run_writes_only_its_out_dir(tmp_path):
    entry = {"game_id": "2026_12_ATL_MIN", "home": "MIN", "away": "ATL"}
    accepted, _ = sim_triad.accepted_methods()
    if not accepted:
        pytest.skip("no accepted method")
    before = {p: p.stat().st_mtime_ns for p in (ROOT / "snapshots").rglob("*.json")}
    s = sim_triad.run_slate([entry], repo=ROOT, out=tmp_path, as_of=datetime(2026, 11, 29, 12, tzinfo=timezone.utc),
                            trials=300, concurrency=1)
    after = {p: p.stat().st_mtime_ns for p in (ROOT / "snapshots").rglob("*.json")}
    assert before == after                                    # locks, projections and grades untouched
    assert s["projection_ready"] is False
    r1 = json.loads((tmp_path / "2026_12_ATL_MIN" / "sim_v6r1.json").read_text())
    v6 = json.loads((tmp_path / "2026_12_ATL_MIN" / "sim_v6.json").read_text())
    assert r1["is_original_sim_v6"] is False and r1["not_sim_v6"] is True and r1["engine"] == "sim_v6r1"
    assert v6["is_original_sim_v6"] is True and v6["engine"] == "sim_v6"
    assert r1["legs"] > 0 and r1["trials_per_method_per_scenario"] == 300
    leg = r1["results"][0]
    assert set(leg["methods"]) == set(accepted)
    for m in accepted:
        assert set(leg["methods"][m]) >= {"favorite_controls", "underdog_chases", "competitive", "residual"}
    assert s["games"][0]["trials"]["sim_v6r1"] == r1["legs"] * len(accepted) * 4 * 300

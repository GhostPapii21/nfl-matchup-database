"""Snapshot locker / scorer: as-of refusals, price conversion, scoring maths. Offline."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
from snapshots import lock, score

CFG = {"config_id": "x", "game": {"home": "NYG", "away": "WAS", "week_asof_exclusive": 10, "game_id": "2026_10_WAS_NYG"},
       "history": {"weeks_inclusive": list(range(1, 10))}}
KO = datetime(2026, 11, 13, 1, 15, tzinfo=timezone.utc)


def _pbp(tmp_path, ids):
    p = tmp_path / "pbp.parquet"
    pd.DataFrame({"game_id": ids, "week": [9] * len(ids), "season": [2026] * len(ids)}).to_parquet(p)
    return str(p)


def test_asof_pass(tmp_path):
    assert lock.asof_checks(CFG, _pbp(tmp_path, ["2026_09_A_B"]), KO - timedelta(hours=8), KO, None) == []


def test_refuses_after_kickoff(tmp_path):
    assert any("kickoff" in w for w in lock.asof_checks(CFG, _pbp(tmp_path, ["a"]), KO, KO, None))


def test_refuses_leaked_target_game(tmp_path):
    assert any("leakage" in w for w in lock.asof_checks(CFG, _pbp(tmp_path, ["2026_10_WAS_NYG"]), KO - timedelta(hours=1), KO, None))


def test_refuses_history_not_before_week(tmp_path):
    c = json.loads(json.dumps(CFG)); c["history"]["weeks_inclusive"] = list(range(1, 11))
    assert lock.asof_checks(c, _pbp(tmp_path, ["a"]), KO - timedelta(hours=1), KO, None)


def test_refuses_freeze_pulled_after_lock(tmp_path):
    fr = {"meta": {"pulled_utc": (KO + timedelta(minutes=1)).isoformat()}}
    assert lock.asof_checks(CFG, _pbp(tmp_path, ["a"]), KO - timedelta(hours=1), KO, fr)


def test_packet_prices_conversion():
    pk = {"books": {"retrieved_utc": "2026-11-12T11:16:37+00:00", "markets": {
        "spread": {"sides": ["NYJ", "BUF"], "books": {"draftkings": {"line": 8.5, "prices": {"NYJ": -112, "BUF": -108}, "no_vig": {"NYJ": 0.5043, "BUF": 0.4957}}}}}}}
    f = lock.packet_prices(pk)
    assert f["meta"]["status"] == "PACKET_TWO_BOOK_NOT_FOUR_BOOK"
    r = f["rows"][0]
    assert (r["market"], r["side_a"], r["line"], r["novig_a"]) == ("spreads", "NYJ", 8.5, 0.5043)


def test_summarize_spread_side_math():
    arrays = {k: np.zeros(4, dtype=int) for k in ("h1_home", "h1_away", "h2_home", "h2_away", "went_ot")}
    arrays["fg_home"] = np.array([20, 20, 20, 10]); arrays["fg_away"] = np.array([10, 18, 24, 30])
    lines = {"spreads": [{"book": "b", "line": 2.5, "side_a": "WAS", "novig_a": 0.5, "reference_only": False}], "totals": [], "h2h": []}
    s = lock.summarize(arrays, lines, "NYG", "WAS", "NYG", "WAS")
    # WAS +2.5 covers when home margin < 2.5: margins 10, 2, -4, -20 -> 3 of 4
    assert s["vs_market"][0]["p_model_cover"] == 0.75


def test_crps_point_mass():
    assert abs(score.crps(np.array([3.0] * 10), 3.0)) < 1e-12
    assert abs(score.crps(np.array([0.0] * 10), 3.0) - 3.0) < 1e-12


def test_score_refuses_tampered_lock(tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "LOCK.json").write_text(json.dumps({"files": {"a.txt": "0" * 64}}))
    import pytest
    with pytest.raises(SystemExit, match="REFUSED"):
        score.score(tmp_path, {"home_score": 1, "away_score": 0}, {"home": "NYG"})

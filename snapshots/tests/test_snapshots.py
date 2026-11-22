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


def test_lock_review_guard_ok_after_nfl43_review_accepted():
    """NFL-43 bounds accepted at 32b9b92 (Nov 12 ~3:05 PM ET): the lock's review guard passes. Pending/edited-bounds
    refusals stay covered by the tmp-repo tests."""
    assert lock.review_guard()["status"] == "OK"


# NFL-49 P4: the game-day gate passes the newest pregame/price_freezes/*/freeze_*.json to the locker. Free direct-pull
# freezes (pregame/direct_books.write_freeze, schema price-freeze/direct-1) use packet market names
# (moneyline/spread/total) and per-book prices/no_vig dicts, so market_lines() found no rows and the lock compared
# the sim against no book line at all (scored as NOLINE). They must normalize to the same rows as packet_prices.
DIRECT1 = {"meta": {"status": "OK", "schema": "price-freeze/direct-1", "game_id": "2026_11_MIA_BUF", "game": "MIA@BUF",
                    "pulled_utc": "2026-11-22T11:57:46Z"},
           "rows": [{"book": "fanduel", "market": "spread", "line": -16.5, "prices": {"BUF": -113.0, "MIA": -113.0},
                     "no_vig": {"BUF": 0.5, "MIA": 0.5}, "reference_only": False}],
           "markets": {"spread": {"sides": ["BUF", "MIA"], "books": {"fanduel": {
                           "line": -16.5, "prices": {"BUF": -113.0, "MIA": -113.0}, "no_vig": {"BUF": 0.5, "MIA": 0.5},
                           "last_update": "2026-11-22T11:57:46+00:00"}}},
                       "total": {"sides": ["Over", "Under"], "books": {"pinnacle": {
                           "line": 44.5, "prices": {"Over": -109.0, "Under": -105.0}, "no_vig": {"Over": 0.5045, "Under": 0.4955}}}},
                       "moneyline": {"sides": ["BUF", "MIA"], "books": {"fanduel": {
                           "line": None, "prices": {"BUF": -1600.0, "MIA": 900.0}, "no_vig": {"BUF": 0.904, "MIA": 0.096}}}},
                       "rushing_yards|James Cook": {"sides": ["Over", "Under"], "books": {"fanduel": {
                           "line": 84.5, "prices": {"Over": -110.0, "Under": -110.0}, "no_vig": {"Over": 0.5, "Under": 0.5}}}}}}


def test_direct1_freeze_normalizes_to_team_rows():
    f = lock.normalize_freeze(DIRECT1)
    got = {(r["market"], r["book"], r["side_a"], r["line"], r["novig_a"]) for r in f["rows"]}
    assert got == {("spreads", "fanduel", "BUF", -16.5, 0.5), ("totals", "pinnacle", "Over", 44.5, 0.5045),
                   ("h2h", "fanduel", "BUF", None, 0.904)}
    assert f["meta"]["pulled_utc"] == "2026-11-22T11:57:46Z" and f["meta"]["schema"] == "price-freeze/direct-1"
    assert [r for r in f["rows"] if r["book"] == "pinnacle"][0]["reference_only"] is True
    lines = lock.market_lines(f, "BUF", "MIA")
    assert len(lines["spreads"]) == len(lines["totals"]) == len(lines["h2h"]) == 1


def test_multibook_freeze_passes_through_unchanged():
    fr = {"meta": {"pulled_utc": "2026-11-12T11:16:37+00:00"},
          "rows": [{"book": "draftkings", "market": "spreads", "line": 8.5, "side_a": "NYJ", "side_b": "BUF", "novig_a": 0.5043}]}
    assert lock.normalize_freeze(fr) is fr
    assert lock.normalize_freeze(None) is None

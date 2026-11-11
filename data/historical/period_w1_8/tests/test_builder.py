"""Synthetic fixtures exercise logic only; they are never published as NFL results."""
from copy import deepcopy
from datetime import datetime, timezone
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("builder", Path(__file__).resolve().parents[1] / "scripts/build_ledger.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
AS_OF = datetime(2026, 11, 6, 14, tzinfo=timezone.utc)


def schedule(**changes):
    row = dict(game_id="2026_01_AAA_BBB", season=2026, week=1, game_type="REG",
               gameday="2026-09-10", gametime="20:20", home_team="BBB", away_team="AAA",
               home_score=24, away_score=17, overtime=0)
    row.update(changes)
    return row


def plays(s, ends=None):
    ends = ends or [(7, 0), (10, 7), (17, 10), (24, 17)]
    return [dict(game_id=s["game_id"], season=2026, week=s["week"], home_team=s["home_team"],
                 away_team=s["away_team"], play_id=q * 100, qtr=q, total_home_score=h,
                 total_away_score=a, quarter_end=1, desc="END GAME" if q == len(ends) else "END QUARTER")
            for q, (h, a) in enumerate(ends, 1)]


def test_quarters_halves_cumulative_and_final():
    s = schedule()
    games, periods, ledger = b.build_rows([s], list(reversed(plays(s))), "TEST", AS_OF)
    p = {r["period"]: r for r in periods}
    assert [p[q]["home_pts"] for q in ("Q1", "Q2", "Q3", "Q4")] == [7, 3, 7, 7]
    assert (p["H1"]["home_pts"], p["H2"]["home_pts"], p["OT"]["home_pts"]) == (10, 14, 0)
    assert (p["H2"]["cumulative_home"], p["Q3"]["cumulative_away"]) == (24, 10)
    assert not games[0]["overtime"] and games[0]["winner"] == "BBB"
    assert ledger[0]["pff_overview"] == "MISSING"
    assert ledger[0]["market_spread_grade"] == "NOLINE"


@pytest.mark.parametrize("ends,hs,aws,tie", [
    ([(0, 0), (7, 7), (14, 14), (20, 20), (23, 20)], 23, 20, False),
    ([(0, 0), (7, 7), (14, 14), (20, 20), (20, 20)], 20, 20, True),
    ([(0, 0), (7, 7), (14, 14), (20, 20), (20, 20), (20, 26)], 20, 26, False),
])
def test_ot_sum_and_tie(ends, hs, aws, tie):
    s = schedule(home_score=hs, away_score=aws, overtime=1)
    games, periods, ledger = b.build_rows([s], plays(s, ends), "TEST", AS_OF)
    g = games[0]
    assert g["overtime"] is True and g["tie"] is tie
    for side, final in (("home", hs), ("away", aws)):
        assert g[f"h1_{side}"] + g[f"h2_{side}"] + g[f"ot_{side}"] == final
    assert ledger[0]["scoreboard_status"] == "PRESENT"


def test_boundary_pat_included_in_same_quarter():
    s = schedule()
    ps = plays(s)
    # A touchdown with a pre-play score of 0, a PAT starting at 6, then Q1 end at 7.
    for pid, h in ((10, 0), (20, 6)):
        p = dict(ps[0], play_id=pid, total_home_score=h, quarter_end=0, desc="scoring play")
        ps.append(p)
    pts, _, reason = b.reconstruct(s, ps)
    assert not reason and pts["Q1"] == (7, 0)


@pytest.mark.parametrize("desc", [
    "Timeout #1 by ATL at 14:16.",
    "The status of the game clock was assisted by replay.",
    "PENALTY on AAA, Delay of Game, 5 yards - No Play.",
    "(7:31) pass incomplete short right. ** Injury Update: BBB-5 has returned to the game.",
])
@pytest.mark.parametrize("side", ["home", "away"])
def test_stale_non_scoring_score_does_not_erase_quarters(desc, side):
    s = schedule()
    ps = plays(s)
    # Insert BEFORE Q2 end marker so endpoint remains last play of quarter.
    mid = dict(ps[1], play_id=190, quarter_end=0, desc="ordinary play")
    stale = dict(ps[1], play_id=195, quarter_end=0, desc=desc,
                 **{f"total_{side}_score": 0})
    ps.extend([mid, stale])
    pts, overtime, reason = b.reconstruct(s, list(reversed(ps)))
    assert not reason and overtime is False
    assert pts == b.reconstruct(s, plays(s))[0]


def test_timeout_regression_during_overtime_preserves_tie():
    s = schedule(home_score=20, away_score=20, overtime=1)
    ps = plays(s, [(0, 0), (7, 7), (14, 14), (20, 20), (20, 20)])
    ps.append(dict(ps[-1], play_id=450, quarter_end=0, desc="Timeout #1 by AAA",
                   total_home_score=14))
    games, _, ledger = b.build_rows([s], ps, "TEST", AS_OF)
    assert ledger[0]["scoreboard_status"] == "PRESENT"
    assert games[0]["tie"] is True and games[0]["overtime"] is True
    assert games[0]["ot_home"] == games[0]["ot_away"] == 0


def test_delayed_quarter_marker_must_corroborate_own_quarter():
    s = schedule()
    ps = plays(s)
    # Q1 end delayed after a Q2 play: without a same-score Q1 corroboration, Q1 missing.
    ps[0]["play_id"] = 120
    ps.append(dict(ps[0], play_id=110, qtr=2, quarter_end=0, desc="ordinary play",
                   total_home_score=7, total_away_score=0))
    assert b.reconstruct(s, ps)[2] == "NONMONOTONIC_SCORE_OR_QUARTER"
    # Add corroborating Q1 row before the delayed end so Q1 recovers.
    ps.append(dict(ps[0], play_id=90, quarter_end=0, desc="ordinary play",
                   total_home_score=7, total_away_score=0))
    assert b.reconstruct(s, ps)[0]["Q1"] == (7, 0)
    # True scoring non-monotonicity on the delayed Q1 end remains MISSING.
    ps[0]["total_home_score"] = 6
    assert b.reconstruct(s, ps)[2] == "NONMONOTONIC_SCORE_OR_QUARTER"


@pytest.mark.parametrize("changes", [
    dict(desc="touchdown", total_home_score=6),
    dict(desc="ordinary play", qtr=1),
    dict(desc="Timeout #1 by AAA", total_home_score=6, total_away_score=8),
    dict(desc="END QUARTER", quarter_end=1, total_home_score=6),
])
def test_unexplained_regressions_and_mixed_admin_scores_remain_missing(changes):
    s = schedule()
    ps = plays(s)
    ps.append(dict(ps[1], play_id=220, quarter_end=0, **{}))
    ps[-1].update(changes)
    assert b.reconstruct(s, ps)[2] == "NONMONOTONIC_SCORE_OR_QUARTER"


def test_stale_timeout_cannot_replace_missing_endpoint():
    s = schedule()
    ps = plays(s)
    ps[0].update(quarter_end=0, desc="ordinary play")
    ps.append(dict(ps[0], play_id=110, desc="Timeout #1 by AAA", total_home_score=0))
    assert b.reconstruct(s, ps)[2] == "MISSING_QUARTER_END_MARKER"


@pytest.mark.parametrize("changes", [dict(week=9), dict(week=0), dict(season=2025),
                                          dict(game_type="WC"), dict(home_score=None),
                                          dict(gameday="2026-12-01"), dict(home_score=float("nan"))])
def test_scope_and_completion(changes):
    assert b.build_rows([schedule(**changes)], [], "TEST", AS_OF)[0] == []


def test_missing_pbp_keeps_schedule_game_and_missing_panels():
    g, p, l = b.build_rows([schedule(overtime=None)], [], "TEST", AS_OF)
    assert len(g) == 1 and len(p) == 8
    assert all(r["home_pts"] is None and r["period_winner"] is None for r in p)
    assert l[0]["ot_status"] == "MISSING"


@pytest.mark.parametrize("defect,reason", [
    ("identity", "PBP_IDENTITY_MISMATCH"), ("final", "FINAL_SCORE_MISMATCH"),
    ("end", "NO_SCORED_GAME_END"), ("quarter", "MISSING_REGULATION_QUARTER"),
    ("marker", "MISSING_QUARTER_END_MARKER"), ("negative", "NONMONOTONIC_SCORE_OR_QUARTER"),
    ("duplicate", "CONFLICTING_DUPLICATE_PLAY"),
])
def test_bad_pbp_is_missing(defect, reason):
    s = schedule()
    ps = deepcopy(plays(s))
    if defect == "identity": ps[0]["home_team"] = "ZZZ"
    if defect == "final": ps[-1]["total_home_score"] = 23
    if defect == "end": ps[-1]["desc"] = "last play"
    if defect == "quarter": ps.pop(1)
    if defect == "marker": ps[0].update(quarter_end=0, desc="play")
    if defect == "negative": ps[1]["total_home_score"] = 6
    if defect == "duplicate": ps.append(dict(ps[0], total_home_score=8))
    assert b.reconstruct(s, ps)[2] == reason


def test_ot_schedule_conflict_or_missing():
    s = schedule(home_score=23, away_score=20)
    ps = plays(s, [(0, 0), (7, 7), (14, 14), (20, 20), (23, 20)])
    assert b.reconstruct(s, ps)[2] == "OVERTIME_CONFLICT"
    s = schedule(overtime=1)
    assert b.reconstruct(s, plays(s))[2] == "MISSING_OT_PBP"


@pytest.mark.parametrize("line", [3, 7, 10, -7, 0])
def test_schedule_spread_cannot_grade_without_verified_closer(line):
    result = b.market(schedule(spread_line=line), retained=True)
    assert result["market_spread_grade"] == "NOLINE" and result["spread_result_home"] is None
    assert result["spread_line"] == line
    assert result["market_missing_reason"] == "NO_VERIFIED_CLOSER_QUOTE"
    assert result["quote_verified_closer"] is False and result["quote_timestamp"] == ""
    assert result["quote_source"] == b.URLS["schedules"]


@pytest.mark.parametrize("value", [None, "", "invalid", float("nan"), float("inf")])
def test_unusable_quote_is_noline(value):
    result = b.market(schedule(spread_line=value, total_line=value), retained=True)
    assert result["market_spread_grade"] == result["market_total_grade"] == "NOLINE"


def test_unretained_quote_and_moneyline_alone_cannot_grade_spread():
    assert b.market(schedule(spread_line=3, total_line=40), False)["market_spread_grade"] == "NOLINE"
    assert b.market(schedule(home_moneyline=-150), True)["market_spread_grade"] == "NOLINE"


@pytest.mark.parametrize("line", [40, 41, 42])
def test_schedule_total_cannot_grade_without_verified_closer(line):
    result = b.market(schedule(total_line=line), True)
    assert result["total_result"] is None and result["market_total_grade"] == "NOLINE"
    assert result["total_line"] == line
    assert result["market_missing_reason"] == "NO_VERIFIED_CLOSER_QUOTE"


def test_duplicate_schedule_rejected():
    s = schedule()
    with pytest.raises(ValueError, match="Duplicate"):
        b.build_rows([s, s], [], "TEST", AS_OF)


def test_offline_snapshot_replay_and_checksum_rejection(tmp_path, monkeypatch):
    import json
    import polars as pl
    monkeypatch.setattr(b, "ROOT", tmp_path)
    raw = tmp_path / "data/raw"
    raw.mkdir(parents=True)
    s = schedule(spread_line=3, total_line=41)
    manifest = dict(status="FETCHED", season=2026, weeks=[1, 8], pull_utc="FIXTURE_ONLY", fetches={})
    for name, rows in (("schedules", [s]), ("pbp", plays(s))):
        path = raw / f"{name}.parquet"
        pl.from_dicts(rows).write_parquet(path)
        manifest["fetches"][name] = dict(status="OK", file=path.name, sha256=b.digest(path))
    (raw / "manifest.json").write_text(json.dumps(manifest))
    frames, replayed = b.acquire(AS_OF, offline=True)
    assert replayed["pull_utc"] == "FIXTURE_ONLY"
    rows = b.build_rows(frames["schedules"].to_dicts(), frames["pbp"].to_dicts(), "FIXTURE_ONLY", AS_OF, True)
    assert len(rows[0]) == 1 and rows[2][0]["market_spread_grade"] == "NOLINE"
    (raw / "pbp.parquet").write_bytes(b"corrupted fixture")
    with pytest.raises(ValueError, match="checksum"):
        b.acquire(AS_OF, offline=True)


def test_publish_blocked_has_headers_unknown_count_and_no_fake_games(tmp_path, monkeypatch):
    monkeypatch.setattr(b, "ROOT", tmp_path)
    (tmp_path / "data").mkdir()
    (tmp_path / "reviews").mkdir()
    manifest = dict(status="FETCH_FAILED", pull_utc="FIXTURE_ONLY", fetches={})
    result = b.publish({}, manifest, AS_OF)
    assert result["expected_completed_games"] is None and result["built_games"] == 0
    assert result["status"] == "BLOCKED_SOURCE_FETCH"
    for name in ("games", "period_scores", "coverage_ledger"):
        assert len((tmp_path / f"data/{name}_w1_8.csv").read_text().splitlines()) == 1

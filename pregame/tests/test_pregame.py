"""Pregame packet builder: metric definitions, slate selection, fail-closed sources, JSON safety."""
import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pregame import build_packets as B, metrics as M, packet as PK, render as R, sources as S  # noqa: E402


def play(gid, off, dfn, **kw):
    base = dict(play_id=play.n, game_id=gid, posteam=off, defteam=dfn, play_type="pass", down=1, qtr=1, yards_gained=0, sack=0, qb_scramble=0,
                qb_dropback=0, pass_attempt=0, complete_pass=0, pass_touchdown=0, interception=0, fumble_lost=0, qb_hit=0, air_yards=None,
                rush_attempt=0, rush_touchdown=0, receiver_player_id=None, receiver_player_name=None, rusher_player_id=None,
                rusher_player_name=None, passer_player_id=None, passer_player_name=None, epa=0.0, third_down_converted=0,
                third_down_failed=0, score_differential=0, yardline_100=60, fixed_drive=1, fixed_drive_result="Punt",
                run_location=None, run_gap=None, two_point_attempt=0)
    play.n += 1
    base.update(kw)
    return base
play.n = 1


def pass_(gid, off, dfn, rec, yards, complete=True, air=5, **kw):
    return play(gid, off, dfn, qb_dropback=1, pass_attempt=1, complete_pass=int(complete), yards_gained=yards if complete else 0, air_yards=air,
                receiver_player_id=rec, receiver_player_name=rec, passer_player_id="QB1", passer_player_name="QB1", **kw)


def run_(gid, off, dfn, who, yards, **kw):
    return play(gid, off, dfn, play_type="run", rush_attempt=1, yards_gained=yards, rusher_player_id=who, rusher_player_name=who,
                run_location="left", run_gap="end", **kw)


@pytest.fixture
def world():
    rost = pd.DataFrame([dict(gsis_id=i, position=p, week=1, team="AAA", full_name=i, status="ACT") for i, p in
                         (("WR1", "WR"), ("TE1", "TE"), ("RB1", "RB"), ("FB1", "FB"), ("QB1", "QB"))])
    rows = [
        pass_("g1", "AAA", "BBB", "WR1", 25),                       # explosive pass to a WR
        pass_("g1", "AAA", "BBB", "WR1", 19),                       # 19 is not explosive
        pass_("g1", "AAA", "BBB", "TE1", 8),
        pass_("g1", "AAA", "BBB", "TE1", 0, complete=False),        # TE target, incomplete
        pass_("g1", "AAA", "BBB", "FB1", 4),                        # fullback counts as RB
        play("g1", "AAA", "BBB", qb_dropback=1, pass_attempt=1, sack=1, yards_gained=-7, passer_player_id="QB1", passer_player_name="QB1"),
        play("g1", "AAA", "BBB", play_type="run", qb_dropback=1, qb_scramble=1, rush_attempt=1, yards_gained=16, rusher_player_id="QB1", rusher_player_name="QB1"),
        run_("g1", "AAA", "BBB", "RB1", 15),                        # explosive run
        run_("g1", "AAA", "BBB", "RB1", 3),
        run_("g1", "AAA", "BBB", "RB1", 2, down=None),              # no down = two-point try / untimed: excluded
        pass_("g1", "AAA", "BBB", "WR1", 30, two_point_attempt=1),  # two-point try: excluded
        play("g1", "AAA", "BBB", play_type="qb_kneel", rush_attempt=1, yards_gained=-1),
    ]
    pbp = pd.DataFrame(rows)
    games = pd.DataFrame([dict(game_id="g1", season=2026, week=1, gameday="2026-09-10", home_team="BBB", away_team="AAA", home_score=10, away_score=24)])
    return pbp, rost, games


def test_metric_definitions(world):
    pbp, rost, games = world
    p = M.prepare(pbp, rost)
    assert len(p) == 9                                              # kneel, no-down and two-point rows dropped
    d = M.summarize(M.team_games(p, games, "defteam"))
    assert d["games"] == 1 and d["points_pg"] == 24                 # BBB's defence allowed AAA's 24
    assert d["wr_rec_yards_pg"] == 44 and d["wr_receptions_pg"] == 2 and d["wr_targets_pg"] == 2
    assert d["te_rec_yards_pg"] == 8 and d["te_targets_pg"] == 2 and d["te_receptions_pg"] == 1
    assert d["rb_rec_yards_pg"] == 4                                # FB mapped to RB
    assert d["explosive_pass"] == 1                                 # 25 yes, 19 no
    assert d["explosive_rush"] == 2                                 # 15-yard run and 16-yard scramble
    assert d["rush_yards_pg"] == 18 and d["rush_att_pg"] == 2       # scramble is not a designed carry
    assert d["qb_rush_yards_pg"] == 16
    assert d["sacks"] == 1 and d["sack_rate"] == pytest.approx(1 / 7)   # 5 passes + sack + scramble = 7 dropbacks
    assert d["pass_att_pg"] == 5 and d["completions_pg"] == 4       # the sack is not an attempt
    assert d["blitz_rate"] is None                                  # no charting supplied: unknown, not zero
    o = M.summarize(M.team_games(p, games, "posteam"))
    assert o["points_pg"] == 24 and o["wr_rec_yards_pg"] == 44


def test_ranks_direction():
    lg = pd.DataFrame({"points_pg": {"A": 10.0, "B": 30.0}, "sack_rate": {"A": 0.10, "B": 0.02}})
    assert M.ranks(lg, "A", defense=True)["points_pg"]["rank"] == 1     # fewest points allowed = best defence
    assert M.ranks(lg, "B", defense=False)["points_pg"]["rank"] == 1    # most points scored = best offence
    assert M.ranks(lg, "A", defense=True)["sack_rate"]["rank"] == 1     # most sacks = best pass rush
    assert M.ranks(lg, "B", defense=False)["sack_rate"]["rank"] == 1    # fewest sacks allowed = best protection


def test_slate_selection():
    g = pd.DataFrame([
        dict(game_id="a", season=2026, game_type="REG", week=10, gameday="2026-11-12", weekday="Thursday", gametime="20:15", home_score=None),
        dict(game_id="b", season=2026, game_type="REG", week=10, gameday="2026-11-14", weekday="Saturday", gametime="13:00", home_score=None),
        dict(game_id="c", season=2026, game_type="REG", week=10, gameday="2026-11-16", weekday="Monday", gametime="20:15", home_score=None),
        dict(game_id="d", season=2026, game_type="REG", week=11, gameday="2026-11-19", weekday="Thursday", gametime="20:15", home_score=None),
        dict(game_id="z", season=2026, game_type="REG", week=9, gameday="2026-11-09", weekday="Monday", gametime="20:15", home_score=21.0),
    ])
    pick = lambda **k: list(B.pick_games(g, season=2026, **k).game_id)
    assert pick(today=date(2026, 11, 11)) == ["a", "c"]                      # this week only, Thu/Sun/Mon only
    assert pick(today=date(2026, 11, 11), weekdays="all") == ["a", "b", "c"]
    assert pick(today=date(2026, 11, 13)) == ["c"]                           # Thursday game already played/past
    assert pick(today=date(2026, 11, 17)) == ["d"]                           # rolls to the next week
    assert pick(today=date(2026, 11, 11), game="z") == ["z"]
    assert PK.slot_name("Sunday", "20:20") == "Sunday Night Football" and PK.slot_name("Monday", "20:15") == "Monday Night Football"


def test_sources_fail_closed_and_optional(tmp_path):
    def boom(url, timeout=0):
        raise OSError("blocked")
    with pytest.raises(SystemExit):                                  # required data missing: no packet
        S.fetch_all(2026, tmp_path, fetch=boom)
    for name in ("games.parquet", "play_by_play_2026.parquet", "roster_weekly_2026.parquet"):
        (tmp_path / name).write_bytes(b"x")
    src = S.fetch_all(2026, tmp_path, fetch=boom)                    # cached required files: allowed but labelled stale
    assert src["pbp"]["status"].startswith("STALE_CACHE_USED") and src["pbp"]["sha256"]
    assert src["injuries"]["path"] is None and "FETCH_FAILED" in src["injuries"]["status"]
    assert S.espn_injuries(fetch=boom)["status"].startswith("UNAVAILABLE")   # never raises
    ok = S.espn_injuries(fetch=lambda u, timeout=0: json.dumps({"injuries": [{"injuries": [
        {"athlete": {"displayName": "A B", "position": {"abbreviation": "WR"}, "team": {"abbreviation": "WSH"}}, "status": "Out"}]}]}).encode())
    assert ok["teams"]["WAS"][0]["status"] == "Out"                  # ESPN WSH -> nflverse WAS


def test_baseline_and_clean():
    b = PK._baseline([10, 20, 30, 40], 1.1)
    assert b["games"] == 4 and b["weighted_mean"] == pytest.approx(1.1 * (10 * 1 + 20 * 4 / 3 + 30 * 5 / 3 + 40 * 2) / 6, abs=0.06)
    assert b["p50"] == pytest.approx(27.5)
    assert PK._baseline([10, 20], 1.0) is None                       # under three games: no baseline
    assert PK._factor({"k": 200.0}, {"k": 100.0}, "k") == 1.15 and PK._factor({"k": 110.0}, {"k": 100.0}, "k") == pytest.approx(1.05)
    assert PK._factor({}, {"k": 100.0}, "k") == 1.0
    out = B._clean({"a": float("nan"), "b": [pd.NA if False else 1.5, {1, 2}]})
    assert out["a"] is None and json.dumps(out, allow_nan=False)
    assert R.f(None) == "n/a" and R.f(0.123, 1, True) == "12.3%"


def test_ledger_never_claims_ready():
    pk = {"teams": {}, "sources": {}}
    led = PK.phase_ledger(pk)
    assert [p["phase"] for p in led] == list(range(1, 16))
    by = {p["phase"]: p["status"] for p in led}
    assert by[13] == "BLOCKED" and by[15] == "PENDING" and by[14] == "PARTIAL_RESEARCH_ONLY"

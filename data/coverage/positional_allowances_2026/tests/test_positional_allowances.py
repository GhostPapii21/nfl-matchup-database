"""Offline regression tests for build_allowances.py and its committed outputs. No network, no raw parquet needed."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import build_allowances as B  # noqa: E402


# --------------------------------------------------------------------------- synthetic helpers
def play(**kw):
    row = dict(game_id="2026_01_AA_BB", play_id=1, season_type="REG", week=1, game_date="2026-09-10",
               posteam="AA", defteam="BB", play_type="pass", down=1, ydstogo=10, yardline_100=75, shotgun=1,
               qb_dropback=1, pass_attempt=1, sack=0, complete_pass=1, yards_gained=10.0, receiving_yards=10.0,
               passing_yards=10.0, rushing_yards=np.nan, pass_touchdown=0, rush_touchdown=0, interception=0,
               air_yards=5.0, pass_location="left", receiver_player_id="WRA", rusher_player_id=None,
               qb_scramble=0, qb_kneel=0, qb_spike=0, two_point_attempt=0, success=1, epa=0.5, first_down=1)
    row.update(kw)
    return row


ROSTER = pd.DataFrame([
    dict(gsis_id=g, week=w, team="AA", position=pos, pfr_id=f"p{g}", full_name=g)
    for w in (1, 2, 3) for g, pos in (("WRA", "WR"), ("WRB", "WR"), ("WRC", "WR"), ("WRD", "WR"),
                                      ("TE1", "TE"), ("RB1", "RB"), ("QB1", "QB"))
] + [dict(gsis_id="FB1", week=1, team="AA", position="FB", pfr_id="pFB1", full_name="FB1")])


def snaps(game_id, week, rows):
    return pd.DataFrame([dict(game_id=game_id, week=week, team="AA", player=g, pfr_player_id=f"p{g}",
                              position="WR", offense_snaps=s) for g, s in rows])


# --------------------------------------------------------------------------- unit tests
def test_depth_and_location_buckets():
    assert B.depth_bucket(-3) == "short" and B.depth_bucket(9.9) == "short"
    assert B.depth_bucket(10) == "inter" and B.depth_bucket(19) == "inter"
    assert B.depth_bucket(20) == "deep"
    assert B.depth_bucket(float("nan")) == "unknown" and B.depth_bucket(None) == "unknown"
    assert B.loc_bucket("middle") == "middle"
    assert B.loc_bucket("left") == B.loc_bucket("right") == "outside"
    assert B.loc_bucket(None) == "unknown"


def test_scrimmage_excludes_kneel_spike_2pt_noplay_postseason():
    p = pd.DataFrame([play(play_id=1), play(play_id=2, qb_kneel=1, play_type="run"), play(play_id=3, qb_spike=1),
                      play(play_id=4, two_point_attempt=1), play(play_id=5, play_type="no_play"),
                      play(play_id=6, season_type="POST")])
    assert B.scrimmage(p)["play_id"].tolist() == [1]


def test_wr_rank_uses_prior_targets_then_snaps():
    t = pd.DataFrame([
        # week 1: WRB 3 targets, WRA 1
        *[dict(game_id="g1", week=1, posteam="AA", receiver_player_id="WRB", rpos="WR") for _ in range(3)],
        dict(game_id="g1", week=1, posteam="AA", receiver_player_id="WRA", rpos="WR"),
        # week 2: WRA 5 targets (must not affect his week-2 rank)
        *[dict(game_id="g2", week=2, posteam="AA", receiver_player_id="WRA", rpos="WR") for _ in range(5)],
    ])
    act = pd.concat([snaps("g1", 1, [("WRA", 60), ("WRB", 50), ("WRC", 40), ("WRD", 10)]),
                     snaps("g2", 2, [("WRA", 60), ("WRB", 50), ("WRC", 40), ("WRD", 30)])])
    act["gsis_id"] = act["player"]
    games = pd.DataFrame([dict(game_id="g1", week=1, posteam="AA"), dict(game_id="g2", week=2, posteam="AA")])
    r, stats = B.wr_ranks(t, act, games)
    # week 1: no prior -> snaps order
    assert [r[("g1", "AA", g)] for g in ("WRA", "WRB", "WRC", "WRD")] == ["WR1", "WR2", "WR3", "WR_other"]
    # week 2: prior targets WRB 3 > WRA 1 > WRC 0 (snaps 40) > WRD 0 (snaps 30)
    assert [r[("g2", "AA", g)] for g in ("WRB", "WRA", "WRC", "WRD")] == ["WR1", "WR2", "WR3", "WR_other"]
    assert stats["week1_snap_ranked"] == 1


def test_opp_adjusted_leave_one_out():
    tg = pd.DataFrame([dict(posteam="AA", group="WR1", defteam=d, week=w, yds=y)
                       for d, w, y in (("BB", 1, 100.0), ("CC", 2, 40.0), ("DD", 3, 70.0))])
    oa = B.opp_adjusted(tg, ["yds"])
    # game vs BB: baseline = mean(40, 70) = 55 -> +45
    assert oa.loc[0, "yds_offbase"] == pytest.approx(55.0)
    assert oa.loc[0, "yds_oa"] == pytest.approx(45.0)
    assert oa.loc[1, "yds_oa"] == pytest.approx(40 - 85.0)
    assert (oa["offbase_games"] == 2).all()
    single = B.opp_adjusted(tg.iloc[:1], ["yds"])
    assert math.isnan(single.loc[0, "yds_oa"])  # one game: no baseline, unknown not zero


def test_window_games_last_n_played():
    assert B.window_games([1, 2, 3, 5, 6, 7], 3) == [5, 6, 7]
    assert B.window_games([1, 2], 5) == [1, 2]
    assert B.window_games([3, 1, 2], None) == [1, 2, 3]


def test_team_game_table_counts_and_zero_rows():
    plays = pd.DataFrame([
        play(play_id=1, receiver_player_id="WRA", air_yards=25, receiving_yards=30.0, yards_gained=30.0,
             pass_location="middle"),
        # lateral after catch: receiver credited 2, play gained 40 -> table must use 2
        play(play_id=2, receiver_player_id="TE1", air_yards=12, receiving_yards=2.0, yards_gained=40.0,
             yardline_100=15),
        play(play_id=3, receiver_player_id="RB1", air_yards=-2, receiving_yards=6.0, yards_gained=6.0, complete_pass=1),
        play(play_id=4, receiver_player_id="WRB", complete_pass=0, receiving_yards=np.nan, yards_gained=0.0,
             air_yards=np.nan, pass_location=None),
        play(play_id=5, play_type="run", qb_dropback=0, pass_attempt=0, receiver_player_id=None, complete_pass=0,
             rusher_player_id="RB1", rushing_yards=12.0, yards_gained=12.0, air_yards=np.nan),
        play(play_id=6, play_type="run", qb_dropback=0, pass_attempt=0, receiver_player_id=None, complete_pass=0,
             rusher_player_id="FB1", rushing_yards=3.0, yards_gained=3.0, air_yards=np.nan),
        play(play_id=7, play_type="run", qb_dropback=0, pass_attempt=0, receiver_player_id=None, complete_pass=0,
             rusher_player_id="QB1", rushing_yards=8.0, yards_gained=8.0, air_yards=np.nan),
        play(play_id=8, receiver_player_id=None, sack=1, complete_pass=0, yards_gained=-7.0, passing_yards=np.nan),
        play(play_id=9, play_type="run", qb_scramble=1, pass_attempt=0, receiver_player_id=None, complete_pass=0,
             rusher_player_id="QB1", rushing_yards=9.0, yards_gained=9.0),
    ])
    sn = snaps("2026_01_AA_BB", 1, [("WRA", 60), ("WRB", 50), ("WRC", 20)])
    ftn = pd.DataFrame([dict(nflverse_game_id="2026_01_AA_BB", nflverse_play_id=3, is_screen_pass=True,
                             is_play_action=False, n_blitzers=0)])
    tg, p, stats = B.team_game_table(plays, ROSTER, sn, ftn)
    row = tg.set_index("group")
    assert set(B.GROUPS) | {"QB"} == set(row.index)
    assert row.loc["WR1", "tgt"] == 1 and row.loc["WR1", "deep_yds"] == 30 and row.loc["WR1", "explo20"] == 1
    assert row.loc["WR1", "middle_yds"] == 30
    assert row.loc["WR2", "tgt"] == 1 and row.loc["WR2", "rec"] == 0 and row.loc["WR2", "depth_unknown_tgt"] == 1
    assert row.loc["WR2", "loc_unknown_tgt"] == 1
    assert row.loc["WR3", "tgt"] == 0  # WRC played, no target: a 0 row, not missing
    assert row.loc["TE", "yds"] == 2 and row.loc["TE", "rz_tgt"] == 1 and row.loc["TE", "inter_tgt"] == 1
    assert row.loc["RB", "rb_rush_att"] == 2 and row.loc["RB", "rb_rush_yds"] == 15  # FB counts as RB
    assert row.loc["RB", "rb_rush_explo10"] == 1
    assert row.loc["RB", "rb_screen_tgt"] == 1 and row.loc["RB", "rb_behind_los_yds"] == 6
    assert row.loc["QB", "sacks"] == 1 and row.loc["QB", "scrambles"] == 1 and row.loc["QB", "scramble_yds"] == 9
    assert row.loc["QB", "qb_designed_runs"] == 1 and row.loc["QB", "qb_designed_yds"] == 8
    assert row.loc["QB", "pass_att"] == 4
    nonqb = tg[tg.group != "QB"]
    assert nonqb["tgt"].sum() == 4


def test_check_inputs_stops_on_sha_mismatch(tmp_path):
    for name in B.EXPECTED_SHA:
        (tmp_path / name).write_bytes(b"not the recorded pull")
    with pytest.raises(SystemExit):
        B.check_inputs(tmp_path, allow_new=False)
    got = B.check_inputs(tmp_path, allow_new=True)
    assert set(got) == set(B.EXPECTED_SHA)


def test_sharp_windows_pooled_and_team_code_fix(tmp_path):
    rows = []
    for wk, man, cov in ((1, 2, 10), (2, 8, 10), (3, 0, 20)):
        rows.append(dict(source_game_id=f"g{wk}", season=2026, week=wk, team="AA", opponent="LAR",
                         metrics=dict(man=man, cov=cov, blitz=1, db=10, prsr=3, air=50, att=8, deep=1, pa=2,
                                      db_epa=1.0, explo=2, plays=60)))
    (tmp_path / "team_games.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    w = B.sharp_defense_windows(tmp_path).set_index("window")
    assert set(B.sharp_defense_windows(tmp_path)["defteam"]) == {"LA"}
    assert w.loc["season", "man_rate"] == pytest.approx(10 / 40)  # pooled, not mean of rates
    assert w.loc["L3", "games"] == 3
    assert w.loc["season", "man_rate_minus_season"] == 0


# --------------------------------------------------------------------------- committed-output integrity
OUT = HERE


@pytest.fixture(scope="module")
def built():
    if not (OUT / "team_game_allowed.csv").exists():
        pytest.skip("outputs not built")
    return {n: pd.read_csv(OUT / f"{n}.csv") for n in
            ("team_game_allowed", "allowances_windows", "allowance_trends", "situational_allowed",
             "sharp_defense_windows")}


def test_manifest_research_only():
    m = json.loads((OUT / "MANIFEST.json").read_text())
    assert m["projection_ready"] is False and m["research_only"] is True
    assert m["wr_rank_stats"]["unmapped_active_wr"] >= 0
    for k, v in m["built_from"].items():
        assert v["sha256"] == B.EXPECTED_SHA[k]


def test_32_defenses_every_table(built):
    for n in ("team_game_allowed", "allowances_windows", "situational_allowed", "sharp_defense_windows"):
        assert built[n]["defteam"].nunique() == 32, n
    assert "LAR" not in set(built["sharp_defense_windows"]["defteam"])


def test_season_window_totals_equal_team_game_sums(built):
    tg, w = built["team_game_allowed"], built["allowances_windows"]
    s = w[w.window == "season"]
    for grp in ("WR1", "TE", "RB"):
        exp = tg[tg.group == grp].groupby("defteam")["yds"].sum()
        got = s[s.group == grp].set_index("defteam")["yds_total"]
        assert (exp.sort_index() - got.sort_index()).abs().max() < 1e-6, grp


def test_window_game_counts(built):
    w = built["allowances_windows"]
    for wname, n in (("L3", 3), ("L5", 5), ("L10", 10)):
        assert (w[w.window == wname]["games"] <= n).all()
    s = w[w.window == "season"].groupby("defteam")["games"].first()
    assert ((s >= 10) & (s <= 12)).all()


def test_depth_buckets_partition_targets(built):
    tg = built["team_game_allowed"]
    r = tg[tg.group != "QB"]
    assert (r.short_tgt + r.inter_tgt + r.deep_tgt + r.depth_unknown_tgt == r.tgt).all()
    assert (r.middle_tgt + r.outside_tgt + r.loc_unknown_tgt == r.tgt).all()


def test_opp_adjusted_mean_near_zero_league_wide(built):
    # leave-one-out residuals are centred near zero across the league; a large mean would mean a join error
    w = built["allowances_windows"]
    s = w[(w.window == "season") & (w.group == "WR1")]
    assert abs(s["yds_oa_pg"].mean()) < 5


def test_ranks_in_range(built):
    w = built["allowances_windows"]
    rk = w[[c for c in w.columns if c.endswith("_rank")]]
    assert ((rk.min(skipna=True) >= 1) & (rk.max(skipna=True) <= 32)).all()


def test_trend_flags_values(built):
    assert set(built["allowance_trends"]["L3_flag"]) <= {"UP", "DOWN", "noise", "unknown"}

"""Player credit in packet logs must match official stats (what books settle on). refs NFL-75.

Bug 1: receiving yards were credited from yards_gained, so a receiver who lateraled was credited with the yards
gained after the lateral (2026 W3 SF: Mike Evans 114 in our log vs 34 official; Deebo Samuel 0 vs 80; 27 player-weeks
W1-W11 off by up to 80 yards).
Bug 2: a QB's rushing log counted designed runs only. Official rushing yards (and every rushing-yards prop) include
scrambles and kneel-downs (W1-W11: 285 of 318 QB-weeks off, mean -12.3 yards; Josh Allen W5 14 vs 121).
Carry share for the 60% rule keeps its existing denominator (designed carries); only the yardage credit changes.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pregame import metrics as M, packet as PK  # noqa: E402

N = iter(range(1, 10_000))


def play(gid, **kw):
    base = dict(play_id=next(N), game_id=gid, posteam="AAA", defteam="BBB", play_type="pass", down=1, qtr=1, yards_gained=0, sack=0,
                qb_scramble=0, qb_dropback=0, pass_attempt=0, complete_pass=0, pass_touchdown=0, interception=0, fumble_lost=0, qb_hit=0,
                air_yards=None, rush_attempt=0, rush_touchdown=0, receiver_player_id=None, receiver_player_name=None,
                rusher_player_id=None, rusher_player_name=None, passer_player_id=None, passer_player_name=None, epa=0.0,
                third_down_converted=0, third_down_failed=0, score_differential=0, yardline_100=60, fixed_drive=1,
                fixed_drive_result="Punt", run_location=None, run_gap=None, two_point_attempt=0,
                receiving_yards=None, rushing_yards=None, lateral_receiver_player_id=None, lateral_receiving_yards=None)
    base.update(kw)
    return base


def catch(gid, who, gained, credit=None, **kw):
    return play(gid, qb_dropback=1, pass_attempt=1, complete_pass=1, yards_gained=gained, air_yards=5,
                receiving_yards=gained if credit is None else credit, receiver_player_id=who, receiver_player_name=who,
                passer_player_id="QB1", passer_player_name="QB1", **kw)


def designed(gid, who, yds):
    return play(gid, play_type="run", rush_attempt=1, yards_gained=yds, rushing_yards=yds, rusher_player_id=who, rusher_player_name=who,
                run_location="left", run_gap="end")


def scramble(gid, who, yds):
    return play(gid, play_type="run", qb_dropback=1, qb_scramble=1, rush_attempt=1, yards_gained=yds, rushing_yards=yds,
                rusher_player_id=who, rusher_player_name=who)


def kneel(gid, who, yds=-1):
    return play(gid, play_type="qb_kneel", rush_attempt=1, yards_gained=yds, rushing_yards=yds, rusher_player_id=who, rusher_player_name=who)


ROST = pd.DataFrame([dict(gsis_id=i, position=p, week=1) for i, p in (("WR1", "WR"), ("WR2", "WR"), ("RB1", "RB"), ("QB1", "QB"))])


def games(n):
    return pd.DataFrame([dict(game_id=f"g{i}", season=2026, week=i, gameday=f"2026-09-{10 + i}", home_team="BBB", away_team="AAA",
                              home_score=10, away_score=20) for i in range(1, n + 1)])


def test_lateral_yards_go_to_the_player_who_gained_them():
    # WR1 catches at +34, laterals to WR2 who goes 80 more: official WR1 34, WR2 80 (play gained 114).
    pbp = pd.DataFrame([catch("g1", "WR1", 114, credit=34, lateral_receiver_player_id="WR2", lateral_receiving_yards=80),
                        catch("g1", "WR2", 10)])
    p = M.prepare(pbp, ROST)
    recs = {r["player_id"]: r for r in M.offense_players(p, "AAA", ["g1"], games(1))["receivers"]}
    assert recs["WR1"]["yards"] == 34 and recs["WR1"]["log"][0]["yards"] == 34
    assert recs["WR2"]["yards"] == 90 and recs["WR2"]["log"][0]["yards"] == 90
    top = M.top_lines_allowed(p, "BBB", ["g1"], games(1))[0]["top_receiver"]
    assert top["player"] == "WR2" and top["yards"] == 90
    # team and position-group totals keep the whole play (official team passing yards include lateral yards)
    assert M.summarize(M.team_games(p, games(1), "posteam"))["pass_yards_pg"] == 124


def test_receiving_credit_falls_back_when_the_column_is_absent():
    pbp = pd.DataFrame([catch("g1", "WR1", 12)]).drop(columns=["receiving_yards", "lateral_receiver_player_id", "lateral_receiving_yards"])
    p = M.prepare(pbp, ROST)
    assert M.offense_players(p, "AAA", ["g1"], games(1))["receivers"][0]["yards"] == 12


def test_qb_rushing_credit_includes_scrambles_and_kneels():
    rows = []
    for g in ("g1", "g2", "g3"):
        rows += [designed(g, "QB1", 4)] * 5 + [scramble(g, "QB1", 10), kneel(g, "QB1", -1), kneel(g, "QB1", -2)] + [designed(g, "RB1", 5)] * 15
    pbp = pd.DataFrame(rows).assign(play_id=range(1, len(rows) + 1))
    p = M.prepare(pbp, ROST)
    kn = M.kneel_credit(pbp)
    ru = {r["player_id"]: r for r in M.offense_players(p, "AAA", ["g1", "g2", "g3"], games(3), kneels=kn)["rushers"]}
    qb = ru["QB1"]
    assert qb["carries"] == 15                                   # designed carries: the 60% carry-share basis is unchanged
    assert qb["carry_share"] == pytest.approx(15 / 60)
    assert qb["rush_attempts_official"] == 15 + 3 + 6
    assert qb["rushing_yards_official"] == 3 * (20 + 10 - 3)
    assert [g["official_yards"] for g in qb["log"]] == [27, 27, 27]
    assert qb["yards"] == 60                                     # designed-run yards stay as they were
    rb = ru["RB1"]
    assert rb["rushing_yards_official"] == rb["yards"] == 225 and rb["carry_share"] == pytest.approx(45 / 60)
    base = {r["player"]: r for r in PK.player_baselines(M.offense_players(p, "AAA", ["g1", "g2", "g3"], games(3), kneels=kn),
                                                       {}, {})["players"]}
    assert base["QB1"]["rushing_yards"]["weighted_mean"] == pytest.approx(27.0)   # the market's definition
    assert base["RB1"]["rushing_yards"]["weighted_mean"] == pytest.approx(75.0)


def test_kneels_unknown_is_labelled_not_silently_zero():
    rows = [designed(g, "QB1", 4) for g in ("g1", "g2", "g3") for _ in range(5)]
    pbp = pd.DataFrame(rows).assign(play_id=range(1, len(rows) + 1))
    qb = M.offense_players(M.prepare(pbp, ROST), "AAA", ["g1", "g2", "g3"], games(3))["rushers"][0]
    assert qb["rushing_yards_official"] == 60 and qb["kneels_included"] is False


def test_official_credit_matches_nflverse_weekly_stats_when_available():
    """Full-season check against nflverse stats_player_week (skipped offline when the files are not cached)."""
    d = Path("/tmp/nfv1121")
    if not (d / "play_by_play_2026.parquet").exists() or not (d / "stats_player_week_2026.parquet").exists():
        pytest.skip("nflverse 2026 pbp + weekly stats not cached locally")
    pbp = pd.read_parquet(d / "play_by_play_2026.parquet"); pbp = pbp[pbp.season_type == "REG"]
    st = pd.read_parquet(d / "stats_player_week_2026.parquet"); st = st[st.season_type == "REG"]
    ros = st.rename(columns={"player_id": "gsis_id"})[["gsis_id", "position", "week"]]
    p, kn = M.prepare(pbp, ros), M.kneel_credit(pbp)
    g = pbp.drop_duplicates("game_id")[["game_id", "season", "week", "home_team", "away_team"]].assign(gameday="x", home_score=0, away_score=0)
    bad = []
    for team in ("SF", "BUF", "WAS"):
        gids = list(g[(g.home_team == team) | (g.away_team == team)].game_id)
        pl = M.offense_players(p, team, gids, g, kneels=kn)
        wk = g.set_index("game_id").week
        off = st[st.team == team].set_index(["player_id", "week"])
        for r in pl["receivers"]:
            for e in r["log"]:
                o = off.receiving_yards.get((r["player_id"], e["week"]))
                if o is not None and abs(o - e["yards"]) > 0.5:
                    bad.append(("rec", r["player"], e["week"], e["yards"], o))
        for r in pl["rushers"]:
            for e in r["log"]:
                o = off.rushing_yards.get((r["player_id"], e["week"]))
                if o is not None and abs(o - e["official_yards"]) > 0.5:
                    bad.append(("rush", r["player"], e["week"], e["official_yards"], o))
    assert not bad, bad[:10]

"""Player-board assembly. No network. Distributions come from dashboard.opportunity."""
from pathlib import Path

import numpy as np
import pandas as pd

from dashboard import opportunity as O
from sunday.player_board import (
    CHECKDOWN_MIN, QUESTIONABLE_SNAP_SHARE, SCHEMA, allocate_receiving, aliases, assemble,
    availability, measure_situational, replay, role_tags,
)

ROOT = Path(__file__).resolve().parents[2]


def _log(n=6, targets=6, yards=40):
    return [{"week": i + 1, "targets": targets, "receptions": 4, "yards": yards, "carries": 10} for i in range(n)]


def _receiver(pid="p1", name="J.Waddle", pos="WR", targets=36, share=0.25, **extra):
    row = {"player": name, "player_id": pid, "pos": pos, "games": 6, "targets": targets, "receptions": 24,
           "yards": 240, "td": 2, "target_share": share, "air_yards_share": 0.3, "avg_depth_of_target": 9.0,
           "yards_per_target": 6.7, "explosive": 2, "red_zone_targets": 4, "log": _log()}
    row.update(extra)
    return row


def _rusher(pid="b1", name="J.Williams", carries=80, share=0.55):
    return {"player": name, "player_id": pid, "pos": "RB", "games": 6, "carries": carries, "yards": 320, "td": 3,
            "carry_share": share, "yards_per_carry": 4.0, "red_zone_carries": 8, "explosive": 4,
            "log": [{"week": i + 1, "carries": 12, "yards": 50} for i in range(6)]}


def _pools():
    rng = np.random.default_rng(1)
    catch = rng.normal(11, 4, size=300)
    return {"catch": {"WR": catch, "TE": catch, "RB": catch}, "catch_rate": {"WR": 0.64, "TE": 0.68, "RB": 0.75},
            "ypr": {"WR": 12.0, "TE": 10.0, "RB": 8.0}, "carry": rng.normal(4.2, 2, size=300), "ypc": 4.3,
            "source": "test pool"}


def _spec(**team_overrides):
    team = {"opponent": "PIT", "site": "away", "window_games": 6, "season_games_played": 6,
            "produced": {"games": 6, "plays_pg": 60, "pass_att_pg": 32, "rush_att_pg": 25},
            "by_game": [{"week": i + 1, "opp": "vs PIT" if i % 2 == 0 else "@ KC", "wr_targets": 20, "te_targets": 5,
                         "rb_targets": 5, "carries": 25} for i in range(6)],
            "defense_allowed": {"games": 6, "wr_targets_pg": 20, "wr_receptions_pg": 12, "wr_rec_yards_pg": 150,
                                "rb_yards_per_carry": 4.0},
            "snap_share": {"Jaylen Waddle": 0.8, "Javonte Williams": 0.62},
            "depth_chart": {"status": "OK", "as_of": "2026-11-26", "starters": [{"player": "Jaylen Waddle", "slot": "WR"}],
                            "second_string": [{"player": "Javonte Williams", "slot": "RB"}]},
            "injuries": {"official_report": [], "espn_live": []},
            "players": {"receivers": [_receiver()], "rushers": [_rusher()], "quarterbacks": [
                {"player": "B.Nix", "player_id": "qb1", "games": 6, "attempts": 180, "yards": 1400, "td": 8,
                 "log": [{"week": i + 1, "att": 30, "yards": 230} for i in range(6)]}]},
            "baselines": {"status": "BASELINE_RESEARCH_ONLY", "players": [
                {"player": "J.Waddle", "receiving_yards": {"weighted_mean": 999.0}}]}}
    team.update(team_overrides)
    return {"game_id": "2026_12_DEN_PIT", "season": 2026, "week": 12, "home": "PIT", "away": "DEN",
            "as_of": "weeks < 12", "home_spread": 4.5, "pools": _pools(), "teams": {"DEN": team}}


def _player(board, name="J.Waddle"):
    return next(p for t in board["teams"] for p in t["players"] if p["player"] == name)


def test_aliases_join_short_and_full_names():
    assert aliases("Jaylen Waddle") & aliases("J.Waddle")
    assert aliases("J.K. Dobbins") & aliases("J.Dobbins")


def test_projection_ready_stays_false_and_models_stay_distinct():
    board = assemble(_spec(), n=400, seed=89)
    assert board["schema"] == SCHEMA
    assert board["projection_ready"] is False
    ids = {m["id"]: m["invoked"] for m in board["models"]}
    assert ids["dashboard.opportunity.simulate_receiver"] is True
    assert ids["dashboard.opportunity.simulate_rusher"] is True
    assert ids["pregame.packet.player_baselines"] is False
    assert ids["core.possession_engine_v0.opportunity.OpportunityRecorder"] is False
    player = _player(board)
    assert player["projection_ready"] is False
    assert player["projections"]["receiving"]["receiving_yards"]["mean"] != 999.0
    assert board["teams"][0]["separate_models"]["pregame.packet.player_baselines"]["players"][0]["receiving_yards"]["weighted_mean"] == 999.0


def test_receiver_draw_matches_the_engine():
    board = assemble(_spec(), n=500, seed=3)
    proj = _player(board)["projections"]["receiving"]
    inputs = proj["volume"]["engine_inputs"]
    pool = _pools()["catch"]["WR"]
    tg, rec, yds = O.simulate_receiver(exp_targets=inputs["exp_targets"], k=inputs["k"], catch_rate=inputs["catch_rate"],
                                       ypr=inputs["ypr"], pool=pool, n=inputs["n"], seed=inputs["seed"])
    summary = O.summary_receiver(tg, rec, yds, inputs["catch_rate"] * inputs["ypr"])
    assert proj["receptions"]["mean"] == summary["receptions_mean"]
    assert proj["receiving_yards"]["mean"] == summary["yards_mean"]
    assert proj["receiving_yards"]["thresholds"] == summary["yards"]
    assert proj["receptions"]["model"] == "dashboard.opportunity.simulate_receiver"


def test_missing_team_attempts_do_not_invent_a_pass_rate():
    spec = _spec()
    spec["teams"]["DEN"]["produced"] = {"games": 6}
    board = assemble(spec, n=200, seed=1)
    volume = _player(board)["projections"]["receiving"]["volume"]
    assert volume["status"] == "BLOCKED"
    assert "0.55" in volume["reason"]
    assert _player(board)["usage"]["targets"]["count"] == 36


def test_missing_defense_rate_does_not_apply_a_factor():
    spec = _spec()
    spec["teams"]["DEN"]["defense_allowed"] = {}
    board = assemble(spec, n=300, seed=2)
    eff = _player(board)["projections"]["receiving"]["efficiency"]["catch_rate"]
    assert eff["matchup"]["status"] == "BLOCKED"
    assert eff["matchup"]["factor"] is None
    assert _player(board)["projections"]["receiving"]["receiving_yards"]["status"] == "DOWNGRADED"
    raw = O.shrink(24, 36, 0.64, O.PRIOR_TARGETS)
    assert eff["value"] == round(raw, 3)


def test_routes_and_coverage_stay_blocked_without_those_columns():
    board = assemble(_spec(), n=200, seed=1)
    usage = _player(board)["usage"]
    assert usage["routes"]["status"] == "BLOCKED"
    assert usage["route_participation"]["value"] is None
    sit = _player(board)["situational"]
    assert sit["coverage_route_access"]["status"] == "BLOCKED"
    assert sit["third_down"]["status"] == "BLOCKED"
    assert all(t["tag"] != "checkdown" for t in _player(board)["role_tags"])


def test_out_player_is_blocked_and_teammate_bump_is_the_fitted_rule():
    gone = _receiver("p2", "C.Sutton", share=0.20, targets=30)
    stay = _receiver("p1", "J.Waddle", share=0.40, targets=48)
    rows = allocate_receiving([stay, gone], weeks_map=None, out_ids={"p2"}, questionable={})
    by_id = {b["row"]["player_id"]: b for b in rows}
    assert "p2" not in by_id
    assert abs(by_id["p1"]["bump"] - max(O.OUT_TOP_SAME, O.OUT_REST_SAME) * 0.20) < 1e-9
    spec = _spec()
    spec["teams"]["DEN"]["players"]["receivers"] = [stay, gone]
    spec["teams"]["DEN"]["injuries"] = {"official_report": [
        {"player": "Courtland Sutton", "game_status": "Out", "source": "nflverse official report"}], "espn_live": []}
    board = assemble(spec, n=200, seed=1)
    out = _player(board, "C.Sutton")
    assert out["projections"]["receiving"]["receptions"]["status"] == "BLOCKED"
    assert any(w["warning"] == "out" for w in out["warnings"])
    assert _player(board)["share"]["receiving"]["bump"] == round(0.18, 3)


def test_questionable_wr_uses_fitted_factor_and_qb_does_not():
    assert QUESTIONABLE_SNAP_SHARE == {"RB": 0.69, "TE": 0.89, "WR": 0.91}
    text = (ROOT / "research/projections_2026_w12/project.py").read_text()
    assert 'QF = {"RB": 0.69, "TE": 0.89, "WR": 0.91}' in text
    rows = allocate_receiving([_receiver(share=0.40, targets=40)], None, set(), {"p1": "questionable"})
    assert rows[0]["q_factor"] == 0.91
    assert abs(rows[0]["share_used"] - 0.40 * 0.91) < 1e-9
    spec = _spec()
    spec["teams"]["DEN"]["injuries"]["espn_live"] = [
        {"player": "Bo Nix", "position": "QB", "status": "Questionable"},
        {"player": "Jaylen Waddle", "position": "WR", "status": "Questionable"}]
    board = assemble(spec, n=200, seed=1)
    qb = _player(board, "B.Nix")
    assert qb["projections"]["passing"]["status"] == "BLOCKED"
    assert "OpportunityRecorder" in qb["projections"]["passing"]["models_not_invoked"][0]
    assert any("no fitted snap factor" in w["detail"] for w in qb["warnings"])
    wr = _player(board)
    assert wr["share"]["receiving"]["questionable_factor"] == 0.91


def test_checkdown_tag_requires_measured_third_down_targets():
    player = _receiver(avg_depth_of_target=6.0, targets=40)
    assert role_tags(player, None, None, None) == [] or all(t["tag"] != "checkdown" for t in role_tags(player, {}, {}, None))
    sit = {"checkdown_targets": CHECKDOWN_MIN + 4, "third_down_targets_with_air": CHECKDOWN_MIN + 6, "targets": 40}
    tags = {t["tag"] for t in role_tags(player, sit, None, None)}
    assert "checkdown" in tags
    thin = dict(sit, checkdown_targets=2)
    assert "checkdown" not in {t["tag"] for t in role_tags(player, thin, None, None)}


def test_rush_plus_receiving_does_not_treat_a_missing_side_as_zero():
    board = assemble(_spec(), n=200, seed=1)
    joint = _player(board)["projections"]["rush_plus_receiving"]
    assert joint["status"] == "BLOCKED"
    assert "zero" in joint["reason"]


def test_depth_and_snaps_match_full_names_and_do_not_zero_fill():
    board = assemble(_spec(), n=200, seed=1)
    player = _player(board)
    assert player["depth_chart"]["status"] == "starter"
    assert player["snaps"]["offense_snap_share"] == 0.8
    assert player["snaps"]["matched"] == "Jaylen Waddle"
    missing = _player(board, "B.Nix")
    assert missing["snaps"]["status"] == "MISSING"
    assert missing["snaps"]["offense_snap_share"] is None


def test_availability_takes_the_stronger_status():
    official = [{"player": "Jaylen Waddle", "game_status": "Questionable"}]
    espn = [{"player": "J.Waddle", "status": "Out"}]
    assert availability("J.Waddle", official, espn)["state"] == "out"
    assert availability("Nobody", official, espn)["state"] == "not_listed"


def test_situational_counts_use_denominators_and_skip_routes():
    rows = []
    def play(**kw):
        base = {"posteam": "DEN", "defteam": "PIT", "week": 2, "game_id": "g2", "play_type": "pass", "down": 1,
                "pass_attempt": 0, "sack": 0, "qb_hit": 0, "air_yards": None, "yardline_100": 50,
                "receiver_player_id": None, "receiver_player_name": None, "rusher_player_id": None,
                "rusher_player_name": None, "third_down_converted": 0, "third_down_failed": 0, "home_team": "DEN",
                "yards_gained": 0, "complete_pass": 0, "rush_attempt": 0, "qb_scramble": 0}
        base.update(kw)
        rows.append(base)
    play(posteam="OTHER", defteam="PIT", week=1, game_id="g1", pass_attempt=1, complete_pass=1, yards_gained=100,
         receiver_player_id="x", air_yards=10)
    play(pass_attempt=1, air_yards=3, third_down_failed=1, qb_hit=1, receiver_player_id="p1", receiver_player_name="J.Waddle",
         yards_gained=4, complete_pass=1)
    play(pass_attempt=1, air_yards=18, yardline_100=4, receiver_player_id="p1", receiver_player_name="J.Waddle")
    play(play_type="run", rush_attempt=1, yardline_100=3, rusher_player_id="b1", rusher_player_name="J.Williams", yards_gained=2)
    out = measure_situational(pd.DataFrame(rows), {"DEN"}, before_week=12)
    assert out["_meta"]["routes"]["status"] == "BLOCKED"
    assert out["_meta"]["coverage"]["status"] == "BLOCKED"
    p = out["DEN"]["p1"]
    assert p["targets"] == 2
    assert p["team_targets"] == 2
    assert p["third_down_targets"] == 1 and p["checkdown_targets"] == 1
    assert p["goal_line_targets"] == 1 and p["red_zone_targets"] == 1
    assert p["pressure_targets"] == 1 and p["team_pressure_targets"] == 1
    assert p["opponent_pass_yards_allowed_entering"] == 100
    assert out["DEN"]["b1"]["goal_line_carries"] == 1
    assert "targets" not in out["DEN"]["b1"]
    assert "carries" not in out["DEN"]["p1"]
    assert "g1" not in out  # week-1 offense is not DEN; its plays still inform opponent quality


def test_home_away_comes_from_the_game_log_marker():
    board = assemble(_spec(), n=200, seed=1)
    split = _player(board)["trends"]["home_away"]
    assert split["status"] == "OK"
    assert split["home_games"] == 3 and split["away_games"] == 3


def test_historical_packet_replay_blocks_only_the_missing_pieces():
    packet = ROOT / "pregame/packets/2026_12_DEN_PIT/packet.json"
    pbp = ROOT / "data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet"
    rosters = ROOT / "data/historical/nflverse/roster_weekly_2026.parquet"
    snaps = ROOT / "data/historical/nflverse/snaps_2026.parquet"
    if not packet.exists() or not pbp.exists():
        return
    board = replay(packet, pbp_path=pbp, roster_path=rosters, snaps_path=snaps, n=300, seed=89)
    assert board["projection_ready"] is False
    assert board["player_count"] > 10
    assert {t["team"] for t in board["teams"]} == {"DEN", "PIT"}
    modeled = [p for t in board["teams"] for p in t["players"]
               if (p.get("projections") or {}).get("receiving") and (p["projections"]["receiving"].get("receptions") or {}).get("mean") is not None]
    assert modeled, "expected at least one receiver draw from dashboard.opportunity"
    for team in board["teams"]:
        for player in team["players"]:
            assert player["usage"]["routes"]["status"] == "BLOCKED"
            assert player["situational"]["coverage_route_access"]["status"] == "BLOCKED"
            assert player["projections"]["passing"]["status"] == "BLOCKED" or player["projections"]["passing"]["model"] is None
            assert player["projection_ready"] is False
    snap = board["snap_file"]
    assert snap["status"] == "BLOCKED"
    assert snap["on_disk_max_week"] < snap["packet_window_max_week"]
    # A ruled-out skill player, when one is in the packet, does not receive a yard draw.
    outs = [p for t in board["teams"] for p in t["players"] if p["availability"]["state"] == "out"]
    for player in outs:
        rec = (player["projections"].get("receiving") or {}).get("receiving_yards") or {}
        assert rec.get("mean") is None

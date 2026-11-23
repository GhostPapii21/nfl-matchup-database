"""Offline tests for the game board's extra sections. No network."""
import json
from pathlib import Path

import pandas as pd

from dashboard import extras as X
from dashboard.build import render_site


def test_weather_verdict_levels():
    ok = {"status": "OK", "during_game": {"precip_chance_pct_max": 10, "wind_mph_max": 5, "temp_f_min": 50}}
    assert X.weather_verdict(ok, "outdoors")["level"] == "good"
    assert X.weather_verdict(ok, "dome")["headline"].startswith("Indoors")
    storm = {"status": "OK", "during_game": {"precip_chance_pct_max": 80, "wind_mph_max": 18, "temp_f_min": 50}}
    v = X.weather_verdict(storm, "outdoors")
    assert v["level"] == "bad" and v["headline"].startswith("Weather game")
    hurricane = X.weather_verdict(ok, "outdoors", [{"event": "Hurricane Warning", "headline": "Hurricane warning in effect"}])
    assert hurricane["level"] == "bad" and "Hurricane" in hurricane["details"][0]
    assert X.weather_verdict({"status": "UNAVAILABLE"}, "outdoors")["level"] == "unknown"


def _rec(name, pid, share, tgt, rec, yds, adot, rz, log_yds):
    return {"player": name, "player_id": pid, "pos": "WR", "games": len(log_yds), "targets": tgt, "receptions": rec, "yards": yds,
            "td": 1, "target_share": share, "avg_depth_of_target": adot, "red_zone_targets": rz,
            "log": [{"week": i + 1, "targets": tgt // len(log_yds), "receptions": 3, "yards": y} for i, y in enumerate(log_yds)]}


def test_receiver_roles_tags():
    players = {"receivers": [
        _rec("A.One", "1", 0.30, 80, 50, 700, 9.0, 12, [90, 85, 80, 95, 88, 92, 87, 83]),
        _rec("B.Two", "2", 0.20, 56, 30, 500, 15.0, 2, [5, 150, 10, 120, 0, 140, 20, 55]),
    ], "rushers": [
        {"player": "C.Back", "player_id": "3", "pos": "RB", "games": 8, "carries": 140, "yards": 600, "td": 4, "carry_share": 0.7,
         "yards_per_carry": 4.3, "red_zone_carries": 15, "log": [{"week": 1, "carries": 17, "yards": 75}] * 8},
    ]}
    r = X.receiver_roles(players, {"Alpha One": 0.95, "Beta Two": 0.80}, {"1": "Alpha One", "2": "Beta Two"})
    tags = {x["player"]: {t["tag"] for t in x["tags"]} for x in r["receivers"]}
    assert {"Primary", "Red-zone #1", "Steady", "Most on field"} <= tags["A.One"] and "Volume" not in tags["A.One"]
    assert {"Deep threat", "Boom-bust", "Volume"} <= tags["B.Two"]
    rb = {t["tag"] for t in r["rushers"][0]["tags"]}
    assert {"Lead back", "Goal-line back"} <= rb


def test_returning_players_flags_reduced_snaps():
    games = pd.DataFrame([{"game_id": f"g{i}", "season": 2026, "game_type": "REG", "gameday": f"2026-10-0{i}", "home_team": "AAA",
                           "away_team": "BBB", "home_score": 20} for i in range(1, 7)])
    rows = []
    for i in range(1, 7):
        if i not in (3, 4):   # Hurt Guy missed games 3 and 4
            pct = 0.9 if i < 3 else (0.4 if i == 5 else 0.5)
            rows.append({"game_id": f"g{i}", "team": "AAA", "player": "Hurt Guy", "position": "WR", "offense_pct": pct, "defense_pct": 0.0})
        rows.append({"game_id": f"g{i}", "team": "AAA", "player": "Healthy Guy", "position": "WR", "offense_pct": 0.8, "defense_pct": 0.0})
    out = X.returning_players(pd.DataFrame(rows), games, 2026, "AAA", "2026-10-09")
    assert [r["player"] for r in out] == ["Hurt Guy"]
    assert out[0]["status"] == "Working back in" and out[0]["games_missed"] == 2


def test_same_player_matches_abbreviated_names():
    assert X._same_player("J.Love", "Jordan Love")
    assert not X._same_player("C.Wentz", "Kirk Cousins")
    assert not X._same_player(None, "Kirk Cousins")


def test_schedule_context_flags_short_week_and_international():
    games = pd.DataFrame([
        {"game_id": "a", "season": 2026, "week": 9, "gameday": "2026-11-01", "weekday": "Sunday", "home_team": "JAX", "away_team": "HOU",
         "location": "Neutral", "stadium": "Wembley Stadium", "home_score": 20, "away_score": 17},
        {"game_id": "b", "season": 2026, "week": 9, "gameday": "2026-11-02", "weekday": "Monday", "home_team": "SEA", "away_team": "LA",
         "location": "Home", "stadium": "Lumen Field", "home_score": 24, "away_score": 21},
    ])
    g = pd.Series({"season": 2026, "gameday": "2026-11-06", "away_team": "SEA", "home_team": "JAX", "location": "Home", "stadium": "EverBank"})
    pk = {"game": {"away_rest_days": 4, "home_rest_days": 5, "kickoff_et": "13:00"}}
    c = X.schedule_context(games, g, pk)
    seattle = " | ".join(f["text"] for f in c["SEA"]["flags"])
    jax = " | ".join(f["text"] for f in c["JAX"]["flags"])
    assert "Short week" in seattle and "time zones" in seattle and "10:00 AM body clock" in seattle and "Monday" in seattle
    assert "international" in jax and "Short week: 5 days" in jax


def test_render_site_embeds_data_safely():
    html = render_site([{"game": {"note": "</script><b>"}}], "2026-11-13T00:00:00+00:00")
    assert "/*__BOARD_DATA__*/" not in html
    assert "</script><b>" not in html.split("const BOARD = ", 1)[1].split(";\n", 1)[0]
    payload = html.split("const BOARD = ", 1)[1].split(";\n", 1)[0]
    assert json.loads(payload.replace("<\\/", "</"))["built_utc"].startswith("2026-11-13")


def test_template_has_placeholder_once():
    tpl = (Path(__file__).resolve().parents[1] / "template.html").read_text()
    assert tpl.count("/*__BOARD_DATA__*/null") == 1


def test_opportunity_more_volume_means_better_chances():
    import numpy as np
    from dashboard import opportunity as O
    pool = np.array([5.0, 8.0, 12.0, 15.0, 25.0, 40.0])
    lo = O.summary_receiver(*O.simulate_receiver(exp_targets=4, k=8, catch_rate=0.65, ypr=12, pool=pool, n=4000, seed=1), 7.8)
    hi = O.summary_receiver(*O.simulate_receiver(exp_targets=10, k=8, catch_rate=0.65, ypr=12, pool=pool, n=4000, seed=1), 7.8)
    assert hi["yards"]["70"] > lo["yards"]["70"] and hi["targets_mean"] > lo["targets_mean"]
    # the fitted volume correction is applied: 10 raw targets come out below 10
    assert hi["targets_mean"] < 10
    assert hi["targets_needed"]["70"] == 9


def test_opportunity_rain_and_defense_factors_are_bounded():
    from dashboard import opportunity as O
    assert O.def_factor(None, 0.65) == 1.0
    assert 0.8 <= O.def_factor(0.1, 0.65) <= 1.2 and 0.8 <= O.def_factor(5, 0.65) <= 1.2
    p, r = O.script_multipliers(14)                       # refit 2022-24 (research/qb_script_2026-11-22); capped at 10
    assert abs(p - (0.9855 - 0.006)) < 1e-9 and abs(r - (1.0016 + 0.037)) < 1e-9
    assert O.script_multipliers(14) == O.script_multipliers(10)
    assert O.script_multipliers(None) == (1.0, 1.0)


def test_backup_qb_detection():
    from dashboard import opportunity as O
    phi = {"qb": {"player": "Joe Milton III"}, "quarterbacks": [{"player": "J.Hurts", "player_id": "a", "games": 4},
                                                                {"player": "T.McKee", "player_id": "b", "games": 3}]}
    assert O.backup_qb(phi) == {"starter": "Joe Milton III", "usual": "J.Hurts", "usual_games": 4, "starter_recent_starts": None, "veteran": False}
    vet = {"qb": {"player": "Kirk Cousins", "player_id": "c", "recent_starts": 24}, "quarterbacks": [{"player": "K.Murray", "player_id": "m", "games": 5}]}
    assert O.backup_qb(vet)["veteran"] is True                     # changed teams, not a backup: no yards factor
    import pandas as pd
    g = pd.DataFrame({"game_type": "REG", "season": [2025, 2026, 2026, 2026], "week": [3, 2, 9, 12],
                      "home_qb_id": ["c", "x", "c", "c"], "away_qb_id": ["y", "c", "z", "z"]})
    assert O.qb_recent_starts(g, "c", 2026, 11) == 3               # 2025 wk3, 2026 wk2, 2026 wk9; not wk12
    assert O.backup_qb({"qb": {"player": "Jalen Hurts", "player_id": "a"}, "quarterbacks": phi["quarterbacks"]}) is None
    assert O.backup_qb({"qb": {"player": "Jalen Hurts"}, "quarterbacks": phi["quarterbacks"]}) is None      # by last name
    assert O.backup_qb({"qb": {"player": "X", "player_id": "z"}, "quarterbacks": [{"player": "Y", "player_id": "y", "games": 1}]}) is None
    assert O.BACKUP_QB_YARDS < 1


# ------------------------------------------------------------------------------------------- teammate out
def _side(recs, rushers):
    by_game = [{"week": w, "wr_targets": 20, "te_targets": 6, "rb_targets": 6, "carries": 25} for w in (5, 6, 7, 8, 9)]
    return {"offense": "AAA", "defense": "BBB", "offense_produced": {"plays_pg": 62, "pass_att_pg": 34, "rush_att_pg": 25},
            "defense_allowed": {"plays_pg": 62}, "offense_by_game": by_game, "roles": {"receivers": recs, "rushers": rushers}}


def _r(name, pos, share, per_game):
    log = [{"week": w, "targets": per_game, "receptions": int(per_game * 0.65), "yards": per_game * 8} for w in (5, 6, 7, 8, 9)]
    return {"player": name, "full_name": name, "player_id": name, "pos": pos, "targets": per_game * 5, "receptions": int(per_game * 0.65) * 5,
            "yards": per_game * 40, "target_share": share, "log": log}


def _b(name, share, per_game):
    log = [{"week": w, "carries": per_game, "yards": per_game * 4} for w in (5, 6, 7, 8, 9)]
    return {"player": name, "full_name": name, "player_id": name, "pos": "RB", "carries": per_game * 5, "yards": per_game * 20,
            "carry_share": share, "log": log}


def _pools():
    import numpy as np
    one = np.array([3.0, 6.0, 9.0, 12.0, 20.0, 35.0])
    return {"catch": {"WR": one, "TE": one, "RB": one}, "catch_rate": {"WR": 0.62, "TE": 0.7, "RB": 0.78},
            "ypr": {"WR": 12.6, "TE": 10.5, "RB": 7.8}, "carry": np.array([0.0, 2.0, 3.0, 4.0, 5.0, 9.0]), "ypc": 4.3}


def test_missing_receiver_helps_the_top_player_at_his_position_most():
    from dashboard import opportunity as O
    recs = [_r("Star WR", "WR", 0.30, 10), _r("WR Two", "WR", 0.20, 6), _r("WR Three", "WR", 0.10, 3), _r("Tight End", "TE", 0.15, 5)]
    side = _side(recs, [])
    base = {r["player"]: r for r in O.board_side(side, {}, None, _pools(), set())["receivers"]}
    out = {r["player"]: r for r in O.board_side(side, {}, None, _pools(), {"Star WR"})["receivers"]}
    assert out["Star WR"]["status"].startswith("OUT")
    bump = {n: out[n]["inputs"]["injury_bump"] for n in ("WR Two", "WR Three", "Tight End")}
    prop = 0.20 / 0.45                                                        # his slice of the healthy share
    assert abs(bump["WR Two"] - max(O.OUT_TOP_SAME, O.OUT_REST_SAME * prop) * 0.30) < 1e-3
    assert bump["WR Two"] >= O.OUT_TOP_SAME * 0.30                            # top healthy receiver: at least 18% of the missing share
    assert bump["WR Two"] > bump["WR Three"] > 0 and bump["WR Two"] > bump["Tight End"] > 0
    assert sum(bump.values()) < 0.30 * 0.8                                    # less than the old rule: the rest goes to replacements
    assert out["WR Two"]["targets_mean"] > base["WR Two"]["targets_mean"]


def test_missing_lead_back_moves_carries_to_the_next_back():
    from dashboard import opportunity as O
    side = _side([], [_b("Lead Back", 0.70, 17), _b("Backup", 0.20, 5), _b("Third", 0.10, 2)])
    base = {r["player"]: r for r in O.board_side(side, {}, None, _pools(), set())["rushers"]}
    out = {r["player"]: r for r in O.board_side(side, {}, None, _pools(), {"lead back"})["rushers"]}   # names match case-insensitively
    assert out["Lead Back"]["status"].startswith("OUT")
    assert abs(out["Backup"]["inputs"]["injury_bump"] - O.OUT_TOP_RB * 0.70) < 1e-3
    assert out["Backup"]["carries_mean"] > base["Backup"]["carries_mean"] * 1.8
    assert out["Backup"]["inputs"]["carry_share_used"] <= 0.95 and out["Third"]["inputs"]["injury_bump"] > 0


def test_espn_out_beats_a_friday_questionable():
    pk = {"injuries": {"official_report": [{"player": "Lead Back", "position": "RB", "game_status": "Questionable"}],
                       "espn_live": [{"player": "Lead Back", "position": "RB", "status": "Out", "comment": "ruled out"},
                                     {"player": "Other Guy", "position": "WR", "status": "Questionable"}]}}
    rows = {r["player"]: r for r in X.injury_impact(pk, {}, {})}
    assert rows["Lead Back"]["status_level"] == 3 and rows["Other Guy"]["status_level"] == 2


# ------------------------------------------------------------------------------------------- 80-yard watch
def _watch_side(log_t, log_y, share=0.30):
    from dashboard import watch as W
    by_game = [{"week": w, "wr_targets": 24, "te_targets": 6, "rb_targets": 6, "pass_yards": 300} for w in range(1, 9)]
    log = [{"week": w, "targets": t, "yards": y, "receptions": int(t * 0.65)} for w, (t, y) in enumerate(zip(log_t, log_y), 1)]
    rec = {"player": "Star", "full_name": "Star", "player_id": "p1", "pos": "WR", "log": log, "explosive": 10, "games": len(log), "target_share": share}
    opp = {"receivers": [{"player_id": "p1", "player": "Star", "inputs": {"target_share_window": share, "target_share_last3": share, "target_share_used": share, "injury_bump": 0}}], "rushers": []}
    return {"offense": "AAA", "defense": "BBB", "offense_by_game": by_game, "roles": {"receivers": [rec], "rushers": []}, "opportunity": opp,
            "offense_rank": {"pass_yards_pg": {"rank": 1}}}, W


def test_watch_stars_follow_volume_and_game_type():
    model = __import__("dashboard.watch", fromlist=["x"]).load_model()
    assert model and model["stars"] == {"3": 0.5, "2": 0.4, "1": 0.3}
    alpha, W = _watch_side([11, 10, 12, 9, 11, 10, 12, 11], [110, 95, 120, 80, 105, 99, 130, 90])
    low, _ = _watch_side([5, 4, 6, 5, 4, 5, 6, 5], [40, 35, 50, 45, 30, 38, 55, 42])
    dctx = {"BBB": {"games": 9, "ex_rate_rel": 1.0, "g80_WR_pg": 0.5, "g80_TE_pg": 0.1, "g80_rank": 10, "ex_rank": 10}}
    hi = W.watch_side(alpha, {"AAA": 28.0, "BBB": 21.0}, dctx, model)["receivers"][0]
    lo = W.watch_side(low, {"AAA": 28.0, "BBB": 21.0}, dctx, model)["receivers"][0]
    assert hi["tier"] == "alpha" and hi["stars"] >= 2 and hi["p80"] > 0.4 and lo["stars"] == 0 and lo["p80"] < hi["p80"] / 3
    low_team = W.watch_side(alpha, {"AAA": 18.0, "BBB": 24.0}, dctx, model)["receivers"][0]
    assert low_team["p80"] < hi["p80"]                                    # same player, team expected to score less
    stingy = {"BBB": {**dctx["BBB"], "g80_WR_pg": 0.1}}
    assert W.watch_side(alpha, {"AAA": 28.0, "BBB": 21.0}, stingy, model)["receivers"][0]["p80"] < hi["p80"]


def test_watch_skips_players_who_are_out_and_missing_inputs():
    from dashboard import watch as W
    side, _ = _watch_side([8, 9, 10], [70, 80, 90])
    side["opportunity"]["receivers"][0]["status"] = "OUT: no projection"
    model = W.load_model()
    assert W.watch_side(side, {"AAA": 25.0, "BBB": 22.0}, {}, model)["receivers"] == []
    assert W.watch_side(side, None, {}, model) is None and W.watch_side(side, {"AAA": 25.0}, {}, None) is None


def test_blend_with_book_sits_between_the_two_and_is_symmetric():
    from dashboard import watch as W
    b = W.blend_with_book(0.20, 0.40)
    assert 0.20 < b < 0.40 and abs(W.blend_with_book(0.30, 0.30) - 0.30) < 1e-9
    assert abs(W.blend_with_book(0.20, 0.40) - W.blend_with_book(0.40, 0.20)) < 1e-9
    assert W.blend_with_book(0.0, 1.0) > 0 and W.blend_with_book(0.0, 1.0) < 1   # clipped, no log(0)


def test_book_price_matches_names_and_rung():
    from dashboard import watch as W
    rows = [{"book": "fanduel", "market": "alt_receiving_yards", "player": "Ja'Marr Chase", "side": "Over", "line": 79.5, "american": 118, "break_even": 0.4587},
            {"book": "fanduel", "market": "alt_receiving_yards", "player": "Ja'Marr Chase", "side": "Over", "line": 99.5, "american": 250, "break_even": 0.2857}]
    assert W.book_price(rows, "Ja'Marr Chase", "alt_receiving_yards")["american"] == 118
    assert W.book_price(rows, "JaMarr Chase Jr.", "alt_receiving_yards")["break_even"] == 0.4587
    assert W.book_price(rows, "Ja'Marr Chase", "alt_rushing_yards") is None and W.book_price(None, "x", "alt_receiving_yards") is None


def test_watch_rain_and_wind_lower_the_80_yard_chance():
    model = __import__("dashboard.watch", fromlist=["x"]).load_model()
    dctx = {"BBB": {"games": 9, "ex_rate_rel": 1.0, "g80_WR_pg": 0.5, "g80_TE_pg": 0.1, "g80_rank": 10, "ex_rank": 10}}
    dry, W = _watch_side([11, 10, 12, 9, 11, 10, 12, 11], [110, 95, 120, 80, 105, 99, 130, 90])
    wet, _ = _watch_side([11, 10, 12, 9, 11, 10, 12, 11], [110, 95, 120, 80, 105, 99, 130, 90])
    wet["opportunity"]["weather_attempts_multiplier"] = 0.957
    wet["opportunity"]["receivers"][0]["inputs"].update(rain_yards=0.887, rain_catch=0.935)
    a = W.watch_side(dry, {"AAA": 28.0, "BBB": 21.0}, dctx, model)["receivers"][0]
    b = W.watch_side(wet, {"AAA": 28.0, "BBB": 21.0}, dctx, model)["receivers"][0]
    assert b["p80"] < a["p80"] and b["targets"] < a["targets"]
    assert any("rain/wind" in w for w in b["why"]) and not any("rain/wind" in w for w in a["why"])


def test_calibration_lifts_carries_inside_range_only_and_stays_monotonic():
    import numpy as np
    from dashboard import opportunity as O
    cal = O._calibration()
    assert cal["carries"]["enabled"] and not cal["receptions"]["enabled"]
    assert O.calibrate(0.38, "carries", 12) > 0.38                         # the simulation ran low on 12+ carries
    assert O.calibrate(0.38, "carries", 20) == 0.38 and O.calibrate(0.30, "receptions", 4) == 0.30   # outside range / switched off
    car = np.random.default_rng(1).poisson(12, 20000)
    ch = O.chances(car, O.CARRY_THRESHOLDS, "carries")
    vals = [ch[str(t)] for t in sorted(O.CARRY_THRESHOLDS)]
    assert all(a >= b for a, b in zip(vals, vals[1:]))


def test_backs_who_split_starts_are_scaled_back_to_the_team_total():
    from dashboard import opportunity as O
    a = _b("Back One", 0.60, 15)
    b = _b("Back Two", 0.60, 15)
    b["log"] = [{"week": w, "carries": 15, "yards": 60} for w in (5, 6, 9)]       # each started part of the season, both active now
    a["log"] = [{"week": w, "carries": 15, "yards": 60} for w in (7, 8, 9)]
    out = O.board_side(_side([], [a, b]), {}, None, _pools(), set())
    used = [r["inputs"]["carry_share_used"] for r in out["rushers"]]
    sc = out["share_scaling"]
    assert sc["carries_scale"] < 1 and sum(used) <= sc["rb_share_of_team_carries"] + 0.01


def test_players_with_no_recent_snaps_do_not_shrink_the_starters():
    from dashboard import opportunity as O
    a = _b("Starter", 0.60, 15)
    gone = _b("Gone Back", 0.60, 15)
    gone["log"] = [{"week": w, "carries": 15, "yards": 60} for w in (5, 6)]       # no snaps in the last two games
    out = O.board_side(_side([], [a, gone]), {}, None, _pools(), set())
    assert out["share_scaling"]["carries_scale"] == 1.0


def test_watch_split_backfield_lowers_the_lead_back():
    from dashboard import watch as W
    model = W.load_model()
    assert "mate_car" in model["rusher"]["models"]["80"]["coef"]
    def back(pid, car):
        log = [{"week": w, "carries": car, "yards": int(car * 4.6)} for w in range(1, 7)]
        return {"player": pid, "full_name": pid, "player_id": pid, "pos": "RB", "log": log, "yards_pg": car * 4.6}
    def side(backs):
        opp = {"receivers": [], "rushers": [{"player_id": b["player_id"], "player": b["player"], "inputs": {}} for b in backs]}
        return {"offense": "AAA", "defense": "BBB", "offense_by_game": [], "roles": {"receivers": [], "rushers": backs}, "opportunity": opp,
                "defense_allowed": {"rb_rush_yards_pg": 110}}
    imp = {"AAA": 27.0, "BBB": 20.0}
    alone = W.watch_side(side([back("Lead", 20)]), imp, {}, model)["rushers"][0]
    split = [x for x in W.watch_side(side([back("Lead", 20), back("Other", 13)]), imp, {}, model)["rushers"] if x["player"] == "Lead"][0]
    assert split["p80"] < alone["p80"] and any("splits the backfield" in w for w in split["why"])


def test_watch_stars_use_the_blend_when_a_price_exists():
    from dashboard import watch as W
    cuts = {"3": 0.5, "2": 0.4, "1": 0.3}
    e = {"player": "DeVonta Smith", "p80": 0.453, "stars": 2}
    W._attach_price(e, [{"book": "fanduel", "market": "alt_receiving_yards", "player": "DeVonta Smith", "side": "Over", "line": 79.5,
                         "american": 320, "break_even": 0.2381}], "alt_receiving_yards", cuts)
    assert e["stars_model"] == 2 and e["stars"] == 1 and e["book80"]["blend"] < 0.4
    assert any("big disagreement" in w for w in e["why"])
    f = {"player": "Nobody", "p80": 0.45, "stars": 2}
    W._attach_price(f, [], "alt_receiving_yards", cuts)
    assert f["stars"] == 2 and "book80" not in f                     # no price: model stars stand


def test_starting_qb_skips_a_listed_qb_who_is_out():
    import pandas as pd
    from dashboard import build as B
    pbp = pd.DataFrame({"qb_dropback": 1, "posteam": "BAL", "week": [1, 1, 2, 3, 3, 3],
                        "passer_player_name": ["L.Jackson", "L.Jackson", "T.Huntley", "J.Brissett", "J.Brissett", "T.Huntley"]})
    assert B.starting_qb("Tyler Huntley", {"injuries": []}, [], pbp, "BAL", [1, 2, 3]) == "Tyler Huntley"
    tp = {"injuries": [{"player": "Lamar Jackson", "game_status": "Out"}]}
    assert B.starting_qb("Tyler Huntley", tp, ["Tyler Huntley"], pbp, "BAL", [1, 2, 3]) == "J.Brissett"
    packet_shape = {"injuries": {"official_report": [{"player": "Tyler Huntley", "game_status": "Out"}, "junk"], "espn": [{"player": "Lamar Jackson", "status": "Out"}]}}
    assert B.starting_qb("Tyler Huntley", packet_shape, [], pbp, "BAL", [1, 2, 3]) == "J.Brissett"
    assert B._safe_starting_qb("Tyler Huntley", None, [], pbp, "BAL", [1]) == "Tyler Huntley"      # bad input never breaks the build


def test_defensive_gate_and_pressure_note():
    from dashboard import watch as W
    sd = {"defense_rank": {"wr_rec_yards_pg": {"rank": 28, "of": 32, "league_avg": 149.3}, "rb_rush_yards_pg": {"rank": 3, "of": 32}},
          "defense_allowed": {"wr_rec_yards_pg": 181.0},
          "coverage_profile": {"five_plus_rushers_rate": 0.41},
          "qb": {"player": "J.McCarthy", "this_season": {"vs_blitz": {"dropbacks": 60, "yards_per_attempt": 5.1}, "no_blitz": {"yards_per_attempt": 7.0}}}}
    g = W.defensive_gate(sd, "WR")
    assert g["label"] == "soft" and g["rank"] == 28 and g["allowed_pg"] == 181.0
    assert W.defensive_gate(sd, "RB")["label"] == "tough" and W.defensive_gate(sd, "TE") is None
    assert "5+ rushers 41%" in W.pressure_note(sd)
    sd["coverage_profile"]["five_plus_rushers_rate"] = 0.20
    assert W.pressure_note(sd) is None


def test_health_flags_questionable_concussion_returning():
    from dashboard import watch as W
    sd = {"offense_injuries": [{"player": "Brock Bowers", "game_status": "Questionable", "injury": "Concussion"},
                               {"player": "Other Guy", "game_status": "Out", "injury": "Knee"}],
          "returning": [{"player": "Tee Higgins", "unit": "offense", "games_missed": 3, "games_since_return": 0, "snap_pct_before": 0.88,
                         "snap_pct_last_game": 0.0, "status": "Back this week"}]}
    b = W.health_flags(sd, "Brock Bowers")
    assert b["status"] == "Questionable" and b["concussion"] and any("inactives" in n for n in b["notes"])
    h = W.health_flags(sd, "Tee Higgins")
    assert h["returning"]["games_missed"] == 3 and "status" not in h
    assert W.health_flags(sd, "Other Guy") is None and W.health_flags(sd, "Nobody") is None

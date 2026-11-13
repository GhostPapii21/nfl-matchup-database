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

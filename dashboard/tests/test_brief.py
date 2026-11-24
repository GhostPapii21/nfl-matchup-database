"""Game-day brief: weather flag, availability, de-biased reads and the six-pick rules."""
from dashboard import brief as B


def _rec(name, pid, pos, rec_tab, yds_tab, bl, status=None):
    e = {"player": name, "player_id": pid, "pos": pos, "receptions": rec_tab, "yards": yds_tab, "book_lines": bl}
    if status:
        e["status"] = status
    return e


NAMES = ["Alpha One", "Bravo Two", "Charlie Three", "Delta Four", "Echo Five", "Foxtrot Six", "Golf Seven", "Hotel Eight"]


def _board(blitz=0.45):
    lines = lambda r, y: {"receptions": {"fair_line": r, "fair_over": 0.5, "n": 5}, "receiving_yards": {"fair_line": y, "fair_over": 0.5, "n": 5}}
    recs = [_rec(NAMES[i], f"p{i}", "WR", {str(k): max(0.05, 0.9 - 0.12 * k) for k in range(1, 9)},
                 {str(t): max(0.02, 0.95 - 0.009 * t) for t in range(20, 130, 10)}, lines(3.5, 55.5)) for i in range(8)]
    recs[0]["receptions"] = {str(k): min(0.97, 1.0 - 0.06 * k) for k in range(1, 9)}             # clear catches over
    side = {"offense": "AAA", "defense": "BBB",
            "opportunity": {"receivers": recs + [_rec("Hurt Guy", "px", "WR", {}, {}, {}, status="OUT: no projection")], "rushers": []},
            "roles": {"receivers": [{"player_id": "p1", "target_share": 0.28}]},
            "coverage_profile": {"blitz_this_season": {"blitz_rate": blitz, "blitz_rank": 3, "season": 2026}},
            "offense_injuries": [{"player": "Charlie Three", "game_status": "Questionable", "injury": "Ankle"}],
            "watch": {"receivers": [{"player": "Delta Four", "shadow": {"season_share": 0.20, "last_game_share": 0.03}}]},
            "defense_allowed": {}, "defense_rank": {}, "defenders": {"coverage": []}}
    return {"game": {"season": 2026, "away": "AAA", "home": "BBB", "date": "2026-11-26", "kickoff_et": "20:20", "roof": "outdoors"},
            "weather": {"roof": "outdoors", "during_game": {"wind_mph_max": 8, "precip_chance_pct_max": 10}, "url": "https://api.weather.gov/gridpoints/X/1,1/forecast/hourly",
                        "kickoff_utc": "2026-11-27T01:20:00+00:00", "retrieved_utc": "2026-11-26T20:00:00+00:00"},
            "sides": {"AAA_vs_BBB": side}}


def test_weather_flag_from_live_forecast_and_observation():
    def fetch(url):
        if url.endswith("/forecast/hourly"):
            return {"properties": {"periods": [{"startTime": "2026-11-27T01:00:00+00:00", "windSpeed": "17 mph", "probabilityOfPrecipitation": {"value": 60}, "shortForecast": "Rain"}]}}
        if url.endswith("/stations"):
            return {"features": [{"properties": {"stationIdentifier": "KXYZ"}}]}
        return {"properties": {"timestamp": "t", "textDescription": "Light Rain", "windSpeed": {"value": 25.0}}}
    w = B.weather_now(_board(), fetch=fetch)
    assert w["flag"] and "light rain" in w["flag"] and "rain chance now 60%" in w["flag"] and "wind" in w["flag"]
    assert B.weather_now(_board(), offline=True)["flag"] is None
    b = _board(); b["weather"]["roof"] = "dome"
    assert B.weather_now(b)["status"] == "INDOORS"


def test_availability_inactive_questionable_role_in_doubt():
    av = B.availability(_board(), {"AAA": ["Echo Five"]})
    flags = {(a["player"], a["flag"]) for a in av}
    assert ("Echo Five", "INACTIVE") in flags and ("Charlie Three", "QUESTIONABLE") in flags and ("Delta Four", "ROLE IN DOUBT") in flags
    assert not any(a["player"] == "Hurt Guy" for a in av)


def test_reads_remove_slate_lean_and_picks_follow_the_rules():
    b = _board()
    rs = B.reads(b, None)
    assert rs and all(abs(r["model_shift_removed"]) > 0 for r in rs)
    wr0 = [r for r in rs if r["player"] == "Alpha One" and r["market"] == "receptions"][0]
    assert wr0["side"] == "Over"                                    # his catches stand out from the slate
    wr1 = [r for r in rs if r["player"] == "Bravo Two" and r["market"] == "receiving_yards"][0]
    assert any("blitz-heavy" in f for f in wr1["flags"])
    av = B.availability(b, {"AAA": ["Echo Five"]})
    picks = B.six_picks(rs, av)
    names = [p["player"] for p in picks]
    assert len(names) == len(set(names)) and len(picks) <= 3                 # one per player, three per team
    assert "Echo Five" not in names and "Delta Four" not in names
    assert not any(p["player"] == "Bravo Two" and p["market"] == "receiving_yards" and p["side"] == "Over" for p in picks)

"""refs NFL-75 bug hunt.
1. NWS hourly windSpeed can be a range ("10 to 20 mph"); the packet took the LOW end, so a game forecast at
   "10 to 20 mph" never raised the 15 mph wind flag (Rico's weather gate).
2. best_retail_price compared prices across DIFFERENT lines, so a worse number with a better price was labelled
   "best" (W11 PIT@PHI: Barkley rec yds Under 9.5 -112 at DraftKings beat Under 10.5 -114 at FanDuel; 312 of 748
   over/under sides in the committed W10-W11 packets had a better line at another book).
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pregame import odds as O, weather as W  # noqa: E402


def _nws(speeds, gusts=None):
    ko = W.kickoff_utc("2026-11-22", "13:00")
    periods = [{"startTime": (ko + timedelta(hours=h)).isoformat(), "temperature": 40, "windSpeed": s, "windDirection": "W",
                "probabilityOfPrecipitation": {"value": 10}, "shortForecast": "Cloudy"} for h, s in enumerate(speeds)]

    def fetch(url, timeout=30):
        return {"properties": {"forecastHourly": "hourly"}} if "points" in url else {"properties": {"periods": periods}}
    return W.forecast("BUF", "outdoors", "Home", "2026-11-22", "13:00", fetch=fetch)


@pytest.mark.parametrize("speeds,max_wind,flag", [
    (["10 to 20 mph", "5 mph", "5 mph"], 20.0, True),
    (["12 mph", "14 mph", "9 mph"], 14.0, False),
    (["5 to 15 mph"], 15.0, True),
])
def test_wind_range_uses_the_upper_end(speeds, max_wind, flag):
    f = _nws(speeds)
    assert f["status"] == "OK"
    assert f["during_game"]["wind_mph_max"] == max_wind
    assert ("WIND_15_PLUS" in f["flags"]) is flag


def _event(rows):
    return {"bookmakers": [{"key": bk, "markets": [{"key": "player_reception_yds", "outcomes": [
        {"name": "Over", "description": "Saquon Barkley", "point": line, "price": o},
        {"name": "Under", "description": "Saquon Barkley", "point": line, "price": u}]}]} for bk, line, o, u in rows]}


def test_best_price_only_compares_books_at_the_same_line():
    ev = _event([("pinnacle", 10.5, -116, -114), ("fanduel", 10.5, -114, -114), ("betonlineag", 10.5, -114, -114),
                 ("draftkings", 9.5, -112, -112), ("betrivers", 9.5, -110, -121)])
    m = next(iter(O.summarize_event(ev, "PHI", "PIT").values()))
    best = m["best_retail_price"]
    assert best["Under"]["line"] == 10.5 and best["Under"]["book"] in ("fanduel", "betonlineag") and best["Under"]["price"] == -114
    assert best["Over"]["line"] == 10.5 and best["Over"]["price"] == -114
    by = best["Under"]["by_line"]
    assert by[9.5]["book"] == "draftkings" and by[9.5]["price"] == -112 and by[10.5]["price"] == -114


def test_best_price_on_a_split_market_names_no_single_best():
    ev = _event([("fanduel", 10.5, -114, -114), ("draftkings", 9.5, -112, -112)])
    best = next(iter(O.summarize_event(ev, "PHI", "PIT").values()))["best_retail_price"]
    assert best["Over"]["book"] is None and "split" in best["Over"]["note"]
    assert set(best["Over"]["by_line"]) == {9.5, 10.5}


def test_best_price_single_line_unchanged():
    ev = _event([("fanduel", 10.5, -110, -120), ("draftkings", 10.5, -105, -125)])
    best = next(iter(O.summarize_event(ev, "PHI", "PIT").values()))["best_retail_price"]
    assert best["Over"]["book"] == "draftkings" and best["Over"]["price"] == -105 and best["Over"]["break_even"] == round(105 / 205, 4)
    assert best["Under"]["book"] == "fanduel"

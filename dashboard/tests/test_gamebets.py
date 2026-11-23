from dashboard import gamebets as GB, gamemodel as G

T = "2026-11-22T12:00:00+00:00"


def _r(market, side, line, a, book="fanduel"):
    return {"book": book, "market": market, "player": None, "side": side, "line": line, "american": a, "retrieved_utc": T}


def test_outcome_counts_pushes_and_sides():
    nb = G.neighbors(27.0, 20.0)
    w, p, l = G.outcome(nb, "spread", "DET", -7.0, "DET", "TB")
    assert abs(w + p + l - 1) < 1e-9 and p > 0.04                     # 7 is a key number: pushes are common
    w1, p1, l1 = G.outcome(nb, "q1_moneyline", "DET", None, "DET", "TB")
    assert p1 > 0.12 and w1 > l1                                       # quarter ties are frequent; favorite wins more
    o, _, u = G.outcome(nb, "total", "Over", 46.5, "DET", "TB")
    assert 0.25 < o < 0.75


def test_game_finder_shops_price_and_uses_market_anchor():
    rows = [_r("spread", "DET", -3.5, -110, "pinnacle"), _r("spread", "TB", 3.5, -110, "pinnacle"),
            _r("total", "Over", 47.5, -110, "pinnacle"), _r("total", "Under", 47.5, -110, "pinnacle"),
            _r("spread", "Detroit Lions", -3.5, -110), _r("spread", "Tampa Bay Buccaneers", 3.5, 120),   # generous dog price
            _r("total", "Over", 47.5, -110), _r("total", "Under", 47.5, -110)]
    res = GB.game_best_bets(rows, "DET", "TB")
    assert res["implied_points"]["home"] > res["implied_points"]["away"]
    sp = next(p for p in res["picks"] if p["market"] == "spread")
    assert sp["best"]["side"] == "TB" and sp["best"]["american"] == 120 and sp["best"]["book"] == "fanduel"
    assert all(p["best"]["book"] != "pinnacle" for p in res["picks"])


def test_opening_and_untimestamped_quotes_are_flagged_and_get_no_ev():
    """Stale openers (same pull timestamp as live books) are not bettable; neither are quotes with no timestamp."""
    live = [_r("spread", "DET", -6.0, -110, "pinnacle"), _r("spread", "TB", 6.0, -110, "pinnacle"),
            _r("total", "Over", 47.5, -110, "pinnacle"), _r("total", "Under", 47.5, -110, "pinnacle"),
            _r("spread", "Detroit Lions", -6.0, -110), _r("spread", "Tampa Bay Buccaneers", 6.0, -110),
            _r("total", "Over", 47.5, -110), _r("total", "Under", 47.5, -110),
            _r("moneyline", "Detroit Lions", None, -260), _r("moneyline", "Tampa Bay Buccaneers", None, 210)]
    openers = [{"book": "open", "market": "spread", "player": None, "side": "DET", "line": -1.5, "american": -110, "retrieved_utc": T},
               {"book": "open", "market": "spread", "player": None, "side": "TB", "line": 1.5, "american": -110, "retrieved_utc": T},
               {"book": "open", "market": "moneyline", "player": None, "side": "DET", "line": None, "american": -125, "retrieved_utc": T},
               {"book": "open", "market": "moneyline", "player": None, "side": "TB", "line": None, "american": 105, "retrieved_utc": T}]
    # a current-looking but untimestamped generous price must also be dropped
    no_time = {"book": "betrivers", "market": "spread", "player": None, "side": "DET", "line": -6.0, "american": 150}
    res = GB.game_best_bets(live + openers + [no_time], "DET", "TB")
    assert res["implied_points"]["home"] > res["implied_points"]["away"]          # uses the live -6 / 47.5, not open -1.5
    assert all(p["best"]["book"] not in {"open", "pinnacle", "consensus"} for p in res["picks"])
    assert not any(p["best"]["book"] == "open" and p["best"]["line"] == -1.5 for p in res["picks"])
    assert not any(p["best"].get("american") == -125 for p in res["picks"])
    stale = res["stale_quotes"]
    assert all(s["ev_per_dollar"] is None for s in stale)
    reasons = { (s["book"], s["reason"]) for s in stale }
    assert any(b == "open" and "opening line" in r for b, r in reasons)
    assert any(b == "betrivers" and r == "no timestamp" for b, r in reasons)
    # a quote 4 hours older than the live pull is stale even with a timestamp
    old = T.replace("12:00:00", "08:00:00")
    aged = _r("spread", "Tampa Bay Buccaneers", 6.0, 200, "betmgm")
    aged["retrieved_utc"] = old
    res2 = GB.game_best_bets(live + [aged], "DET", "TB")
    assert all(p["best"]["book"] != "betmgm" for p in res2["picks"])
    assert any(s["book"] == "betmgm" and s["ev_per_dollar"] is None and "180 minutes" in (s["reason"] or "") for s in res2["stale_quotes"])


def test_quote_exactly_stale_min_old_is_still_current():
    """A quote pulled exactly STALE_MIN minutes before the newest is still current.

    quote_status uses a strict less-than (t < newest - STALE_MIN), so the 180-minute
    boundary falls on the inclusive/current side: exact equality may carry an EV;
    one second older is stale and gets ev_per_dollar None. That matches the
    'prices pulled 3+ hours before the newest' wording (older than 180 minutes).
    """
    from datetime import datetime, timedelta

    newest = datetime.fromisoformat(T)
    exact = (newest - timedelta(minutes=GB.STALE_MIN)).isoformat()
    older = (newest - timedelta(minutes=GB.STALE_MIN, seconds=1)).isoformat()
    assert GB.STALE_MIN == 180
    assert GB.quote_status({"book": "fanduel", "t": exact}, newest) == (True, None)
    ok, reason = GB.quote_status({"book": "fanduel", "t": older}, newest)
    assert ok is False and "180 minutes" in reason

    def live(book, market, side, line, a, t=T):
        return {"book": book, "market": market, "player": None, "side": side, "line": line,
                "american": a, "retrieved_utc": t}

    rows = [live("pinnacle", "spread", "DET", -6.0, -110), live("pinnacle", "spread", "TB", 6.0, -110),
            live("pinnacle", "total", "Over", 47.5, -110), live("pinnacle", "total", "Under", 47.5, -110),
            live("fanduel", "spread", "Detroit Lions", -6.0, -110), live("fanduel", "spread", "Tampa Bay Buccaneers", 6.0, -110),
            live("fanduel", "total", "Over", 47.5, -110), live("fanduel", "total", "Under", 47.5, -110),
            live("betmgm", "spread", "Tampa Bay Buccaneers", 6.0, 200, exact),  # exactly 180 min old: still current
            live("betrivers", "spread", "Tampa Bay Buccaneers", 6.0, 200, older)]  # one second older: stale, no EV
    res = GB.game_best_bets(rows, "DET", "TB")
    books = {p["best"]["book"] for p in res["picks"]}
    # the exact-boundary 200-price is eligible; the one-second-older twin is not
    assert "betmgm" in books
    assert "betrivers" not in books
    stale = [s for s in res["stale_quotes"] if s["book"] == "betrivers"]
    assert stale and all(s["ev_per_dollar"] is None for s in stale)
    assert all(s["book"] != "betmgm" for s in res["stale_quotes"])


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

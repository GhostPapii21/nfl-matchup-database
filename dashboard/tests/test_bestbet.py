from dashboard import bestbet as B

T = "2026-11-23T16:00:00+00:00"


def _side(rec_yds, recs):
    return {"opportunity": {"receivers": [{"player": "Star Guy", "player_id": "p1", "pos": "WR", "yards": rec_yds, "receptions": recs}], "rushers": []}}


def _r(book, market, side, line, a, t=T, source="direct"):
    return {"book": book, "market": market, "player": "Star Guy", "side": side, "line": line, "american": a, "retrieved_utc": t, "source": source}


YDS = {"40": 0.70, "50": 0.60, "60": 0.50, "70": 0.40, "80": 0.30, "100": 0.15}
RECS = {"3": 0.85, "4": 0.70, "5": 0.55, "6": 0.40, "7": 0.25}


def test_exact_line_probability_interpolates_and_reads_integers():
    assert abs(B.p_over(YDS, 59.5, False) - 0.505) < 0.01
    assert B.p_over(RECS, 4.5, True) == 0.55 and B.p_over(YDS, 30.5, False) is None


def test_best_bet_prefers_better_line_and_price_and_reports_shopping():
    rows = [_r("pinnacle", "receiving_yards", "Over", 64.5, -110), _r("pinnacle", "receiving_yards", "Under", 64.5, -110),
            _r("fanduel", "receiving_yards", "Over", 64.5, -115), _r("fanduel", "receiving_yards", "Under", 64.5, -105),
            _r("draftkings", "receiving_yards", "Over", 59.5, -110), _r("draftkings", "receiving_yards", "Under", 59.5, -110)]
    flat = {"40": 0.72, "50": 0.64, "60": 0.55, "70": 0.45, "80": 0.35, "100": 0.18}     # model agrees with the market at 64.5
    picks = B.side_best_bets(_side(flat, RECS), rows)["picks"]
    p = picks[0]
    assert p["best"]["book"] == "draftkings" and p["best"]["side"] == "Over" and p["best"]["line"] == 59.5   # 5 yards lower, same price
    assert p["best"]["p_market"] > 0.5 and p["vs_fanduel_main"]["ev_gain"] > 0.05
    assert any("StartWho" in f for f in p["flags"])            # line gap via an aggregator: confirm on the book


def test_stale_prices_dropped_and_long_shots_never_picked():
    old = "2026-11-23T10:00:00+00:00"
    rows = [_r("pinnacle", "receptions", "Over", 4.5, -120), _r("pinnacle", "receptions", "Under", 4.5, 100),
            _r("fanduel", "receptions", "Over", 4.5, -125), _r("fanduel", "receptions", "Under", 4.5, 105),
            _r("williamhill_us", "receptions", "Over", 4.5, 300, t=old, source="grok"),          # stale: ignored
            _r("fanduel", "alt_receptions", "Over", 7.5, 900)]                                    # not a modeled alt market
    p = B.side_best_bets(_side(YDS, {**RECS, "5": 0.45}), rows)["picks"][0]
    assert p["best"]["book"] != "williamhill_us" and p["best"]["break_even"] >= B.MIN_BREAK_EVEN


def test_one_sided_ladder_rungs_in_the_main_market_are_never_the_pick():
    rows = [_r("pinnacle", "receptions", "Over", 4.5, -110), _r("pinnacle", "receptions", "Under", 4.5, -110),
            _r("fanduel", "receptions", "Over", 4.5, -110), _r("fanduel", "receptions", "Under", 4.5, -110),
            _r("fanduel", "receptions", "Over", 6.5, 300)]                         # one-sided rung listed under receptions
    picks = B.side_best_bets(_side(YDS, {**RECS, "7": 0.40}), rows)["picks"]
    assert all(p["best"]["line"] == 4.5 for p in picks)

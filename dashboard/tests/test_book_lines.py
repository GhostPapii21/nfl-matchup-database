"""Every book's main yardage line vs the projection."""
from dashboard import book_lines as BL

T = "2026-11-23T20:00:00+00:00"


def _r(book, line, side, a, market="receiving_yards", player="Tee Higgins"):
    return {"book": book, "market": market, "player": player, "line": line, "side": side, "american": a, "retrieved_utc": T}


def test_main_line_is_two_sided_and_nearest_even():
    rows = [_r("draftkings", 76.5, "Over", -115), _r("draftkings", 76.5, "Under", -115),
            _r("draftkings", 70.5, "Over", -160), _r("draftkings", 70.5, "Under", 120),       # second two-sided line, further from even
            _r("draftkings", 90.5, "Over", 200),                                                # one-sided: never the main line
            _r("betmgm", 75.5, "Over", -110), _r("betmgm", 75.5, "Under", -110),
            _r("fanduel", 75.5, "Over", -114), _r("fanduel", 75.5, "Under", -114),
            _r("bovada", 96.5, "Over", -115), _r("bovada", 96.5, "Under", -115),               # far from everyone: outlier
            _r("fanduel", 90, "Over", 250, market="alt_receiving_yards")]
    x = BL.player_lines(rows)["tee higgins"]["receiving_yards"]
    assert x["books"] == {"betmgm": 75.5, "bovada": 96.5, "draftkings": 76.5, "fanduel": 75.5}
    assert x["outliers"] == ["bovada"] and x["median"] == 75.5 and x["n"] == 3 and x["alt_books"] == ["fanduel"]


def test_attach_model_minus_median():
    rows = [_r(b, 75.5, s, -110) for b in ("draftkings", "betmgm") for s in ("Over", "Under")]
    side = {"opportunity": {"receivers": [{"player": "Tee Higgins", "yards_median": 82.0, "receptions_mean": 5.6},
                                          {"player": "Hurt Guy", "status": "OUT: no projection"}], "rushers": []}}
    BL.attach(side, rows)
    e = side["opportunity"]["receivers"][0]["book_lines"]["receiving_yards"]
    assert e["model"] == 82.0 and e["model_minus_median"] == 6.5 and e["books"]["draftkings"] == 75.5
    assert "book_lines" not in side["opportunity"]["receivers"][1]

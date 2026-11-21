import json

from pregame import direct_books as D


def _write(tmp, rows, name="2026_12_KC_BUF", t="2026-11-23T16:30:00Z"):
    (tmp / f"{name}.json").write_text(json.dumps({"retrieved_utc": t, "rows": rows}))


def _r(book, market, player, side, line, a):
    return {"book": book, "market": market, "player": player, "side": side, "line": line, "american": a}


def test_pairs_clean_and_consensus_same_line(tmp_path):
    rows = []
    for bk, o, u in (("fanduel", -115, -105), ("draftkings", -110, -110), ("betmgm", -112, -108), ("bovada", 150, -190)):
        rows += [_r(bk, "receptions", "A B", "Over", 4.5, o), _r(bk, "receptions", "A B", "Under", 4.5, u)]
    rows += [_r("caesars", "receptions", "A B", "Over", 4.5, -200), _r("caesars", "receptions", "A B", "Under", 4.5, 50)]  # invalid odds
    _write(tmp_path, rows)
    blk = D.books_block("2026_12_KC_BUF", "BUF", "KC", ("fanduel", "draftkings", "betmgm", "bovada"), direct=tmp_path, grok=tmp_path / "x")
    m = blk["markets"]["receptions|A B"]
    assert set(m["books"]) == {"fanduel", "draftkings", "betmgm"}            # bovada dropped as an outlier, caesars invalid odds
    assert any(d["book"] == "bovada" for d in blk["dropped"])
    assert m["consensus"]["line"] == 4.5 and m["consensus"]["n_books_at_line"] == 3
    assert abs(sum(m["consensus"]["no_vig"].values()) - 1) < 1e-6


def test_hold_guard_and_stamp_is_oldest_required_book(tmp_path):
    rows = [_r("fanduel", "total", None, "Over", 47.5, -110), _r("fanduel", "total", None, "Under", 47.5, -110),
            _r("draftkings", "total", None, "Over", 47.5, -150), _r("draftkings", "total", None, "Under", 47.5, -150)]   # hold 20%
    _write(tmp_path, rows)
    (tmp_path / "g").mkdir()
    (tmp_path / "g" / "2026_12_KC_BUF.json").write_text(json.dumps({"books": {"betmgm": {"retrieved_utc": "2026-11-23T15:00:00Z"}}, "rows": [
        _r("betmgm", "total", None, "Over", 47.5, -108), _r("betmgm", "total", None, "Under", 47.5, -112)]}))
    blk = D.books_block("2026_12_KC_BUF", "BUF", "KC", ("fanduel", "betmgm"), direct=tmp_path, grok=tmp_path / "g")
    assert "draftkings" not in blk["markets"]["total"]["books"]
    assert blk["retrieved_utc"] == "2026-11-23T15:00:00Z"                  # the stalest required book sets the age


def test_spread_stored_from_home_side(tmp_path):
    _write(tmp_path, [_r("fanduel", "spread", None, "Kansas City Chiefs", 3.0, -115), _r("fanduel", "spread", None, "Buffalo Bills", -3.0, -105)])
    blk = D.books_block("2026_12_KC_BUF", "BUF", "KC", ("fanduel",), direct=tmp_path, grok=tmp_path / "x")
    assert blk["markets"]["spread"]["books"]["fanduel"]["line"] == -3.0

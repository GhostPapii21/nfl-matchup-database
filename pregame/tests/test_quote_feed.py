"""The free direct-lines freeze must be readable by the gate, the snapshot locker and the pristine evaluator (NFL-49 P1)."""
import json

from pipeline import hooks as H
from pregame import direct_books as D
from snapshots import lock as L

T = "2026-11-22T16:30:00+00:00"


def _rows():
    rows = []
    for bk, sp_home, tot in (("fanduel", -115, -110), ("draftkings", -110, -112), ("betmgm", -105, -108), ("williamhill_us", -112, -109),
                             ("consensus", -110, -110)):
        rows += [{"book": bk, "market": "spread", "player": None, "side": "DAL", "line": -7.5, "american": sp_home},
                 {"book": bk, "market": "spread", "player": None, "side": "TEN", "line": 7.5, "american": -105},
                 {"book": bk, "market": "total", "player": None, "side": "Over", "line": 55.0, "american": tot},
                 {"book": bk, "market": "total", "player": None, "side": "Under", "line": 55.0, "american": -110},
                 {"book": bk, "market": "moneyline", "player": None, "side": "DAL", "line": None, "american": -350},
                 {"book": bk, "market": "moneyline", "player": None, "side": "TEN", "line": None, "american": 290}]
    rows += [{"book": "bovada", "market": "receptions", "player": "A B", "side": "Over", "line": 4.5, "american": -110},
             {"book": "bovada", "market": "receptions", "player": "A B", "side": "Under", "line": 4.5, "american": -110}]
    return rows


def _freeze(tmp_path):
    (tmp_path / "2026_11_TEN_DAL.json").write_text(json.dumps({"retrieved_utc": T, "rows": _rows()}))
    blk = D.books_block("2026_11_TEN_DAL", "DAL", "TEN", ("fanduel", "draftkings", "betmgm", "williamhill_us"), direct=tmp_path, grok=tmp_path / "x")
    return D.write_freeze("2026_11_TEN_DAL", "2026-11-22", "TEN", "DAL", blk, tmp_path / "fz", sources=[tmp_path / "2026_11_TEN_DAL.json"])


def test_freeze_rows_are_in_the_locker_format(tmp_path):
    f = _freeze(tmp_path)
    d = json.loads(f.read_text())
    ml = L.market_lines(d, "Dallas Cowboys", "Tennessee Titans")
    assert {r["book"] for r in ml["spreads"]} >= {"fanduel", "draftkings", "betmgm", "williamhill_us"}
    sp = next(r for r in ml["spreads"] if r["book"] == "fanduel")
    assert sp["side_a"] == "Tennessee Titans" and sp["line"] == 7.5 and sp["price_a"] == -105        # away side's view
    assert all(r["reference_only"] for r in ml["spreads"] if r["book"] == "consensus")
    assert d["meta"]["books"] == ["betmgm", "draftkings", "fanduel", "williamhill_us"]
    assert len(d["meta"]["raw_sha256"]) == 64 and d["meta"]["source_files"][0]["sha256"]


def test_gate_counts_only_books_with_game_lines(tmp_path):
    f = _freeze(tmp_path)
    d = json.loads(f.read_text())
    d["rows"] = [r for r in d["rows"] if r["book"] != "williamhill_us"] + [
        {"book": "williamhill_us", "market": "receptions|A B", "player": "prop", "reference_only": False}]    # props only
    f.write_text(json.dumps(d))
    pk = {"game": {"away": "TEN", "home": "DAL", "date": "2026-11-22"}}
    res = H.four_book_prices(pk, base=tmp_path / "fz")
    assert res["status"] == "OK" and "williamhill_us" not in res["books"] and "bovada" not in res["books"]

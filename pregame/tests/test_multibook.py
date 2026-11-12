"""Offline tests for the price feed in pregame/odds.py (consensus, labels, matching, floor) and the multibook CLI."""
import json

import pytest

from pregame import odds as O

HOME, AWAY = "New York Giants", "Washington Commanders"


def _game_book(key, home_pt, total):
    return {"key": key, "markets": [
        {"key": "spreads", "outcomes": [{"name": HOME, "price": -110, "point": home_pt}, {"name": AWAY, "price": -110, "point": -home_pt}]},
        {"key": "totals", "outcomes": [{"name": "Over", "price": -105, "point": total}, {"name": "Under", "price": -115, "point": total}]}]}


def _prop_book(key, lines):
    oc = []
    for (market, player), (pt, po, pu) in lines.items():
        oc_m = [{"name": "Over", "description": player, "price": po, "point": pt}, {"name": "Under", "description": player, "price": pu, "point": pt}]
        oc.append((market, oc_m))
    by = {}
    for market, o in oc:
        by.setdefault(market, []).extend(o)
    return {"key": key, "markets": [{"key": k, "outcomes": v} for k, v in by.items()]}


def _event(caesars_props=False):
    props = {("player_reception_yds", "Malik Nabers"): (66.5, -113, -113), ("player_pass_yds", "Jayden Daniels"): (215.5, -110, -110),
             ("player_rush_yds", "Cam Skattebo"): (56.5, -115, -105), ("player_receptions", "Mike Williams"): (2.5, -110, -110)}
    bms = [_game_book("fanduel", -1.5, 41.5), _game_book("draftkings", -2.5, 40.5), _game_book("hardrockbet", -2.0, 41.0),
           _game_book("williamhill_us", -2.0, 41.0), _game_book("pinnacle", -2.5, 40.5)]
    dk_props = dict(props); dk_props[("player_reception_yds", "Malik Nabers")] = (68.5, -110, -114)
    hr_props = dict(props); hr_props[("player_reception_yds", "Malik Nabers")] = (68.5, -115, -115)
    hr_props[("player_rush_yds", "Cam Skattebo")] = (55.5, -110, -110)
    bms += [_prop_book("fanduel", props), _prop_book("draftkings", dk_props), _prop_book("hardrockbet", hr_props), _prop_book("pinnacle", props)]
    if caesars_props:
        bms.append(_prop_book("williamhill_us", props))
    return {"id": "ev1", "home_team": HOME, "away_team": AWAY, "commence_time": "2026-11-13T01:15:00Z", "bookmakers": bms}


PACKET = {"teams": {
    "NYG": {"depth_chart": {"starters": [{"player": "Malik Nabers"}, {"player": "Cam Skattebo"}], "second_string": [{"player": "M.Fields"}]},
            "injuries": {"official_report": [{"player": "Cam Skattebo"}], "espn_live": []}},
    "WAS": {"depth_chart": {"starters": [{"player": "Jayden Daniels"}, {"player": "Mike Williams"}], "second_string": []},
            "injuries": {"official_report": [], "espn_live": [{"player": "Mike Williams"}]}}}}


def _cons(**kw):
    mk = O.summarize_event(_event(**kw), "NYG", "WAS")
    return O.consensus(mk, O.roster_from_packet(PACKET))


# --- 3: consensus only from books at the same line ---------------------------------------------------------------

def test_split_lines_use_only_books_at_the_modal_line():
    c = _cons()["receiving_yards|Malik Nabers"]          # FD 66.5, DK 68.5, HR 68.5 -> 68.5 with 2 books
    assert c["consensus"]["line"] == 68.5 and c["consensus"]["n_books_at_line"] == 2
    assert c["consensus"]["books_at_line"] == ["draftkings", "hardrockbet"]
    assert c["consensus"]["books_off_line"] == {"fanduel": 66.5}
    # the no-vig is the mean of the two 68.5 books only, never FanDuel's 66.5
    dk, hr = O.devig(-110, -114)[0], O.devig(-115, -115)[0]
    assert c["consensus"]["no_vig"]["Over"] == pytest.approx((dk + hr) / 2, abs=1e-4)
    sk = _cons()["rushing_yards|Cam Skattebo"]           # FD 56.5, DK 56.5, HR 55.5 -> 56.5 (2)
    assert sk["consensus"]["n_books_at_line"] == 2


def test_even_split_and_all_different_lines_are_no_consensus():
    mk = O.summarize_event(_event(), "NYG", "WAS")
    # spread: FD -1.5, DK -2.5, HR -2, CZR -2 -> -2 with 2 books (HR, CZR)
    cons = O.consensus(mk, {})
    assert cons["spread"]["consensus"]["line"] == -2.0 and cons["spread"]["consensus"]["n_books_at_line"] == 2
    # make every retail book hang a different total
    for bk, ln in zip(O.RETAIL, (40.5, 41.0, 41.5, 42.0)):
        mk["total"]["books"][bk]["line"] = ln
    c = O.consensus(mk, {})["total"]
    assert c["consensus"] == "no consensus" and "fewer than 2 books share a line" in c["reason"]
    # 2 v 2 tie between lines is also refused
    for bk, ln in zip(O.RETAIL, (40.5, 40.5, 41.0, 41.0)):
        mk["total"]["books"][bk]["line"] = ln
    c = O.consensus(mk, {})["total"]
    assert c["consensus"] == "no consensus" and "split evenly" in c["reason"]


def test_one_book_case_is_no_consensus():
    mk = O.summarize_event(_event(), "NYG", "WAS")
    for bk in ("draftkings", "hardrockbet", "williamhill_us"):
        mk["spread"]["books"].pop(bk)
    c = O.consensus(mk, {})["spread"]
    assert c["n_books_quoting"] == 1 and c["label"] == "one-book game-line consensus"
    assert c["consensus"] == "no consensus" and "fewer than 2 books" in c["reason"]
    assert c["reference"]["book"] == "pinnacle"                     # shown, never counted


# --- 4: labels carry the true book count; Caesars without props is 'no props' ------------------------------------

def test_book_count_labels_and_no_props():
    cons = _cons()
    assert cons["spread"]["label"] == "four-book game-line consensus"
    nab = cons["receiving_yards|Malik Nabers"]
    assert nab["label"] == "three-book prop consensus" and nab["n_books_quoting"] == 3
    assert nab["book_lines"]["williamhill_us"] == "no props"
    cons2 = _cons(caesars_props=True)
    assert cons2["receiving_yards|Malik Nabers"]["label"] == "four-book prop consensus"


def test_pass_yards_kept_as_reference_never_a_leg():
    c = _cons()["passing_yards|Jayden Daniels"]
    assert c["never_a_leg"] is True and "banned" in c["never_a_leg_reason"]


# --- 5: full name + team, fail closed ------------------------------------------------------------------------------

def test_match_on_full_name_and_team():
    r = O.roster_from_packet(PACKET)
    assert O.match_player("Malik Nabers", r) == {"status": "MATCHED", "team": "NYG", "reason": None}
    assert O.match_player("Cam Skattebo", r)["team"] == "NYG"
    assert O.match_player("Malachi Fields", r)["status"] == "UNMATCHED"      # 'M.Fields' abbreviation is never used
    assert O.norm_name("D'Andre Swift Jr.") == "dandre swift"
    r2 = O.roster_from_packet({"teams": {"MIN": {"depth_chart": {"starters": [{"player": "J.J. McCarthy"}]}}}})
    assert O.match_player("J.J. McCarthy", r2)["team"] == "MIN" and O.match_player("JJ McCarthy", r2)["team"] == "MIN"


def test_ambiguous_names_fail_closed():
    pk = json.loads(json.dumps(PACKET))
    pk["teams"]["NYG"]["depth_chart"]["second_string"].append({"player": "Mike Williams"})   # same name on both teams
    r = O.roster_from_packet(pk)
    assert O.match_player("Mike Williams", r)["status"] == "AMBIGUOUS"
    mk = O.summarize_event(_event(), "NYG", "WAS")
    c = O.consensus(mk, r)["receptions|Mike Williams"]
    assert c["consensus"] == "no consensus" and "failed closed" in c["reason"]
    pk2 = json.loads(json.dumps(PACKET))
    pk2["teams"]["WAS"]["injuries"]["espn_live"] = [{"player": "Mike Williams Jr."}]       # two spellings on one team
    assert O.match_player("Mike Williams", O.roster_from_packet(pk2))["status"] == "AMBIGUOUS"


# --- credit floor and the single pull path ------------------------------------------------------------------------

class Fake:
    def __init__(self, remaining):
        self.remaining, self.urls = remaining, []

    def __call__(self, url, timeout=30):
        self.urls.append(url.split("?")[0])
        if url.split("?")[0].endswith("/events"):
            cost, body = 0, [{"id": "ev1"}]
        elif "/events/" in url:
            cost, body = 7, _event()
        else:
            cost, body = 3, [_event()]
        self.remaining -= cost
        O.QUOTA.update(credits_remaining=self.remaining, last_call_cost=cost)
        return body


def test_floor_refuses_paid_call_and_reads_free_balance(monkeypatch):
    monkeypatch.setattr(O, "QUOTA", {}); monkeypatch.setattr(O, "CREDIT_LOG", [])
    f = Fake(802)
    r = O.fetch_game_lines(key="k", fetch=f, floor=800)
    assert r["status"].startswith("SKIPPED_CREDIT_FLOOR") and f.urls[-1].endswith("/events")
    O.CREDIT_LOG.clear()
    f2 = Fake(1865)
    ok = O.fetch_game_lines(key="k", fetch=f2, floor=800)
    assert ok["status"] == "OK" and O.CREDIT_LOG[-1]["estimate_credits"] == 3
    pr = O.fetch_props("ev1", key="k", fetch=f2, floor=800)
    assert pr["status"] == "OK" and O.CREDIT_LOG[-1]["estimate_credits"] == 7
    assert O.credit_line() == "odds credits used this run=10 remaining=1855"


def test_unknown_balance_fails_closed(monkeypatch):
    monkeypatch.setattr(O, "QUOTA", {}); monkeypatch.setattr(O, "CREDIT_LOG", [])
    r = O.fetch_game_lines(key="k", fetch=lambda url, timeout=0: [], floor=800)
    assert r["status"].startswith("SKIPPED_UNKNOWN_BALANCE")
    assert O.credit_line() == "odds credits used this run=unknown remaining=unknown"


def test_freeze_and_movement_vs_schema1(tmp_path, monkeypatch):
    monkeypatch.setattr(O, "CREDIT_LOG", [])
    mk = O.summarize_event(_event(), "NYG", "WAS")
    cons = O.consensus(mk, O.roster_from_packet(PACKET))
    m = O.write_freeze("2026_10_WAS_NYG", "WAS", "NYG", mk, cons, {"x": 1}, tmp_path)
    fz = json.loads(open(m["files"][1]).read())
    assert fz["meta"]["schema"] == "price-freeze/2" and fz["meta"]["projection_ready"] is False
    assert "no consensus" in open(m["files"][2]).read() or "three-book" in open(m["files"][2]).read()
    old = {"rows": [{"book": "fanduel", "market": "spreads", "player": None, "line": 1.5, "side_a": AWAY, "side_b": HOME,
                     "price_a": 100, "price_b": -120, "novig_a": 0.478, "novig_b": 0.522}]}
    mv = O.movement_vs_freeze(mk, old)
    fd = next(r for r in mv if r["market"] == "spread" and r["book"] == "fanduel")
    assert fd["then_line"] == -1.5 and fd["now_line"] == -1.5 and fd["line_move"] == 0

"""Offline tests for pregame.multibook (no network; fake client)."""
import json
from datetime import datetime, timezone

import pytest

from pregame import multibook as mb

HOME, AWAY = "New York Giants", "Washington Commanders"


def _bm(key, spread_home, ph, pa, total, po, pu, ml_home, ml_away):
    return {"key": key, "markets": [
        {"key": "h2h", "outcomes": [{"name": HOME, "price": ml_home}, {"name": AWAY, "price": ml_away}]},
        {"key": "spreads", "outcomes": [{"name": HOME, "price": ph, "point": spread_home},
                                        {"name": AWAY, "price": pa, "point": -spread_home}]},
        {"key": "totals", "outcomes": [{"name": "Over", "price": po, "point": total},
                                       {"name": "Under", "price": pu, "point": total}]}]}


def _props(key):
    return {"key": key, "markets": [
        {"key": "player_rush_yds", "outcomes": [
            {"name": "Over", "description": "Cam Skattebo", "price": -115, "point": 62.5},
            {"name": "Under", "description": "Cam Skattebo", "price": -105, "point": 62.5},
            {"name": "Over", "description": "Brian Robinson", "price": -110, "point": 30.5},
            {"name": "Under", "description": "Brian Robinson", "price": -110, "point": 30.5}]},
        {"key": "player_reception_yds", "outcomes": [
            {"name": "Over", "description": "Malik Nabers", "price": -110, "point": 70.5},
            {"name": "Under", "description": "Malik Nabers", "price": -110, "point": 70.5},
            {"name": "Over", "description": "Mike Williams", "price": -110, "point": 20.5},
            {"name": "Under", "description": "Mike Williams", "price": -110, "point": 20.5}]}]}


class FakeClient(mb.Client):
    def __init__(self, remaining=1870, books=mb.ALL_BOOKS):
        super().__init__(key="test-key-not-real", opener=self._fake)
        self.remaining, self.books, self.urls = remaining, books, []

    def _fake(self, url):
        self.urls.append(url)
        if url.split("?")[0].endswith("/events"):
            body = [{"id": "ev1", "home_team": HOME, "away_team": AWAY, "commence_time": "2026-11-13T01:15:00Z"}]
            cost = 0
        else:
            markets = url.split("markets=")[1].split("&")[0]
            if "h2h" in markets:
                bms = [_bm(b, -2.5, -110, -110, 41.5, -105, -115, -135, 115) for b in self.books]
                cost = 3
            else:
                bms = [_props(b) for b in self.books]
                cost = 2
            body = {"id": "ev1", "home_team": HOME, "away_team": AWAY, "bookmakers": bms}
        self.remaining -= cost
        return {"x-requests-remaining": str(self.remaining), "x-requests-last": str(cost)}, json.dumps(body).encode()


NOW = datetime(2026, 11, 12, 16, 30, tzinfo=timezone.utc)


def test_cost_estimate_and_floor():
    assert mb.estimate_cost(3, 5) == 3
    assert mb.estimate_cost(2, 11) == 4
    assert mb.floor_check(805, 5, 800)[0] is True
    assert mb.floor_check(804, 5, 800)[0] is False
    assert mb.floor_check(None, 5, 800)[0] is False  # unknown balance fails closed


def test_multiplicative_devig_sums_to_one():
    rows = mb.normalize({"home_team": HOME, "away_team": AWAY, "bookmakers": [_bm("fanduel", -2.5, -110, -110, 41.5, -105, -115, -135, 115)]}, "NYG", "WAS")
    for r in rows:
        assert abs(r["novig_a"] + r["novig_b"] - 1) < 1e-3
        assert r["hold"] > 0
    sp = [r for r in rows if r["market"] == "spreads"][0]
    assert sp["side_a"] == AWAY and sp["line"] == 2.5


def test_full_run_writes_freeze_and_never_the_key(tmp_path):
    c = FakeClient()
    meta = mb.run(out=str(tmp_path), client=c, now=NOW)
    assert meta["status"] == "OK" and meta["credits_used_this_run"] == 5
    assert meta["projection_ready"] is False
    files = list(tmp_path.rglob("*"))
    assert any(f.name.startswith("freeze_") for f in files)
    for f in files:
        if f.is_file():
            assert "test-key-not-real" not in f.read_text()
    freeze = json.loads(next(f for f in files if f.name.startswith("freeze_")).read_text())
    players = {r["player"] for r in freeze["rows"] if r["player"]}
    assert players == {"Cam Skattebo", "Malik Nabers"}  # Mike Williams rejected (A. Williams wanted)
    cons = {(c_["market"], c_["player"]): c_ for c_ in meta["consensus"]}
    assert cons[("spreads", None)]["books_quoting"] == sorted(mb.TARGET_BOOKS)
    assert cons[("spreads", None)]["pinnacle_line"] == 2.5


def test_floor_skips_paid_calls(tmp_path):
    c = FakeClient(remaining=801)
    meta = mb.run(out=str(tmp_path), client=c, now=NOW)
    assert all(s["status"] == "SKIPPED_CREDIT_FLOOR" for s in meta["steps"])
    assert len(c.urls) == 1  # only the free /events call


def test_missing_book_is_reported_not_invented(tmp_path):
    c = FakeClient(books=("fanduel", "draftkings", "pinnacle"))
    meta = mb.run(out=str(tmp_path), client=c, now=NOW)
    sp = [x for x in meta["consensus"] if x["market"] == "spreads"][0]
    assert sp["books_missing"] == ["hardrockbet", "williamhill_us"]


def test_started_game_refused(tmp_path):
    meta = mb.run(out=str(tmp_path), client=FakeClient(), now=datetime(2026, 11, 13, 2, 0, tzinfo=timezone.utc))
    assert meta["status"].startswith("IN_PLAY")


def test_no_key():
    assert mb.run(client=mb.Client(key="")) ["status"].startswith("NO_KEY")

"""Pregame packet builder: metric definitions, slate selection, fail-closed sources, JSON safety."""
import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pregame import build_packets as B, metrics as M, packet as PK, render as R, sources as S  # noqa: E402


def play(gid, off, dfn, **kw):
    base = dict(play_id=play.n, game_id=gid, posteam=off, defteam=dfn, play_type="pass", down=1, qtr=1, yards_gained=0, sack=0, qb_scramble=0,
                qb_dropback=0, pass_attempt=0, complete_pass=0, pass_touchdown=0, interception=0, fumble_lost=0, qb_hit=0, air_yards=None,
                rush_attempt=0, rush_touchdown=0, receiver_player_id=None, receiver_player_name=None, rusher_player_id=None,
                rusher_player_name=None, passer_player_id=None, passer_player_name=None, epa=0.0, third_down_converted=0,
                third_down_failed=0, score_differential=0, yardline_100=60, fixed_drive=1, fixed_drive_result="Punt",
                run_location=None, run_gap=None, two_point_attempt=0)
    play.n += 1
    base.update(kw)
    return base
play.n = 1


def pass_(gid, off, dfn, rec, yards, complete=True, air=5, **kw):
    return play(gid, off, dfn, qb_dropback=1, pass_attempt=1, complete_pass=int(complete), yards_gained=yards if complete else 0, air_yards=air,
                receiver_player_id=rec, receiver_player_name=rec, passer_player_id="QB1", passer_player_name="QB1", **kw)


def run_(gid, off, dfn, who, yards, **kw):
    return play(gid, off, dfn, play_type="run", rush_attempt=1, yards_gained=yards, rusher_player_id=who, rusher_player_name=who,
                run_location="left", run_gap="end", **kw)


@pytest.fixture
def world():
    rost = pd.DataFrame([dict(gsis_id=i, position=p, week=1, team="AAA", full_name=i, status="ACT") for i, p in
                         (("WR1", "WR"), ("TE1", "TE"), ("RB1", "RB"), ("FB1", "FB"), ("QB1", "QB"))])
    rows = [
        pass_("g1", "AAA", "BBB", "WR1", 25),                       # explosive pass to a WR
        pass_("g1", "AAA", "BBB", "WR1", 19),                       # 19 is not explosive
        pass_("g1", "AAA", "BBB", "TE1", 8),
        pass_("g1", "AAA", "BBB", "TE1", 0, complete=False),        # TE target, incomplete
        pass_("g1", "AAA", "BBB", "FB1", 4),                        # fullback counts as RB
        play("g1", "AAA", "BBB", qb_dropback=1, pass_attempt=1, sack=1, yards_gained=-7, passer_player_id="QB1", passer_player_name="QB1"),
        play("g1", "AAA", "BBB", play_type="run", qb_dropback=1, qb_scramble=1, rush_attempt=1, yards_gained=16, rusher_player_id="QB1", rusher_player_name="QB1"),
        run_("g1", "AAA", "BBB", "RB1", 15),                        # explosive run
        run_("g1", "AAA", "BBB", "RB1", 3),
        run_("g1", "AAA", "BBB", "RB1", 2, down=None),              # no down = two-point try / untimed: excluded
        pass_("g1", "AAA", "BBB", "WR1", 30, two_point_attempt=1),  # two-point try: excluded
        play("g1", "AAA", "BBB", play_type="qb_kneel", rush_attempt=1, yards_gained=-1),
    ]
    pbp = pd.DataFrame(rows)
    games = pd.DataFrame([dict(game_id="g1", season=2026, week=1, gameday="2026-09-10", home_team="BBB", away_team="AAA", home_score=10, away_score=24)])
    return pbp, rost, games


def test_metric_definitions(world):
    pbp, rost, games = world
    p = M.prepare(pbp, rost)
    assert len(p) == 9                                              # kneel, no-down and two-point rows dropped
    d = M.summarize(M.team_games(p, games, "defteam"))
    assert d["games"] == 1 and d["points_pg"] == 24                 # BBB's defence allowed AAA's 24
    assert d["wr_rec_yards_pg"] == 44 and d["wr_receptions_pg"] == 2 and d["wr_targets_pg"] == 2
    assert d["te_rec_yards_pg"] == 8 and d["te_targets_pg"] == 2 and d["te_receptions_pg"] == 1
    assert d["rb_rec_yards_pg"] == 4                                # FB mapped to RB
    assert d["explosive_pass"] == 1                                 # 25 yes, 19 no
    assert d["explosive_rush"] == 2                                 # 15-yard run and 16-yard scramble
    assert d["rush_yards_pg"] == 18 and d["rush_att_pg"] == 2       # scramble is not a designed carry
    assert d["qb_rush_yards_pg"] == 16
    assert d["sacks"] == 1 and d["sack_rate"] == pytest.approx(1 / 7)   # 5 passes + sack + scramble = 7 dropbacks
    assert d["pass_att_pg"] == 5 and d["completions_pg"] == 4       # the sack is not an attempt
    assert d["blitz_rate"] is None                                  # no charting supplied: unknown, not zero
    o = M.summarize(M.team_games(p, games, "posteam"))
    assert o["points_pg"] == 24 and o["wr_rec_yards_pg"] == 44


def test_ranks_direction():
    lg = pd.DataFrame({"points_pg": {"A": 10.0, "B": 30.0}, "sack_rate": {"A": 0.10, "B": 0.02}})
    assert M.ranks(lg, "A", defense=True)["points_pg"]["rank"] == 1     # fewest points allowed = best defence
    assert M.ranks(lg, "B", defense=False)["points_pg"]["rank"] == 1    # most points scored = best offence
    assert M.ranks(lg, "A", defense=True)["sack_rate"]["rank"] == 1     # most sacks = best pass rush
    assert M.ranks(lg, "B", defense=False)["sack_rate"]["rank"] == 1    # fewest sacks allowed = best protection


def test_slate_selection():
    g = pd.DataFrame([
        dict(game_id="a", season=2026, game_type="REG", week=10, gameday="2026-11-12", weekday="Thursday", gametime="20:15", home_score=None),
        dict(game_id="b", season=2026, game_type="REG", week=10, gameday="2026-11-14", weekday="Saturday", gametime="13:00", home_score=None),
        dict(game_id="c", season=2026, game_type="REG", week=10, gameday="2026-11-16", weekday="Monday", gametime="20:15", home_score=None),
        dict(game_id="d", season=2026, game_type="REG", week=11, gameday="2026-11-19", weekday="Thursday", gametime="20:15", home_score=None),
        dict(game_id="z", season=2026, game_type="REG", week=9, gameday="2026-11-09", weekday="Monday", gametime="20:15", home_score=21.0),
    ])
    pick = lambda **k: list(B.pick_games(g, season=2026, **k).game_id)
    assert pick(today=date(2026, 11, 11)) == ["a", "c"]                      # this week only, Thu/Sun/Mon only
    assert pick(today=date(2026, 11, 11), weekdays="all") == ["a", "b", "c"]
    assert pick(today=date(2026, 11, 13)) == ["c"]                           # Thursday game already played/past
    assert pick(today=date(2026, 11, 17)) == ["d"]                           # rolls to the next week
    assert pick(today=date(2026, 11, 11), game="z") == ["z"]
    assert PK.slot_name("Sunday", "20:20") == "Sunday Night Football" and PK.slot_name("Monday", "20:15") == "Monday Night Football"


def test_sources_fail_closed_and_optional(tmp_path):
    def boom(url, timeout=0):
        raise OSError("blocked")
    with pytest.raises(SystemExit):                                  # required data missing: no packet
        S.fetch_all(2026, tmp_path, fetch=boom)
    for name in ("games.parquet", "play_by_play_2026.parquet", "roster_weekly_2026.parquet"):
        (tmp_path / name).write_bytes(b"x")
    src = S.fetch_all(2026, tmp_path, fetch=boom)                    # cached required files: allowed but labelled stale
    assert src["pbp"]["status"].startswith("STALE_CACHE_USED") and src["pbp"]["sha256"]
    assert src["injuries"]["path"] is None and "FETCH_FAILED" in src["injuries"]["status"]
    assert S.espn_injuries(fetch=boom)["status"].startswith("UNAVAILABLE")   # never raises
    ok = S.espn_injuries(fetch=lambda u, timeout=0: json.dumps({"injuries": [{"injuries": [
        {"athlete": {"displayName": "A B", "position": {"abbreviation": "WR"}, "team": {"abbreviation": "WSH"}}, "status": "Out"}]}]}).encode())
    assert ok["teams"]["WAS"][0]["status"] == "Out"                  # ESPN WSH -> nflverse WAS


def test_baseline_and_clean():
    b = PK._baseline([10, 20, 30, 40], 1.1)
    assert b["games"] == 4 and b["weighted_mean"] == pytest.approx(1.1 * (10 * 1 + 20 * 4 / 3 + 30 * 5 / 3 + 40 * 2) / 6, abs=0.06)
    assert b["p50"] == pytest.approx(27.5)
    assert PK._baseline([10, 20], 1.0) is None                       # under three games: no baseline
    assert PK._factor({"k": 200.0}, {"k": 100.0}, "k") == 1.15 and PK._factor({"k": 110.0}, {"k": 100.0}, "k") == pytest.approx(1.05)
    assert PK._factor({}, {"k": 100.0}, "k") == 1.0
    out = B._clean({"a": float("nan"), "b": [pd.NA if False else 1.5, {1, 2}]})
    assert out["a"] is None and json.dumps(out, allow_nan=False)
    assert R.f(None) == "n/a" and R.f(0.123, 1, True) == "12.3%"


def test_ledger_never_claims_ready():
    pk = {"teams": {}, "sources": {}}
    led = PK.phase_ledger(pk)
    assert [p["phase"] for p in led] == list(range(1, 16))
    by = {p["phase"]: p["status"] for p in led}
    assert by[13] == "BLOCKED" and by[15] == "PENDING" and by[14] == "PARTIAL_RESEARCH_ONLY"


# ---------------------------------------------------------------- book odds, no-vig, movement, weather
from pregame import odds as O, weather as W  # noqa: E402


def _event():
    def book(key, spread, sp_h, sp_a, tot, o, u, ml_h, ml_a):
        return {"key": key, "last_update": "2026-11-16T15:00:00Z", "markets": [
            {"key": "spreads", "outcomes": [{"name": "Baltimore Ravens", "price": sp_h, "point": spread}, {"name": "Los Angeles Chargers", "price": sp_a, "point": -spread}]},
            {"key": "totals", "outcomes": [{"name": "Over", "price": o, "point": tot}, {"name": "Under", "price": u, "point": tot}]},
            {"key": "h2h", "outcomes": [{"name": "Baltimore Ravens", "price": ml_h}, {"name": "Los Angeles Chargers", "price": ml_a}]}]}
    return {"id": "ev1", "home_team": "Baltimore Ravens", "away_team": "Los Angeles Chargers", "bookmakers": [
        book("pinnacle", -4.5, -105, -105, 38.5, -108, -102, -215, 190),
        book("draftkings", -4.5, -110, -110, 38.5, -112, -108, -225, 185),
        book("fanduel", -4, -115, -105, 39.5, -110, -110, -220, 180),
        {"key": "betmgm", "markets": []},
        {"key": "draftkings", "markets": [{"key": "player_reception_yds", "outcomes": [
            {"name": "Over", "description": "Zay Flowers", "price": -115, "point": 58.5}, {"name": "Under", "description": "Zay Flowers", "price": -105, "point": 58.5},
            {"name": "Over", "description": "One Sided", "price": -110, "point": 20.5}]}]}]}


def test_devig_and_validation():
    a, b, hold = O.devig(-110, -110)
    assert (a, b) == (0.5, 0.5) and hold == pytest.approx(0.0476, abs=1e-4)
    a, b, _ = O.devig(-150, 130)
    assert a + b == pytest.approx(1.0) and a == pytest.approx(0.6 / (0.6 + 100 / 230))
    with pytest.raises(ValueError):
        O.implied(-50)


def test_summarize_event_reference_and_best_price():
    m = O.summarize_event(_event(), "BAL", "LAC")
    assert set(m["spread"]["books"]) == {"pinnacle", "draftkings", "fanduel"}          # betmgm ignored
    assert m["spread"]["reference"] == {"book": "pinnacle", "line": -4.5, "no_vig": {"BAL": 0.5, "LAC": 0.5}}
    assert m["spread"]["books_agree_on_line"] is False                                    # FanDuel hangs -4
    assert m["total"]["best_retail_price"]["Over"] == {"book": "fanduel", "price": -110, "line": 39.5, "break_even": pytest.approx(0.5238, abs=1e-4)}
    assert m["moneyline"]["best_retail_price"]["LAC"]["book"] == "draftkings"            # +185 beats +180; Pinnacle is not a retail book
    prop = m["receiving_yards|Zay Flowers"]
    assert prop["books"]["draftkings"]["no_vig"]["Over"] == pytest.approx(0.5108, abs=1e-4)
    assert prop["reference"]["book"] is None                                              # no Pinnacle prop: say so, do not invent
    assert "receiving_yards|One Sided" not in m                                           # one-sided quote cannot be de-vigged


def test_no_key_and_failure_never_invent(tmp_path):
    assert O.fetch_game_lines(key="")["status"].startswith("NO_KEY") and O.fetch_props("ev1", key="")["status"] == "NO_KEY"
    def boom(url, timeout=0):
        raise OSError("down apiKey=SECRETKEY")
    r = O.fetch_game_lines(key="SECRETKEY", fetch=boom)
    assert r["status"].startswith("UNAVAILABLE") and "SECRETKEY" not in r["status"] and r["events"] == {}
    ok = O.fetch_game_lines(key="k", fetch=lambda url, timeout=0: [_event()])
    assert list(ok["events"]) == [("LAC", "BAL")]


def test_line_movement_first_seen_to_now(tmp_path):
    m1 = O.summarize_event(_event(), "BAL", "LAC")
    r1 = O.record_and_movement("g", m1, tmp_path, now="t1")
    assert r1["snapshots"] == 1 and all(x.get("line_move", 0) == 0 for x in r1["moves"])
    assert O.record_and_movement("g", m1, tmp_path, now="t2")["snapshots"] == 1         # unchanged prices: no new snapshot
    ev = _event(); ev["bookmakers"][1]["markets"][0]["outcomes"] = [{"name": "Baltimore Ravens", "price": -110, "point": -6}, {"name": "Los Angeles Chargers", "price": -110, "point": 6}]
    r3 = O.record_and_movement("g", O.summarize_event(ev, "BAL", "LAC"), tmp_path, now="t3")
    dk = next(x for x in r3["moves"] if x["market"] == "spread" and x["book"] == "draftkings")
    assert r3["snapshots"] == 2 and dk["first_line"] == -4.5 and dk["current_line"] == -6 and dk["line_move"] == -1.5
    assert "not the true opening line" in r3["note"]


def test_prop_check_uses_counts_not_edges():
    pk = {"books": {"markets": O.summarize_event(_event(), "BAL", "LAC")},
          "matchup": {"x": {"player_baselines": {"players": [{"player": "Z.Flowers", "pos": "WR", "receiving_yards": PK._baseline([40, 60, 80, 70], 1.0)}]}}}}
    PK.prop_check(pk)
    row = pk["books"]["prop_check"]["rows"][0]
    assert row["player"] == "Zay Flowers" and row["line"] == 58.5 and row["baseline_games"] == 4
    assert row["baseline_minus_line"] == pytest.approx(row["baseline_weighted_mean"] - 58.5, abs=0.06)
    assert "NOT an edge" in pk["books"]["prop_check"]["note"] and "edge" not in row


def test_weather_paths():
    assert W.kickoff_utc("2026-11-16", "20:15").isoformat() == "2026-11-17T01:15:00+00:00"   # EST
    assert W.kickoff_utc("2026-10-25", "13:00").isoformat() == "2026-10-25T17:00:00+00:00"   # EDT
    assert W.forecast("NO", "dome", "Home", "2026-11-15", "13:00")["status"] == "INDOOR"
    assert W.forecast("DET", "outdoors", "Neutral", "2026-11-15", "09:30")["status"].startswith("NOT_MAPPED")
    def fake(url, timeout=0):
        if "/points/" in url:
            return {"properties": {"forecastHourly": "https://api.weather.gov/x"}}
        return {"properties": {"periods": [
            {"startTime": f"2026-11-16T{h:02d}:00:00-05:00", "temperature": t, "windSpeed": f"{w} mph", "windDirection": "NW",
             "probabilityOfPrecipitation": {"value": p}, "shortForecast": "Clear"} for h, t, w, p in ((19, 40, 8, 0), (20, 38, 12, 10), (21, 35, 18, 60), (22, 31, 20, None))]}}
    r = W.forecast("BAL", "outdoors", "Home", "2026-11-16", "20:15", fetch=fake)
    assert r["status"] == "OK" and r["at_kickoff"]["temp_f"] == 38 and r["at_kickoff"]["wind_mph"] == 12
    assert r["during_game"] == {"temp_f_min": 31, "wind_mph_max": 20.0, "precip_chance_pct_max": 60}
    assert r["flags"] == ["WIND_15_PLUS", "PRECIP_50_PLUS", "FREEZING"]
    assert W.forecast("BAL", "outdoors", "Home", "2026-11-16", "20:15", fetch=lambda u, timeout=0: 1 / 0)["status"].startswith("UNAVAILABLE")


# ---------------------------------------------------------------- NFL Savant and keyed connectors
from pregame import connectors as C, savant as SV  # noqa: E402


def _savant_csv():
    head = "GameId,GameDate,OffenseTeam,DefenseTeam,Yards,Formation,IsRush,IsPass,IsIncomplete,PassType,IsSack,IsNoPlay"
    rows = []
    for i in range(12):
        rows.append(f"1,2026-11-01,BLT,LAC,{8 if i % 2 else 0},SHOTGUN,0,1,{0 if i % 2 else 1},DEEP LEFT,0,0")     # BLT -> BAL
    for i in range(10):
        rows.append("1,2026-11-01,BLT,LAC,4,UNDER CENTER,1,0,0,,0,0")
    rows.append("1,2026-11-01,BLT,LAC,50,SHOTGUN,0,1,0,DEEP LEFT,0,1")                                              # no-play: dropped
    rows.append("2,2026-11-20,BLT,LAC,99,SHOTGUN,0,1,0,DEEP LEFT,0,0")                                              # after the game date: excluded
    return ("\n".join([head] + rows)).encode()


def test_savant_splits_and_failures():
    s = SV.load(2026, fetch=lambda u, timeout=0: _savant_csv())
    assert s["status"] == "OK" and s["latest_game"] == "2026-11-20"
    t = SV.team_splits(s["plays"], "BAL", "2026-11-16")
    sg = next(r for r in t["offense_by_formation"] if r["formation"] == "Shotgun")
    assert sg["plays"] == 12 and sg["pass_rate"] == 1.0 and sg["yards_per_play"] == 4.0 and sg["share"] == pytest.approx(12 / 22, abs=1e-3)
    z = t["offense_pass_zones"][0]
    assert z == {"zone": "Deep Left", "attempts": 12, "share": 1.0, "completion_rate": 0.5, "yards_per_attempt": 4.0}
    assert SV.team_splits(s["plays"], "LAC", "2026-11-16")["defense_pass_zones_allowed"][0]["attempts"] == 12
    assert SV.team_splits(s["plays"], "ZZZ", "2026-11-16") is None
    assert SV.load(2026, fetch=lambda u, timeout=0: b"a,b\n1,2\n")["status"].startswith("SCHEMA_CHANGED")
    assert SV.load(2026, fetch=lambda u, timeout=0: 1 / 0)["status"].startswith("UNAVAILABLE")
    assert SV.team_splits(None, "BAL", "2026-11-16") is None


def test_connector_check_reports_status_never_keys():
    none = C.check(2026, 10, [("LAC", "BAL")], env={})
    assert {v["status"] for v in none["sources"].values()} == {"KEY_NOT_CONFIGURED_IN_THIS_RUN"}

    def fake(provider, resource, **kw):
        if provider == "balldontlie_nfl":
            return {"data": {"data": [{"home_team": {"abbreviation": "BAL"}, "visitor_team": {"abbreviation": "LAC"}},
                                      {"home_team": {"abbreviation": "NYG"}, "visitor_team": {"abbreviation": "WSH"}}]}}
        raise PermissionError("no entitlement SECRET123")
    env = {"ODDS_API_KEY": "SECRET123", "NFL_BDL_API_KEY": "SECRET123", "NFL_API_SPORTS_KEY": "SECRET123"}
    r = C.check(2026, 10, [("LAC", "BAL"), ("WAS", "NYG"), ("SF", "DAL")], env=env, fetch_http=fake)
    bdl = r["sources"]["NFL_BDL_API_KEY"]
    assert bdl["status"] == "OK" and bdl["slate_check"] == "MISMATCH" and bdl["games_not_found_at_provider"] == ["SF@DAL"]   # WSH mapped to WAS
    assert r["sources"]["NFL_API_SPORTS_KEY"]["status"] == "KEY_PRESENT_REQUEST_FAILED: PermissionError"
    assert r["sources"]["ODDS_API_KEY"]["status"] == "KEY_PRESENT"
    assert "SECRET123" not in json.dumps(r)

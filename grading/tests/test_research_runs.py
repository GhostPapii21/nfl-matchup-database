"""Offline tests for the ESPN result source and research-artifact grading. No network, no paid API."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from grading import core as C
from grading import espn as E
from grading import research_runs as R

KO = datetime(2026, 11, 13, 1, 15, tzinfo=timezone.utc)
NOW = datetime(2026, 11, 13, 5, 0, tzinfo=timezone.utc)


def summary(status="STATUS_FINAL", completed=True, home_score="21", away_score="24"):
    ath = lambda i, n: {"id": str(i), "displayName": n}
    return {
        "header": {"competitions": [{"date": "2026-11-13T01:15Z", "status": {"type": {"name": status, "completed": completed}},
                   "competitors": [
                       {"homeAway": "home", "score": home_score, "team": {"abbreviation": "NYG"}, "linescores": [{"displayValue": x} for x in ("0", "7", "7", "7")]},
                       {"homeAway": "away", "score": away_score, "team": {"abbreviation": "WSH"}, "linescores": [{"displayValue": x} for x in ("0", "10", "7", "7")]}]}]},
        "boxscore": {"players": [
            {"team": {"abbreviation": "NYG"}, "statistics": [
                {"name": "rushing", "labels": ["CAR", "YDS", "AVG", "TD", "LONG"], "athletes": [{"athlete": ath(1, "Cam Skattebo"), "stats": ["18", "78", "4.3", "2", "14"]}]},
                {"name": "receiving", "labels": ["REC", "YDS", "AVG", "TD", "LONG", "TGTS"], "athletes": [
                    {"athlete": ath(1, "Cam Skattebo"), "stats": ["3", "44", "14.7", "0", "34", "4"]},
                    {"athlete": ath(2, "Malik Nabers"), "stats": ["5", "44", "8.8", "0", "37", "7"]}]},
                {"name": "passing", "labels": ["C/ATT", "YDS"], "athletes": [{"athlete": ath(3, "J.J. McCarthy"), "stats": ["23/36", "293"]}]}]},
            {"team": {"abbreviation": "WSH"}, "statistics": [
                {"name": "receiving", "labels": ["REC", "YDS", "AVG", "TD", "LONG", "TGTS"], "athletes": [
                    {"athlete": ath(4, "Antonio Williams"), "stats": ["2", "42", "21.0", "1", "31", "2"]},
                    {"athlete": ath(5, "Mike Williams"), "stats": ["1", "9", "9.0", "0", "9", "1"]}]},
                {"name": "rushing", "labels": ["CAR", "YDS"], "athletes": [{"athlete": ath(6, "Jayden Daniels"), "stats": ["11", "28"]}]}]}]},
    }


def actuals(**kw):
    rec = {"url": "u", "retrieved_utc": "2026-11-13T05:00:00+00:00", "sha256_full_response": "x", **summary(**kw)}
    return E.ESPNActuals("2026_10_WAS_NYG", rec, "grading/results/sources/test.json")


# ---------------------------------------------------------------- ESPN source
def test_espn_final_score_alias_and_halves():
    a = actuals()
    assert a.final() and (a.home, a.away) == ("NYG", "WAS")
    assert a.score("WAS") == 24 and a.score("NYG") == 21
    assert a.half_score("NYG", 1) == 7 and a.half_score("WAS", 1) == 10
    assert a.kickoff == KO


def test_espn_not_final_is_unknown():
    a = actuals(status="STATUS_IN_PROGRESS", completed=False)
    assert not a.final() and a.score("NYG") == C.UNKNOWN
    who = a.resolve_full("Malik Nabers", "NYG")
    assert a.stat(who["gsis_id"], "Malik Nabers", "NYG", "receiving_yards") == C.UNKNOWN


def test_espn_stats_and_zero_only_when_in_box():
    a = actuals()
    s = a.resolve_full("Cam Skattebo", "NYG")
    assert a.stat(s["gsis_id"], None, "NYG", "rushing_yards") == 78
    assert a.stat(s["gsis_id"], None, "NYG", "targets") == 4
    q = a.resolve_short("J.McCarthy", "NYG")
    assert a.stat(q["gsis_id"], None, "NYG", "pass_attempts") == 36 and a.stat(q["gsis_id"], None, "NYG", "completions") == 23
    d = a.resolve_full("Jayden Daniels", "WAS")
    assert a.stat(d["gsis_id"], None, "WAS", "receiving_yards") == 0          # in the box, no catches
    missing = a.resolve_full("Darius Slayton", "NYG")
    assert missing["gsis_id"] == C.UNKNOWN
    assert a.stat(missing["gsis_id"], None, "NYG", "receiving_yards") == C.UNKNOWN


def test_espn_surname_ambiguity_is_unknown_and_initial_resolves():
    a = actuals()
    assert a.resolve_surname("Williams")["gsis_id"] == C.UNKNOWN
    assert a.resolve_surname("Williams", initial="A")["full_name"] == "Antonio Williams"


def test_espn_offline_reads_saved_copy_and_refuses_without_one(tmp_path):
    with pytest.raises(SystemExit):
        E.load("2026_10_WAS_NYG", "401873052", offline=True, root=tmp_path)
    raw = json.dumps(summary()).encode()
    a = E.load("2026_10_WAS_NYG", "401873052", fetch=lambda url: raw, root=tmp_path)
    saved = tmp_path / "espn_summary_2026_10_WAS_NYG_401873052.json"
    rec = json.loads(saved.read_text())
    assert rec["retrieved_utc"] and len(rec["sha256_full_response"]) == 64 and a.final()
    b = E.load("2026_10_WAS_NYG", None, offline=True, root=tmp_path)
    assert b.score("WAS") == 24


def test_find_event_matches_home_and_away():
    sb = {"events": [{"id": "1", "competitions": [{"competitors": [{"homeAway": "home", "team": {"abbreviation": "NYG"}}, {"homeAway": "away", "team": {"abbreviation": "DAL"}}]}]},
                     {"id": "401873052", "competitions": [{"competitors": [{"homeAway": "home", "team": {"abbreviation": "NYG"}}, {"homeAway": "away", "team": {"abbreviation": "WSH"}}]}]}]}
    assert E.find_event("2026_10_WAS_NYG", fetch=lambda u: json.dumps(sb).encode()) == "401873052"
    assert E.find_event("2026_10_NYG_WAS", fetch=lambda u: json.dumps(sb).encode()) is None


# ---------------------------------------------------------------- leg grammar
@pytest.mark.parametrize("name,stat,line", [
    ("Nabers 40+ yds", "receiving_yards", 39.5), ("Nabers O67.5 yds", "receiving_yards", 67.5),
    ("Likely 4+ rec", "receptions", 3.5), ("Skattebo 25+ rush", "rushing_yards", 24.5),
    ("Skattebo 30+ R+R", "rush_rec_yards", 29.5), ("Skattebo 50+ rush+rec", "rush_rec_yards", 49.5),
    ("Diggs 30+ rec yds", "receiving_yards", 29.5)])
def test_parse_leg(name, stat, line):
    p = R.parse_leg(name)
    assert p["stat"] == stat and p["line"] == line and p["side"] == "Over"


def test_parse_leg_initial_total_and_unknown():
    assert R.parse_leg("A.Williams 15+ yds")["initial"] == "A"
    assert R.parse_leg("Under 54.5") == {"type": "game_total", "side": "Under", "line": 54.5}
    assert R.parse_leg("NYG 1H 3-way") == {"type": "first_half_win", "team": "NYG"}
    assert R.parse_leg("something odd") is None


# ---------------------------------------------------------------- grading
def ctx(snaps=()):
    return R.Ctx("2026_10_WAS_NYG", actuals(), list(snaps), KO, "NYG", "WAS", Path("."), NOW)


def test_alt_leg_graded_with_unknown_close_and_reference_main_line():
    snap = {"market_key": "receiving_yards|Malik Nabers", "book": "fanduel", "line": 66.5, "prices": {"Over": -113, "Under": -113},
            "snapshot_utc": "2026-11-13T00:01:35Z", "source": "freeze"}
    late = dict(snap, line=60.5, snapshot_utc="2026-11-13T02:00:00Z")          # after kickoff: never the close
    r = ctx([snap, late]).grade_leg("Nabers 40+ yds", "legs.json", "t", {"model": 0.72})
    assert r["result"] == "win" and r["actual"]["value"] == 44 and r["margin_vs_rung"] == 4.5
    assert r["closing_line"]["value"] == C.UNKNOWN
    assert r["closing_main_line_reference"]["value"] == 66.5
    assert "analyst read" in r["analyst_probabilities"]["model"]["label"]
    assert ctx().grade_leg("Nabers 60+ yds", "legs.json", "t", {})["result"] == "loss"


def test_rush_rec_total_and_first_half_legs():
    c = ctx()
    assert c.grade_leg("Skattebo 50+ rush+rec", "a", "t", {})["actual"]["value"] == 122
    assert c.grade_leg("Under 54.5", "a", "t", {})["result"] == "win"
    assert c.grade_leg("NYG 1H 3-way", "a", "t", {})["result"] == "loss"
    unk = c.grade_leg("Williams 20+ yds", "a", "t", {})                         # two Williamses: unknown, not 0
    assert unk["actual"]["value"] == C.UNKNOWN and unk["result"] == C.UNKNOWN


def test_outcomes_spread_ml_total():
    c = ctx()
    assert c.outcome("NYG -1.5") == 0 and c.outcome("WAS +2.5") == 1 and c.outcome("NYG +3") == "push"
    assert c.outcome("NYG ML") == 0 and c.outcome("WAS win") == 1
    assert c.outcome("Under 40.5") == 0 and c.outcome("Over 45") == "push"
    p = c.team_prob("a", "t", "engine", "NYG win", 0.4858, c.outcome("NYG win"))
    assert p["brier"] == round(0.4858 ** 2, 4)
    assert c.team_prob("a", "t", "engine", "x", 0.5, "push")["brier"] == C.UNKNOWN


def test_spec_slip_logic(tmp_path):
    spec = {"slips": [
        {"slip": "A", "legs": ["Under 54.5", "Nabers 40+ yds"], "complete": True},
        {"slip": "D", "legs": ["Nabers 60+ yds", "Skattebo 25+ rush"], "complete": True},
        {"slip": "B", "legs": ["Under 55.5"], "complete": False}]}
    p = tmp_path / "grading_spec.json"; p.write_text(json.dumps(spec))
    rows = {r["slip"]: r for r in R._grade_spec(ctx(), p, tmp_path, [])}
    assert rows["A"]["result"] == "win" and rows["A"]["legs_hit"] == 2
    assert rows["D"]["result"] == "loss"
    assert rows["B"]["result"] == C.UNKNOWN                                  # incomplete leg list never reads as a win


def test_spec_flagged_prop_clv_uses_close_saved_after_bet_quote(tmp_path):
    bet = {"market_key": "rushing_yards|Cam Skattebo", "book": "fanduel", "line": 63.5, "prices": {"Over": -113, "Under": -113},
           "snapshot_utc": "2026-11-12T22:11:36+00:00", "source": "packet#books"}
    close = dict(bet, line=62.5, snapshot_utc="2026-11-13T00:01:35Z", source="freeze")
    spec = {"flagged_props": [{"player": "Cam Skattebo", "team": "NYG", "stat": "rushing_yards", "side": "Under", "line": 63.5, "book": "fanduel"}]}
    p = tmp_path / "grading_spec.json"; p.write_text(json.dumps(spec))
    r = R._grade_spec(ctx([bet, close]), p, tmp_path, [])[0]
    assert r["result"] == "loss" and r["actual"]["value"] == 78
    assert r["closing_line"]["value"] == 62.5 and r["clv"]["positive"] is True and r["clv"]["line_points"] == 1.0
    r2 = R._grade_spec(ctx([bet]), p, tmp_path, [])[0]                        # no later snapshot: CLV unknown
    assert r2["clv"]["positive"] == C.UNKNOWN


def test_research_rows_never_set_projection_ready():
    r = ctx().grade_leg("Nabers 40+ yds", "a", "t", {})
    assert r["projection_ready"] is False


def test_stored_was_nyg_grade_is_consistent():
    """The committed WAS@NYG grade: final score, sources and pull times present, no zero standing in for unknown."""
    root = Path(__file__).resolve().parents[2] / "grading" / "results"
    rp = root / "2026_10_WAS_NYG.research.jsonl"
    if not rp.exists():
        pytest.skip("WAS@NYG grade not stored in this checkout")
    rows = [json.loads(l) for l in rp.read_text().splitlines() if l.strip()]
    summ = json.loads((root / "2026_10_WAS_NYG.summary.json").read_text())
    assert summ["final_score"]["WAS"] == 24 and summ["final_score"]["NYG"] == 21 and summ["final_score"]["pulled_utc"]
    assert summ["projection_ready"] is False
    for r in rows:
        assert r["projection_ready"] is False
        a = r.get("actual")
        if isinstance(a, dict):
            assert a["value"] == C.UNKNOWN or (a["source"] != C.UNKNOWN and a["pulled_utc"] != C.UNKNOWN)
        cl = r.get("closing_line")
        if isinstance(cl, dict) and cl["value"] not in (C.UNKNOWN, None):
            assert cl["pulled_utc"] != C.UNKNOWN

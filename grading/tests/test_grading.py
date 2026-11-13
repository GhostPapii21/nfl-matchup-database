"""Offline tests for the grading loop. No network, no paid API."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

from grading import core as C
from grading import grade as G
from grading import sources as S

KO = datetime(2026, 11, 13, 1, 15, tzinfo=timezone.utc)          # 8:15 PM ET Nov 12
CFG = dict(G.CONFIG)
VOL_OK = {"supports": True, "reason": "test"}
REC_OK = {"holdout_ready": True, "positive": True, "n": 40}


# ---------------------------------------------------------------- edge rule
def test_edge_only_when_all_three_hold():
    d = C.edge_decision(0.60, 0.52, VOL_OK, REC_OK, CFG)
    assert d["edge"] is True and d["label"] == "edge"


@pytest.mark.parametrize("broken", ["c1", "c2", "c3"])
def test_edge_fails_when_any_one_condition_is_false(broken):
    mp, be, vol, rec = 0.60, 0.52, dict(VOL_OK), dict(REC_OK)
    if broken == "c1":
        mp = 0.50                         # model does not beat best retail break-even
    elif broken == "c2":
        vol = {"supports": False, "reason": "volume short"}
    else:
        rec = {"holdout_ready": True, "positive": False, "n": 40}
    d = C.edge_decision(mp, be, vol, rec, CFG)
    assert d["edge"] is False
    assert d["label"] == "not an edge"
    key = {"c1": "c1_model_beats_best_retail_break_even", "c2": "c2_volume_supports_number",
           "c3": "c3_positive_clv_record_on_holdout"}[broken]
    assert d[key]["pass"] is False
    assert sum(d[k]["pass"] for k in d if k.startswith("c")) == 2


@pytest.mark.parametrize("mp,be", [(C.UNKNOWN, 0.5), (None, 0.5), (0.7, C.UNKNOWN), (0.5, 0.5)])
def test_unknown_or_equal_probability_never_passes_c1(mp, be):
    assert C.edge_decision(mp, be, VOL_OK, REC_OK, CFG)["c1_model_beats_best_retail_break_even"]["pass"] is False


def test_no_holdout_labels_research_only_even_if_other_conditions_hold():
    rec = C.clv_record([], "receptions", KO, "g", 30)
    assert rec["holdout_ready"] is False and rec["n"] == 0
    d = C.edge_decision(0.9, 0.5, VOL_OK, rec, CFG)
    assert d["edge"] is False and d["label"] == "research only, not validated"


def _hist(n, positive, mt="receptions", t="2026-11-01T17:00:00+00:00"):
    return [{"kind": "flagged_prop", "market_type": mt, "game_id": f"g{i}", "kickoff_utc": t, "market_key": f"{mt}|P{i}",
             "side": "Over", "clv": {"positive": positive(i)}, "bet_break_even": {"value": 0.52}} for i in range(n)]


def test_holdout_minimum_and_positive_record():
    assert C.clv_record(_hist(29, lambda i: True), "receptions", KO, "x", 30)["holdout_ready"] is False
    r = C.clv_record(_hist(30, lambda i: i < 16), "receptions", KO, "x", 30)
    assert r["holdout_ready"] and r["positive"] and r["beat_close"] == 16
    r = C.clv_record(_hist(30, lambda i: i < 15), "receptions", KO, "x", 30)
    assert r["holdout_ready"] and not r["positive"]          # 15 v 15 is not positive


def test_holdout_excludes_this_game_later_games_unknown_clv_and_other_markets():
    rows = _hist(30, lambda i: True, t="2026-11-20T17:00:00+00:00")           # after this kickoff
    rows += _hist(30, lambda i: C.UNKNOWN)                                       # CLV unknown
    rows += _hist(30, lambda i: True, mt="rushing_yards")
    rows += [dict(r, game_id="this") for r in _hist(30, lambda i: True)]
    assert C.clv_record(rows, "receptions", KO, "this", 30)["n"] == 0


def test_holdout_counts_one_quote_per_prop():
    rows = _hist(30, lambda i: True)
    rows += [dict(r, bet_break_even={"value": 0.60}, clv={"positive": False}) for r in _hist(30, lambda i: True)]
    r = C.clv_record(rows, "receptions", KO, "x", 30)
    assert r["n"] == 30 and r["beat_close"] == 30            # the better-priced quote represents each prop


# ---------------------------------------------------------------- volume
BASE = {"player": "M.Nabers", "receptions": {"games": 8, "weighted_mean": 7.5, "p50": 6.5},
        "receiving_yards": {"games": 8, "weighted_mean": 87.3, "p50": 91.7},
        "targets": {"games": 8, "weighted_mean": 10.1, "p50": 8.5}}


def test_volume_supports_and_rejects():
    ok = C.volume_check(BASE, "receptions", "Over", 5.5, 4)          # needed 5.5/(7.5/10.1)=7.41 < 8.5
    assert ok["supports"] is True and ok["volume_field"] == "targets"
    hi = C.volume_check(BASE, "receiving_yards", "Over", 120.5, 4)   # needed 13.9 targets > 8.5
    assert hi["supports"] is False
    assert C.volume_check(BASE, "receiving_yards", "Under", 120.5, 4)["supports"] is True


@pytest.mark.parametrize("mutate", [
    lambda b: b.pop("targets"),
    lambda b: b["targets"].pop("p50"),
    lambda b: b["targets"].update(games=3),
    lambda b: b["targets"].update(p50=C.UNKNOWN),
])
def test_volume_missing_or_thin_fails(mutate):
    b = json.loads(json.dumps(BASE))
    mutate(b)
    v = C.volume_check(b, "receptions", "Over", 5.5, 4)
    assert v["supports"] is False and v["reason"]


def test_volume_no_baseline_or_unmapped_market_fails():
    assert C.volume_check(None, "receptions", "Over", 5.5, 4)["supports"] is False
    assert C.volume_check(BASE, "anytime_td", "Over", 0.5, 4)["supports"] is False


# ---------------------------------------------------------------- prices, closing line, CLV
def test_break_even_and_no_vig():
    assert C.break_even(-110) == 0.5238 and C.break_even(120) == 0.4545
    assert C.break_even(None) == C.UNKNOWN and C.break_even(C.UNKNOWN) == C.UNKNOWN
    assert C.no_vig({"Over": -110}, "Over") == C.UNKNOWN


def _snap(t, line, prices, book="draftkings", key="receptions|Malik Nabers"):
    return {"market_key": key, "book": book, "line": line, "prices": prices, "snapshot_utc": t, "source": "test"}


def test_closing_quote_uses_latest_before_kickoff_only():
    snaps = [_snap("2026-11-12T16:00:00Z", 5.5, {"Over": -110, "Under": -110}),
             _snap("2026-11-12T23:45:00Z", 6.5, {"Over": -105, "Under": -115}),
             _snap("2026-11-13T01:30:00Z", 7.5, {"Over": -110, "Under": -110}),      # after kickoff: ignored
             _snap("2026-11-12T23:50:00Z", 4.5, {"Over": -110, "Under": -110}, book="fanduel")]
    q = C.closing_quote(snaps, "receptions|Malik Nabers", "draftkings", KO)
    assert q["line"] == 6.5
    assert C.closing_quote(snaps, "receptions|Malik Nabers", "betmgm", KO) is None


def test_clv_signs():
    close_up = {"line": 6.5, "prices": {"Over": -110, "Under": -110}}
    assert C.clv("receptions", "Over", "NYG", 5.5, {}, close_up)["line_points"] == 1.0
    assert C.clv("receptions", "Under", "NYG", 5.5, {}, close_up)["positive"] is False
    # spread stored as home handicap: bet NYG -1.5, close NYG -2.5 -> NYG side gained a point
    sp = {"line": -2.5, "prices": {"NYG": -110, "WAS": -110}}
    assert C.clv("spread", "NYG", "NYG", -1.5, {}, sp)["line_points"] == 1.0
    assert C.clv("spread", "WAS", "NYG", -1.5, {}, sp)["line_points"] == -1.0
    # same line, price moved toward the side
    same = {"line": 5.5, "prices": {"Over": -140, "Under": 110}}
    r = C.clv("receptions", "Over", "NYG", 5.5, {"Over": -110, "Under": -110}, same)
    assert r["line_points"] == 0 and r["prob"] > 0 and r["positive"] is True


def test_clv_unknown_close_is_unknown_not_zero():
    r = C.clv("receptions", "Over", "NYG", 5.5, {"Over": -110, "Under": -110}, None)
    assert r["line_points"] == C.UNKNOWN and r["prob"] == C.UNKNOWN and r["positive"] == C.UNKNOWN


def test_best_retail_break_even_same_line_only_and_excludes_reference():
    books = {"draftkings": {"line": 5.5, "prices": {"Over": -141, "Under": 111}},
             "fanduel": {"line": 5.5, "prices": {"Over": -130, "Under": -102}},
             "pinnacle": {"line": 5.5, "prices": {"Over": -101, "Under": 104}},
             "hardrockbet": {"line": 4.5, "prices": {"Over": -105, "Under": -115}}}
    b = C.best_retail_break_even(books, "receptions", "Over", 5.5, "NYG", ["pinnacle"])
    assert b["book"] == "fanduel" and b["break_even"] == C.break_even(-130)
    assert C.best_retail_break_even({}, "receptions", "Over", 5.5, "NYG", ["pinnacle"])["break_even"] == C.UNKNOWN


def test_freeze_snapshot_parse_converts_spread_to_home_handicap(tmp_path):
    d = tmp_path / "pregame/price_freezes/2026-11-12_WAS@NYG"
    d.mkdir(parents=True)
    (d / "freeze_20261112T161430Z.json").write_text(json.dumps({"meta": {"pulled_utc": "2026-11-12T16:14:30Z"}, "rows": [
        {"book": "draftkings", "market": "spreads", "line": 2.5, "player": None, "price_a": -110, "price_b": -110,
         "side_a": "Washington Commanders", "side_b": "New York Giants", "book_last_update": "2026-11-12T16:14:23Z"},
        {"book": "draftkings", "market": "player_reception_yds", "line": 68.5, "player": "Malik Nabers",
         "price_a": -110, "price_b": -114, "side_a": "Over", "side_b": "Under"},
        {"book": "draftkings", "market": "player_weird", "line": 1, "player": "X", "side_a": "Over", "side_b": "Under"}]}))
    snaps = S.freeze_snapshots("WAS", "NYG", root=tmp_path)
    sp = [s for s in snaps if s["market_key"] == "spread"][0]
    assert sp["line"] == -2.5 and sp["prices"] == {"WAS": -110, "NYG": -110}
    assert any(s["market_key"] == "receiving_yards|Malik Nabers" for s in snaps) and len(snaps) == 2


def test_names():
    assert S.abbrev("Malik Nabers") == S.short_key("M.Nabers")
    assert S.abbrev("J.J. McCarthy") == S.short_key("J.McCarthy")
    assert S.abbrev("Marvin Harrison Jr.") == S.short_key("M.Harrison")
    assert S.abbrev("Jacory Croskey-Merritt") == S.short_key("J.Croskey-Merritt")


# ---------------------------------------------------------------- packet before kickoff (git)
def test_packet_before_kickoff_skips_post_kickoff_refresh(tmp_path):
    run = lambda *a: subprocess.run(["git", "-C", str(tmp_path), *a], check=True, capture_output=True)
    run("init", "-q"); run("config", "user.email", "t@t"); run("config", "user.name", "t")
    p = tmp_path / "pregame/packets/G/packet.json"
    p.parent.mkdir(parents=True)
    for gen, tag in (("2026-11-12T23:00:00+00:00", "pre"), ("2026-11-13T04:00:00+00:00", "post")):
        p.write_text(json.dumps({"generated_utc": gen, "tag": tag}))
        run("add", "-A"); run("commit", "-qm", tag)
    pk, src, pulled = S.packet_before_kickoff("G", KO, root=tmp_path)
    assert pk["tag"] == "pre" and src.startswith("git:") and pulled == "2026-11-12T23:00:00+00:00"
    pk, reason, _ = S.packet_before_kickoff("G", KO - timedelta(days=1), root=tmp_path)
    assert pk is None and "before kickoff" in reason


# ---------------------------------------------------------------- full game grading with fake actuals
def _actuals(final=True):
    games = pd.DataFrame([{"game_id": "2026_10_WAS_NYG", "week": 10, "home_team": "NYG", "away_team": "WAS",
                           "home_score": 20 if final else None, "away_score": 17 if final else None,
                           "gameday": "2026-11-12", "gametime": "20:15"}])
    ids = {"Malik Nabers": "N1", "Cam Skattebo": "S1", "Darnell Mooney": "M1", "Jayden Daniels": "D1"}
    rosters = pd.DataFrame([{"gsis_id": v, "full_name": k, "team": "WAS" if k == "Jayden Daniels" else "NYG", "week": 10}
                            for k, v in ids.items()])
    base = dict(game_id="2026_10_WAS_NYG", two_point_attempt=0, sack=0, passer_player_id="Q1",
                rusher_player_id=None, receiver_player_id=None, passing_yards=0, rushing_yards=0, receiving_yards=0,
                complete_pass=0, pass_attempt=0, rush_attempt=0, play_type="pass")
    plays = [dict(base, pass_attempt=1, receiver_player_id="N1", complete_pass=1, receiving_yards=12, passing_yards=12)] * 6
    plays += [dict(base, pass_attempt=1, receiver_player_id="N1")] * 3
    plays += [dict(base, play_type="run", passer_player_id=None, rush_attempt=1, rusher_player_id="D1", rushing_yards=5)]
    pbp = pd.DataFrame(plays)
    snaps = pd.DataFrame([{"game_id": "2026_10_WAS_NYG", "team": "NYG", "player": "Darnell Mooney", "offense_snaps": 30}])
    prov = {k: {"url": f"https://example.invalid/{k}", "sha256": "abc", "retrieved_utc": "2026-11-13T05:00:00+00:00"}
            for k in ("games", "pbp", "rosters", "snap_counts")}
    return S.Actuals("2026_10_WAS_NYG", games, pbp, rosters, snaps, prov)


def _packet():
    q = lambda line, o, u_: {"line": line, "prices": {"Over": o, "Under": u_}}
    return {
        "generated_utc": "2026-11-12T22:00:00+00:00", "projection_ready": False,
        "game": {"game_id": "2026_10_WAS_NYG", "home": "NYG", "away": "WAS", "date": "2026-11-12", "kickoff_et": "20:15"},
        "market": {"source": "nflverse schedule", "home_spread": -2.5, "total": 40.5},
        "books": {"retrieved_utc": "2026-11-12T22:00:00+00:00", "markets": {
            "receptions|Malik Nabers": {"books": {"draftkings": q(5.5, -141, 111), "fanduel": q(5.5, -130, -102)}},
            "rushing_yards|Cam Skattebo": {"books": {"draftkings": q(55.5, -115, -109)}},
            "receptions|Darnell Mooney": {"books": {"draftkings": q(2.5, 120, -150)}},
            "spread": {"books": {"draftkings": {"line": -2.5, "prices": {"NYG": -105, "WAS": -115}}}},
            "total": {"books": {"draftkings": q(40.5, -118, -102)}},
        }, "prop_check": {"rows": [
            {"player": "Malik Nabers", "stat": "receptions", "book": "draftkings", "line": 5.5,
             "prices": {"Over": -141, "Under": 111}, "baseline_weighted_mean": 7.5, "baseline_minus_line": 2.0},
            {"player": "Cam Skattebo", "stat": "rushing_yards", "book": "draftkings", "line": 55.5,
             "prices": {"Over": -115, "Under": -109}, "baseline_weighted_mean": 67.4, "baseline_minus_line": 11.9},
            {"player": "Darnell Mooney", "stat": "receptions", "book": "draftkings", "line": 2.5,
             "prices": {"Over": 120, "Under": -150}, "baseline_weighted_mean": 2.0, "baseline_minus_line": -0.5},
        ]}},
        "matchup": {"NYG_offense_vs_WAS_defense": {"player_baselines": {"players": [
            dict(BASE, player="M.Nabers"),
            {"player": "C.Skattebo", "rushing_yards": {"games": 6, "weighted_mean": 67.4, "p50": 55.1}},
        ]}}},
        "team_projection": {"samplers": {"matchup_pair": {"home_points": 24.5, "away_points": 22.8, "home_margin": 1.7,
                                                           "total": 47.3, "home_win": 0.532, "away_win": 0.462,
                                                           "home_covers_market_spread": 0.477, "over_market_total": 0.683}}},
    }


def _grade(history=(), snapshots=None):
    pk = _packet()
    snaps = S.packet_snapshots(pk, "git:abc:pregame/packets/2026_10_WAS_NYG/packet.json") if snapshots is None else snapshots
    return G.grade_game("2026_10_WAS_NYG", pk, "git:abc:pregame/packets/2026_10_WAS_NYG/packet.json",
                        pk["generated_utc"], KO, _actuals(), snaps, list(history), CFG,
                        now=datetime(2026, 11, 13, 6, tzinfo=timezone.utc))


def _walk(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from _walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v)
    else:
        yield o


def test_grade_game_results_and_unknowns():
    rows = _grade()
    props = {r["player"]: r for r in rows if r["kind"] == "flagged_prop"}
    nab = props["Malik Nabers"]
    assert nab["actual"]["value"] == 6 and nab["result"] == "win" and nab["side"] == "Over"
    assert nab["actual"]["source"].startswith("https://example.invalid/pbp") and nab["actual"]["pulled_utc"] != C.UNKNOWN
    # Skattebo: on the roster but no plays and no snaps -> unknown, never 0
    sk = props["Cam Skattebo"]
    assert sk["actual"]["value"] == C.UNKNOWN and sk["result"] == C.UNKNOWN
    # Mooney: played (snaps) but no targets -> a real 0
    assert props["Darnell Mooney"]["actual"]["value"] == 0 and props["Darnell Mooney"]["result"] == "win"
    # packet has no prop model probability -> unknown, c1 fails
    assert nab["model_prob"]["value"] == C.UNKNOWN
    assert nab["edge_rule"]["c1_model_beats_best_retail_break_even"]["pass"] is False
    assert nab["edge_rule"]["c2_volume_supports_number"]["pass"] is True
    # Mooney has no baseline in the packet -> volume fails
    assert props["Darnell Mooney"]["edge_rule"]["c2_volume_supports_number"]["pass"] is False
    # closing line from the only pre-kickoff snapshot, which is the bet quote itself -> CLV unknown, not 0
    assert nab["closing_line"]["value"] == 5.5
    assert nab["clv"]["line_points"] == C.UNKNOWN and nab["clv"]["positive"] == C.UNKNOWN
    team = {r["market_key"]: r for r in rows if r["kind"] == "team_projection"}
    assert team["total|matchup_pair"]["actual"]["value"] == 37
    assert team["total|matchup_pair"]["error_actual_minus_projection"] == round(37 - 47.3, 2)
    for r in rows:
        assert r["projection_ready"] is False
        assert r.get("label", (r.get("edge_rule") or {}).get("label")) == "research only, not validated"
        assert (r.get("edge_rule") or {}).get("edge", False) is False


def test_later_snapshot_gives_clv():
    pk = _packet()
    later = _snap("2026-11-13T00:05:00+00:00", 6.5, {"Over": -110, "Under": -110})
    rows = _grade(snapshots=S.packet_snapshots(pk, "git:abc:p") + [later])
    nab = [r for r in rows if r.get("player") == "Malik Nabers" and r["kind"] == "flagged_prop"][0]
    assert nab["closing_line"]["value"] == 6.5 and nab["closing_line"]["minutes_before_kickoff"] == 70.0
    assert nab["clv"]["line_points"] == 1.0 and nab["clv"]["positive"] is True


def test_no_closing_snapshot_means_unknown_close():
    rows = _grade(snapshots=[])
    for r in rows:
        if "closing_line" in r:
            assert r["closing_line"]["value"] == C.UNKNOWN
            assert r["clv"]["positive"] == C.UNKNOWN and r["clv"]["line_points"] == C.UNKNOWN


def test_unknown_values_are_never_zero_or_none_in_figures():
    rows = _grade(snapshots=[])
    for r in rows:
        for k in ("actual", "model_prob", "closing_line", "closing_price", "best_retail_break_even", "bet_price"):
            if k in r:
                assert r[k]["value"] is not None
                assert r[k]["source"] is not None and r[k]["pulled_utc"] is not None
    sk = [r for r in rows if r.get("player") == "Cam Skattebo" and r["kind"] == "flagged_prop"][0]
    assert sk["actual"]["value"] == C.UNKNOWN and sk["closing_line"]["value"] == C.UNKNOWN
    assert None not in [v for v in _walk(sk["clv"])]


def test_edge_label_with_holdout_and_model_prob():
    pk = _packet()
    pk["books"]["prop_check"]["rows"][0]["model_prob_over"] = 0.70          # beats best retail 0.5652
    hist = _hist(30, lambda i: i < 20)                                         # receptions record 20-10
    rows = G.grade_game("2026_10_WAS_NYG", pk, "git:abc:p", pk["generated_utc"], KO, _actuals(),
                        S.packet_snapshots(pk, "git:abc:p"), hist, CFG)
    nab = [r for r in rows if r.get("player") == "Malik Nabers" and r["kind"] == "flagged_prop"][0]
    assert nab["edge_rule"]["edge"] is True and nab["edge_rule"]["label"] == "edge"
    mooney = [r for r in rows if r.get("player") == "Darnell Mooney"][0]
    assert mooney["edge_rule"]["label"] == "not an edge"                      # holdout exists, volume fails
    sk = [r for r in rows if r.get("player") == "Cam Skattebo" and r["kind"] == "flagged_prop"][0]
    assert sk["edge_rule"]["label"] == "research only, not validated"         # no rushing_yards holdout


def test_refuses_when_not_final():
    assert _actuals(final=False).final() is False
    assert _actuals(final=False).stat("N1", "Malik Nabers", "NYG", "receptions") == C.UNKNOWN


def test_package_never_calls_paid_sources():
    src = "".join(p.read_text() for p in Path(G.__file__).parent.glob("*.py"))
    for banned in ("the-odds-api", "ODDS_API_KEY", "pregame.odds", "pregame.multibook", "from pregame", "import pregame"):
        assert banned not in src
    assert G.CONFIG["min_holdout_props_per_market_type"] >= 1


# ---------------------------------------------------------------- freeze_v2, --freeze-ref, "no consensus"
def _v2(pulled="2026-11-13T00:00:00Z"):
    q = lambda line, o, u_: {"line": line, "prices": {"Over": o, "Under": u_}, "last_update": pulled}
    return {"meta": {"schema": "price-freeze/2", "pulled_utc": pulled},
            "markets": {
                "receptions|Malik Nabers": {"books": {"draftkings": q(6.5, -110, -110), "fanduel": q(5.5, -150, 120),
                                                      "williamhill_us": "no props"}},
                "spread": {"books": {"draftkings": {"line": -3.0, "prices": {"NYG": -110, "WAS": -110}}}}},
            "consensus": {
                "receptions|Malik Nabers": {"consensus": "no consensus", "reason": "books split 1-1",
                                            "book_lines": {"draftkings": 6.5, "fanduel": 5.5, "williamhill_us": "no props"}},
                "spread": {"consensus": {"line": -3.0, "n_books_at_line": 2, "books_at_line": ["draftkings", "hardrockbet"],
                                         "no_vig": {"NYG": 0.5, "WAS": 0.5}}}}}


def _repo_with_freeze_branch(tmp_path):
    run = lambda *a: subprocess.run(["git", "-C", str(tmp_path), *a], check=True, capture_output=True)
    run("init", "-q", "-b", "main"); run("config", "user.email", "t@t"); run("config", "user.name", "t")
    (tmp_path / "README").write_text("x"); run("add", "-A"); run("commit", "-qm", "base")
    run("checkout", "-q", "-b", "research/feed")
    d = tmp_path / "pregame/price_freezes/2026-11-12_WAS@NYG"
    d.mkdir(parents=True)
    (d / "freeze_v2_20261113T000000Z.json").write_text(json.dumps(_v2()))
    (d / "raw_20261113T000000Z.json").write_text("{}")                          # not a freeze: ignored
    (d / "freeze_v2_broken.json").write_text("{not json")                       # unparseable: skipped
    run("add", "-A"); run("commit", "-qm", "freeze")
    run("checkout", "-q", "main")
    return tmp_path


def test_freeze_ref_reads_other_branch_as_data(tmp_path):
    root = _repo_with_freeze_branch(tmp_path)
    assert S.freeze_snapshots("WAS", "NYG", root=root) == []                    # default: working tree (main) has none
    snaps, cons = S.freeze_data("WAS", "NYG", root=root, ref="research/feed")
    books = {(s["market_key"], s["book"]) for s in snaps}
    assert ("receptions|Malik Nabers", "draftkings") in books and ("receptions|Malik Nabers", "fanduel") in books
    assert ("receptions|Malik Nabers", "williamhill_us") not in books           # "no props" is not a quote
    assert all(s["source"].startswith("git:research/feed@") and "freeze_v2_20261113T000000Z.json" in s["source"] for s in snaps)
    sp = [s for s in snaps if s["market_key"] == "spread"][0]
    assert sp["line"] == -3.0 and sp["snapshot_utc"] == "2026-11-13T00:00:00Z"   # v2 spread is already the home handicap
    assert {c["market_key"] for c in cons} == {"receptions|Malik Nabers", "spread"}
    with pytest.raises(subprocess.CalledProcessError):
        S.freeze_data("WAS", "NYG", root=root, ref="no/such/ref")


def test_no_consensus_is_unknown_but_per_book_lines_still_grade():
    pk = _packet()
    fz_snaps, fz_cons = [], []
    # build from the v2 dict directly through the same parser path
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "pregame/price_freezes/2026-11-12_WAS@NYG"
        d.mkdir(parents=True)
        (d / "freeze_v2_20261113T000000Z.json").write_text(json.dumps(_v2()))
        fz_snaps, fz_cons = S.freeze_data("WAS", "NYG", root=Path(td))
    nc = S.closing_consensus(fz_cons, "receptions|Malik Nabers", KO)
    assert nc["value"] == C.UNKNOWN and nc["reason"] == "no consensus"
    assert nc["value"] not in (0, None, "")
    ok = S.closing_consensus(fz_cons, "spread", KO)
    assert ok["value"]["line"] == -3.0 and ok["value"]["n_books_at_line"] == 2
    rows = G.grade_game("2026_10_WAS_NYG", pk, "git:abc:p", pk["generated_utc"], KO, _actuals(),
                        S.packet_snapshots(pk, "git:abc:p") + fz_snaps, [], CFG, consensus=fz_cons)
    nab = [r for r in rows if r.get("player") == "Malik Nabers" and r["kind"] == "flagged_prop"][0]
    assert nab["closing_consensus_reference_only"]["value"] == C.UNKNOWN
    # per-book close still used: the DraftKings bet (5.5) closes at DraftKings 6.5 in the freeze
    assert nab["book"] == "draftkings" and nab["closing_line"]["value"] == 6.5
    assert nab["clv"]["line_points"] == 1.0 and nab["clv"]["positive"] is True


def test_clv_is_per_book_never_borrowed_from_another_book():
    pk = _packet()
    other = _snap("2026-11-13T00:30:00+00:00", 7.5, {"Over": -110, "Under": -110}, book="fanduel")
    rows = _grade(snapshots=S.packet_snapshots(pk, "git:abc:p") + [other])
    nab = [r for r in rows if r.get("player") == "Malik Nabers" and r["kind"] == "flagged_prop"][0]
    assert nab["book"] == "draftkings"
    assert nab["closing_line"]["value"] == 5.5                                  # DraftKings' own pre-kick quote
    assert nab["clv"]["positive"] == C.UNKNOWN                                  # no later DraftKings snapshot


def test_freeze_v2_listed_before_v1_on_same_pull_time(tmp_path):
    d = tmp_path / "pregame/price_freezes/2026-11-12_WAS@NYG"
    d.mkdir(parents=True)
    (d / "freeze_v2_20261113T000000Z.json").write_text(json.dumps(_v2()))
    (d / "freeze_20261113T000000Z.json").write_text(json.dumps({"meta": {"pulled_utc": "2026-11-13T00:00:00Z"}, "rows": [
        {"book": "draftkings", "market": "player_receptions", "line": 9.5, "player": "Malik Nabers",
         "price_a": -110, "price_b": -110, "side_a": "Over", "side_b": "Under"}]}))
    snaps = S.freeze_snapshots("WAS", "NYG", root=tmp_path)
    q = C.closing_quote(snaps, "receptions|Malik Nabers", "draftkings", KO)
    assert q["line"] == 6.5 and "freeze_v2_" in q["source"]

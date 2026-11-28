"""DEN@PIT Week 12 (Fri Nov 27, 2026; ESPN 401873083; PIT 27, DEN 5) as the first postgame regression case.

Source package: PR #146 (commit fbfde112, merged in ef4cc690). Audit: docs/audits/postgame_grading_audit.md.
Tests named test_current_* pin today's behaviour (they pass). Tests marked xfail(strict=True) state the behaviour
the audit proposes; each names its gap id (G-xx). When a gap is fixed the xfail turns into a strict failure, which
is the signal to drop the marker. Offline, read-only.
"""
from __future__ import annotations

import collections
import hashlib
import json
import subprocess

import pytest

from _pg_common import (ESPN_FINAL, FIXED_NOW, GAME, LOCK_DIR, PACKET_REL, ROOT, RUN_DIR, denpit_actuals,
                        git_history_available)
from grading import core as C
from grading import grade as G
from grading import research_runs as R
from grading import sources as S

needs_history = pytest.mark.skipif(not git_history_available(), reason="needs full git history of the packet (CI is depth 1)")


@pytest.fixture(scope="module")
def act():
    return denpit_actuals()


@pytest.fixture(scope="module")
def packet(act):
    if not git_history_available():
        pytest.skip("needs full git history")
    return S.packet_before_kickoff(GAME, act.kickoff)


@pytest.fixture(scope="module")
def graded(act, packet):
    pk, src, pulled = packet
    snaps = S.packet_snapshots(pk, src) + S.line_history_snapshots(GAME)
    fz, cons = S.freeze_data("DEN", "PIT")
    rows = G.grade_game(GAME, pk, src, pulled, act.kickoff, act, snaps + fz, [], consensus=cons, now=FIXED_NOW)
    return rows, snaps + fz


# ---------------------------------------------------------------- Q1: where final stats enter
def test_espn_final_summary_is_final_and_matches_score(act):
    assert act.final() is True
    assert (act.away, act.home) == ("DEN", "PIT")
    assert act.score("PIT") == 27 and act.score("DEN") == 5
    assert act.half_score("PIT", 1) == 24 and act.half_score("DEN", 1) == 5   # halftime DEN 5, PIT 24 (POSTGAME_REVIEW.md)


@pytest.mark.parametrize("name,team,stat,expected", [
    ("Jonah Coleman", "DEN", "carries", 15), ("Jonah Coleman", "DEN", "rushing_yards", 26),
    ("Jonah Coleman", "DEN", "receptions", 8), ("Jonah Coleman", "DEN", "receiving_yards", 46),
    ("Courtland Sutton", "DEN", "receptions", 1), ("Courtland Sutton", "DEN", "receiving_yards", 4),
    ("Courtland Sutton", "DEN", "targets", 8),
    ("Pat Freiermuth", "PIT", "receptions", 1), ("Jaylen Warren", "PIT", "rushing_yards", 46),
    ("Jaylen Warren", "PIT", "receptions", 1), ("DK Metcalf", "PIT", "receiving_yards", 36),
    ("Bo Nix", "DEN", "passing_yards", 169), ("Bo Nix", "DEN", "pass_attempts", 40),
])
def test_box_stats_match_postgame_review(act, name, team, stat, expected):
    who = act.resolve_full(name, team)
    assert who["reason"] == "", who
    assert act.stat(who["gsis_id"], who["full_name"], team, stat) == expected


# ---------------------------------------------------------------- Q3: zero-stat and inactive players
def test_zero_catch_player_in_box_is_real_zero(act):
    who = act.resolve_full("Evan Engram", "DEN")
    assert act.stat(who["gsis_id"], who["full_name"], "DEN", "receptions") == 0
    assert act.stat(who["gsis_id"], who["full_name"], "DEN", "targets") == 2


@pytest.mark.parametrize("name,team", [("J.K. Dobbins", "DEN"), ("Drew Allar", "PIT"), ("Darnell Washington", "PIT")])
def test_current_absent_player_is_unknown_not_zero(act, name, team):
    """Dobbins (suspended), Allar (inactive, emergency QB), Washington (no box line, status not in any committed source)."""
    who = act.resolve_full(name, team)
    assert act.stat(who.get("gsis_id"), who.get("full_name"), team, "receptions") == C.UNKNOWN


def test_current_unknown_reason_does_not_separate_inactive_from_name_miss(act):
    """G-03: an inactive player and a spelling miss produce the same 'N ESPN box-score matches' reason."""
    inactive = act.resolve_full("Drew Allar", "PIT")["reason"]
    misspelt = act.resolve_full("Michael Pittman", "PIT")["reason"]
    assert inactive.startswith("0 ESPN box-score matches") and misspelt.startswith("0 ESPN box-score matches")


@pytest.mark.xfail(strict=True, reason="G-03: no participation source (gamebook / inactives) is read, so no void status exists")
def test_proposed_inactive_player_settles_as_void(graded):
    rows, _ = graded
    allar = [r for r in rows if r.get("player") in ("Drew Allar",)]
    dobbins = [r for r in rows if "Dobbins" in str(r.get("player"))]
    assert any(r.get("settlement") == "void" for r in allar + dobbins)


# ---------------------------------------------------------------- name joins (feeds Q2/Q3)
def test_current_suffix_variant_in_packet_is_not_matched(act):
    """G-04: the packet carries both 'Michael Pittman' and 'Michael Pittman Jr.'; only the exact box spelling matches."""
    assert act.resolve_full("Michael Pittman Jr.", "PIT")["reason"] == ""
    assert act.resolve_full("Michael Pittman", "PIT")["gsis_id"] == C.UNKNOWN
    assert act.resolve_full("Marvin Mims", "DEN")["gsis_id"] == C.UNKNOWN


@pytest.mark.xfail(strict=True, reason="G-04: resolve_full uses norm(), which keeps Jr./II/III; proposed suffix-insensitive key")
def test_proposed_suffix_insensitive_match(act):
    assert act.resolve_full("Michael Pittman", "PIT")["reason"] == ""
    assert act.resolve_full("Marvin Mims", "DEN")["reason"] == ""


# ---------------------------------------------------------------- Q2 / Q5: original projection and line
@needs_history
def test_packet_used_by_grader_is_the_packet_hashed_in_the_pr141_lock(packet):
    pk, src, pulled = packet
    assert src.startswith("git:aa60efa4")
    assert pulled == "2026-11-27T04:31:50+00:00"
    blob = subprocess.run(["git", "-C", str(ROOT), "show", f"{src.split(':')[1]}:{PACKET_REL}"],
                          capture_output=True, check=True).stdout
    lock = json.loads((LOCK_DIR / "LOCK.json").read_text())
    assert hashlib.sha256(blob).hexdigest() == lock["inputs"]["packet_sha256"]
    assert lock["inputs"]["price_freeze_pulled_utc"] == pk["books"]["retrieved_utc"] == "2026-11-27T04:26:21Z"


@needs_history
def test_every_graded_prop_line_is_the_packet_book_line_with_its_pull_time(graded, packet):
    rows, _ = graded
    pk, _, _ = packet
    src_rows = {(r["stat"], r["player"], r["book"]): r for r in pk["books"]["prop_check"]["rows"]}
    props = [r for r in rows if r["kind"] == "flagged_prop"]
    assert len(props) == len(pk["books"]["prop_check"]["rows"]) == 221
    for r in props:
        s = src_rows[(r["market_type"], r["player"], r["book"])]
        assert r["bet_line"]["value"] == s["line"]
        assert r["bet_line"]["pulled_utc"] == "2026-11-27T04:26:21Z"


@needs_history
def test_current_no_quote_after_bet_quote_so_clv_is_unknown_for_every_prop(graded):
    """G-06: the last saved DEN@PIT quote is 04:26:21Z (about 15.5 h before kick); no T-60/T-90 freeze exists."""
    rows, snaps = graded
    kick = C.parse_utc("2026-11-27T20:00:00Z")
    later = [s for s in snaps if C.parse_utc(s.get("snapshot_utc")) and
             C.parse_utc("2026-11-27T04:26:21Z") < C.parse_utc(s["snapshot_utc"]) < kick]
    assert later == []
    assert all(r["clv"]["positive"] == C.UNKNOWN for r in rows if r["kind"] == "flagged_prop")


@needs_history
def test_current_props_without_a_baseline_get_no_result(graded):
    """G-05: 116 of 221 prop_check rows have no baseline, so no side, so no result, even with actual and line known."""
    rows, _ = graded
    props = [r for r in rows if r["kind"] == "flagged_prop"]
    no_side = [r for r in props if r["side"] == C.UNKNOWN]
    assert len(no_side) == 121          # 116 with no baseline + 5 with baseline_minus_line exactly 0
    known_actual = [r for r in no_side if C.known(r["actual"]["value"])]
    assert known_actual and all(r["result"] == C.UNKNOWN for r in known_actual)


@needs_history
@pytest.mark.xfail(strict=True, reason="G-05: proposed side-neutral 'line_outcome' (over/under/push) on every row with actual+line")
def test_proposed_side_neutral_outcome_recorded(graded):
    rows, _ = graded
    for r in rows:
        if r["kind"] == "flagged_prop" and C.known(r["actual"]["value"]):
            assert r.get("line_outcome") in ("over", "under", "push")


@needs_history
def test_grade_counts_regression(graded):
    rows, _ = graded
    cnt = collections.Counter((r["kind"], r.get("result", "-")) for r in rows)
    assert cnt[("flagged_prop", "win")] == 34
    assert cnt[("flagged_prop", "loss")] == 55
    assert cnt[("flagged_prop", "unknown")] == 132
    assert all(r["projection_ready"] is False for r in rows)


# ---------------------------------------------------------------- Rico's slips and the PR #146 package
RICO_LEGS = ["Jonah Coleman anytime TD", "Pat Freiermuth 2+ receptions", "Jonah Coleman 70+ rush+rec yds",
             "Courtland Sutton 15+ rec yds", "Evan Engram 2+ receptions", "Jaylen Warren 60+ rush+rec yds",
             "Courtland Sutton 30+ rec yds", "Evan Engram over 2.5 receptions", "Jaylen Warren 2+ receptions",
             "Jaylen Warren anytime TD", "Jonah Coleman 1st-half anytime TD", "DK Metcalf 15+ rec yds",
             "Alternate game total Under 51.5"]


def test_rico_legs_are_the_ones_in_the_lock_file():
    text = (RUN_DIR / "RICO_SLIPS_LOCK.md").read_text()
    for leg in RICO_LEGS:
        assert leg in text, leg


@pytest.mark.parametrize("leg", RICO_LEGS)
def test_current_rico_leg_text_is_not_machine_parseable(leg):
    """G-02: Rico's slips are graded by hand in POSTGAME_REVIEW.md; parse_leg() reads none of the 13 leg strings."""
    assert R.parse_leg(leg) is None


def test_current_pr146_run_folder_is_not_discovered_by_research_grader():
    """G-01: research_runs only scans research/runs/*_<AWAY>_<HOME>*; the PR #146 package lives in runs/<date>_<AWAY>@<HOME>/."""
    dirs = [str(p.relative_to(ROOT)) for p in R.run_dirs(GAME)]
    assert not any(d.startswith("runs/") for d in dirs)
    assert RUN_DIR.is_dir()


def test_current_lock_research_grade_covers_team_means_and_win_prob_only(act):
    rr = R.grade_research(GAME, act, [], act.kickoff, "PIT", "DEN", FIXED_NOW)
    lock_rows = [r for r in rr if "snapshots/2026_12_DEN_PIT/20261127T111648Z" in r["artifact"]["path"]]
    kinds = collections.Counter(r["kind"] for r in lock_rows)
    assert kinds == {"research_team_projection": 4, "research_team_probability": 1}
    total = next(r for r in lock_rows if r.get("quantity") == "total")
    assert total["actual"]["value"] == 32 and round(total["projection"]["value"], 2) == 40.22
    if git_history_available():   # a depth-1 checkout reports the checkout commit's time instead
        assert total["artifact"]["committed_utc"] == "2026-11-27T06:20:29-05:00"     # PR #141 commit, before the 3:01 PM ET kick


def test_postgame_review_flags_its_own_post_kick_projection_file():
    """PREGAME_PROJECTION.md was written 3:02:19 PM ET, after the scheduled 3:01 PM ET kick; the review says so."""
    text = (RUN_DIR / "POSTGAME_REVIEW.md").read_text()
    assert "not a true pregame freeze" in text

"""Q3 / Q4 / Q6: participation (inactive, did-not-play, substitution, start), zero-stat games and error attribution.

The official NFL game summaries that data/gamebooks/ already parses carry the participation lists the grader is
missing. pg_audit_reference.py (in this folder, imported by nothing else) is the audit's proposed reader; these tests
check it against committed Week 11 gamebooks and pin how grading/sources.py treats the same situations today.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import pg_audit_reference as P
from _pg_common import ROOT
from grading import core as C
from grading import sources as S

WK11 = ROOT / "data" / "gamebooks" / "2026" / "wk11"


@pytest.fixture(scope="module")
def ari_kc():
    gb = P.load_gamebook(WK11 / "2026_11_ARI_KC")
    if gb is None:
        pytest.skip("Week 11 ARI@KC gamebook not present")
    return gb


@pytest.mark.parametrize("team,name,status", [
    ("ARZ", "Trey McBride", P.STARTED),            # lineups.csv offense TE 85 T.McBride
    ("ARZ", "Zonovan Knight", P.SUBSTITUTION),     # participation.csv substitution RB 20 Z.Knight
    ("ARZ", "Jacoby Aguilar", P.DID_NOT_PLAY),     # 'Did Not Play' list, QB 18 J.Aguilar
    ("ARZ", "Carson Beck", P.NOT_ACTIVE),          # 'Not Active' list, QB 19 C.Beck
    ("KC", "Kenneth Walker III", P.NOT_ACTIVE),    # suffix dropped: K.Walker
])
def test_gamebook_participation_classes(ari_kc, team, name, status):
    assert P.participation_status(ari_kc, team, name)["status"] == status


def test_gamebook_team_codes_are_printed_codes(ari_kc):
    """The PDF prints ARZ/BLT/CLV/HST; a caller passing nflverse ARI must map first (data/gamebooks/README.md)."""
    assert P.participation_status(ari_kc, "ARI", "Trey McBride")["status"] == C.UNKNOWN


@pytest.mark.parametrize("participation,settle", [
    (P.STARTED, P.GRADED), (P.SUBSTITUTION, P.GRADED), (P.DID_NOT_PLAY, P.VOID), (P.NOT_ACTIVE, P.VOID),
    (P.NOT_LISTED, C.UNKNOWN), (C.UNKNOWN, C.UNKNOWN),
])
def test_proposed_settlement_mapping(participation, settle):
    assert P.settlement_status(participation) == settle


def test_ambiguous_printed_name_is_unknown():
    gb = {"KC": {"j.smith": [P.STARTED, P.SUBSTITUTION]}}
    assert P.participation_status(gb, "KC", "Jaylen Smith")["status"] == C.UNKNOWN


def test_no_week12_gamebook_yet_for_den_pit():
    """Q1: the official game summary for DEN@PIT is not in the repo yet, so the ESPN box is the only final-stat source."""
    assert not (ROOT / "data" / "gamebooks" / "2026" / "wk12").exists() or \
        not (ROOT / "data" / "gamebooks" / "2026" / "wk12" / "2026_12_DEN_PIT").exists()


def test_current_grader_imports_no_gamebook_reader():
    for f in ("grade.py", "sources.py", "espn.py", "research_runs.py", "core.py"):
        assert "gamebook" not in (ROOT / "grading" / f).read_text().lower(), f


# ---------------------------------------------------------------- nflverse path: special-teams-only appearances
def _actuals(offense_snaps, st_snaps, pbp_rows):
    games = pd.DataFrame([{"game_id": "2026_11_ARI_KC", "week": 11, "home_team": "KC", "away_team": "ARI",
                           "home_score": 30, "away_score": 10}])
    cols = ["game_id", "play_type", "pass_attempt", "rush_attempt", "sack", "complete_pass", "two_point_attempt",
            "passer_player_id", "rusher_player_id", "receiver_player_id", "passing_yards", "rushing_yards", "receiving_yards"]
    pbp = pd.DataFrame(pbp_rows or [dict(zip(cols, ["2026_11_ARI_KC", "run", 0, 1, 0, 0, 0, None, "00-OTHER", None, 0, 4, 0]))],
                       columns=cols)
    rosters = pd.DataFrame([{"team": "ARI", "week": 11, "gsis_id": "00-TE2", "full_name": "Test Blocker"}])
    snaps = pd.DataFrame([{"game_id": "2026_11_ARI_KC", "team": "ARI", "player": "Test Blocker",
                           "offense_snaps": offense_snaps, "st_snaps": st_snaps}])
    return S.Actuals("2026_11_ARI_KC", games, pbp, rosters, snaps, {})


def test_offensive_snaps_without_a_touch_is_a_real_zero():
    a = _actuals(offense_snaps=22, st_snaps=0, pbp_rows=None)
    assert a.stat("00-TE2", "Test Blocker", "ARI", "receptions") == 0


def test_current_special_teams_only_player_is_unknown():
    """G-03 / G-09: _played() counts offensive snaps only, so a player who played 12 special-teams snaps is 'unknown'.
    Most books settle a played player's Over as a loss; whether ST-only counts as 'played' is Rico's rule to set."""
    a = _actuals(offense_snaps=0, st_snaps=12, pbp_rows=None)
    assert a.stat("00-TE2", "Test Blocker", "ARI", "receptions") == C.UNKNOWN


def test_current_no_snap_file_means_unknown_even_for_a_player_who_played():
    a = _actuals(offense_snaps=22, st_snaps=0, pbp_rows=None)
    a.snaps = None
    assert a.stat("00-TE2", "Test Blocker", "ARI", "receptions") == C.UNKNOWN


# ---------------------------------------------------------------- names
@pytest.mark.parametrize("a,b", [("Michael Pittman Jr.", "Michael Pittman"), ("Luther Burden III", "Luther Burden"),
                                 ("Ollie Gordon II", "Ollie Gordon"), ("Marvin Mims Jr.", "Marvin Mims")])
def test_proposed_name_key_is_suffix_insensitive(a, b):
    assert P.name_key(a) == P.name_key(b) != C.UNKNOWN
    assert S.norm(a) != S.norm(b)          # today's grading/sources.norm keeps the suffix (G-04)


def test_name_key_does_not_merge_different_players():
    assert P.name_key("Travis Etienne") != P.name_key("Trevor Etienne")


# ---------------------------------------------------------------- Q6: error attribution
def test_attribution_parts_sum_to_total_error():
    # Sutton-style miss: projected 7 targets at 9 yds/target (63), actual 8 targets for 4 yards
    out = P.attribute_error(proj_volume=7, proj_rate=9.0, act_volume=8, act_stat=4)
    assert out["projected"] == 63.0 and out["total_error"] == -59.0
    assert out["opportunity"] == 9.0 and out["efficiency"] == -68.0
    assert round(out["opportunity"] + out["efficiency"], 6) == out["total_error"]


def test_attribution_unknown_inputs_stay_unknown():
    out = P.attribute_error(7, 9.0, C.UNKNOWN, 4)
    assert set(out.values()) == {C.UNKNOWN}


def test_current_graded_rows_carry_only_a_single_error_number():
    """G-10: player_projection rows store error_actual_minus_projection only; no opportunity/efficiency/script split."""
    src = (ROOT / "grading" / "grade.py").read_text()
    assert "error_actual_minus_projection" in src
    for word in ("opportunity", "efficiency", "game_script", "attribution"):
        assert word not in src

"""Q5 / Q7 / Q8: timestamps, look-ahead and walk-forward ordering in the grading loop.

Uses throwaway git repositories under pytest's tmp_path, so nothing in the real repository is read for writing or
changed. Tests named test_current_* pin today's behaviour; xfail(strict=True) tests state the audit's proposal.
"""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone

import pytest

from _pg_common import FIXED_NOW, GAME, denpit_actuals
from grading import core as C
from grading import research_runs as R
from grading import sources as S

KICK = datetime(2026, 11, 27, 20, 0, tzinfo=timezone.utc)


def _git(root, *args, date=None):
    env = dict(os.environ, GIT_AUTHOR_NAME="audit", GIT_AUTHOR_EMAIL="audit@example.invalid",
               GIT_COMMITTER_NAME="audit", GIT_COMMITTER_EMAIL="audit@example.invalid")
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, env=env)


@pytest.fixture
def repo(tmp_path):
    _git(tmp_path, "init", "-q")
    return tmp_path


def _commit_packet(root, generated_utc, commit_date, books_line=20.5):
    rel = root / "pregame" / "packets" / GAME / "packet.json"
    rel.parent.mkdir(parents=True, exist_ok=True)
    rel.write_text(json.dumps({"generated_utc": generated_utc, "game": {"home": "PIT", "away": "DEN"},
                               "books": {"retrieved_utc": generated_utc, "line_marker": books_line}}))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", f"packet {generated_utc}", date=commit_date)


# ---------------------------------------------------------------- packet selection (Q5 / Q7)
def test_packet_generated_after_kickoff_is_never_selected(repo):
    _commit_packet(repo, "2026-11-27T04:31:50+00:00", "2026-11-27T04:33:57+00:00", books_line=20.5)
    _commit_packet(repo, "2026-11-27T21:00:00+00:00", "2026-11-27T21:01:00+00:00", books_line=99.5)   # post-kick refresh
    pk, src, pulled = S.packet_before_kickoff(GAME, KICK, root=repo)
    assert pulled == "2026-11-27T04:31:50+00:00" and pk["books"]["line_marker"] == 20.5


def test_no_pre_kickoff_packet_refuses(repo):
    _commit_packet(repo, "2026-11-27T21:00:00+00:00", "2026-11-27T21:01:00+00:00")
    pk, reason, _ = S.packet_before_kickoff(GAME, KICK, root=repo)
    assert pk is None and "before kickoff" in reason


def test_current_packet_committed_after_kickoff_is_accepted_on_its_own_generated_utc(repo):
    """G-07: selection trusts the packet's self-reported generated_utc; the commit time is not checked or recorded."""
    _commit_packet(repo, "2026-11-27T04:31:50+00:00", "2026-11-28T02:00:00+00:00")   # committed 6 h after kick
    pk, src, pulled = S.packet_before_kickoff(GAME, KICK, root=repo)
    assert pk is not None and pulled == "2026-11-27T04:31:50+00:00"


@pytest.mark.xfail(strict=True, reason="G-07: proposed: refuse (or flag) a packet whose commit time is at/after kickoff")
def test_proposed_packet_committed_after_kickoff_is_refused(repo):
    _commit_packet(repo, "2026-11-27T04:31:50+00:00", "2026-11-28T02:00:00+00:00")
    pk, _, _ = S.packet_before_kickoff(GAME, KICK, root=repo)
    assert pk is None


# ---------------------------------------------------------------- research artifacts (Q5 / Q7)
def _commit_legs(root, commit_date):
    d = root / "research" / "runs" / "2026-11-27_DEN_PIT_audit"
    d.mkdir(parents=True, exist_ok=True)
    (d / "legs.json").write_text(json.dumps({"Coleman 70+ R+R": {"p": 0.61}}))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "legs", date=commit_date)


def test_current_research_leg_committed_after_kickoff_is_graded_without_a_flag(repo):
    """G-08: grade_research reads the working-tree file and records committed_utc, but never compares it to kickoff."""
    _commit_legs(repo, "2026-11-28T02:00:00+00:00")
    act = denpit_actuals()
    rows = R.grade_research(GAME, act, [], KICK, "PIT", "DEN", FIXED_NOW, root=repo)
    leg = [r for r in rows if r["kind"] == "research_leg"]
    assert len(leg) == 1
    assert leg[0]["result"] == "win" and leg[0]["actual"]["value"] == 72          # Coleman 26 rush + 46 rec
    assert C.parse_utc(leg[0]["artifact"]["committed_utc"]) > KICK
    assert "post_kickoff" not in json.dumps(leg[0])


@pytest.mark.xfail(strict=True, reason="G-08: proposed: research rows carry pre_kickoff=true/false and post-kick artifacts are excluded")
def test_proposed_research_leg_committed_after_kickoff_is_excluded(repo):
    _commit_legs(repo, "2026-11-28T02:00:00+00:00")
    rows = R.grade_research(GAME, denpit_actuals(), [], KICK, "PIT", "DEN", FIXED_NOW, root=repo)
    assert not [r for r in rows if r["kind"] == "research_leg" and r.get("pre_kickoff") is not True]


# ---------------------------------------------------------------- CLV and holdout ordering (Q7 / Q8)
def _snap(t, line, over=-110, under=-110):
    return {"market_key": "receptions|X", "book": "fanduel", "line": line, "prices": {"Over": over, "Under": under},
            "snapshot_utc": t, "source": "test", "quote_utc": t}


def test_closing_quote_ignores_snapshots_at_or_after_kickoff():
    snaps = [_snap("2026-11-27T19:00:00Z", 3.5), _snap("2026-11-27T20:00:00Z", 4.5), _snap("2026-11-27T21:00:00Z", 5.5)]
    assert C.closing_quote(snaps, "receptions|X", "fanduel", KICK)["line"] == 3.5


def test_clv_against_the_bet_quote_itself_is_unknown_not_a_tie():
    s = _snap("2026-11-27T04:26:21Z", 2.5)
    out = C.clv("receptions", "Over", "PIT", 2.5, s["prices"], s, bet_utc="2026-11-27T04:26:21Z")
    assert out["positive"] == C.UNKNOWN


def _graded_row(game, kickoff, positive, market="receptions"):
    return {"kind": "flagged_prop", "market_type": market, "game_id": game, "kickoff_utc": kickoff,
            "market_key": f"{market}|P{game}", "side": "Over", "clv": {"positive": positive},
            "bet_break_even": {"value": 0.52}}


def test_holdout_record_uses_only_earlier_games():
    rows = [_graded_row("2026_11_A_B", "2026-11-22T18:00:00+00:00", True),
            _graded_row(GAME, "2026-11-27T20:00:00+00:00", True),                 # this game: excluded
            _graded_row("2026_12_C_D", "2026-11-29T18:00:00+00:00", True)]        # later game: excluded
    rec = C.clv_record(rows, "receptions", KICK, GAME, min_n=1)
    assert rec["n"] == 1 and rec["beat_close"] == 1


def test_holdout_unknown_clv_rows_do_not_count():
    rows = [_graded_row(f"2026_11_G{i}_H", "2026-11-22T18:00:00+00:00", C.UNKNOWN) for i in range(40)]
    rec = C.clv_record(rows, "receptions", KICK, GAME, min_n=30)
    assert rec["n"] == 0 and rec["holdout_ready"] is False and rec["positive"] is False


# ---------------------------------------------------------------- readiness spots (Q8)
def _results_dir(tmp_path, books=("fanduel", "draftkings", "betmgm")):
    d = tmp_path / "results"
    d.mkdir()
    rows = []
    for bk in books:   # one bet idea (same game, player, market, side), quoted at several books
        rows.append({"kind": "flagged_prop", "game_id": "2026_12_DEN_PIT", "market_type": "rushing_yards",
                     "market_key": "rushing_yards|Jonah Coleman", "side": "Under", "book": bk, "result": "win",
                     "kickoff_utc": "2026-11-27T20:00:00+00:00",
                     "bet_price": {"value": -115, "pulled_utc": "2026-11-27T04:26:21Z", "source": "test"}})
    (d / "2026_12_DEN_PIT.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return d


def test_current_readiness_counts_each_book_quote_as_a_separate_spot(tmp_path):
    """G-11: evaluation.readiness.spots() keeps one spot per book row. On main today that is 1,067 spots for 288 distinct
    (game, market, side) bets, and the bootstrap CI treats them as independent. clv_record() already dedupes."""
    from evaluation import readiness as RD
    sp, _ = RD.spots(_results_dir(tmp_path))
    assert len(sp) == 3


@pytest.mark.xfail(strict=True, reason="G-11: proposed: one spot per (game, market_key, side), best-priced quote, like clv_record")
def test_proposed_readiness_dedupes_book_quotes(tmp_path):
    from evaluation import readiness as RD
    sp, _ = RD.spots(_results_dir(tmp_path))
    assert len(sp) == 1

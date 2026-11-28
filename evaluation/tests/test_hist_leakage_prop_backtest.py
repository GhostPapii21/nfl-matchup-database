"""Historical leakage audit: dashboard/backtest_opportunity.py (the historical player-prop backtest behind the board's
chance tables, the calibration layer and research/model_audit_2026-11-24).

Behavioural tests on a synthetic league (evaluation/tests/hist_leakage_synth.py): we change only data from the target
week or later and check whether the projection for the target game moves. Tests marked xfail document a REAL finding
in production code; they must not be "fixed" by weakening the assertion. See docs/audits/historical_leakage_audit.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dashboard import backtest_opportunity as B  # noqa: E402
import hist_leakage_synth as S  # noqa: E402

SEASON, PREV = 2031, 2030
TARGET_WEEK = 7


def _league(season, zero_weeks=None, status_override=None, mutate=None):
    sc = S.schedule(season)
    p = S.pbp(season, sc, zero_weeks=zero_weeks)
    if mutate is not None:
        p = mutate(p)
    return sc, p, S.roster(season, sc, status_override)


def _run(monkeypatch, tmp_path, cur, prev):
    sc_c, p_c, r_c = cur
    sc_p, p_p, r_p = prev
    pd.concat([sc_p, sc_c]).to_parquet(tmp_path / "games.parquet")
    data = {SEASON: (p_c, r_c), PREV: (p_p, r_p)}
    monkeypatch.setattr(B, "CACHE", tmp_path)
    monkeypatch.setattr(B, "load", lambda s: data[s])
    monkeypatch.setattr(B, "NS", 400)
    return pd.DataFrame(B.run_season(SEASON, PREV))


def _target(df):
    return df[(df.week == TARGET_WEEK)].set_index(["player", "kind"]).sort_index()


PRED_COLS = ["exp_targets", "exp_carries", "pred_yards_mean", "share", "games_prior"]


def _preds(df):
    t = _target(df)
    cols = [c for c in PRED_COLS if c in t] + [c for c in t if c.startswith("p_")]
    return t[cols]


def test_future_weeks_do_not_move_target_week_projection(monkeypatch, tmp_path):
    """Rolling/share/rate inputs must use weeks < target only: inflate every yard gained in weeks >= target."""
    base = _run(monkeypatch, tmp_path, _league(SEASON), _league(PREV))

    def future_boom(p):
        p = p.copy()
        m = p.week >= TARGET_WEEK
        p.loc[m, "receiving_yards"] = p.loc[m, "receiving_yards"] * 5
        p.loc[m, "rushing_yards"] = p.loc[m, "rushing_yards"] * 5
        return p
    moved = _run(monkeypatch, tmp_path, _league(SEASON, mutate=future_boom), _league(PREV))
    a, b = _preds(base), _preds(moved)
    assert len(a) > 0
    pd.testing.assert_frame_equal(a, b)


def test_opponent_defense_uses_only_prior_weeks(monkeypatch, tmp_path):
    """Opponent-allowed rates: make the target opponent's defence allow 0 completions from the target week on."""
    sc = S.schedule(SEASON)
    opp = sc[(sc.week == TARGET_WEEK) & (sc.home_team == "AAA")].away_team.iloc[0]
    base = _run(monkeypatch, tmp_path, _league(SEASON), _league(PREV))

    def shut_down(p):
        p = p.copy()
        m = (p.defteam == opp) & (p.week >= TARGET_WEEK)
        p.loc[m, "complete_pass"] = 0
        p.loc[m, "receiving_yards"] = 0.0
        return p
    moved = _run(monkeypatch, tmp_path, _league(SEASON, mutate=shut_down), _league(PREV))
    pd.testing.assert_frame_equal(_preds(base), _preds(moved))


def test_active_zero_stat_player_stays_in_population(monkeypatch, tmp_path):
    """An ACTIVE receiver with 0 targets in the target game must be scored (actual 0), not dropped."""
    zw = {("AAA", TARGET_WEEK): {"WR1"}}
    df = _run(monkeypatch, tmp_path, _league(SEASON, zero_weeks=zw), _league(PREV))
    row = df[(df.week == TARGET_WEEK) & (df.player == "AAA_WR1") & (df.kind == "rec")]
    assert len(row) == 1
    assert row.actual_yards.iloc[0] == 0.0 and row.actual_targets.iloc[0] == 0


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED): backtest_opportunity.py:82-83,107,135 keep only players whose GAME-DAY roster status is ACT for the "
    "target week. Game-day inactives are dropped from the evaluation population and their status is read from the "
    "final weekly roster, not a pre-kickoff snapshot. There is no 'inactive' row or counter, so the population "
    "shrink is invisible in opportunity_backtest.json."))
def test_inactive_player_is_counted_not_silently_dropped(monkeypatch, tmp_path):
    zw = {("AAA", TARGET_WEEK): {"WR1"}}
    st = {("AAA", TARGET_WEEK, "WR1"): "INA"}
    df = _run(monkeypatch, tmp_path, _league(SEASON, zero_weeks=zw, status_override=st), _league(PREV))
    row = df[(df.week == TARGET_WEEK) & (df.player == "AAA_WR1")]
    # Acceptable fixes: keep the row flagged (e.g. column 'availability'='INA') so it can be voided explicitly.
    assert len(row) >= 1 and "availability" in df.columns


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED): the 'active' filter (backtest_opportunity.py:82) reads roster_weekly status for the target week, "
    "which is the post-hoc game-day status. A pre-kickoff projection cannot know it. Changing ONLY the target-week "
    "status of a player changes whether he is projected at all (look-ahead selection)."))
def test_target_week_status_does_not_change_who_is_projected(monkeypatch, tmp_path):
    a = _run(monkeypatch, tmp_path, _league(SEASON), _league(PREV))
    st = {("AAA", TARGET_WEEK, "WR2"): "INA"}
    b = _run(monkeypatch, tmp_path, _league(SEASON, status_override=st), _league(PREV))
    ka = set(map(tuple, a[a.week == TARGET_WEEK][["player", "kind"]].values))
    kb = set(map(tuple, b[b.week == TARGET_WEEK][["player", "kind"]].values))
    assert ka == kb


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED): backtest_opportunity.py:77 builds the position map from the WHOLE current-season roster "
    "(all weeks, later rows win), so a position change later in the season is applied to earlier projections."))
def test_position_map_is_point_in_time(monkeypatch, tmp_path):
    sc = S.schedule(SEASON)

    def later_te(r):
        r = r.copy()
        r.loc[(r.gsis_id == "AAA_WR2") & (r.week >= TARGET_WEEK + 1), "position"] = "TE"
        return r
    cur = _league(SEASON)
    cur_changed = (cur[0], cur[1], later_te(cur[2]))
    a = _run(monkeypatch, tmp_path, cur, _league(PREV))
    b = _run(monkeypatch, tmp_path, cur_changed, _league(PREV))
    pa = a[(a.week == TARGET_WEEK) & (a.player == "AAA_WR2")].pos.tolist()
    pb = b[(b.week == TARGET_WEEK) & (b.player == "AAA_WR2")].pos.tolist()
    assert pa == pb, (pa, pb)


def test_threshold_hit_rate_and_brier_are_reported(monkeypatch, tmp_path):
    df = _run(monkeypatch, tmp_path, _league(SEASON), _league(PREV))
    res = B.evaluate(df)
    t = res["rec"]["thresholds"][0]
    assert {"hit_rate", "brier_sim", "calibration"} <= set(t)


@pytest.mark.xfail(strict=True, reason=(
    "MISSING METRIC (LOW): backtest_opportunity.evaluate() (lines 163-181) reports Brier and a reliability table but "
    "no log loss, so over-confident tails (p near 0/1 on 100+ yard rungs) are under-penalised."))
def test_log_loss_is_reported(monkeypatch, tmp_path):
    df = _run(monkeypatch, tmp_path, _league(SEASON), _league(PREV))
    t = B.evaluate(df)["rec"]["thresholds"][0]
    assert any("log" in k.lower() for k in t)

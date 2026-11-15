"""NFL-75 stricter readiness report (outside-AI review memo B11 / item 5; refs NFL-75).

Report-only columns are layered on Rico's n>=30 / +3-pt / game-cluster CI bar; they do not change that bar or
projection_ready. fit() cannot promote a market unless the week-clustered margin and profit CIs both clear 0.
Only countable legs count when the column is present. Synthetic data only; no network.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from calibration import selective_edge as se
from calibration.tests.test_selective_edge import _graded, _train, leg


def test_countable_allowlist_rejects_the_string_false():
    assert se.is_countable(True) is True and se.is_countable("true") is True and se.is_countable(1) is True
    for v in (False, None, 0, "false", "False", "no", "", "TRUE "):
        # "TRUE " stripped lower is "true" — allow. Test the clearly-off values:
        if str(v).strip().lower() == "true":
            continue
        assert se.is_countable(v) is False, v
    assert se.is_countable("TRUE") is True
    keep, meta = se.countable_rows(pd.DataFrame({"countable": [True, "true", "false", False, 1, 0]}))
    assert list(keep.index) == [0, 1, 4] and meta["n_excluded_not_countable"] == 3
    allr, missing = se.countable_rows(pd.DataFrame({"x": [1]}))
    assert missing["countable_filter"] == "absent" and len(allr) == 1


def test_summarize_week_cluster_adds_profit_ci_and_week_count():
    df = se.settle(_train(24, 16))   # 4 weeks, 10 legs each, 6-4 every week
    g = se.summarize(df, B=2000, cluster="game")
    w = se.summarize(df, B=2000, cluster="week")
    assert g["n"] == 40 and w["n"] == 40 and w["n_weeks"] == 4 and w["weeks_ge_4"] is True
    assert w["cluster"] == "week" and w["week_bootstrap_degenerate"] is False
    assert w["roi_lo"] > 0 and w["profit_ci_gt_0"] is True and se.ci_clears_zero(w)
    # game-cluster margin CI is still deterministic and matches the original contract
    a, b = se.summarize(df, B=2000), se.summarize(df, B=2000)
    assert a["margin_lo"] == b["margin_lo"] and a["n"] == 40


def test_week_bootstrap_is_degenerate_on_a_single_week():
    df = se.settle(_train(24, 6).assign(week=8))
    w = se.summarize(df, B=500, cluster="week")
    assert w["n_weeks"] == 1 and w["weeks_ge_4"] is False and w["week_bootstrap_degenerate"] is True
    assert w["profit_ci_gt_0"] is False and se.ci_clears_zero(w) is False
    # the interval collapses to the point estimate
    assert w["margin_lo"] == pytest.approx(w["margin"]) and w["roi_lo"] == pytest.approx(w["roi"])


def test_fit_still_promotes_the_balanced_n40_plus3_four_week_sample():
    """Existing contract: 24-16 over weeks 4-7 at -110 is strong, and the week-clustered CIs also clear 0."""
    p = se.fit(_train(24, 16))
    assert p["strong_markets"] == ["rushyds"] and p["projection_ready"] is False
    assert p["rules"]["promote_requires_week_clustered_ci"] is True
    row = next(r for r in p["train_strong_under_by_market"] if r["market"] == "rushyds")
    assert row["promoted"] is True and row["n_weeks"] == 4 and row["profit_ci_gt_0"] is True


def test_fit_will_not_promote_when_week_clustered_profit_ci_crosses_zero():
    """n=40 and +7.6 pts, but all the profit is in one week and the other is a blowout loss: CI must block promotion."""
    rows = []
    # week 4: 24-0, weeks 5-7: 0-16 split across 16 games (one terrible cluster + three empty-ish loss weeks)
    for i in range(24):
        rows.append(leg(week=4, game_id=f"w4-{i}", gsis=f"p{i}", actual=40.0))
    for i in range(16):
        rows.append(leg(week=5 + (i % 3), game_id=f"wx-{i}", gsis=f"q{i}", actual=80.0))
    p = se.fit(pd.DataFrame(rows))
    assert p["strong_markets"] == []
    row = next(r for r in p["train_strong_under_by_market"] if r["market"] == "rushyds")
    assert row["n"] == 40 and row["margin"] >= se.STRONG_MIN_MARGIN - 1e-12
    assert row["promoted"] is False
    assert row["week_bootstrap_degenerate"] is False
    assert not (row["roi_lo"] > 0 and row["margin_lo"] > 0)


def test_fit_counts_only_countable_legs_when_the_column_is_present():
    df = _train(24, 16)
    df["countable"] = [True] * 20 + [False] * 20   # first 20 are wins, so countable n=20 < 30
    p = se.fit(df)
    assert p["strong_markets"] == []
    assert p["rules"]["countable_filter"] == "countable_only"
    row = next(r for r in p["train_strong_under_by_market"] if r["market"] == "rushyds")
    assert row["n"] == 20 and row["n_excluded_not_countable"] == 20


def test_graduation_bar_is_unchanged_and_strict_flags_are_report_only():
    # same rows as the existing bar tests: all week=10, so weeks_ge_4 is false and strict_checks_pass is false,
    # but status still follows Rico's n>=30 / +3 / game-cluster CI bar.
    g = se.graduation(_graded(24, 6))
    r = g.iloc[0]
    assert r.status == se.SPOT_READY and r.n == 30 and r.margin_lo > 0
    assert r.weeks_ge_4 == False and r.week_bootstrap_degenerate == True
    assert r.strict_checks_pass == False and r.projection_ready == False
    assert se.graduation(_graded(20, 9)).iloc[0].status != se.SPOT_READY
    assert se.graduation(_graded(17, 13)).iloc[0].status != se.SPOT_READY
    assert se.graduation(_graded(16, 14, dec=1.80)).iloc[0].status != se.SPOT_READY


def test_graduation_strict_checks_pass_on_four_profitable_weeks():
    # 24-6 over weeks 4-7: n=30 and the game-cluster CI clears (Rico's bar), and the week-clustered
    # profit/margin CIs also clear, so strict_checks_pass is True. projection_ready stays False.
    df = se.settle(_train(24, 6).assign(source="live"))
    df["label"] = se.STRONG_UNDER
    df["countable"] = True
    g = se.graduation(df)
    r = g.iloc[0]
    assert r.status == se.SPOT_READY and r.weeks_ge_4 == True and r.profit_ci_gt_0 == True
    assert r.strict_checks_pass == True and r.countable_filter == "countable_only"
    assert r.week_roi_lo > 0 and r.projection_ready == False


def test_graduation_excludes_non_countable_legs():
    live = _graded(24, 6)
    live["countable"] = [True] * 20 + [False] * 10
    g = se.graduation(live)
    r = g.iloc[0]
    assert r.n == 20 and r.n_excluded_not_countable == 10
    assert r.status != se.SPOT_READY and r.projection_ready == False


def test_graduation_never_writes_projection_ready_true():
    df = se.settle(_train(24, 16).assign(source="live", countable=True))
    df["label"] = se.STRONG_UNDER
    g = se.graduation(df)
    assert (g.projection_ready == False).all()  # noqa: E712

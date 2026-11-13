"""NFL-75 Phase 4 selective-edge classifier: Rico's gates, labels, holdout refusal, graduation rule.
Synthetic legs only (no book prices, no network). Research only; projection_ready stays false."""
from __future__ import annotations
import math

import numpy as np
import pandas as pd
import pytest

from calibration import selective_edge as se

PARAMS = {"strong_markets": ["rushyds"], "alt_min_cushion": 0.20, "train_weeks": [4, 5, 6, 7]}


def leg(**kw):
    d = dict(week=8, game_id="2026_08_AAA_BBB", gsis="00-1", player="P", position="RB", market="rushyds",
             side="Under", kind="main", line=60.5, dec=1.91, p_nv=0.50, p_model=0.55, defender_verified=False,
             carry_n_prior=4, carry_n60=4, usual=np.nan, price_source="book:test", actual=np.nan, source="live")
    d.update(kw)
    return d


def lab(rows, params=PARAMS):
    return se.classify(pd.DataFrame(rows), params)


# ---------- gates ----------
def test_passing_yards_market_excluded():
    out = lab([leg(market="passyds", position="QB"), leg(market="pass_yds", position="QB")])
    assert (out.label == se.NO_EDGE).all() and (out.reason == "excluded_market_passing").all()


def test_rb_under_60pct_carry_share_is_do_not_play():
    out = lab([leg(carry_n60=2), leg(carry_n60=3)])
    assert out.label.tolist() == [se.NO_EDGE, se.STRONG_UNDER]
    assert out.reason.iloc[0] == "do_not_play_rb_carry_lt_60"


def test_rb_without_carry_history_is_insufficient():
    out = lab([leg(carry_n_prior=2, carry_n60=2), leg(carry_n_prior=np.nan, carry_n60=np.nan)])
    assert (out.label == se.INSUFFICIENT).all() and (out.reason == "carry_history_unknown").all()


def test_qb_rush_leg_not_subject_to_rb_carry_gate():
    out = lab([leg(position="QB", carry_n_prior=np.nan, carry_n60=np.nan)])
    assert out.label.iloc[0] == se.STRONG_UNDER


def test_receiving_leg_needs_verified_main_defender():
    rows = [leg(market="recyds", position="WR"), leg(market="rec", position="TE", defender_verified=np.nan),
            leg(market="recyds", position="WR", defender_verified=True)]
    out = lab(rows)
    assert out.label.tolist() == [se.INSUFFICIENT, se.INSUFFICIENT, se.STANDARD]
    assert out.reason.iloc[0] == "main_defender_unverified"


def test_missing_price_is_insufficient_never_filled():
    rows = [leg(dec=np.nan), leg(kind="alt", side="Over", line=30.5, usual=80, dec=np.nan, p_nv=np.nan),
            leg(price_source=None)]
    out = lab(rows)
    assert (out.label == se.INSUFFICIENT).all()
    assert out.reason.tolist() == ["price_missing", "alt_price_missing", "price_missing"]
    assert out.dec.isna().iloc[:2].all()  # classifier never invents a price


def test_missing_model_probability_is_insufficient():
    out = lab([leg(p_model=np.nan)])
    assert out.label.iloc[0] == se.INSUFFICIENT and out.reason.iloc[0] == "model_prob_missing"


# ---------- edge tiers are flags, not cuts ----------
def test_edge_tiers_flag_but_do_not_cut():
    out = lab([leg(p_model=0.505), leg(p_model=0.52), leg(p_model=0.56)])
    assert (out.label == se.STRONG_UNDER).all()
    assert out.edge_tier.tolist() == ["", "+1", "+3"]


def test_model_disagreeing_with_under_is_no_edge():
    out = lab([leg(p_model=0.45)])
    assert out.label.iloc[0] == se.NO_EDGE and out.reason.iloc[0] == "model_disagrees"


def test_strong_under_only_for_markets_fit_as_strong():
    out = lab([leg(), leg(position="QB")], params={**PARAMS, "strong_markets": []})
    assert (out.label == se.STANDARD).all()


# ---------- alt floors ----------
def test_alt_floor_needs_line_at_or_below_usual_output_and_cushion():
    base = dict(kind="alt", side="Over", p_nv=np.nan, dec=1.30, p_model=0.85, usual=80.0)
    rows = [leg(line=59.5, **base),   # cushion 25.6% -> candidate
            leg(line=70.5, **base),   # cushion 11.9% < 20% -> no edge
            leg(line=85.5, **base),   # above usual output
            leg(line=59.5, **{**base, "usual": np.nan})]
    out = lab(rows)
    assert out.label.tolist() == [se.ALT_LINE, se.NO_EDGE, se.NO_EDGE, se.INSUFFICIENT]
    assert out.reason.tolist()[1:] == ["cushion_below_min", "alt_above_usual_output", "usual_output_unknown"]
    assert math.isclose(out.cushion.iloc[0], (80 - 59.5) / 80)


def test_alt_floor_disabled_when_not_shown_in_train():
    out = lab([leg(kind="alt", side="Over", line=40.5, usual=80, dec=1.3, p_nv=np.nan, p_model=0.9)],
              params={**PARAMS, "alt_min_cushion": None})
    assert out.label.iloc[0] == se.NO_EDGE and out.reason.iloc[0] == "alt_floor_not_shown_in_train"


def test_alt_edge_is_vs_break_even_of_real_price():
    out = lab([leg(kind="alt", side="Over", line=40.5, usual=80, dec=1.25, p_nv=np.nan, p_model=0.79)])
    assert out.label.iloc[0] == se.NO_EDGE  # 0.79 < 1/1.25 = 0.80
    assert math.isclose(out.edge.iloc[0], 0.79 - 0.80)


# ---------- context is point in time ----------
def _pbp():
    rows = []
    for w in range(1, 10):
        for i in range(10):  # 10 team carries per game; RB A gets 7 (70%) in weeks 1-8, 2 in week 9
            rb = "A" if i < (7 if w < 9 else 2) else "B"
            rows.append(dict(week=w, game_id=f"g{w}", posteam="T", rush_attempt=1, qb_kneel=0, pass_attempt=0,
                             rusher_player_id=rb, receiver_player_id=None, rushing_yards=10.0, receiving_yards=np.nan,
                             complete_pass=0, two_point_attempt=0, season_type="REG"))
    return pd.DataFrame(rows)


def test_context_uses_only_prior_weeks():
    pbp = _pbp()
    legs = pd.DataFrame([leg(gsis="A", week=9)])
    a = se.attach_context(legs, pbp)
    pbp2 = pbp.copy()
    pbp2.loc[pbp2.week >= 9, "rushing_yards"] = 999.0
    pbp2.loc[(pbp2.week >= 9), "rusher_player_id"] = "B"
    b = se.attach_context(legs, pbp2)
    cols = ["carry_n_prior", "carry_n60", "carry_share", "usual"]
    pd.testing.assert_frame_equal(a[cols], b[cols])
    assert a.carry_n_prior.iloc[0] == 4 and a.carry_n60.iloc[0] == 4 and a.usual.iloc[0] == 70.0


def test_context_excludes_kneels_and_two_point():
    pbp = _pbp()
    extra = pbp.iloc[[0]].assign(rusher_player_id="B", qb_kneel=1)
    a = se.attach_context(pd.DataFrame([leg(gsis="A", week=2)]), pd.concat([pbp, extra]))
    assert a.carry_share.iloc[0] == pytest.approx(0.7)


# ---------- holdout refusal ----------
def test_fit_refuses_any_week_outside_4_7():
    df = pd.DataFrame([leg(week=w) for w in (4, 5, 8)])
    with pytest.raises(se.HoldoutError):
        se.fit(df)
    with pytest.raises(se.HoldoutError, match="holdout"):
        se.fit(pd.DataFrame([leg(week=10)]))


def test_evaluate_refuses_holdout_and_train_weeks():
    for w in (10, 11, 12):
        with pytest.raises(se.HoldoutError, match="holdout"):
            se.evaluate(pd.DataFrame([leg(week=w)]), PARAMS)
    with pytest.raises(se.HoldoutError):
        se.evaluate(pd.DataFrame([leg(week=7)]), PARAMS)
    out = se.evaluate(pd.DataFrame([leg(week=8, actual=40.0), leg(week=9, actual=70.0)]), PARAMS)
    assert out.win.tolist() == [1.0, 0.0]


def _train(n_win, n_loss, market="rushyds", position="RB", **kw):
    rows = []
    for i in range(n_win + n_loss):
        rows.append(leg(week=4 + i % 4, game_id=f"g{i}", gsis=f"p{i}", market=market, position=position,
                        actual=(40.0 if i < n_win else 80.0), **kw))
    return pd.DataFrame(rows)


def test_fit_marks_market_strong_only_with_n30_and_plus3():
    p = se.fit(_train(24, 16))   # 60% vs BE 52.4% -> strong
    assert p["strong_markets"] == ["rushyds"]
    assert se.fit(_train(21, 19))["strong_markets"] == []   # 52.5% -> below +3
    assert se.fit(_train(20, 9))["strong_markets"] == []    # n=29
    assert p["train_weeks"] == [4, 5, 6, 7] and p["projection_ready"] is False


# ---------- settlement & summary ----------
def test_settle_under_over_push():
    df = pd.DataFrame([leg(actual=40.0), leg(actual=60.5), leg(actual=61.0),
                       leg(kind="alt", side="Over", line=30.5, actual=31.0)])
    s = se.settle(df)
    assert s.win.tolist()[0] == 1.0 and s.push.tolist() == [0, 1, 0, 0]
    assert np.isnan(s.win.iloc[1]) and s.win.iloc[2] == 0.0 and s.win.iloc[3] == 1.0


def test_summary_margin_and_cluster_bootstrap_deterministic():
    df = se.settle(_train(18, 5).assign(week=8))
    a, b = se.summarize(df, B=2000), se.summarize(df, B=2000)
    assert (a["n"], a["W"], a["L"]) == (23, 18, 5)
    assert a["margin"] == pytest.approx(18 / 23 - 1 / 1.91)
    assert a == b and a["margin_lo"] < a["margin"] < a["margin_hi"]


# ---------- graduation rule (report-only) ----------
def _graded(n_win, n_loss, source="live", label=None, dec=1.91):
    df = se.settle(_train(n_win, n_loss).assign(week=10, source=source, dec=dec))
    df["label"] = label or se.STRONG_UNDER
    return df


def test_graduation_needs_n30_plus3_and_ci_above_zero():
    g = se.graduation(_graded(24, 6))
    r = g.iloc[0]
    assert r.status == se.SPOT_READY and r.n == 30 and r.margin_lo > 0
    assert se.graduation(_graded(20, 9)).iloc[0].status != se.SPOT_READY            # n=29
    assert se.graduation(_graded(17, 13)).iloc[0].status != se.SPOT_READY           # +4.3 but CI crosses 0
    assert se.graduation(_graded(16, 14, dec=1.80)).iloc[0].status != se.SPOT_READY  # +2.0 < +3


def test_graduation_counts_only_requested_sources_and_real_prices():
    live = _graded(10, 2)
    oos = _graded(18, 5, source="backtest_oos").assign(week=8)
    nopx = _graded(5, 0).assign(dec=np.nan)
    allr = pd.concat([live, oos, nopx], ignore_index=True)
    g_live = se.graduation(allr)
    assert g_live.iloc[0].n == 12 and g_live.iloc[0].excluded_no_real_price == 5
    g_comb = se.graduation(allr, sources=("live", "backtest_oos"))
    assert g_comb.iloc[0].n == 35


def test_graduation_never_flips_projection_ready():
    g = se.graduation(_graded(28, 2))
    assert (g.projection_ready == False).all()  # noqa: E712
    assert not hasattr(se, "set_projection_ready")


def test_graduation_ignores_non_candidate_labels():
    df = pd.concat([_graded(28, 2), _graded(28, 2, label=se.NO_EDGE), _graded(28, 2, label=se.INSUFFICIENT)])
    g = se.graduation(df)
    assert set(g.label) == {se.STRONG_UNDER}

"""NFL-75 (outside-AI review memo B1, B5, B6): one settlement + EV module and the emitter's EV-at-price label gate.
Synthetic data only; no network. Research only; projection_ready stays false."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from calibration import selective_edge as se
from calibration import selective_edge_emit as EM
from calibration import settlement_ev as S
from calibration.tests import test_selective_edge_emit as T

ROOT = Path(__file__).resolve().parents[2]
M110 = float(S.american_to_decimal(-110))


# ---------------------------------------------------------------- invariants
@pytest.mark.parametrize("line", [2.5, 3.0, 0.5, 40.0])
def test_three_way_split_sums_to_one_and_half_lines_never_push(line):
    x = np.random.default_rng(0).poisson(3.2, 50_000).astype(float)
    pu, pp, po = S.split_from_samples(x, line)
    assert pu + pp + po == pytest.approx(1.0, abs=1e-12)
    if not float(line).is_integer():
        assert pp == 0.0
    else:
        assert pp == pytest.approx(np.mean(x == line))


def test_integer_two_way_line_pushes_but_milestone_wins_at_equality():
    x = np.array([39.0, 40.0, 40.0, 41.0])
    assert S.split_from_samples(x, 40.0) == (0.25, 0.5, 0.25)
    assert S.split_from_samples(x, 40.0, milestone=True) == (0.25, 0.0, 0.75)   # "40+" wins at exactly 40
    w, p = S.settle_outcome([40, 40, 39, 41, np.nan], [40] * 5, ["Over", "Under", "Under", "Over", "Over"])
    assert list(p) == [1, 1, 0, 0, 0] and np.isnan(w[0]) and np.isnan(w[1]) and w[2] == 1 and w[3] == 1
    assert np.isnan(w[4])
    w, p = S.settle_outcome([40, 39], [40, 40], ["Over", "Over"], milestone=True)
    assert list(w) == [1.0, 0.0] and list(p) == [0, 0]


def test_split_from_ge_refuses_to_put_the_push_in_the_over():
    pu, pp, po = S.split_from_ge(0.6, 3.0)               # integer line, no P(x == 3): unknown, not 0.4 / 0.6
    assert np.isnan(pp) and np.isnan(po)
    pu, pp, po = S.split_from_ge(0.6, 3.0, p_eq=0.15)
    assert (float(pu), float(pp), float(po)) == pytest.approx((0.4, 0.15, 0.45))
    pu, pp, po = S.split_from_ge(0.6, 3.5)
    assert (float(pu), float(pp), float(po)) == pytest.approx((0.4, 0.0, 0.6))
    pu, pp, po = S.split_from_ge(0.6, 40.0, milestone=True)
    assert (float(pu), float(pp), float(po)) == pytest.approx((0.4, 0.0, 0.6))


# ---------------------------------------------------------------- EV at the price (B1, B5)
def test_break_even_is_the_price_not_the_no_vig():
    assert float(S.break_even(M110)) == pytest.approx(110 / 210)          # 0.5238, not the 0.500 no-vig
    assert float(S.ev_at_price(0.51, 0.0, M110)) < 0                      # memo B1 example: negative EV
    assert float(S.ev_at_price(0.53, 0.0, M110)) > 0
    assert float(S.break_even(M110, 0.10)) == pytest.approx(0.9 * 110 / 210)


def test_game_ev_is_p_win_times_net_odds_not_gross():
    # memo B5: pw*dec - (1-pw-pp) overstated EV by exactly pw
    pw, pp, d = 0.55, 0.05, 1.95
    assert float(S.ev_at_price(pw, pp, d)) == pytest.approx(pw * (d - 1) - (1 - pw - pp))
    assert pw * d - (1 - pw - pp) - float(S.ev_at_price(pw, pp, d)) == pytest.approx(pw)


def test_push_refund_ev_and_decisive_conversion():
    # P(win|no push)=0.55 with 10% push at +100: unconditional win 0.495, loss 0.405 -> EV 0.09
    pw = float(S.win_from_decisive(0.55, 0.10))
    assert pw == pytest.approx(0.495)
    assert float(S.ev_at_price(pw, 0.10, 2.0)) == pytest.approx(0.495 - 0.405)


def test_s3_candidates_uses_the_shared_ev_and_milestone_settlement():
    src = (ROOT / "backtests/selective_under_alt_2026-11-12/s3_candidates.py").read_text()
    assert "from calibration.settlement_ev import ev_at_price, settle_outcome" in src
    assert "pw*r.dec-(1-pw-pp)" not in src and "pw*piv[side].max()-(1-pw-pp)" not in src
    assert "pw*piv[t].max()-(1-pw-pp)" not in src
    assert src.count("ev_at_price(") == 4 and "milestone=True" in src


# ---------------------------------------------------------------- label gate
def _cand(**kw):
    d = dict(label=se.STRONG_UNDER, reason="gated_under_strong_market", side="Under", line=30.5, dec=M110,
             p_model=0.51, p_nv=0.5)
    d.update(kw)
    return d


def test_no_candidate_label_without_positive_ev_at_the_actual_price():
    df = pd.DataFrame([_cand(), _cand(p_model=0.53), _cand(p_model=110 / 210),
                       _cand(label=se.STANDARD, p_model=0.52, side="Over"),
                       _cand(label=se.ALT_LINE, kind="alt", side="Over", dec=1.5, p_model=0.70),
                       _cand(label=se.NO_EDGE, reason="model_disagrees", p_model=0.40),
                       _cand(label=se.INSUFFICIENT, reason="model_prob_missing", p_model=np.nan)])
    g = S.apply_ev_gate(df, se.CANDIDATE_LABELS, se.NO_EDGE)
    assert list(g.label) == [se.NO_EDGE, se.STRONG_UNDER, se.NO_EDGE, se.NO_EDGE, se.ALT_LINE, se.NO_EDGE,
                             se.INSUFFICIENT]
    assert list(g.reason[:4]) == [S.EV_REASON, "gated_under_strong_market", S.EV_REASON, S.EV_REASON]
    assert g.label_pre_ev.iloc[0] == se.STRONG_UNDER and g.ev_gate.iloc[0] == "demoted"
    assert list(g.ev_gate[5:]) == ["", ""] and g.reason.iloc[5] == "model_disagrees"
    assert g.be_true.iloc[0] == pytest.approx(110 / 210) and g.edge_vs_be.iloc[0] < 0
    cand = g[g.label.isin(se.CANDIDATE_LABELS)]
    assert (cand.ev > 0).all()


def test_integer_line_needs_a_push_probability_and_uses_it():
    df = pd.DataFrame([_cand(line=3.0, p_model=0.60),                                         # no p_push
                       _cand(line=3.0, p_model=0.60, p_push=0.15),                            # 0.6*0.909-0.25 > 0
                       _cand(line=3.0, p_model=0.55, p_push=0.10, p_model_basis="decisive", dec=2.0)])
    g = S.apply_ev_gate(df, se.CANDIDATE_LABELS, se.NO_EDGE)
    assert g.label.iloc[0] == se.NO_EDGE and g.reason.iloc[0] == S.PUSH_MISSING_REASON
    assert g.label.iloc[1] == se.STRONG_UNDER and g.ev.iloc[1] == pytest.approx(0.6 * (M110 - 1) - 0.25)
    assert g.p_win.iloc[2] == pytest.approx(0.495) and g.ev.iloc[2] == pytest.approx(0.09)


def test_emitter_attaches_push_mass_for_integer_cdf_lines():
    legs = pd.DataFrame([dict(week=10, game_id=T.GAME, gsis="00-QB1", market="rushyds", side="Under", line=30.0),
                         dict(week=10, game_id=T.GAME, gsis="00-QB1", market="rushyds", side="Under", line=30.5)])
    out = EM.attach_probs(legs, T._cdf(T.CDF_ROWS), source="s")
    pu, po = (29.5 - 20) / 60 + 0.5, 1 - ((30.5 - 20) / 60 + 0.5)
    assert out.p_push.iloc[0] == pytest.approx(1 - pu - po) and out.p_model_basis.iloc[0] == "decisive"
    assert out.p_push.iloc[1] == pytest.approx(0.0)


def test_emitter_demotes_a_strong_under_with_negative_ev_at_minus_110(tmp_path):
    """End to end: p_model >= no-vig 0.5 but below the -110 break-even 0.524 -> NO EDGE, never STRONG UNDER."""
    cdf = T._cdf(T.CDF_ROWS)
    # Skattebo RB: set P(under 70.5) = 0.51 (>= no-vig 0.50, < break-even 0.5238)
    sk = cdf.gsis == "00-RB1"
    cdf.loc[sk & (cdf.line == 70.5), ["p_under", "p_over"]] = [0.51, 0.49]
    r = EM.emit(freeze_paths=[T._freeze(tmp_path)], probs=cdf, probs_source="p.csv", roster=T._roster(),
                pbp=T._pbp(), date="2026-11-15", out_root=tmp_path / "research/runs",
                now=datetime.fromisoformat("2026-11-15T16:00:00+00:00"), **T.PROV)
    f = pd.read_csv(r["flags_csv"])
    f = f[f.side == "Under"].set_index("player")
    assert f.loc["Cam Skattebo", "label_pre_ev"] == se.STRONG_UNDER
    assert f.loc["Cam Skattebo", "label"] == se.NO_EDGE and f.loc["Cam Skattebo", "reason"] == S.EV_REASON
    assert f.loc["Jayden Daniels", "label"] == se.STRONG_UNDER and f.loc["Jayden Daniels", "ev"] > 0
    cand = f[f.label.isin(se.CANDIDATE_LABELS)]
    assert (cand.ev > 0).all() and (f.projection_ready == False).all()  # noqa: E712

"""NFL-62: push-aware P(over)/P(push)/P(under) and push-weighted EV."""
import pytest

from market_calibration.push_probability import (
    american_to_decimal, blend_conditional, conditional_nonpush,
    discrete_pmf_probs, line_is_integer, negative_binomial_pmf, poisson_pmf,
    push_aware_probs, push_weighted_ev, refuse_unconditional_market_blend,
    side_probs,
)


def test_half_line_has_zero_push_and_probs_sum_to_one():
    values = [38, 40, 40, 41, 42]
    out = push_aware_probs(values, 40.5)
    assert out["line_kind"] == "half_or_fractional"
    assert out["p_push"] == 0
    assert out["p_over"] == pytest.approx(2 / 5)
    assert out["p_under"] == pytest.approx(3 / 5)
    assert out["sum"] == pytest.approx(1)
    assert out["n"] == 5


def test_integer_line_keeps_push_mass():
    values = [38, 40, 40, 41, 42]
    out = push_aware_probs(values, 40)
    assert out["line_kind"] == "integer"
    assert out["p_push"] == pytest.approx(2 / 5)
    assert out["p_over"] == pytest.approx(2 / 5)
    assert out["p_under"] == pytest.approx(1 / 5)
    assert out["p_over"] + out["p_push"] + out["p_under"] == pytest.approx(1)
    decisive = conditional_nonpush(out["p_over"], out["p_push"], out["p_under"])
    assert decisive["basis"] == "two_way_push_excluded"
    assert decisive["p_over_decisive"] == pytest.approx((2 / 5) / (3 / 5))
    assert decisive["p_under_decisive"] == pytest.approx((1 / 5) / (3 / 5))
    assert decisive["p_over_decisive"] + decisive["p_under_decisive"] == pytest.approx(1)


def test_poisson_integer_and_half_lines_match_pmf():
    lam = 3.0
    integer = discrete_pmf_probs(lambda k: poisson_pmf(k, lam), 3)
    half = discrete_pmf_probs(lambda k: poisson_pmf(k, lam), 3.5)
    assert integer["p_push"] == pytest.approx(poisson_pmf(3, lam))
    assert integer["p_under"] == pytest.approx(sum(poisson_pmf(k, lam) for k in range(3)))
    assert integer["p_over"] + integer["p_push"] + integer["p_under"] == pytest.approx(1, abs=1e-12)
    assert half["p_push"] == 0
    assert half["p_under"] == pytest.approx(sum(poisson_pmf(k, lam) for k in range(4)))
    assert half["p_over"] == pytest.approx(1 - half["p_under"])
    # Empirical draws from the same PMF recover the analytic masses at n=1 (dirac) and stay in range.
    point = push_aware_probs([3, 3, 3], 3)
    assert point["p_push"] == 1 and point["p_over"] == 0 and point["p_under"] == 0


def test_negative_binomial_integer_line():
    mean, kappa, line = 6.0, 4.0, 6
    out = discrete_pmf_probs(lambda k: negative_binomial_pmf(k, mean, kappa), line)
    assert out["p_push"] == pytest.approx(negative_binomial_pmf(6, mean, kappa))
    assert out["p_over"] + out["p_push"] + out["p_under"] == pytest.approx(1, abs=1e-9)
    # Overdispersion puts more mass at zero than the Poisson with the same mean.
    assert negative_binomial_pmf(0, mean, kappa) > poisson_pmf(0, mean)
    assert (mean + mean * mean / kappa) == pytest.approx(15)


def test_push_weighted_ev_and_break_even():
    assert american_to_decimal(100) == pytest.approx(2.0)
    assert american_to_decimal(-110) == pytest.approx(1 + 100 / 110)
    # Half line, fair +100, 50/50: EV is zero.
    assert push_weighted_ev(p_win=0.5, p_push=0.0, p_lose=0.5, american_price=100) == pytest.approx(0)
    # Integer line: the push must not be treated as a loss. At +100 with
    # p_win = p_lose, EV is zero even when push mass is positive.
    assert push_weighted_ev(p_win=0.4, p_push=0.2, p_lose=0.4, american_price=100) == pytest.approx(0)
    # Treating 1-p_win as the loss would wrongly call this a break-even bet:
    # p_win=0.5, p_push=0.1, p_lose=0.4 at +100 has EV = +0.1.
    ev = push_weighted_ev(p_win=0.5, p_push=0.1, p_lose=0.4, american_price=100)
    assert ev == pytest.approx(0.1)
    naive = 0.5 * (2 - 1) - (1 - 0.5)
    assert naive == pytest.approx(0)
    # Break-even price on a half line is the usual implied probability.
    p = 110 / 210
    assert push_weighted_ev(p_win=p, p_push=0, p_lose=1 - p, american_price=-110) == pytest.approx(0)
    # Integer-line break-even uses p_lose, not 1-p_win.
    p_win, p_push, p_lose = 0.45, 0.10, 0.45
    d = 1 + p_lose / p_win  # EV = p_win*(d-1)-p_lose = 0
    # d=2 is +100. Already covered; here a slightly juiced price should be negative.
    assert push_weighted_ev(p_win=p_win, p_push=p_push, p_lose=p_lose, american_price=-110) < 0


def test_blend_only_comparable_conditionals():
    model = conditional_nonpush(0.4, 0.2, 0.4)
    blended = blend_conditional(model_decisive=model["p_over_decisive"], market_novig=0.55, model_weight=0.5)
    assert blended == pytest.approx(0.5 * (0.4 / 0.8) + 0.5 * 0.55)
    with pytest.raises(ValueError, match="unconditional"):
        refuse_unconditional_market_blend(0.4, 0.55, model_p_push=0.2)
    with pytest.raises(ValueError):
        blend_conditional(model_decisive=1.2, market_novig=0.5, model_weight=0.5)
    with pytest.raises(ValueError):
        blend_conditional(model_decisive=0.5, market_novig=0.5, model_weight=1.5)


def test_all_push_conditional_is_undefined():
    out = conditional_nonpush(0.0, 1.0, 0.0)
    assert out["p_over_decisive"] is None
    assert out["basis"] == "undefined_all_push"


def test_invalid_prices_and_empty_sim_fail_closed():
    with pytest.raises(ValueError):
        american_to_decimal(-50)
    with pytest.raises(ValueError):
        push_aware_probs([], 40.5)
    with pytest.raises(ValueError):
        push_weighted_ev(p_win=0.5, p_push=0.0, p_lose=0.4, american_price=100)
    assert line_is_integer(41.0)
    assert not line_is_integer(40.5)


def test_saved_was_nyg_100k_integer_and_half_lines():
    numpy = pytest.importorskip("numpy")
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    path = root / "snapshots/2026_10_WAS_NYG/20261112T171258Z/sim_arrays.npz"
    summary_path = root / "snapshots/2026_10_WAS_NYG/20261112T171258Z/summary.json"
    if not path.is_file():
        pytest.skip("saved WAS@NYG sim arrays are not present")
    import json
    arrays = numpy.load(path, allow_pickle=False)
    total = arrays["fg_home"].astype(float) + arrays["fg_away"].astype(float)
    half = push_aware_probs(total, 40.5)
    integer = push_aware_probs(total, 41.0)
    assert half["p_push"] == 0
    assert half["p_over"] == pytest.approx(0.28097)
    assert integer["p_push"] == pytest.approx(0.02807)
    assert integer["p_over"] == pytest.approx(0.2529)
    assert integer["p_over"] + integer["p_push"] + integer["p_under"] == pytest.approx(1)
    # WAS (away) +2: cover iff away - home + 2 > 0.
    away_margin = arrays["fg_away"].astype(float) - arrays["fg_home"].astype(float)
    spread = push_aware_probs(away_margin, -2.0)
    assert spread["p_over"] == pytest.approx(0.81673)
    assert spread["p_push"] == pytest.approx(0.01265)
    sides = side_probs(integer, "over")
    assert sides["p_win"] == integer["p_over"]
    assert sides["p_lose"] == integer["p_under"]
    saved = json.loads(summary_path.read_text())
    listed = next(row for row in saved["vs_market"] if row["market"] == "total" and row["line"] == 41.0)
    assert listed["p_model"] == pytest.approx(integer["p_over"])
    assert listed["p_model_push"] == pytest.approx(integer["p_push"])

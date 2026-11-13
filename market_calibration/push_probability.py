"""Push-aware market probabilities from a sim distribution (NFL-62).

Given trial values and a line, this reports P(over), P(push), and P(under)
that sum to 1. Integer lines keep push mass; half-lines have P(push)=0 for
integer-valued scores. EV uses the push-weighted form
P(win)*(decimal-1) - P(loss). Conditional (non-push) probabilities are the
only quantities that may be blended with two-way no-vig market prices.

This module does not change model weights and does not claim a fitted
calibration. Continuous yard values are compared with exact equality; that
is not a claim that sportsbook yard pushes have been discretized.
"""
from __future__ import annotations

import math
from typing import Iterable, Mapping, Sequence

PUSH_TOLERANCE = 1e-12


def american_to_decimal(price: float) -> float:
    price = float(price)
    if not math.isfinite(price) or -100.0 < price < 100.0:
        raise ValueError(f"invalid American price {price!r}: must be <= -100 or >= +100")
    return 1.0 + price / 100.0 if price > 0 else 1.0 + 100.0 / abs(price)


def line_is_integer(line: float, *, tol: float = PUSH_TOLERANCE) -> bool:
    line = float(line)
    if not math.isfinite(line):
        raise ValueError("line must be finite")
    return abs(line - round(line)) < tol


def _as_floats(values: Iterable[float]) -> list[float]:
    out = []
    for value in values:
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("sim values must be finite")
        out.append(number)
    return out


def push_aware_probs(values: Iterable[float], line: float, *, tol: float = PUSH_TOLERANCE) -> dict:
    """Empirical P(over), P(push), P(under) from a saved or fixture distribution."""
    line = float(line)
    if not math.isfinite(line):
        raise ValueError("line must be finite")
    sample = _as_floats(values)
    n = len(sample)
    if n == 0:
        raise ValueError("sim values must be nonempty")
    over = push = under = 0
    for value in sample:
        delta = value - line
        if abs(delta) < tol:
            push += 1
        elif delta > 0:
            over += 1
        else:
            under += 1
    p_over, p_push, p_under = over / n, push / n, under / n
    return {
        "p_over": p_over,
        "p_push": p_push,
        "p_under": p_under,
        "n": n,
        "line": line,
        "line_kind": "integer" if line_is_integer(line, tol=tol) else "half_or_fractional",
        "sum": p_over + p_push + p_under,
        "yard_push_claim": "EXACT_EQUALITY_ONLY_DISCRETIZATION_UNVERIFIED",
    }


def conditional_nonpush(p_over: float, p_push: float, p_under: float) -> dict:
    for name, value in (("p_over", p_over), ("p_push", p_push), ("p_under", p_under)):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be a finite probability")
    total = p_over + p_push + p_under
    if abs(total - 1.0) > 1e-12:
        raise ValueError("P(over)+P(push)+P(under) must sum to 1")
    remain = 1.0 - p_push
    if remain <= 0:
        return {
            "p_over_decisive": None,
            "p_under_decisive": None,
            "p_push": p_push,
            "basis": "undefined_all_push",
        }
    return {
        "p_over_decisive": p_over / remain,
        "p_under_decisive": p_under / remain,
        "p_push": p_push,
        "basis": "two_way_push_excluded",
    }


def push_weighted_ev(*, p_win: float, p_push: float, p_lose: float, american_price: float) -> float:
    """EV per unit stake: P(win)*(decimal-1) - P(loss). A push returns the stake."""
    for name, value in (("p_win", p_win), ("p_push", p_push), ("p_lose", p_lose)):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be a finite probability")
    if abs((p_win + p_push + p_lose) - 1.0) > 1e-12:
        raise ValueError("P(win)+P(push)+P(loss) must sum to 1")
    decimal = american_to_decimal(american_price)
    return p_win * (decimal - 1.0) - p_lose


def blend_conditional(*, model_decisive: float, market_novig: float, model_weight: float) -> float:
    """Blend comparable non-push probabilities only. No default weight."""
    for name, value in (("model_decisive", model_decisive), ("market_novig", market_novig),
                        ("model_weight", model_weight)):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
    if not 0 <= model_decisive <= 1 or not 0 <= market_novig <= 1:
        raise ValueError("conditional probabilities must be in [0, 1]")
    if not 0 <= model_weight <= 1:
        raise ValueError("model_weight must be in [0, 1]")
    return model_weight * model_decisive + (1.0 - model_weight) * market_novig


def refuse_unconditional_market_blend(model_p_over, market_novig, model_p_push=None):
    """Refuse mixing an unconditional tail with a push-excluded market price."""
    raise ValueError(
        "refusing to blend unconditional P(over) with two-way no-vig; "
        "convert the model side with conditional_nonpush first"
    )


def poisson_pmf(k: int, lam: float) -> float:
    if k < 0 or not math.isfinite(lam) or lam < 0:
        raise ValueError("invalid Poisson parameters")
    if lam == 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1))


def negative_binomial_pmf(k: int, mean: float, kappa: float) -> float:
    """NB with mean mu and size kappa: Var = mu + mu^2/kappa."""
    if k < 0 or not math.isfinite(mean) or not math.isfinite(kappa) or mean <= 0 or kappa <= 0:
        raise ValueError("invalid negative-binomial parameters")
    p = kappa / (kappa + mean)
    return math.exp(
        math.lgamma(k + kappa) - math.lgamma(kappa) - math.lgamma(k + 1)
        + kappa * math.log(p) + k * math.log(1.0 - p)
    )


def discrete_pmf_probs(pmf, line: float, *, k_max: int | None = None) -> dict:
    """Exact P(over/push/under) from a count PMF on k = 0, 1, ..."""
    line = float(line)
    if not math.isfinite(line):
        raise ValueError("line must be finite")
    if k_max is None:
        k_max = max(400, int(math.ceil(line + 80)))
    p_under = p_push = p_over = 0.0
    integer = line_is_integer(line)
    push_k = int(round(line)) if integer else None
    for k in range(0, k_max + 1):
        p = float(pmf(k))
        if p < 0 or not math.isfinite(p):
            raise ValueError("PMF must return a finite non-negative probability")
        if integer and k == push_k:
            p_push += p
        elif k < line:
            p_under += p
        else:
            p_over += p
    total = p_over + p_push + p_under
    # Leftover tail beyond k_max is over when the support is unbounded and k_max > line.
    remainder = max(0.0, 1.0 - total)
    if remainder > 0:
        p_over += remainder
        total = 1.0
    return {
        "p_over": p_over,
        "p_push": p_push,
        "p_under": p_under,
        "n": None,
        "line": line,
        "line_kind": "integer" if integer else "half_or_fractional",
        "sum": p_over + p_push + p_under,
        "source": "analytic_pmf",
    }


def side_probs(probs: Mapping[str, float], side: str) -> dict:
    side = side.strip().lower()
    if side not in {"over", "under"}:
        raise ValueError("side must be over or under")
    p_win = probs["p_over"] if side == "over" else probs["p_under"]
    p_lose = probs["p_under"] if side == "over" else probs["p_over"]
    return {"p_win": p_win, "p_push": probs["p_push"], "p_lose": p_lose}


def snapshot_period_values(arrays: Mapping[str, Sequence[float]], *, period: str = "fg") -> dict[str, list[float]]:
    """Map a saved sim_arrays.npz period to home, away, total, and home-margin series."""
    period = period.lower()
    try:
        home = _as_floats(arrays[f"{period}_home"])
        away = _as_floats(arrays[f"{period}_away"])
    except KeyError as exc:
        raise ValueError(f"snapshot arrays missing {period} points") from exc
    if len(home) != len(away):
        raise ValueError("home and away series length mismatch")
    return {
        "home": home,
        "away": away,
        "total": [h + a for h, a in zip(home, away)],
        "margin_home": [h - a for h, a in zip(home, away)],
    }


def market_values(series: Mapping[str, Sequence[float]], market: str, *, side_is_away: bool = False) -> list[float]:
    market = market.strip().lower()
    if market in {"total", "totals", "total_2way"}:
        return list(series["total"])
    if market in {"spread", "spreads", "spread_2way"}:
        margin = series["margin_home"]
        return [-m for m in margin] if side_is_away else list(margin)
    if market in {"team_total_home", "home_points"}:
        return list(series["home"])
    if market in {"team_total_away", "away_points"}:
        return list(series["away"])
    raise ValueError(f"unsupported market {market!r}")

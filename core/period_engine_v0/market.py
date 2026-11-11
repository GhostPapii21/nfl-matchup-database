"""§9 market mirror: raw preserved; Pin/consensus no-vig; anchored PENDING only."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional


import math

NOVIG_METHODS = ("multiplicative", "power")


def american_to_implied(a: float) -> float:
    a = float(a)
    # American prices are <= -100 or >= +100 (-100 and +100 are both even money).
    if not math.isfinite(a) or -100.0 < a < 100.0:
        raise ValueError(f"invalid American price {a!r}: must be <= -100 or >= +100")
    return 100.0 / (a + 100.0) if a > 0 else (-a) / ((-a) + 100.0)


def _novig(implied: list[float], method: str) -> tuple[float, ...]:
    """Remove the overround so the probabilities sum to 1.

    multiplicative (default, legacy): p_i = q_i / sum(q). Spreads the margin in proportion to price,
        which over-states long shots when the book shades them (favourite-longshot bias).
    power: p_i = q_i ** k with k > 1 chosen so sum(p) = 1. Takes more margin from long shots;
        usually closer to observed outcome rates on lopsided markets. Equal to multiplicative
        when the sides are priced alike.
    """
    if method not in NOVIG_METHODS:
        raise ValueError(f"method must be one of {NOVIG_METHODS}")
    s = sum(implied)
    if s <= 0:
        raise ValueError("invalid prices")
    if method == "multiplicative" or abs(s - 1.0) < 1e-12:
        return tuple(q / s for q in implied)
    # sum(q**k) is strictly decreasing in k for 0 < q < 1: bisect.
    f = lambda k: sum(q ** k for q in implied) - 1.0
    lo, hi = (1.0, 2.0) if s > 1 else (0.01, 1.0)
    while s > 1 and f(hi) > 0:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    k = 0.5 * (lo + hi)
    p = [q ** k for q in implied]
    t = sum(p)
    return tuple(x / t for x in p)


def novig_two_way(price_a: float, price_b: float, method: str = "multiplicative") -> tuple[float, float]:
    return _novig([american_to_implied(price_a), american_to_implied(price_b)], method)


def novig_three_way(price_a: float, price_b: float, price_tie: float, method: str = "multiplicative") -> tuple[float, float, float]:
    return _novig([american_to_implied(price_a), american_to_implied(price_b), american_to_implied(price_tie)], method)


def forbidden_drop_tie_renorm(price_a: float, price_b: float, price_tie: float) -> None:
    raise RuntimeError("FORBIDDEN: dropping Tie and renormalizing two sides of a three-way market")


OLD_SHRINK = lambda p: 0.5 + 0.7 * (p - 0.5)


@dataclass
class Quote:
    book: str
    period: str
    settlement: str
    line: Optional[float]
    side: str
    price: float
    pulled_et: str
    source: str


@dataclass
class MarketMirror:
    raw_model_p: dict
    pinnacle_novig_p: Optional[float]
    pinnacle_status: str
    consensus_novig_p: Optional[float]
    consensus_meta: dict
    market_anchored_p: Optional[float]
    market_anchored_status: str
    flags: list[str] = field(default_factory=list)
    divergence_audit: Optional[dict] = None
    comparison_basis: Optional[str] = None
    pinnacle_novig_p_raw_blocked: Optional[float] = None

    def to_dict(self):
        return asdict(self)


def build_mirror(
    raw_model_p: dict,
    *,
    pinnacle_two_way: Optional[tuple[float, float]] = None,
    pinnacle_three_way: Optional[tuple[float, float, float]] = None,
    pinnacle_side_index: int = 0,
    consensus_two_ways: Optional[list[tuple[str, float, float]]] = None,
    consensus_side_index: int = 0,
    consensus_pulled_et: Optional[str] = None,
    identity_flags: Optional[list[str]] = None,
    divergence_pts: float = 0.10,
    proposed_blend_weight: Optional[float] = None,
    comparison_basis: Optional[str] = None,
) -> MarketMirror:
    flags = list(identity_flags or [])
    blocked = bool(flags)
    pin_p_usable = None
    pin_p_blocked_raw = None
    pin_status = "PINNACLE_MISSING"

    if pinnacle_three_way is not None:
        probs = novig_three_way(*pinnacle_three_way)
        computed = probs[pinnacle_side_index]
        if blocked:
            pin_status = "IDENTITY_BLOCKED"
            pin_p_blocked_raw = computed
            flags.append("PIN_VALUE_SUPPRESSED")
        else:
            pin_status = "OK"
            pin_p_usable = computed
    elif pinnacle_two_way is not None:
        probs = novig_two_way(*pinnacle_two_way)
        computed = probs[pinnacle_side_index]
        if blocked:
            pin_status = "IDENTITY_BLOCKED"
            pin_p_blocked_raw = computed
            flags.append("PIN_VALUE_SUPPRESSED")
        else:
            pin_status = "OK"
            pin_p_usable = computed
    else:
        flags.append("PINNACLE_MISSING")

    cons_p = None
    cons_meta = {"books": [], "method": None, "pulled_et": consensus_pulled_et}
    if consensus_two_ways:
        books, vals = [], []
        for book, a, b in consensus_two_ways:
            pa, pb = novig_two_way(a, b)
            books.append(book)
            vals.append(pa if consensus_side_index == 0 else pb)
        cons_p = sum(vals) / len(vals)
        cons_meta = {"books": books, "method": "equal_weight_novig_mean", "pulled_et": consensus_pulled_et}
        if not consensus_pulled_et:
            flags.append("CONSENSUS_MISSING_PULLED_ET")
        if blocked:
            # consensus also not usable for Pin-style compare when identity broken
            cons_p = None
            flags.append("CONSENSUS_SUPPRESSED_IDENTITY_BLOCKED")
    else:
        flags.append("CONSENSUS_MISSING")

    anchored = None
    anchored_status = "ABSENT"
    if blocked:
        anchored_status = "SUPPRESSED_IDENTITY_BLOCKED"
    elif proposed_blend_weight is not None and pin_p_usable is not None:
        # Prefer decisive for blend input when present
        mc = raw_model_p.get("monte_carlo_decisive", raw_model_p.get("p_win_decisive", raw_model_p.get("monte_carlo")))
        if isinstance(mc, (int, float)):
            w = float(proposed_blend_weight)
            anchored = w * float(mc) + (1 - w) * pin_p_usable
            anchored_status = "PENDING_VALIDATION"
            flags.append("ANCHORED_PENDING_VALIDATION")

    # Divergence uses decisive when comparison_basis says so and field present
    audit = None
    if comparison_basis == "decisive_two_way":
        mc = raw_model_p.get("monte_carlo_decisive", raw_model_p.get("p_win_decisive", raw_model_p.get("monte_carlo")))
    else:
        mc = raw_model_p.get("monte_carlo")
    if (not blocked) and isinstance(mc, (int, float)) and pin_p_usable is not None:
        gap = abs(float(mc) - pin_p_usable)
        if gap >= divergence_pts:
            audit = {
                "abs_gap": gap,
                "action": "INPUT_CALIBRATION_AUDIT",
                "auto_promote_edge": False,
                "auto_cut_scenario": False,
                "compared_field": "decisive" if comparison_basis == "decisive_two_way" else "unconditional_monte_carlo",
            }
            flags.append("LARGE_RAW_PIN_DIVERGENCE")

    basis = comparison_basis
    if basis is None and raw_model_p.get("p_win_decisive") is not None:
        basis = "decisive_two_way_available_unconditional_also_retained"
    elif basis is None:
        basis = "unconditional_monte_carlo"

    return MarketMirror(
        raw_model_p=dict(raw_model_p),
        pinnacle_novig_p=pin_p_usable,
        pinnacle_status=pin_status,
        consensus_novig_p=cons_p,
        consensus_meta=cons_meta,
        market_anchored_p=anchored,
        market_anchored_status=anchored_status,
        flags=flags,
        divergence_audit=audit,
        comparison_basis=basis,
        pinnacle_novig_p_raw_blocked=pin_p_blocked_raw,
    )


def edge_basis_allowed(mirror: MarketMirror) -> str:
    if mirror.pinnacle_status == "IDENTITY_BLOCKED":
        return "raw_only_identity_blocked"
    if mirror.market_anchored_status == "PENDING_VALIDATION":
        return "raw_vs_pinnacle_only"
    if mirror.pinnacle_status != "OK" or mirror.pinnacle_novig_p is None:
        return "raw_only_pin_missing"
    return "raw_vs_pinnacle"

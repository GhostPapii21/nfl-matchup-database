"""Compare a thesis to timestamped sportsbook quotes.

Implied probability and the model-minus-no-vig gap are calculated only when
the side has a usable American price and a model probability. The gap is
arithmetic. It is not an edge claim.
"""

from __future__ import annotations

import math
from typing import Any

from core.period_engine_v0.market import american_to_implied, novig_two_way
from pregame.direct_books import REFERENCE_BOOKS

MARKET_ALIASES = {
    "spreads": "spread",
    "spread": "spread",
    "totals": "total",
    "total": "total",
    "h2h": "moneyline",
    "ml": "moneyline",
    "moneyline": "moneyline",
}

# Display consensus only. Disagreements are not averaged into a pick.
AGREE_SPREAD = 0.05
SOFT_DISAGREE_SPREAD = 0.08

EDGE_NOT_CLAIMED = "COMPARISON_ONLY_NOT_AN_EDGE_CLAIM"


def normalize_market(market: str) -> str:
    key = str(market or "").strip().lower()
    return MARKET_ALIASES.get(key, key)


def same_line(a: Any, b: Any) -> bool:
    if a is None or b is None:
        return a is None and b is None
    try:
        left, right = float(a), float(b)
    except (TypeError, ValueError):
        return False
    return math.isfinite(left) and math.isfinite(right) and abs(left - right) < 1e-9


def _finite(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def valid_american(price: Any) -> float | None:
    number = _finite(price)
    if number is None or -100.0 < number < 100.0:
        return None
    return number


def quote_is_reference(quote: dict) -> bool:
    book = str(quote.get("book") or "").strip().lower()
    return bool(quote.get("reference_only")) or book in REFERENCE_BOOKS


def _before_kickoff(timestamp: str | None, kickoff_utc: str | None) -> bool:
    if not timestamp or not kickoff_utc:
        return bool(timestamp) and not kickoff_utc
    return str(timestamp) < str(kickoff_utc)


def model_views(thesis: dict) -> list[dict]:
    """Copy each supplied probability. Nothing here is shrunk or capped."""
    views = []
    for raw in thesis.get("models") or []:
        probability = _finite(raw.get("probability"))
        views.append({
            "model_id": raw.get("model_id"),
            "method": raw.get("method"),
            "probability": probability,
            "probability_kind": raw.get("probability_kind"),
            "n": raw.get("n"),
            "seed": raw.get("seed"),
            "calibration_status": raw.get("calibration_status") or "unfitted",
            "push_probability": _finite(raw.get("push_probability")),
            "uncertainty": dict(raw.get("uncertainty") or {}),
        })
    return views


def consensus(views: list[dict]) -> dict:
    """The read uses the lower probability when models are close.

    A mean would move the threshold toward the more optimistic model. The
    disclosed mean is recorded and is not the number the board acts on.
    Wider disagreement keeps every probability and withholds the threshold.
    """
    probs = [view["probability"] for view in views if view["probability"] is not None]
    if not probs:
        return {
            "model_consensus": "absent",
            "threshold_probability": None,
            "threshold_basis": "withheld_no_model_probability",
            "model_disagreement": None,
            "disclosed_mean": None,
        }
    if len(probs) == 1:
        return {
            "model_consensus": "single_model",
            "threshold_probability": probs[0],
            "threshold_basis": "single_model",
            "model_disagreement": None,
            "disclosed_mean": None,
        }
    spread = max(probs) - min(probs)
    disclosed = sum(probs) / len(probs)
    if spread > SOFT_DISAGREE_SPREAD:
        return {
            "model_consensus": "disagree",
            "threshold_probability": None,
            "threshold_basis": "withheld_models_disagree",
            "model_disagreement": spread,
            "disclosed_mean": None,
        }
    if spread > AGREE_SPREAD:
        return {
            "model_consensus": "soft_disagree",
            "threshold_probability": min(probs),
            "threshold_basis": "min_of_models_spread_within_0.08",
            "model_disagreement": spread,
            "disclosed_mean": disclosed,
        }
    return {
        "model_consensus": "agree",
        "threshold_probability": min(probs),
        "threshold_basis": "min_of_models_within_0.05",
        "model_disagreement": spread,
        "disclosed_mean": disclosed,
    }


def _matching_quotes(thesis: dict, lines: list[dict], kickoff_utc: str | None) -> tuple[list[dict], list[dict]]:
    kept, rejected = [], []
    for quote in lines:
        if normalize_market(quote.get("market")) != normalize_market(thesis.get("market")):
            continue
        if str(quote.get("subject")) != str(thesis.get("subject")):
            continue
        if str(quote.get("side")) != str(thesis.get("side")):
            continue
        if not same_line(quote.get("line"), thesis.get("line")):
            continue
        timestamp = quote.get("timestamp_utc")
        if timestamp and kickoff_utc and not _before_kickoff(str(timestamp), kickoff_utc):
            rejected.append(dict(quote, reject_reason="POST_KICKOFF_EXCLUDED"))
            continue
        kept.append(quote)
    kept.sort(key=lambda quote: (str(quote.get("book") or ""), str(quote.get("source") or "")))
    return kept, rejected


def _priced(quote: dict, model_probability: float | None, views: list[dict], consensus_name: str) -> dict:
    price = valid_american(quote.get("price"))
    opposite = valid_american(quote.get("opposite_price"))
    timestamp = quote.get("timestamp_utc")
    base = {
        "book": quote.get("book"),
        "market": normalize_market(quote.get("market")),
        "subject": quote.get("subject"),
        "side": quote.get("side"),
        "line": quote.get("line"),
        "price": price,
        "opposite_side": quote.get("opposite_side"),
        "opposite_price": opposite,
        "timestamp_utc": timestamp,
        "timestamp_kind": quote.get("timestamp_kind") or ("book_timestamp" if timestamp else None),
        "reference_only": quote_is_reference(quote),
        "source": quote.get("source"),
        "missing_line": False,
        "model_probability": model_probability,
        "implied_probability": None,
        "no_vig_probability": None,
        "edge": None,
        "model_edges": [],
        "edge_claim": False,
        "supplied_novig": _finite(quote.get("supplied_novig")),
    }
    if not timestamp:
        base["edge_status"] = "NOT_COMPUTED_TIMESTAMP_ABSENT"
        return base
    if price is None:
        base["edge_status"] = "NOT_COMPUTED_PRICE_UNAVAILABLE"
        return base
    published = [view for view in views if view["probability"] is not None]
    if not published:
        base["edge_status"] = "NOT_COMPUTED_MODEL_PROBABILITY_ABSENT"
        return base
    implied = american_to_implied(price)
    base["implied_probability"] = implied
    if opposite is None:
        base["edge_status"] = "NOT_COMPUTED_OPPOSITE_PRICE_ABSENT"
        return base
    no_vig, _opposite_novig = novig_two_way(price, opposite)
    base["no_vig_probability"] = no_vig
    base["model_edges"] = [
        {
            "model_id": view["model_id"],
            "probability": view["probability"],
            "edge": view["probability"] - no_vig,
            "edge_claim": False,
        }
        for view in published
    ]
    supplied = base["supplied_novig"]
    if supplied is not None and abs(supplied - no_vig) > 0.01:
        base["supplied_novig_disagrees"] = True
    if consensus_name == "disagree" or model_probability is None:
        base["edge_status"] = "NOT_COMPUTED_MODELS_DISAGREE"
        return base
    base["edge"] = model_probability - no_vig
    base["edge_status"] = EDGE_NOT_CLAIMED
    return base


def missing_snapshot(thesis: dict, model_probability: float | None, status: str) -> dict:
    return {
        "book": None,
        "market": normalize_market(thesis.get("market")),
        "subject": thesis.get("subject"),
        "side": thesis.get("side"),
        "line": thesis.get("line"),
        "price": None,
        "opposite_side": None,
        "opposite_price": None,
        "timestamp_utc": None,
        "timestamp_kind": None,
        "reference_only": False,
        "source": None,
        "missing_line": True,
        "model_probability": model_probability,
        "implied_probability": None,
        "no_vig_probability": None,
        "edge": None,
        "model_edges": [],
        "edge_claim": False,
        "edge_status": status,
        "supplied_novig": None,
    }


def compare_thesis(thesis: dict, lines: list[dict], kickoff_utc: str | None) -> dict:
    views = model_views(thesis)
    agreed = consensus(views)
    probability = agreed["threshold_probability"]
    quotes, rejected = _matching_quotes(thesis, lines, kickoff_utc)
    if not quotes:
        status = "NOT_COMPUTED_MISSING_LINE" if not rejected else "NOT_COMPUTED_POST_KICKOFF_EXCLUDED"
        snapshots = [missing_snapshot(thesis, probability, status)]
        missing = True
    else:
        snapshots = [
            _priced(quote, probability, views, agreed["model_consensus"])
            for quote in quotes
        ]
        missing = False
    return {
        "thesis_id": thesis.get("thesis_id"),
        "subject": thesis.get("subject"),
        "market": normalize_market(thesis.get("market")),
        "side": thesis.get("side"),
        "line": thesis.get("line"),
        "missing_line": missing,
        "models": views,
        "rejected_lines": [
            {
                "book": quote.get("book"),
                "timestamp_utc": quote.get("timestamp_utc"),
                "reject_reason": quote.get("reject_reason"),
            }
            for quote in rejected
        ],
        "snapshots": snapshots,
        **agreed,
    }

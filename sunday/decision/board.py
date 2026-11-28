"""Assemble the decision board from joined research and model output.

The caller may pass ``projection_ready=true`` or a pick target. Both are
refused. Sections may be empty.
"""

from __future__ import annotations

from .market import compare_thesis
from .review import review_thesis

SECTIONS = ("strong_reads", "soft_leans", "avoids", "no_plays")
CONFIDENCE = {
    "strong_reads": "high",
    "soft_leans": "medium",
    "avoids": "low",
    "no_plays": "none",
}
PRIMARY_BOOKS = ("fanduel", "draftkings", "betmgm", "betrivers", "bet365", "williamhill_us")


def _primary_snapshot(snapshots: list[dict]) -> dict | None:
    usable = [
        snapshot for snapshot in snapshots
        if not snapshot.get("missing_line") and snapshot.get("price") is not None and not snapshot.get("reference_only")
    ]
    if not usable:
        priced = [snapshot for snapshot in snapshots if snapshot.get("price") is not None]
        usable = priced or snapshots
    def rank(snapshot: dict) -> tuple:
        book = str(snapshot.get("book") or "")
        preferred = PRIMARY_BOOKS.index(book) if book in PRIMARY_BOOKS else len(PRIMARY_BOOKS)
        return (preferred, book)
    return sorted(usable, key=rank)[0] if usable else None


def _row(thesis: dict, comparison: dict, review: dict) -> dict:
    primary = _primary_snapshot(comparison.get("snapshots") or []) or {}
    probability = review["adopted_probability"]
    return {
        "thesis_id": thesis.get("thesis_id"),
        "player_or_team": thesis.get("subject"),
        "subject_kind": thesis.get("subject_kind"),
        "market": comparison.get("market"),
        "side": review["adopted_side"],
        "original_side": review["original_side"],
        "line": thesis.get("line"),
        "projection": thesis.get("projection"),
        "threshold_probability": probability,
        "threshold_basis": comparison.get("threshold_basis"),
        "role_tag": thesis.get("role_tag"),
        "confidence": CONFIDENCE[review["section"]],
        "model_consensus": comparison.get("model_consensus"),
        "model_disagreement": comparison.get("model_disagreement"),
        "models": comparison.get("models"),
        "warnings": review["warnings"],
        "decision": review["decision"],
        "reasons": review["reasons"],
        "book": primary.get("book"),
        "price": primary.get("price"),
        "timestamp_utc": primary.get("timestamp_utc"),
        "missing_line": bool(primary.get("missing_line")),
        "implied_probability": primary.get("implied_probability"),
        "no_vig_probability": primary.get("no_vig_probability"),
        "edge": primary.get("edge"),
        "edge_status": primary.get("edge_status"),
        "edge_claim": False,
    }


def build_board(packet: dict, pick_target: int | None = None) -> dict:
    """Return the market comparison, the red-team review, and the four sections.

    ``pick_target`` is rejected. A number of desired picks is not an input.
    """
    if pick_target is not None or packet.get("pick_target") is not None or packet.get("target_picks") is not None:
        raise ValueError("pick targets are rejected; this board does not fill a quota or inflate a hit rate")
    if not isinstance(packet.get("theses"), list) or not isinstance(packet.get("lines"), list):
        raise ValueError("packet requires theses and lines lists")
    kickoff = packet.get("kickoff_utc")
    comparisons = [compare_thesis(thesis, packet["lines"], kickoff) for thesis in packet["theses"]]
    reviews = [review_thesis(thesis, comparison) for thesis, comparison in zip(packet["theses"], comparisons)]
    rows = [_row(thesis, comparison, review) for thesis, comparison, review in zip(packet["theses"], comparisons, reviews)]
    board = {section: [] for section in SECTIONS}
    for row, review in zip(rows, reviews):
        board[review["section"]].append(row)
    abstentions = [
        {
            "thesis_id": review["thesis_id"],
            "decision": review["decision"],
            "section": review["section"],
            "reasons": review["reasons"],
        }
        for review in reviews
        if review["decision"] in {"reject", "reverse_then_abstain", "abstain"}
        or review["section"] in {"avoids", "no_plays"}
    ]
    return {
        "schema": "sunday-decision-board/1",
        "game_id": packet.get("game_id"),
        "home": packet.get("home"),
        "away": packet.get("away"),
        "kickoff_utc": kickoff,
        "projection_ready": False,
        "research_only": True,
        "edge_claim_allowed": False,
        "pick_quota": None,
        "caller_projection_ready_ignored": packet.get("projection_ready"),
        "market_snapshots": comparisons,
        "adversarial_reviews": reviews,
        "board": board,
        "abstentions": abstentions,
        "section_counts": {section: len(board[section]) for section in SECTIONS},
        "notes": [
            "Sections are a result of the review. An empty section is a valid result.",
            "Implied probability and edge are omitted unless a timestamped price and a model probability both exist.",
            "A computed edge is model probability minus the two-way no-vig price. It is not a bet.",
            "Model probabilities are not shrunk, capped, or averaged across a disagreement.",
            "No hit rate is computed.",
        ],
    }

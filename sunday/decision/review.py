"""Red-team a thesis and allow the review to downgrade, reverse, or reject it.

Section membership is a consequence of the findings. Nothing in this module
asks for a target count of reads, and a positive model-minus-price gap is
not treated as support.
"""

from __future__ import annotations

from .market import quote_is_reference

STRONG_MIN = 0.62
SOFT_MIN = 0.56
OPPOSE_MAX = 0.45
MIN_TRIALS = 1000
VOLUME_MARKETS = {"receptions", "receiving_yards", "rushing_yards", "rush_rec_yards", "targets", "carries"}


def _items(thesis: dict, key: str) -> list:
    value = thesis.get(key)
    return list(value) if isinstance(value, list) else []


def _mapping(thesis: dict, key: str) -> dict:
    value = thesis.get(key)
    return dict(value) if isinstance(value, dict) else {}


def red_team(thesis: dict) -> dict:
    contingencies = _mapping(thesis, "contingencies")
    role = _mapping(thesis, "role_volume")
    sample = _mapping(thesis, "sample_quality")
    return {
        "supporting_evidence": _items(thesis, "evidence_for"),
        "contradicting_evidence": _items(thesis, "evidence_against"),
        "defensive_suppression": _items(thesis, "defensive_suppression"),
        "role_volume_fragility": {
            "tag": role.get("tag") or thesis.get("role_tag"),
            "fragile": bool(role.get("fragile")),
            "reason": role.get("reason") or "",
            "assessed": "role_volume" in thesis,
        },
        "efficiency_dependence": {
            "depends_on_efficiency": bool(thesis.get("efficiency_dependent")),
            "support_cited": any(
                item.get("kind") == "efficiency" for item in _items(thesis, "evidence_for")
            ),
            "assessed": "efficiency_dependent" in thesis,
        },
        "injury": {**contingencies.get("injury", {}), "assessed": "injury" in contingencies},
        "weather": {**contingencies.get("weather", {}), "assessed": "weather" in contingencies},
        "game_script": {**contingencies.get("game_script", {}), "assessed": "game_script" in contingencies},
        "sample_quality": {**sample, "assessed": "sample_quality" in thesis},
    }


def _usable_snapshots(comparison: dict) -> list[dict]:
    usable = []
    for snapshot in comparison.get("snapshots") or []:
        if snapshot.get("missing_line") or snapshot.get("reference_only") or quote_is_reference(snapshot):
            continue
        if snapshot.get("edge_status") != "COMPARISON_ONLY_NOT_AN_EDGE_CLAIM":
            continue
        usable.append(snapshot)
    return usable


def _positive_gap(comparison: dict) -> bool:
    for snapshot in comparison.get("snapshots") or []:
        edge = snapshot.get("edge")
        if edge is not None and edge > 0 and not snapshot.get("reference_only"):
            return True
        for item in snapshot.get("model_edges") or []:
            if item.get("edge") is not None and item["edge"] > 0 and not snapshot.get("reference_only"):
                return True
    return False


def _severity(items: list[dict], level: str) -> list[dict]:
    return [item for item in items if item.get("severity") == level]


def _material_suppression(findings: dict, side: str) -> list[dict]:
    if str(side).lower() != "over":
        return []
    return [item for item in findings["defensive_suppression"] if item.get("material")]


def _trials(findings: dict, comparison: dict) -> int | None:
    sample_n = findings["sample_quality"].get("n")
    if isinstance(sample_n, int):
        return sample_n
    counts = [view.get("n") for view in comparison.get("models") or [] if isinstance(view.get("n"), int)]
    return min(counts) if counts else None


def _unassessed(thesis: dict) -> list[str]:
    missing = []
    if "defensive_suppression" not in thesis:
        missing.append("defensive_suppression")
    if "role_volume" not in thesis:
        missing.append("role_volume_fragility")
    if "efficiency_dependent" not in thesis:
        missing.append("efficiency_dependence")
    contingencies = thesis.get("contingencies") if isinstance(thesis.get("contingencies"), dict) else {}
    for name in ("injury", "weather", "game_script"):
        if name not in contingencies:
            missing.append(name)
    if "sample_quality" not in thesis:
        missing.append("sample_quality")
    return missing


def _opposite_probability(thesis: dict, probability: float | None) -> float | None:
    if probability is None:
        return None
    supplied = thesis.get("opposite_probability")
    if isinstance(supplied, (int, float)) and not isinstance(supplied, bool):
        return float(supplied)
    push = thesis.get("push_probability")
    if isinstance(push, (int, float)) and not isinstance(push, bool):
        return 1.0 - probability - float(push)
    return None


def _reverse_supported(thesis: dict, opposite: float | None) -> bool:
    if opposite is None or opposite < SOFT_MIN:
        return False
    return any(item.get("side") == "opposite" for item in _items(thesis, "evidence_for"))


def review_thesis(thesis: dict, comparison: dict) -> dict:
    findings = red_team(thesis)
    probability = comparison.get("threshold_probability")
    consensus_name = comparison.get("model_consensus")
    side = str(thesis.get("side") or "")
    market = str(comparison.get("market") or "")
    usable = _usable_snapshots(comparison)
    unassessed = _unassessed(thesis)
    reasons: list[str] = []
    warnings = [
        "research_only",
        "projection_ready_false",
        "not_a_pick",
        "edge_is_not_a_claim",
    ]
    if unassessed:
        warnings.append("red_team_categories_not_supplied:" + ",".join(unassessed))

    decision = "reject"
    section = "no_plays"
    adopted_side = side
    considered_side = None

    if findings["sample_quality"].get("withheld") or consensus_name == "absent":
        reasons.append(
            "NO PLAY: model probability is absent, so implied probability and edge were not calculated."
        )
        if comparison.get("missing_line"):
            reasons.append("NO PLAY: sportsbook line is also missing.")
    elif comparison.get("missing_line") or not any(
        snapshot.get("price") is not None and snapshot.get("timestamp_utc")
        for snapshot in comparison.get("snapshots") or []
    ):
        reasons.append("NO PLAY: timestamped sportsbook line or price is missing; edge was not calculated.")
    elif any(str(snapshot.get("edge_status")) == "NOT_COMPUTED_TIMESTAMP_ABSENT" for snapshot in comparison.get("snapshots") or []) and not usable:
        reasons.append("NO PLAY: a price was present without a timestamp, so it was not used.")
    elif findings["injury"].get("invalidates"):
        reasons.append(
            "NO PLAY: an injury contingency invalidates the role this projection assumes. "
            + str(findings["injury"].get("detail") or "")
        )
    elif probability is not None and probability < 0.5 and _positive_gap(comparison):
        considered_side = thesis.get("opposite_side") or "opposite"
        decision = "reverse_then_abstain"
        section = "avoids"
        reasons.append(
            "AVOID: the model probability is below one half. A gap above the no-vig price is not support for this side."
        )
        reasons.append("The opposite side was reviewed and was not promoted.")
        if thesis.get("model_error_flag"):
            reasons.append("AVOID: " + str(thesis["model_error_flag"]))
    elif thesis.get("model_error_flag"):
        decision = "reject"
        section = "avoids"
        reasons.append(
            "AVOID: the model-market gap is flagged as a model error until shown otherwise. "
            + str(thesis["model_error_flag"])
        )
    elif consensus_name == "disagree":
        reasons.append(
            "NO PLAY: the models disagree. Each probability is retained and none was averaged into a pick."
        )
    elif probability is not None and probability <= OPPOSE_MAX and _severity(findings["contradicting_evidence"], "material"):
        opposite = _opposite_probability(thesis, probability)
        considered_side = thesis.get("opposite_side") or "opposite"
        if _reverse_supported(thesis, opposite) and not findings["role_volume_fragility"].get("fragile"):
            decision = "reverse"
            adopted_side = str(thesis.get("opposite_side") or "opposite")
            # A reverse may land on a soft lean. It cannot skip ahead to a strong read.
            section = "soft_leans"
            reasons.append(
                f"Reversed {side} to {adopted_side}. Opposite probability {opposite:.4f} was supplied "
                "with its own supporting evidence. A reversed side stays a soft lean."
            )
        else:
            decision = "reverse_then_abstain"
            section = "avoids"
            reasons.append(
                "AVOID: the review reversed the stated side, then abstained. "
                "The opposite side has no separate supporting evidence, or its probability was not supplied and was not invented."
            )
            if findings["role_volume_fragility"].get("fragile"):
                reasons.append(
                    "AVOID: role and volume fragility blocks the reversed side. "
                    + str(findings["role_volume_fragility"].get("reason") or "")
                )
    elif _material_suppression(findings, side):
        decision = "reject"
        section = "avoids"
        path = _material_suppression(findings, side)[0]
        reasons.append(
            "AVOID: a defensive suppression path contradicts the over. "
            + str(path.get("path") or path.get("detail") or "")
        )
    elif findings["role_volume_fragility"].get("fragile") and market in VOLUME_MARKETS:
        decision = "reject"
        section = "avoids"
        reasons.append(
            "AVOID: role and volume are fragile. "
            + str(findings["role_volume_fragility"].get("reason") or "")
        )
    elif findings["efficiency_dependence"].get("depends_on_efficiency") and not findings["efficiency_dependence"].get("support_cited"):
        decision = "reject"
        section = "avoids"
        reasons.append("AVOID: the thesis depends on efficiency that is not in the supporting evidence.")
    elif findings["sample_quality"].get("blocks_reads"):
        reasons.append(
            "NO PLAY: sample quality blocks a read. "
            + str(findings["sample_quality"].get("limitation") or "")
        )
    elif findings["injury"].get("modeled") is False and findings["injury"].get("assessed"):
        reasons.append(
            "NO PLAY: injury and availability were not modeled. "
            + str(findings["injury"].get("detail") or "")
        )
    elif thesis.get("script_sensitive", True) and findings["game_script"].get("assessed") and not findings["game_script"].get("branches_retained"):
        reasons.append(
            "NO PLAY: game-script branches were not retained, so a script-sensitive read was not published. "
            + str(findings["game_script"].get("detail") or "")
        )
    elif (_trials(findings, comparison) or 0) < MIN_TRIALS:
        reasons.append("NO PLAY: the trial count is below the minimum required to publish a read.")
    elif unassessed:
        reasons.append("NO PLAY: the red team is incomplete, so the thesis was not promoted.")
    else:
        support = findings["supporting_evidence"]
        invalidating = _severity(findings["contradicting_evidence"], "invalidating")
        material = _severity(findings["contradicting_evidence"], "material")
        minor = _severity(findings["contradicting_evidence"], "minor")
        strong_shape = (
            probability is not None
            and probability >= STRONG_MIN
            and consensus_name in {"agree", "single_model"}
            and usable
            and support
            and not invalidating
            and not material
            and thesis.get("role_tag")
            and thesis.get("projection") is not None
        )
        soft_shape = (
            probability is not None
            and probability >= SOFT_MIN
            and consensus_name in {"agree", "single_model", "soft_disagree"}
            and usable
            and support
            and not invalidating
            and not material
            and thesis.get("role_tag")
        )
        if strong_shape and minor:
            decision = "downgrade"
            section = "soft_leans"
            reasons.append("Downgraded from a strong read to a soft lean because minor contradicting evidence remains.")
        elif probability is not None and probability >= STRONG_MIN and consensus_name == "soft_disagree" and usable and support and not invalidating and not material:
            decision = "downgrade"
            section = "soft_leans"
            reasons.append("Downgraded from a strong read to a soft lean because the models are not tight enough to treat as one number.")
        elif strong_shape:
            decision = "keep"
            section = "strong_reads"
            reasons.append("Strong read: the published probabilities clear the bar with assessed, non-contradicting evidence.")
        elif soft_shape and minor:
            decision = "downgrade"
            section = "soft_leans"
            reasons.append("Soft lean after a downgrade: minor contradicting evidence stays attached.")
        elif soft_shape:
            decision = "keep"
            section = "soft_leans"
            reasons.append("Soft lean: the probability clears a lean and does not clear a strong read.")
        else:
            reasons.append(
                "NO PLAY: the probability and the evidence do not clear a lean. The empty section is the result, not a quota miss."
            )

    if findings["game_script"].get("assessed") and not findings["game_script"].get("branches_retained"):
        warnings.append("game_script_branches_not_retained")
    if findings["sample_quality"].get("limitation"):
        warnings.append("sample_limitation")
    if thesis.get("model_error_flag"):
        warnings.append("model_error_flag")
    if comparison.get("model_disagreement"):
        warnings.append("model_disagreement")
    if not usable and section in {"strong_reads", "soft_leans"}:
        decision = "reject"
        section = "no_plays"
        reasons.append("NO PLAY: no non-reference two-sided price was available, so the read was withdrawn.")

    return {
        "thesis_id": thesis.get("thesis_id"),
        "decision": decision,
        "section": section,
        "original_side": side,
        "adopted_side": adopted_side,
        "considered_side": considered_side,
        "reasons": [reason.strip() for reason in reasons if reason.strip()],
        "warnings": warnings,
        "red_team": findings,
        "threshold_probability": probability if section != "strong_reads" or decision != "reverse" else probability,
        "adopted_probability": _opposite_probability(thesis, probability) if decision == "reverse" else probability,
    }

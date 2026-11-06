"""Provenance and split gates; fitting deliberately has no coefficients."""
from copy import deepcopy
from dataclasses import dataclass, asdict
import math
import re

from .quotes import GAME_ID, GAME_LABEL, utc
from .delivery_guard import guard_edge_delivery, identities_match, valid_probability

UNFITTED = "UNIMPLEMENTED_NO_FITTED_CALIB"
INSPECTED_GAMES = {GAME_ID, GAME_LABEL, "2026-11-05_JAX_BAL", "JAX@BAL"}


@dataclass(frozen=True)
class Provenance:
    game_id: str
    season: int
    week: int
    split: str
    inspected: bool
    prediction_utc: str
    outcome_known_utc: str
    model_id: str
    source: str
    source_sha256: str
    scoring_label: str
    event_start_utc: str | None = None
    prediction_family: str = "RAW"
    game_id_namespace: str = "saved_csv_game_id"

    @property
    def is_inspected(self):
        return self.inspected or (self.season == 2026 and 1 <= self.week <= 8) or self.game_id in INSPECTED_GAMES

    @property
    def effective_split(self):
        if self.is_inspected:
            return "development_inspected"
        return self.split

    def to_dict(self):
        return asdict(self) | {"effective_split": self.effective_split}


def validate_splits(rows):
    seen = {}
    for row in rows:
        if row.split not in {"train", "development", "development_inspected", "holdout"}:
            raise ValueError("unknown split")
        if (not row.game_id or not row.model_id or not row.source
                or not re.fullmatch(r"[0-9a-fA-F]{64}", row.source_sha256)):
            raise ValueError("missing or invalid provenance")
        if type(row.season) is not int or type(row.week) is not int or not 1 <= row.week <= 22:
            raise ValueError("invalid season/week")
        utc(row.prediction_utc)
        utc(row.outcome_known_utc)
        if row.event_start_utc is not None:
            utc(row.event_start_utc)
        if type(row.inspected) is not bool or not row.game_id_namespace:
            raise ValueError("explicit inspection state and identity namespace required")
        if row.prediction_family != "RAW":
            raise ValueError("raw scoring provenance cannot contain market-anchored outputs")
        if row.scoring_label not in {"baseline", "hindsight"}:
            raise ValueError("unknown scoring label")
        if row.is_inspected and row.split == "holdout":
            raise ValueError("inspected data cannot be holdout")
        key = (row.game_id_namespace, row.game_id)
        if key in seen and seen[key] != row.split:
            raise ValueError("game overlap between splits")
        seen[key] = row.split
    return [row.to_dict() for row in rows]


class CalibrationBias:
    fitted = False
    coefficients = None
    status = UNFITTED

    def fit(self, rows):
        rows = list(rows)
        if any(row.split == "holdout" for row in rows):
            raise ValueError("refuse fit on holdout")
        provenance = validate_splits(rows)
        if any(row.effective_split != "train" for row in rows):
            raise ValueError("fit accepts only train; inspected development and TNF are excluded")
        if not rows:
            raise ValueError("nonempty train provenance required")
        return {"status": UNFITTED, "coefficients": None, "provenance": provenance,
                "fitted_games": [], "validation_claim": "NONE"}


def separate_outputs(raw, matched, *, raw_weight=None, quote_policy=None,
                     consensus=None, source_registry=None, consensus_requested=True):
    """Only caller-proposed weights. Never treat an anchor as a fitted result.

    p_win must explicitly share the quote's probability_basis; two-way market
    prices exclude pushes, while a three-way market includes Tie unconditionally.
    Consumers must check delivery_guard and use only its surfaceable_payload to
    surface a raw edge. The separate research objects are never delivery approval.
    """
    if raw_weight is not None and (not isinstance(raw_weight, (int, float)) or isinstance(raw_weight, bool)
            or not math.isfinite(raw_weight) or not 0 <= raw_weight <= 1):
        raise ValueError("raw weight must be finite in [0,1]")
    p = raw.get("p_win")
    anchored = None
    flags = list(matched.flags)
    quote = next((q for q in matched.quotes if q.side == matched.requested_side), None)
    quote_identity = ({k: getattr(quote, k) for k in (
        "game_id_namespace", "game_id", "market", "period", "side", "settlement", "team", "line")}
        | {"player": None}) if quote is not None else None
    market_p = (matched.probabilities or {}).get(matched.requested_side) if matched.status == "MATCHED" else None
    if matched.status == "MATCHED" and raw_weight is not None and valid_probability(p) and quote is not None:
        identity = raw.get("market_identity")
        identity_ok = (isinstance(identity, dict) and identity.get("game_id_namespace") == "saved_csv_game_id"
                       and identities_match(identity, quote_identity))
        if not identity_ok:
            flags.append("RAW_QUOTE_IDENTITY_MISMATCH")
        elif raw.get("probability_basis") != matched.comparison_basis:
            flags.append("PROBABILITY_BASIS_MISMATCH")
        elif valid_probability(market_p):
            anchored = raw_weight * p + (1 - raw_weight) * market_p
    output = {"raw_model_output": deepcopy(raw), "market_anchored_output": {
        "status": "PENDING_VALIDATION", "p_win": anchored,
        "probability_basis": matched.comparison_basis,
        "raw_weight": raw_weight, "weight_provenance": "CALLER_PROPOSED_NOT_FITTED" if raw_weight is not None else "ABSENT",
        "actionable_status": "NOLINE", "scope": "RESEARCH_ARITHMETIC_ONLY_RULES_UNVERIFIED",
        "flags": flags, "quote_provenance": deepcopy(matched.provenance)},
        "calibration_status": UNFITTED, "edge_basis": "RAW_ONLY"}
    output["delivery_guard"] = guard_edge_delivery(
        p, market_p, raw_identity=raw.get("market_identity"), quote_identity=quote_identity,
        probability_basis=raw.get("probability_basis"), market_probability_basis=matched.comparison_basis,
        quote_provenance=(asdict(quote) | {"price_format": "american",
            "matched_provenance": deepcopy(matched.provenance)}) if quote is not None else None,
        calibration_status={"status": UNFITTED, "fitted": CalibrationBias.fitted},
        raw_model_output=raw, quote_policy=quote_policy, consensus=consensus,
        source_registry=source_registry, consensus_requested=consensus_requested)
    return output


def score_predictions(rows, *, scoring_label):
    """Brier scoring for explicitly supplied raw predictions; no fitting here."""
    rows = list(rows)
    if scoring_label not in {"baseline", "hindsight"} or not rows:
        raise ValueError("nonempty separately labelled scoring rows required")
    provenance = validate_splits([p for _, _, p in rows])
    splits = {p.effective_split for _, _, p in rows}
    if len(splits) != 1:
        raise ValueError("score each split separately")
    losses = []
    for p_win, outcome, p in rows:
        if p.scoring_label != scoring_label:
            raise ValueError("cannot mix baseline and hindsight labels")
        if not math.isfinite(p_win) or not 0 <= p_win <= 1 or outcome not in (0, 1):
            raise ValueError("binary scoring requires valid probability and outcome; exclude pushes explicitly")
        if scoring_label == "baseline":
            if p.event_start_utc is None or not utc(p.prediction_utc) < utc(p.event_start_utc) <= utc(p.outcome_known_utc):
                raise ValueError("baseline requires prediction before event start and outcome")
        losses.append((p_win - outcome) ** 2)
    return {"scoring_label": scoring_label, "prediction_family": "RAW", "n": len(losses),
            "brier": sum(losses) / len(losses), "split": next(iter(splits)),
            "provenance": provenance, "calibration_status": UNFITTED,
            "validation_claim": "NONE_DESCRIPTIVE_SCORE_ONLY",
            "freeze_eligibility": "TIMESTAMPS_CHECKED_IMMUTABLE_FORECAST_NOT_VERIFIED"}

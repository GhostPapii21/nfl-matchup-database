"""Strict score windows and quote identity before a grade can PASS."""
from dataclasses import dataclass

from research.period_engine_v0.settlement import settle_spread_2way, settle_total_2way
from .quotes import MatchRequest, identity_flags_for_quote, request_flags, side_name


@dataclass(frozen=True)
class ScoreCard:
    game_id: str
    home: str
    away: str
    quarters: dict[str, tuple[int, int]]  # Standalone (home, away) points.
    overtime: tuple[int, int] | None = None  # None = unknown; (0, 0) = known no OT.

    def __post_init__(self):
        if not self.game_id or not self.home or not self.away or self.home == self.away:
            raise ValueError("unresolved or conflicting game/team identity")
        if not isinstance(self.quarters, dict) or not self.quarters or not set(self.quarters) <= {"Q1", "Q2", "Q3", "Q4"}:
            raise ValueError("known standalone quarter scores required")
        for score in [*self.quarters.values(), *([] if self.overtime is None else [self.overtime])]:
            if not isinstance(score, (list, tuple)) or len(score) != 2 or any(type(n) is not int or n < 0 for n in score):
                raise ValueError("scores require two nonnegative integers")

    def points(self, period):
        windows = {"H1": ("Q1", "Q2"), "H2": ("Q3", "Q4"),
                   "REG": ("Q1", "Q2", "Q3", "Q4"), "FG": ("Q1", "Q2", "Q3", "Q4")}
        if period in self.quarters:
            return tuple(self.quarters[period])
        if period not in windows:
            raise ValueError("unsupported period")
        if any(q not in self.quarters for q in windows[period]):
            raise ValueError("missing primitive score for requested window")
        score = tuple(sum(self.quarters[q][i] for q in windows[period]) for i in (0, 1))
        if period == "FG":
            if self.overtime is None:
                raise ValueError("FG requires known OT points (zero if no overtime)")
            score = tuple(score[i] + self.overtime[i] for i in (0, 1))
        return score


def settle(card: ScoreCard, req: MatchRequest):
    if request_flags(req) or req.game_id != card.game_id or card.home != "BAL" or card.away != "JAX":
        raise ValueError("settlement identity mismatch")
    home, away = card.points(req.period)
    scores = {card.home: home, card.away: away}
    side = side_name(req.side)
    if req.market == "spreads":
        margin = scores[side] - scores[card.away if side == card.home else card.home]
        return settle_spread_2way(margin, req.line)
    if req.market in {"totals", "team_totals"}:
        points = scores[req.team] if req.market == "team_totals" else home + away
        return settle_total_2way(points, req.line, side.lower())
    winner = card.home if home > away else card.away if away > home else "TIE"
    if winner == "TIE" and req.settlement == "ml_2way":
        return "push"
    return "win" if side == winner else "lose"


@dataclass(frozen=True)
class GradeComparison:
    status: str
    flags: tuple[str, ...]
    computed_grade: str | None
    scoring_label: str = "hindsight_settlement_audit"
    scope: str = "SCORE_CONVENTION_ONLY"
    book_rules_verified: bool = False


def compare_grade(card, req, quote, observed_grade):
    flags = identity_flags_for_quote(req, quote)
    if flags:
        return GradeComparison("IDENTITY_BLOCKED", flags, None)
    try:
        computed = settle(card, req)
    except ValueError as exc:
        return GradeComparison("IDENTITY_BLOCKED", (str(exc),), None)
    observed = {"W": "win", "L": "lose", "P": "push"}.get(observed_grade)
    if observed is None:
        return GradeComparison("UNGRADABLE", ("MISSING_OR_INVALID_GRADE",), computed)
    return GradeComparison("PASS" if computed == observed else "FAIL", (), computed)

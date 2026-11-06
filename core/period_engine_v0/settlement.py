"""Exact-line settlement for period markets. Research-only."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional

Period = Literal["Q1", "Q2", "Q3", "Q4", "H1", "H2", "FG"]
Settlement = Literal["spread_2way", "winner_3way", "total_2way", "team_total_2way", "ml_2way"]


@dataclass(frozen=True)
class PeriodScore:
    """Points scored in a window. For Qn: that quarter only. For H1: Q1+Q2 cumulative."""
    home: int
    away: int

    @property
    def margin_home(self) -> int:
        return self.home - self.away

    @property
    def total(self) -> int:
        return self.home + self.away


def standalone_quarters_to_h1(q1: PeriodScore, q2: PeriodScore) -> PeriodScore:
    return PeriodScore(home=q1.home + q2.home, away=q1.away + q2.away)


def settle_spread_2way(margin_for_side: float, line: float) -> Literal["win", "lose", "push"]:
    """Grade a side's spread.

    CONVENTION: `line` is the signed spread for THAT side (favorite negative, dog positive).
    Pass margin_for_side = side_points - opp_points.
    Cover iff (margin_for_side + line) > 0; push iff == 0.
    Examples: JAX -2.5 → line=-2.5; cover when margin > 2.5.
              BAL +2.5 → line=+2.5; cover when margin > -2.5.
    """
    adj = margin_for_side + line
    if abs(adj) < 1e-12:
        return "push"
    return "win" if adj > 0 else "lose"


def settle_winner_3way(margin_for_side: int) -> Literal["side", "opp", "tie"]:
    if margin_for_side > 0:
        return "side"
    if margin_for_side < 0:
        return "opp"
    return "tie"


def settle_total_2way(points: float, line: float, side: Literal["over", "under"]) -> Literal["win", "lose", "push"]:
    if abs(points - line) < 1e-12:
        return "push"
    over = points > line
    if side == "over":
        return "win" if over else "lose"
    return "win" if not over else "lose"


def settle_team_total_2way(team_points: float, line: float, side: Literal["over", "under"]) -> Literal["win", "lose", "push"]:
    return settle_total_2way(team_points, line, side)


def identity_flags(
    model_period: Period,
    quote_period: Period,
    model_settlement: Settlement,
    quote_settlement: Settlement,
    model_line: Optional[float],
    quote_line: Optional[float],
) -> list[str]:
    flags = []
    if model_period != quote_period:
        flags.append("PERIOD_MISMATCH")
    if model_settlement != quote_settlement:
        flags.append("SETTLEMENT_MISMATCH")
    if model_line is not None and quote_line is not None and abs(model_line - quote_line) > 1e-9:
        flags.append("LINE_MISMATCH")
    return flags

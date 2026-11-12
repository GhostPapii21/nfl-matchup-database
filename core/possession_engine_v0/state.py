"""Bounded game state + explicit event transitions + period scoreboards."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional


def _empty_periods():
    return {"q1": [0, 0], "q2": [0, 0], "q3": [0, 0], "q4": [0, 0], "ot": [0, 0]}


@dataclass
class GameState:
    home: str
    away: str
    possession: Optional[str] = None
    qtr: int = 1
    half: int = 1
    game_seconds_remaining: int = 900
    down: int = 1
    ydstogo: int = 10
    yardline_100: int = 75
    score_home: int = 0
    score_away: int = 0
    in_ot: bool = False
    final: bool = False
    events: list = field(default_factory=list)
    player_counts: dict = field(default_factory=lambda: {"pass_yards": {}, "rush_yards": {}, "rec_yards": {}})
    sparse_flags: list = field(default_factory=list)
    reg_score_home: Optional[int] = None
    reg_score_away: Optional[int] = None
    period_scores: dict = field(default_factory=_empty_periods)
    # Optional zero-arg callable returning the receiving team's yardline_100 after a kickoff
    # (set by simulate_one from the as-of kickoff outcomes). None = legacy fixed own-25.
    kickoff_sampler: Optional[Callable[[], int]] = field(default=None, repr=False, compare=False)
    # NFL-43 accounting (populated only when cfg["semantics"] enables a path)
    penalty_yards: dict = field(default_factory=dict)
    special_scores: dict = field(default_factory=lambda: {"kick_return_td": {}, "punt_return_td": {}, "def_return_td": {}})
    ot_rule: str = "single_possession_approx_declared_limitation"
    ot_tracker: object = field(default=None, repr=False, compare=False)
    ot_coin: Optional[Callable[[], int]] = field(default=None, repr=False, compare=False)

    @classmethod
    def new_game(cls, home: str, away: str) -> "GameState":
        return cls(home=home, away=away, period_scores=_empty_periods())

    def _period_key(self) -> str:
        if self.qtr <= 0:
            return "q1"
        if self.qtr == 1:
            return "q1"
        if self.qtr == 2:
            return "q2"
        if self.qtr == 3:
            return "q3"
        if self.qtr == 4:
            return "q4"
        return "ot"

    def add_score(self, team: str, pts: int) -> None:
        """Credit team total and the *current* quarter/OT bucket (boundary = current qtr)."""
        idx = 0 if team == self.home else 1
        if team == self.home:
            self.score_home += pts
        else:
            self.score_away += pts
        key = self._period_key()
        self.period_scores[key][idx] += pts
        self.events.append({"type": "score_credit", "team": team, "pts": pts, "period": key, "qtr": self.qtr})

    def period_snapshot(self) -> dict:
        ps = self.period_scores
        h1_h, h1_a = ps["q1"][0] + ps["q2"][0], ps["q1"][1] + ps["q2"][1]
        h2_h, h2_a = ps["q3"][0] + ps["q4"][0], ps["q3"][1] + ps["q4"][1]
        reg_h, reg_a = h1_h + h2_h, h1_a + h2_a
        return {
            "q1_home": ps["q1"][0], "q1_away": ps["q1"][1],
            "q2_home": ps["q2"][0], "q2_away": ps["q2"][1],
            "q3_home": ps["q3"][0], "q3_away": ps["q3"][1],
            "q4_home": ps["q4"][0], "q4_away": ps["q4"][1],
            "h1_home": h1_h, "h1_away": h1_a,
            "h2_home": h2_h, "h2_away": h2_a,
            "ot_home": ps["ot"][0], "ot_away": ps["ot"][1],
            "reg_home": reg_h, "reg_away": reg_a,
            "fg_home": self.score_home, "fg_away": self.score_away,
        }


LEGACY_KICKOFF_YL = 75  # own 25: pre-2024 touchback spot


def kickoff_spot(st: GameState) -> int:
    """Receiving team's yardline_100 after a kickoff: sampled when a sampler is attached, else own 25."""
    return int(st.kickoff_sampler()) if st.kickoff_sampler is not None else LEGACY_KICKOFF_YL


def apply_kickoff(st: GameState, *, receiving: str, yardline_100: int = 75) -> GameState:
    st.possession = receiving
    st.yardline_100 = int(yardline_100)
    st.down = 1
    st.ydstogo = 10
    st.events.append({"type": "kickoff", "receiving": receiving, "yardline_100": yardline_100, "qtr": st.qtr})
    return st


def maybe_halftime(st: GameState, *, q3_receive: str) -> GameState:
    if st.qtr == 2 and st.game_seconds_remaining <= 0 and not st.final:
        st.events.append({"type": "halftime", "score": (st.score_home, st.score_away)})
        st.qtr = 3
        st.half = 2
        st.game_seconds_remaining = 900
        apply_kickoff(st, receiving=q3_receive, yardline_100=kickoff_spot(st))
    return st


def start_ot_if_tied(st: GameState) -> GameState:
    if st.qtr >= 4 and st.game_seconds_remaining <= 0 and not st.final:
        st.reg_score_home = st.score_home
        st.reg_score_away = st.score_away
        if st.score_home == st.score_away:
            st.in_ot = True
            st.qtr = 5
            st.game_seconds_remaining = 600
            if st.ot_rule == "official_2025_regular_season":
                from semantics import OTTracker
                receiver = st.home if (st.ot_coin is not None and st.ot_coin() == 0) else st.away
                st.events.append({"type": "ot_start", "rule": st.ot_rule, "receiver": receiver})
                apply_kickoff(st, receiving=receiver, yardline_100=kickoff_spot(st))
                st.ot_tracker = OTTracker(st, receiver)
            else:
                st.events.append({"type": "ot_start", "rule": "single_possession_approx_declared_limitation"})
                apply_kickoff(st, receiving=st.away, yardline_100=kickoff_spot(st))
        else:
            st.final = True
            st.events.append({"type": "final", "score": (st.score_home, st.score_away)})
    return st

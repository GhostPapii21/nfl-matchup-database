"""NFL-43 official-semantics layer: penalties, returns and official overtime.

Opt-in per config (``cfg["semantics"]``). With no ``semantics`` block the legacy
behaviour is unchanged (penalties absent, return TDs absent, single-possession OT).

Supported paths (possession game-state path in ``simulate.py`` only):

* ``penalties: "canonical_log_v1"`` - accepted scrimmage fouls from the canonical
  ESPN-reconciled log ``data/redistributable/teams/penalty_plays_2026.csv`` (228/238
  team-games match ESPN box totals). Per-snap foul probability = offense's accepted
  offensive fouls per snap + defense's accepted defensive fouls per snap, weeks strictly
  before the target week. Yardage/no-play/auto-first-down are resampled from the
  team's own accepted fouls on that side. Enforcement uses the half-distance rule.
  Kick-play fouls (kickoff/punt/FG rows) are excluded and bounded in SEMANTICS_BOUNDS.md.
* ``returns: "asof_league_v1"`` - kickoff and punt return touchdowns at the as-of
  league rate (nflverse PBP, weeks before target). Interception / fumble-lost return yards and
  return touchdowns are drawn from the as-of LEAGUE pool of turnover rows of the same kind
  (all 32 teams, weeks before target), not from the two teams' own sampled rows (NFL-43 review
  D2, Ghost6 d65ad98: the two-team rows had 0 return TDs, so the old path never scored one). Punt net yardage stays a
  separate PBP field-position quantity (``_punt_net_from_row``); return yards on punts are
  reported as ``kick_distance - net`` and never added a second time.
* ``overtime: "official_2025_regular_season"`` - 10-minute period, coin-toss receiver,
  both teams guaranteed a possession (2025 regular-season rule), then sudden death; a
  defensive score on the opening possession ends it; time expiry leaves a tie.

The frozen joint producer (``joint_producer.py``) still rejects penalties / return yards
as UNSUPPORTED; this module does not change that path.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_PENALTY_LOG = REPO_ROOT / "data/redistributable/teams/penalty_plays_2026.csv"
CANONICAL_PENALTY_GAMES = REPO_ROOT / "data/redistributable/teams/penalties_2026.csv"
KICK_PLAY_TYPES = {"Kickoff", "Punt", "Field Goal Good", "Field Goal Missed", "Kickoff Return Touchdown",
                   "Punt Return Touchdown", "Blocked Punt Touchdown", "Blocked Field Goal",
                   "Extra Point Good", "Extra Point Missed"}
OT_RULES = ("single_possession_approx_declared_limitation", "official_2025_regular_season")
NO_PLAY_CLOCK_SEC = 4
# Pull time of the canonical penalty log (data/redistributable/teams/PENALTY_NOTES.md: "built 2026-11-01 ~9 PM ET"
# from ESPN public scoreboard/summary endpoints; exact fetch minute unknown). Committed in fe2e371 (2026-11-06 1:50 PM ET).
PENALTY_LOG_PULLED_ET = "2026-11-01 about 9 PM ET (exact minute unknown; PENALTY_NOTES.md)"
# nflverse team code -> ESPN code used by the canonical log
ESPN_ALIAS = {"WAS": "WSH", "LA": "LAR"}
# Inverse is used only when labeling nflverse game_ids back onto PEN (WSH) rows.
NFLVERSE_ALIAS = {v: k for k, v in ESPN_ALIAS.items()}
DEFAULT_PBP_FOR_COVERAGE = REPO_ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
_PBP_UNSET = object()



def _espn_team(team: str) -> str:
    return ESPN_ALIAS.get(str(team), str(team))


def penalty_log_unknowns(games, *, season: int, week_asof_exclusive: int,
                         pbp_path=None, pbp_df=None) -> dict:
    """PBP games in weeks < asof that are missing from the canonical penalty log.

    Weeks with no PEN rows at all go in ``unknown_weeks``. Individual games missing
    from a week that otherwise has PEN coverage go in ``unknown_games`` / ``unknown_games_by_team``.
    Missing coverage is UNKNOWN, never treated as zero penalties.
    """
    weeks_in_log = sorted(int(w) for w in games["week"].unique()) if len(games) else []
    unknown_weeks = [w for w in range(1, int(week_asof_exclusive)) if w not in weeks_in_log]
    out = {
        "unknown_weeks": unknown_weeks,
        "unknown_games": [],
        "unknown_games_by_team": {},
        "pbp_games_in_pen_weeks": None,
        "policy": ("UNKNOWN: no canonical penalty data for these weeks/games; rates use weeks_used / "
                   "games present in PEN only and do not treat the gap as zero penalties"),
    }
    if pbp_df is None:
        if not pbp_path or not Path(pbp_path).exists():
            return out
        pbp_df = pd.read_parquet(pbp_path, columns=["game_id", "season", "week", "home_team", "away_team"])
    d = pbp_df[(pbp_df["season"] == season) & (pbp_df["week"] < int(week_asof_exclusive))].drop_duplicates("game_id")
    pen_keys = set()
    for _, sub in games.groupby("game_id"):
        pen_keys.add((int(sub["week"].iloc[0]), frozenset(str(x) for x in sub["team"])))
    missing = []
    by_team: dict[str, list[str]] = {}
    pbp_in_pen_weeks = 0
    for r in d.itertuples():
        week = int(r.week)
        if week in weeks_in_log:
            pbp_in_pen_weeks += 1
        key = (week, frozenset((_espn_team(r.away_team), _espn_team(r.home_team))))
        # A week with no PEN coverage is already in unknown_weeks (e.g. W9). Do not also
        # list every game of that week as an unknown_game; only residual within-week gaps.
        if week in weeks_in_log and key not in pen_keys:
            gid = str(r.game_id)
            missing.append(gid)
            for team in (str(r.away_team), str(r.home_team)):
                by_team.setdefault(team, []).append(gid)
    out["unknown_games"] = sorted(missing)
    out["unknown_games_by_team"] = {k: sorted(v) for k, v in sorted(by_team.items())}
    out["pbp_games_in_pen_weeks"] = int(pbp_in_pen_weeks)
    return out


@dataclass
class PenaltyDraw:
    side: str  # "offense" | "defense"
    team: str
    yards: int
    no_play: bool
    auto_first_down: bool
    penalty_type: str


@dataclass
class PenaltyModel:
    rates: dict  # (team, side) -> per-snap rate
    pools: dict  # (team, side) -> np.ndarray of rows (yards, no_play, auto_first, type)
    meta: dict = field(default_factory=dict)

    def draw(self, rng: np.random.Generator, offense: str, defense: str) -> Optional[PenaltyDraw]:
        p_off = self.rates.get((offense, "offense"), 0.0)
        p_def = self.rates.get((defense, "defense"), 0.0)
        u = rng.random()
        if u < p_off:
            team, side = offense, "offense"
        elif u < p_off + p_def:
            team, side = defense, "defense"
        else:
            return None
        pool = self.pools.get((team, side))
        if pool is None or len(pool) == 0:
            return None
        y, nop, af, typ = pool[int(rng.integers(0, len(pool)))]
        return PenaltyDraw(side=side, team=team, yards=int(y), no_play=bool(nop), auto_first_down=bool(af), penalty_type=str(typ))


def _truthy(s: pd.Series) -> pd.Series:
    return s.astype(str).str.lower().isin(["true", "1", "yes"])


def build_penalty_model(teams, *, week_asof_exclusive: int, season: int = 2026,
                        log_path: Path | str = CANONICAL_PENALTY_LOG,
                        games_path: Path | str = CANONICAL_PENALTY_GAMES,
                        pbp_path=_PBP_UNSET, exclude_kick_formation: bool = False) -> PenaltyModel:
    """exclude_kick_formation (NFL-75 rare plays only): drop accepted pre-snap fouls whose text says "Punt formation" /
    "Field Goal formation" (the log files them as play_type "Penalty", so they sat in the scrimmage rates); rare plays
    draws them on kick decisions instead. False = the pre-NFL-75 model exactly."""
    log = pd.read_csv(log_path)
    games = pd.read_csv(games_path)
    log = log[(log["season"] == season) & (log["week"] < int(week_asof_exclusive))]
    n_games_file = int(games["game_id"].nunique())
    if "season" in games.columns:
        games = games[games["season"] == season]
        season_filter = "season column"
    else:
        # penalties_2026.csv has no season column: keep only games that appear in the season-filtered log.
        games = games[games["game_id"].isin(set(log["game_id"]))]
        season_filter = "game_id present in season-filtered penalty log (file has no season column)"
    games = games[games["week"] < int(week_asof_exclusive)]
    acc = log[(log["status"] == "accepted") & ~log["play_type"].isin(KICK_PLAY_TYPES)].copy()
    n_kick_form = 0
    if exclude_kick_formation:
        kf = acc["text"].fillna("").astype(str).str.contains(r"punt formation|field goal formation", case=False, regex=True)
        n_kick_form = int(kf.sum())
        acc = acc[~kf].copy()
    acc["no_play_b"] = _truthy(acc["no_play"])
    acc["auto_b"] = _truthy(acc["auto_first_down"])
    rates, pools, per_team = {}, {}, {}
    for team in teams:
        espn = ESPN_ALIAS.get(team, team)
        tg = games[games["team"] == espn]
        if tg.empty:
            raise ValueError(f"UNSUPPORTED: no canonical penalty-log games for {team} (ESPN {espn}) before week {week_asof_exclusive}")
        gids = set(tg["game_id"])
        opp = games[games["game_id"].isin(gids) & (games["team"] != espn)]
        off_snaps = float(tg["off_plays"].sum())
        def_snaps = float(opp["off_plays"].sum())
        for side, snaps in (("offense", off_snaps), ("defense", def_snaps)):
            sub = acc[(acc["team_penalized"] == espn) & (acc["side"] == side) & acc["game_id"].isin(gids)]
            n_np = int(sub["no_play_b"].sum())
            denom = snaps + n_np  # plays run + no-play attempts = snap opportunities
            rate = float(len(sub) / denom) if denom > 0 else 0.0
            rates[(team, side)] = rate
            pools[(team, side)] = np.array(list(zip(sub["yards"].fillna(0).astype(int), sub["no_play_b"], sub["auto_b"],
                                                    sub["penalty_type_norm"].astype(str))), dtype=object)
            per_team[f"{team}|{side}"] = {"fouls": int(len(sub)), "no_play": n_np, "snaps_run": snaps,
                                         "rate_per_snap": rate, "yards": int(sub["yards"].sum())}
    weeks = sorted(int(w) for w in log["week"].unique())
    if pbp_path is _PBP_UNSET:
        pbp_path = (DEFAULT_PBP_FOR_COVERAGE
                    if Path(log_path).resolve() == CANONICAL_PENALTY_LOG.resolve() and DEFAULT_PBP_FOR_COVERAGE.exists()
                    else None)
    cov = penalty_log_unknowns(games, season=season, week_asof_exclusive=int(week_asof_exclusive), pbp_path=pbp_path)
    gap = cov["unknown_weeks"]
    by_team = cov["unknown_games_by_team"]
    modeled = {t: by_team.get(t, by_team.get(_espn_team(t), [])) for t in teams}
    meta = {"source": "data/redistributable/teams/penalty_plays_2026.csv (canonical, ESPN-reconciled 228/238)",
            "source_pulled_et": PENALTY_LOG_PULLED_ET,
            "weeks_used": weeks, "week_asof_exclusive": int(week_asof_exclusive),
            "coverage_gap_weeks": gap,
            # NFL-43 review D3 / residual R1: weeks AND individual games missing from PEN are UNKNOWN,
            # not zero-penalty. Rates are per-snap over the games that exist in PEN.
            "unknown_weeks": gap,
            "unknown_weeks_policy": ("UNKNOWN: no canonical penalty data for these weeks; rates use weeks_used only "
                                     "and do not treat the gap as zero penalties") if gap else None,
            "unknown_games": cov["unknown_games"],
            "unknown_games_by_team": by_team,
            "unknown_games_for_modeled_teams": modeled,
            "unknown_games_policy": cov["policy"] if (cov["unknown_games"] or gap) else None,
            "pbp_games_in_pen_weeks": cov["pbp_games_in_pen_weeks"],
            "season_filter": season_filter, "games_in_file": n_games_file,
            "kick_play_fouls_excluded": True, "per_team": per_team,
            **({"kick_formation_presnap_excluded": n_kick_form} if exclude_kick_formation else {})}
    return PenaltyModel(rates=rates, pools=pools, meta=meta)


def half_distance_move(yards: int, yardline_100: int, side: str) -> int:
    """Signed yardline_100 change for the offense. Offense foul -> +move (back), defense -> -move."""
    yards = max(0, int(yards))
    if side == "offense":
        room = 100 - int(yardline_100)  # distance to own goal line
        move = yards if yards <= room / 2 else room // 2
        return int(move)
    room = int(yardline_100)
    move = yards if yards <= room / 2 else room // 2
    return -int(move)


def enforce_penalty(st, pen: PenaltyDraw, *, live_ball: bool) -> dict:
    """Apply an accepted foul to state. Never scores, never changes possession."""
    before = int(st.yardline_100)
    delta = half_distance_move(pen.yards, before, pen.side)
    st.yardline_100 = int(np.clip(before + delta, 1, 99))
    applied = st.yardline_100 - before
    if pen.side == "defense":
        gained = -applied
        if pen.auto_first_down or gained >= st.ydstogo:
            st.down = 1
            st.ydstogo = 10 if st.yardline_100 >= 10 else max(1, st.yardline_100)
        else:
            st.ydstogo = max(1, int(st.ydstogo - gained))
    else:
        st.ydstogo = int(min(40, st.ydstogo + applied))
    ev = {"type": "penalty", "side": pen.side, "team": pen.team, "offense": st.possession,
          "nominal_yards": pen.yards, "applied_yardline_delta": int(applied), "no_play": pen.no_play,
          "live_ball": bool(live_ball), "auto_first_down": pen.auto_first_down, "penalty_type": pen.penalty_type,
          "from_yl": before, "to_yl": st.yardline_100, "qtr": st.qtr}
    st.events.append(ev)
    st.penalty_yards[pen.team] = st.penalty_yards.get(pen.team, 0) + abs(int(applied))
    return ev


@dataclass
class ReturnModel:
    kick_return_td_rate: float
    punt_return_td_rate: float
    meta: dict
    # NFL-43 D2: as-of league pools of (return_yards, return_touchdown) for defensive returns, by turnover kind.
    def_return_pools: dict = field(default_factory=dict)  # {"interception": ndarray[n,2], "fumble_lost": ndarray[n,2]}

    def draw_def_return(self, rng: np.random.Generator, kind: str) -> tuple[float, bool]:
        """League-rate defensive return for an interception or fumble lost. Empty pool -> no return, no TD."""
        pool = self.def_return_pools.get(kind)
        if pool is None or len(pool) == 0:
            return 0.0, False
        y, td = pool[int(rng.integers(0, len(pool)))]
        return float(y), bool(td)


def build_return_model(pbp_path, *, season: int, week_asof_exclusive: int) -> ReturnModel:
    import pyarrow.parquet as pq
    cols = [c for c in ("season", "week", "kickoff_attempt", "punt_attempt", "return_touchdown", "return_yards",
                        "punt_blocked", "interception", "fumble_lost")
            if c in set(pq.ParquetFile(pbp_path).schema_arrow.names)]
    d = pd.read_parquet(pbp_path, columns=cols)
    d = d[(d["season"] == season) & (d["week"] < int(week_asof_exclusive))]
    if "return_touchdown" not in d.columns:
        raise ValueError("UNSUPPORTED: pbp lacks return_touchdown; return semantics cannot be enabled")
    for c in ("interception", "fumble_lost"):
        if c not in d.columns:
            raise ValueError(f"UNSUPPORTED: pbp lacks {c}; league defensive-return pool cannot be built")
    ko = d[d["kickoff_attempt"] == 1]
    pu = d[d["punt_attempt"] == 1]
    pools, pool_meta = {}, {}
    for kind in ("interception", "fumble_lost"):
        t = d[d[kind] == 1]
        arr = np.column_stack([t["return_yards"].fillna(0).to_numpy(float),
                               t["return_touchdown"].fillna(0).to_numpy(float)]) if len(t) else np.zeros((0, 2))
        pools[kind] = arr
        pool_meta[kind] = {"plays": int(len(t)), "return_tds": int(arr[:, 1].sum()) if len(arr) else 0,
                           "mean_return_yards": float(arr[:, 0].mean()) if len(arr) else None}
    meta = {"source": "nflverse play_by_play (league, weeks < target)", "weeks": sorted(int(w) for w in d["week"].unique()),
            "kickoffs": int(len(ko)), "kick_return_tds": int(ko["return_touchdown"].fillna(0).sum()),
            "punts": int(len(pu)), "punt_return_tds": int(pu["return_touchdown"].fillna(0).sum()),
            "mean_kick_return_yards": float(ko["return_yards"].mean()) if len(ko) else None,
            "mean_punt_return_yards": float(pu["return_yards"].mean()) if len(pu) else None,
            "def_return_pools": pool_meta,
            "def_return_mode": "LEAGUE_POOL_BY_TURNOVER_KIND (all teams, weeks < target)",
            "label": "AS_OF_LEAGUE_RATE_NOT_TEAM_FIT"}
    return ReturnModel(kick_return_td_rate=meta["kick_return_tds"] / max(1, meta["kickoffs"]),
                       punt_return_td_rate=meta["punt_return_tds"] / max(1, meta["punts"]), meta=meta,
                       def_return_pools=pools)


class OTTracker:
    """Official 2025 regular-season overtime: both teams possess once, then sudden death."""

    def __init__(self, st, first_receiver: str):
        self.first = first_receiver
        self.second = st.away if first_receiver == st.home else st.home
        self.phase = 0  # 0 first possession, 1 second possession, 2 sudden death
        self.events = st.events

    def update(self, st, prev_possession: str, prev_scores: tuple[int, int]) -> None:
        if st.final:
            return
        scores = (st.score_home, st.score_away)
        scored = scores != prev_scores
        def pts(team):
            return st.score_home if team == st.home else st.score_away
        changed = st.possession != prev_possession
        if self.phase == 0:
            if scored and pts(self.second) > (prev_scores[0] if self.second == st.home else prev_scores[1]):
                self._end(st, "ot_defensive_score_first_possession")
                return
            if changed:
                self.phase = 1
            return
        if self.phase == 1:
            if scored and pts(self.second) > pts(self.first):
                self._end(st, "ot_second_team_leads")
                return
            if scored and pts(self.first) > (prev_scores[0] if self.first == st.home else prev_scores[1]):
                self._end(st, "ot_first_team_defensive_score")
                return
            if changed and st.possession == self.first:
                if pts(self.first) != pts(self.second):
                    self._end(st, "ot_after_both_possessions")
                    return
                self.phase = 2
            return
        if scored:
            self._end(st, "ot_sudden_death_score")

    def _end(self, st, why: str) -> None:
        st.final = True
        st.events.append({"type": "final_ot", "rule": "official_2025_regular_season", "reason": why})

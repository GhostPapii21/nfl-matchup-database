"""Synthetic play-by-play / roster / schedule builders for the historical-leakage audit tests.

Pure test helper (no production import side effects). Used by evaluation/tests/test_hist_leakage_*.py.
Builds a tiny 2-season league where every number is known, so a test can change only FUTURE rows and check
that a point-in-time projection does not move.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

TEAMS = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"]


def schedule(season: int, weeks: int = 8) -> pd.DataFrame:
    """Round-robin-ish schedule: AAA plays a different opponent each week; the others pair up."""
    rows = []
    others = TEAMS[1:]
    for w in range(1, weeks + 1):
        opp = others[(w - 1) % len(others)]
        rest = [t for t in others if t != opp]
        pairs = [("AAA", opp)] + [(rest[i], rest[i + 1]) for i in range(0, len(rest) - 1, 2)]
        for h, a in pairs:
            rows.append(dict(season=season, week=w, game_type="REG", game_id=f"{season}_{w:02d}_{a}_{h}",
                             home_team=h, away_team=a, home_score=24, away_score=20, spread_line=-3.0,
                             gameday=f"{season}-09-{7 + 7 * (w - 1):02d}" if 7 + 7 * (w - 1) <= 30 else
                             f"{season}-10-{(7 + 7 * (w - 1)) - 30:02d}"))
    return pd.DataFrame(rows)


def pbp(season: int, sched: pd.DataFrame, rng_seed: int = 0, zero_weeks: dict | None = None) -> pd.DataFrame:
    """Per team-game: 30 pass plays and 25 runs. WR1 of each team gets 8 targets, RB1 gets 15 carries.
    zero_weeks = {(team, week): {"WR1", "RB1"}} removes that player's plays in that game (inactive / zero-stat)."""
    rng = np.random.default_rng(rng_seed + season)
    zero_weeks = zero_weeks or {}
    rows = []
    for g in sched.itertuples():
        for off, dfn in ((g.home_team, g.away_team), (g.away_team, g.home_team)):
            skip = zero_weeks.get((off, g.week), set())
            for i in range(30):
                tgt = f"{off}_WR1" if i < 8 else f"{off}_WR2" if i < 18 else f"{off}_TE1" if i < 24 else f"{off}_RB1"
                if tgt.split("_")[1] in skip:
                    tgt = f"{off}_WR3"
                comp = int(rng.random() < 0.65)
                rows.append(dict(season=season, season_type="REG", week=g.week, game_id=g.game_id, posteam=off,
                                 defteam=dfn, play_type="pass", pass_attempt=1, rush_attempt=0, sack=0,
                                 qb_scramble=0, two_point_attempt=0, receiver_player_id=tgt, rusher_player_id=None,
                                 complete_pass=comp, receiving_yards=float(rng.integers(3, 25)) if comp else 0.0,
                                 rushing_yards=np.nan, home_team=g.home_team, away_team=g.away_team,
                                 game_date=g.gameday))
            for i in range(25):
                ru = f"{off}_RB1" if i < 15 else f"{off}_RB2"
                if ru.split("_")[1] in skip:
                    ru = f"{off}_RB3"
                rows.append(dict(season=season, season_type="REG", week=g.week, game_id=g.game_id, posteam=off,
                                 defteam=dfn, play_type="run", pass_attempt=0, rush_attempt=1, sack=0, qb_scramble=0,
                                 two_point_attempt=0, receiver_player_id=None, rusher_player_id=ru, complete_pass=0,
                                 receiving_yards=np.nan, rushing_yards=float(rng.integers(-2, 12)),
                                 home_team=g.home_team, away_team=g.away_team, game_date=g.gameday))
    return pd.DataFrame(rows)


def roster(season: int, sched: pd.DataFrame, status_override: dict | None = None) -> pd.DataFrame:
    """Weekly roster rows (status ACT) for every synthetic player; status_override={(team, week, slot): 'INA'}."""
    status_override = status_override or {}
    pos = {"WR1": "WR", "WR2": "WR", "WR3": "WR", "TE1": "TE", "RB1": "RB", "RB2": "RB", "RB3": "RB"}
    rows = []
    for w in sorted(sched.week.unique()):
        for t in TEAMS:
            for slot, p in pos.items():
                rows.append(dict(season=season, week=int(w), game_type="REG", team=t, gsis_id=f"{t}_{slot}",
                                 position=p, status=status_override.get((t, int(w), slot), "ACT")))
    return pd.DataFrame(rows)

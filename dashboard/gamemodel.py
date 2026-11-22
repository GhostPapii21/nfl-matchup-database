"""Game-market model: full game, halves and quarters, from the most similar real games.

For a game with implied points (home_imp, away_imp) from the market's spread and total, take the K most similar
regular-season games 2022-2026 by implied points (dashboard/game_history.csv, rebuilt by
research/game_markets_2026/build_history.py) and use their actual scores by period. Every market is then a count:
  moneyline  win / tie (push) / lose for that period (full game includes overtime)
  spread     margin + line  > 0 win, = 0 push, < 0 lose
  total      points vs line > / = / <
Real games keep the key numbers (3, 7, 10), quarter ties and the 4th-quarter swing that smooth curves miss."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HIST = Path(__file__).resolve().parent / "game_history.csv"
K = 250
PERIODS = {"": ("q1", "q2", "q3", "q4", "ot"), "h1_": ("q1", "q2"), "h2_": ("q3", "q4"), "q1_": ("q1",), "q2_": ("q2",), "q3_": ("q3",), "q4_": ("q4",)}
_H = None


def history() -> pd.DataFrame:
    global _H
    if _H is None:
        _H = pd.read_csv(HIST)
    return _H


_SHARE = None


def shares() -> dict:
    """League share of points scored in each quarter (and overtime), from the history table."""
    global _SHARE
    if _SHARE is None:
        h = history()
        tot = {q: float(h[f"h_{q}"].sum() + h[f"a_{q}"].sum()) for q in ("q1", "q2", "q3", "q4", "ot")}
        _SHARE = {q: v / sum(tot.values()) for q, v in tot.items()}
    return _SHARE


def neighbors(home_imp: float, away_imp: float, k: int = K, hist: pd.DataFrame | None = None) -> pd.DataFrame:
    """The k most similar games, each adjusted to this game's implied points: the gap in implied points is spread across
    the quarters by the league's scoring shares and rounded, so lopsided games are not pulled toward closer games."""
    h = history() if hist is None else hist
    d = np.hypot(h.home_imp - home_imp, h.away_imp - away_imp)
    nb = h.iloc[np.argsort(d.values)[:k]].copy()
    sh = shares()
    dh, da = home_imp - nb.home_imp, away_imp - nb.away_imp
    for q in ("q1", "q2", "q3", "q4"):
        nb[f"h_{q}"] = (nb[f"h_{q}"] + dh * sh[q]).round().clip(lower=0)
        nb[f"a_{q}"] = (nb[f"a_{q}"] + da * sh[q]).round().clip(lower=0)
    return nb


def period_points(nb: pd.DataFrame, prefix: str) -> tuple[np.ndarray, np.ndarray]:
    qs = PERIODS[prefix]
    return nb[[f"h_{q}" for q in qs]].sum(axis=1).values, nb[[f"a_{q}" for q in qs]].sum(axis=1).values


def outcome(nb: pd.DataFrame, market: str, side: str, line: float | None, home: str, away: str) -> tuple[float, float, float] | None:
    """(p_win, p_push, p_lose) for one bet. market like 'q1_spread', 'total', 'h1_moneyline'; side = team code or Over/Under;
    spread line is from the bet side's point of view (e.g. home -3.5)."""
    base = market.split("_")[-1]
    prefix = market[: -len(base)]
    if prefix not in PERIODS:
        return None
    hp, ap = period_points(nb, prefix)
    if base == "total":
        if line is None or side not in ("Over", "Under"):
            return None
        t = hp + ap
        w, p = (t > line).mean(), (t == line).mean()
        return (w, p, 1 - w - p) if side == "Over" else (1 - w - p, p, w)
    if side not in (home, away):
        return None
    m = hp - ap if side == home else ap - hp
    if base == "moneyline":
        return float((m > 0).mean()), float((m == 0).mean()), float((m < 0).mean())
    if base == "spread" and line is not None:
        x = m + line
        return float((x > 0).mean()), float((x == 0).mean()), float((x < 0).mean())
    return None

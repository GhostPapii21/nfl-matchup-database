"""Reconstruct standalone quarter and half scores; regulation vs final (OT) separated."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED = ["game_id","season","week","game_date","home_team","away_team","qtr",
            "total_home_score","total_away_score"]


def load_pbp(path: str | Path, seasons: list[int] | None = None) -> pd.DataFrame:
    import pyarrow.parquet as pq
    path = Path(path)
    schema = set(pq.read_schema(path).names)
    missing = [c for c in REQUIRED if c not in schema]
    if missing:
        raise ValueError(f"pbp missing required columns: {missing}")
    use = list(REQUIRED) + (["season_type"] if "season_type" in schema else [])
    for opt in ("play_id", "game_seconds_remaining", "order_sequence"):
        if opt in schema:
            use.append(opt)
    df = pd.read_parquet(path, columns=use)
    if "season_type" not in df.columns:
        df["season_type"] = "REG"
    df = df[df.season_type == "REG"].copy()
    if seasons:
        df = df[df.season.isin(seasons)]
    return df


def _end_of_q_scores(g: pd.DataFrame, q: int) -> tuple[int, int]:
    """End of regulation quarter q via max cumulative in that quarter (order-invariant)."""
    sub = g[g.qtr == q]
    if sub.empty:
        sub = g[g.qtr <= q]
    if sub.empty:
        return 0, 0
    return int(sub.total_home_score.max()), int(sub.total_away_score.max())


def _final_scores(g: pd.DataFrame) -> tuple[int, int, int]:
    """Official final including OT; returns home, away, max_qtr."""
    return int(g.total_home_score.max()), int(g.total_away_score.max()), int(g.qtr.max())


def period_table_from_pbp(pbp: pd.DataFrame) -> pd.DataFrame:
    """One row per game.

    Columns:
      q1–q4, h1, h2: regulation period scores (standalone or half).
      reg_home/reg_away: end of Q4 (regulation only).
      fg_home/fg_away: official FINAL including OT when played.
      score_scope_reg / score_scope_fg: metadata strings.
      went_ot: bool.
    Book FG team totals typically map to fg_*; period markets Q1–H1 map to q*/h1.
    """
    rows = []
    for gid, g in pbp.groupby("game_id", sort=False):
        home = g.home_team.iloc[0]
        away = g.away_team.iloc[0]
        season = int(g.season.iloc[0])
        week = int(g.week.iloc[0])
        date = str(g.game_date.iloc[0])
        cum = {q: _end_of_q_scores(g, q) for q in (1, 2, 3, 4)}
        h1h, h1a = cum[2]
        q1h, q1a = cum[1]
        q2h, q2a = h1h - q1h, h1a - q1a
        h2h, h2a = cum[4][0] - h1h, cum[4][1] - h1a
        q3_cum_h, q3_cum_a = cum[3]
        q3h, q3a = q3_cum_h - h1h, q3_cum_a - h1a
        q4h, q4a = cum[4][0] - q3_cum_h, cum[4][1] - q3_cum_a
        reg_h, reg_a = cum[4]
        fin_h, fin_a, max_qtr = _final_scores(g)
        went_ot = max_qtr >= 5
        assert min(q2h, q2a, q3h, q3a, q4h, q4a) >= 0
        rows.append(dict(
            game_id=gid, season=season, week=week, game_date=date,
            home_team=home, away_team=away,
            q1_home=q1h, q1_away=q1a, q2_home=q2h, q2_away=q2a,
            q3_home=q3h, q3_away=q3a, q4_home=q4h, q4_away=q4a,
            h1_home=h1h, h1_away=h1a, h2_home=h2h, h2_away=h2a,
            reg_home=reg_h, reg_away=reg_a,
            fg_home=fin_h, fg_away=fin_a,
            went_ot=bool(went_ot), max_qtr=int(max_qtr),
            score_scope_reg="regulation_only",
            score_scope_fg="includes_ot" if went_ot else "regulation_equals_final",
        ))
    return pd.DataFrame(rows)


def as_of_mask(periods: pd.DataFrame, season: int, week: int) -> pd.Series:
    return (periods.season < season) | ((periods.season == season) & (periods.week < week))

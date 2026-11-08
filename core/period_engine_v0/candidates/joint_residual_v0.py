"""EXPLORATORY candidate — joint residual sampling for period totals.

NOT used by walkforward.py. NOT a production model. NOT validated for edge.
Preserves untouched W1–8 evaluation in parent package.

Idea: instead of independent team quarter vectors, draw a shared game shock
and team-centered residuals so P(both high) is dampened toward historical joint rates.
"""
from __future__ import annotations
import hashlib
import numpy as np
import pandas as pd


def _stable(seed: int, key: str) -> int:
    d = hashlib.sha256(f"{seed}|{key}".encode()).hexdigest()
    return (seed + int(d[:8], 16)) % (2**31 - 1)


def team_period_totals(asof: pd.DataFrame, team: str, period: str) -> np.ndarray:
    ph, pa = f"{period}_home", f"{period}_away"
    a = asof.loc[asof.home_team == team, ph].to_numpy(float)
    b = asof.loc[asof.away_team == team, pa].to_numpy(float)
    return np.concatenate([a, b]) if len(a) or len(b) else np.array([], float)


def simulate_joint_totals(
    asof: pd.DataFrame,
    home: str,
    away: str,
    period: str = "fg",
    *,
    n: int = 20_000,
    seed: int = 0,
) -> dict:
    """Return home/away total samples with a shared multiplicative game residual.

    status always includes exploratory=True and not_in_walkforward=True.
    """
    rng = np.random.default_rng(_stable(seed, f"{home}|{away}|{period}"))
    Hh = team_period_totals(asof, home, period)
    Ha = team_period_totals(asof, away, period)
    if len(Hh) < 1 or len(Ha) < 1:
        return {"error": "ASOF_INSUFFICIENT", "exploratory": True, "not_in_walkforward": True}
    mh, ma = float(Hh.mean()), float(Ha.mean())
    # empirical CV of game totals for shared shock scale (data-derived, unfitted for edge)
    games = asof[[f"{period}_home", f"{period}_away"]].sum(axis=1).to_numpy(float)
    mu = games.mean() if len(games) else 1.0
    cv = float(games.std(ddof=1) / mu) if mu > 0 and len(games) > 1 else 0.0
    sigma = float(np.sqrt(np.log(1 + cv**2))) if cv > 0 else 0.0
    shock = rng.lognormal(-0.5 * sigma * sigma, sigma, size=n)
    # team residuals relative to mean, bootstrap then scale by shared shock
    rh = rng.choice(Hh, size=n) - mh
    ra = rng.choice(Ha, size=n) - ma
    home_s = np.maximum(np.rint(mh * shock + rh), 0).astype(int)
    away_s = np.maximum(np.rint(ma * shock + ra), 0).astype(int)
    both35 = float(((home_s >= 35) & (away_s >= 35)).mean())
    return {
        "exploratory": True,
        "not_in_walkforward": True,
        "n": n,
        "seed": _stable(seed, f"{home}|{away}|{period}"),
        "sigma_empirical_cv": sigma,
        "home_mean": float(home_s.mean()),
        "away_mean": float(away_s.mean()),
        "p_both_ge_35": both35,
        "status": "CANDIDATE_UNVALIDATED",
        "disclaimer": "Do not cite as beating baselines or as a cleared model.",
    }

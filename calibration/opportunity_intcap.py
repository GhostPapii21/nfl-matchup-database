"""NFL-75 Phase 2b: walk-forward fit of the engine's opt-in INT pooling (core/possession_engine_v0/int_pool.py).

For eval week w of season S the engine's pool for a team is its season-S rows from weeks 1..w-1. The pooled rate is
p* = (k + m * p_league) / (n + m) with n attempts and k interceptions in that pool (sacks excluded) and p_league the
league-wide rate over the same weeks. m is chosen to maximise the binomial log likelihood of each team-game's actual
interceptions given its actual attempts, over training team-games strictly before the eval week:
2024 and 2025 REG weeks 4-18 (each with its own season-to-date pool) and 2026 weeks 4..w-1. No week >= w is read.
Weeks >= 10 of 2026 are the reserved holdout: fitting a week-10 spec uses weeks <= 9 only; scoring is refused
elsewhere. Research only; zero network, zero Odds API credits."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from calibration import opportunity_fit as F

M_GRID = (0.0, 25.0, 50.0, 100.0, 150.0, 200.0, 300.0, 400.0, 600.0, 800.0, 1200.0, 2000.0, 5000.0, 1e9)
SEASONS = (2024, 2025, 2026)


def _team_week(season: int) -> pd.DataFrame:
    """Per (team, week): pass attempts (sack excluded) and interceptions, REG only."""
    df = F.load_pbp(season)
    if "season_type" in df.columns:
        df = df[df["season_type"] == "REG"]
    sk = pd.to_numeric(df["sack"], errors="coerce").fillna(0)
    a = df[(df["play_type"] == "pass") & (sk != 1)]
    it = pd.to_numeric(a["interception"], errors="coerce").fillna(0)
    g = pd.DataFrame({"team": a["posteam"], "week": a["week"], "att": 1, "int": (it == 1).astype(int)})
    return g.groupby(["team", "week"], as_index=False)[["att", "int"]].sum()


def league_rate(season: int, week: int) -> dict:
    tw = _team_week(season)
    d = tw[tw["week"] < week]
    n, k = int(d["att"].sum()), int(d["int"].sum())
    return {"season": season, "weeks": [1, week - 1], "att": n, "int": k, "rate": k / n if n else None}


def train_rows(eval_season: int, eval_week: int) -> list:
    rows = []
    for s in SEASONS:
        if s > eval_season:
            continue
        tw = _team_week(s)
        maxw = (eval_week - 1) if s == eval_season else 18
        for w in range(4, maxw + 1):
            prior = tw[tw["week"] < w]
            n_l, k_l = prior["att"].sum(), prior["int"].sum()
            if n_l == 0:
                continue
            pl = k_l / n_l
            pt = prior.groupby("team")[["att", "int"]].sum()
            for r in tw[tw["week"] == w].itertuples():
                if r.team in pt.index:
                    rows.append((s, w, r.att, r.int, int(pt.loc[r.team, "att"]), int(pt.loc[r.team, "int"]), pl))
    if any(s == eval_season and w >= eval_week for s, w, *_ in rows):
        raise RuntimeError("leak: training row at/after the eval week")
    return rows


def _ll(rows, m: float) -> float:
    tot = 0.0
    for _s, _w, a, k, n, kk, pl in rows:
        p = (kk + m * pl) / (n + m) if (n + m) > 0 else pl
        p = min(max(p, 1e-6), 1 - 1e-6)
        tot += k * math.log(p) + (a - k) * math.log(1 - p)
    return tot


def fit_week(eval_season: int, eval_week: int) -> dict:
    rows = train_rows(eval_season, eval_week)
    lls = {m: _ll(rows, m) for m in M_GRID}
    best = max(lls, key=lls.get)
    lr = league_rate(eval_season, eval_week)
    return {"schema": "nfl75-int-pool/1", "league_rate": lr["rate"], "m": best,
            "meta": {"eval_season": eval_season, "eval_week": eval_week, "league": lr,
                     "train_team_games": len(rows), "loglik_by_m": {str(k): v for k, v in lls.items()},
                     "at_grid_edge": best in (M_GRID[0], M_GRID[-1]),
                     "loglik_no_pool_m0": lls[0.0], "loglik_league_only": lls[1e9],
                     "fitted_on": f"2024-2025 REG weeks 4-18 + {eval_season} weeks 4..{eval_week - 1}",
                     "research_only": True, "projection_ready": False}}


OUT = F.ROOT / "research/runs/2026-11-13_opportunity_phase2b/int_pool"


def main(argv=None):
    """python3 -m calibration.opportunity_intcap 4 5 6 7 8 9 10 -> int_pool/int_pool_2026_wNN.json (frozen specs)."""
    import json
    import sys
    ws = [int(x) for x in (argv if argv is not None else sys.argv[1:])]
    if any(w > F.HOLDOUT_FIRST_WEEK for w in ws):
        raise SystemExit("eval weeks > 10 are not fitted here (week 10 = the frozen pregame fit on data <= week 9)")
    OUT.mkdir(parents=True, exist_ok=True)
    for w in ws:
        (OUT / f"int_pool_2026_w{w:02d}.json").write_text(json.dumps(fit_week(2026, w), indent=1) + "\n")
        print("froze int_pool", w, flush=True)


if __name__ == "__main__":
    main()

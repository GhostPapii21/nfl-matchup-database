"""Chronological as-of grading — both teams' own prior W1–8 plays (no league/prior-year pool)."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Sequence
import numpy as np
import pandas as pd
from config_load import load_config
from simulate import PlayCatalog, simulate_one, stable_seed, build_catalog
from pbp_filter import COLS


SCOPE_FOCUS = {"JAX", "BAL"}  # target slate focus; opponents allowed as historical partners


def list_jaxbal_games(pbp_path: str | Path) -> list[dict]:
    cols = ["game_id", "week", "home_team", "away_team", "play_id", "total_home_score", "total_away_score", "season"]
    t = pd.read_parquet(pbp_path, columns=cols)
    t = t[(t["season"] == 2026) & (t["week"] <= 8)]
    inv = t["home_team"].isin(SCOPE_FOCUS) | t["away_team"].isin(SCOPE_FOCUS)
    rows = []
    for gid, gg in t[inv].groupby("game_id"):
        home, away = gg["home_team"].iloc[0], gg["away_team"].iloc[0]
        last = gg.sort_values("play_id").iloc[-1]
        rows.append({
            "game_id": gid,
            "week": int(gg["week"].iloc[0]),
            "home": home,
            "away": away,
            "actual_home": float(last["total_home_score"]),
            "actual_away": float(last["total_away_score"]),
            "focus_teams": sorted(set([home, away]) & SCOPE_FOCUS),
        })
    return sorted(rows, key=lambda r: (r["week"], r["game_id"]))


def build_asof_history(pbp_path, *, teams, season, before_week):
    """Legacy helper: multi-team offense catalog, own-season weeks < before_week."""
    return build_asof_history_for_game(
        pbp_path, home=teams[0], away=teams[1] if len(teams) > 1 else teams[0],
        season=season, week=before_week,
    )


def build_asof_history_for_game(
    pbp_path: str | Path,
    *,
    home: str,
    away: str,
    season: int,
    week: int,
) -> dict:
    """Load BOTH teams' posteam plays for weeks strictly before `week`, same season only.

    No prior-year pooling. No league-wide silent fallback.
    """
    if week <= 1:
        return {
            "status": "EMPTY_ASOF",
            "df": None,
            "evidence": {
                "n_plays": 0, "n_plays_home": 0, "n_plays_away": 0,
                "reason": "NO_OWN_SEASON_HISTORY",
                "prior_year_pooled": False, "league_pooled": False,
            },
        }
    import pyarrow.parquet as pq
    path = Path(pbp_path)
    available = set(pq.ParquetFile(path).schema_arrow.names)
    use = [c for c in COLS if c in available]
    for extra in ("season", "qb_hit", "qb_scramble", "sack", "complete_pass"):
        if extra in available and extra not in use:
            use.append(extra)
    df = pd.read_parquet(path, columns=use)
    teams = [home, away]
    mask = (
        (df["season"] == season)
        & (df["week"] < week)
        & (df["week"] >= 1)
        & (df["posteam"].isin(teams))
    )
    off = df.loc[mask].copy()
    n_h = int((off["posteam"] == home).sum())
    n_a = int((off["posteam"] == away).sum())
    evid = {
        "n_plays": int(len(off)),
        "n_plays_home": n_h,
        "n_plays_away": n_a,
        "teams": teams,
        "weeks": [1, week - 1],
        "season": season,
        "prior_year_pooled": False,
        "league_pooled": False,
        "source": str(path),
    }
    if n_h == 0 or n_a == 0:
        return {"status": "SPARSE_ASOF_ONE_TEAM", "df": off.reset_index(drop=True) if len(off) else None, "evidence": evid}
    if off.empty:
        return {"status": "EMPTY_ASOF", "df": None, "evidence": evid}
    # Guard: no future weeks
    if off["week"].max() >= week:
        return {"status": "WEEK_FILTER_FAILED", "df": None, "evidence": evid}
    dmask = (df["season"] == season) & (df["week"] < week) & (df["week"] >= 1) & (df["defteam"].isin(teams))
    def_df = df.loc[dmask].reset_index(drop=True)
    evid["n_def_allowed_rows"] = int(len(def_df))
    return {"status": "OK", "df": off.reset_index(drop=True), "def_df": def_df, "evidence": evid}


def _asof_team_ppg(pbp_path, team: str, season: int, before_week: int) -> float | None:
    """Simple baseline: mean points scored in completed games before week."""
    cols = ["game_id", "week", "home_team", "away_team", "play_id", "total_home_score", "total_away_score", "season"]
    t = pd.read_parquet(pbp_path, columns=cols)
    t = t[(t["season"] == season) & (t["week"] < before_week) & (t["week"] >= 1)]
    inv = (t["home_team"] == team) | (t["away_team"] == team)
    scores = []
    for gid, gg in t[inv].groupby("game_id"):
        last = gg.sort_values("play_id").iloc[-1]
        scores.append(float(last["total_home_score"] if gg["home_team"].iloc[0] == team else last["total_away_score"]))
    return float(np.mean(scores)) if scores else None


def grade_week_games(
    pbp_path: str | Path,
    *,
    weeks: Sequence[int],
    n_sims: int = 200,
    seed_base: int = 20261105,
    config_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    root = Path(__file__).resolve().parents[1]
    cfg_path = Path(config_path) if config_path else root / "config/jax_bal_tnf_2026-11-05_data_only.json"
    base_cfg = load_config(cfg_path)
    games = [g for g in list_jaxbal_games(pbp_path) if g["week"] in set(weeks)]
    rows = []
    for g in games:
        row = {
            **g,
            "config_mode": base_cfg["mode"],
            "n_sims": n_sims,
            "silent_pool_applied": False,
            "prior_year_pooled": False,
            "league_pooled": False,
            "market_edge": None,
            "market_status": "NO_MATCHING_PREKICK_PINNACLE_QUOTES",
            "approved_pick": False,
            "pred_home_mean": None,
            "pred_away_mean": None,
            "pred_h1_home_mean": None,
            "pred_h1_away_mean": None,
            "abs_err_home": None,
            "abs_err_away": None,
            "baseline_home_ppg": None,
            "baseline_away_ppg": None,
            "baseline_abs_err_home": None,
            "baseline_abs_err_away": None,
            "grade_status": None,
            "skip_reason": None,
            "asof_n_plays_home": None,
            "asof_n_plays_away": None,
        }
        asof = build_asof_history_for_game(
            pbp_path, home=g["home"], away=g["away"], season=2026, week=g["week"]
        )
        row["asof_n_plays_home"] = asof["evidence"].get("n_plays_home")
        row["asof_n_plays_away"] = asof["evidence"].get("n_plays_away")
        if asof["status"] == "EMPTY_ASOF":
            row["grade_status"] = "UNGRADEABLE_NO_OWN_SEASON_HISTORY"
            row["skip_reason"] = asof["evidence"].get("reason", "NO_ASOF_OWN_SEASON_HISTORY")
            rows.append(row)
            continue
        if asof["status"] != "OK":
            row["grade_status"] = f"UNGRADEABLE_{asof['status']}"
            row["skip_reason"] = asof["status"]
            rows.append(row)
            continue

        cfg = dict(base_cfg)
        cfg["game"] = {"home": g["home"], "away": g["away"], "season": 2026, "week_asof_exclusive": g["week"]}
        cfg["config_id"] = f"{base_cfg['config_id']}__asof_w{g['week']}_{g['game_id']}"
        df = asof["df"]
        cat, _prov = build_catalog(df, cfg, games_df=asof.get("def_df"))
        seed = stable_seed(seed_base, g["week"], g["game_id"])
        rng = np.random.default_rng(seed)
        scores = []
        h1s = []
        for _ in range(n_sims):
            st = simulate_one(df, cat, cfg, np.random.default_rng(int(rng.integers(0, 2**31 - 1))))
            snap = st.period_snapshot()
            scores.append((st.score_home, st.score_away))
            h1s.append((snap["h1_home"], snap["h1_away"]))
        ph = float(np.mean([s[0] for s in scores]))
        pa = float(np.mean([s[1] for s in scores]))
        bh = _asof_team_ppg(pbp_path, g["home"], 2026, g["week"])
        ba = _asof_team_ppg(pbp_path, g["away"], 2026, g["week"])
        row.update({
            "grade_status": "GRADED_FULL",
            "skip_reason": None,
            "pred_home_mean": ph,
            "pred_away_mean": pa,
            "pred_h1_home_mean": float(np.mean([x[0] for x in h1s])),
            "pred_h1_away_mean": float(np.mean([x[1] for x in h1s])),
            "abs_err_home": abs(ph - g["actual_home"]),
            "abs_err_away": abs(pa - g["actual_away"]),
            "baseline_home_ppg": bh,
            "baseline_away_ppg": ba,
            "baseline_abs_err_home": abs(bh - g["actual_home"]) if bh is not None else None,
            "baseline_abs_err_away": abs(ba - g["actual_away"]) if ba is not None else None,
            "seed": seed,
            "asof_n_plays": int(asof["evidence"].get("n_plays", 0)),
        })
        rows.append(row)
    return rows

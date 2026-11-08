"""Build evidence tables from local PBP + FTN charting (read-only, no spend)."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Optional
import json
import numpy as np
import pandas as pd
from effects.definitions import EXPLOSIVE_PASS_YARDS, EXPLOSIVE_RUSH_YARDS

# Public repo does not ship FTN charting. A local licensed file may be placed here.
FTN_CANDIDATES = [
    Path(__file__).resolve().parents[2] / "data" / "licensed" / "ftn_charting_2026.parquet",
]


def _find_ftn() -> Optional[Path]:
    for p in FTN_CANDIDATES:
        if p.exists():
            return p
    return None


from functools import lru_cache


@lru_cache(maxsize=4)
def _read_ftn_cached(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def load_ftn_join(pbp: pd.DataFrame, *, teams=("JAX", "BAL"), weeks=(1, 8)) -> dict[str, Any]:
    ftn_path = _find_ftn()
    meta = {
        "ftn_path": str(ftn_path) if ftn_path else None,
        "status": "MISSING_FTN" if ftn_path is None else "OK",
        "man_zone_mofo_mofc_in_ftn": False,
        "note": "FTN 2026 local extract has n_blitzers/n_pass_rushers; no man/zone/MOFO/MOFC/route columns",
    }
    if ftn_path is None:
        return {"meta": meta, "joined": None}
    ftn = _read_ftn_cached(str(ftn_path)).copy()
    # join keys
    left = pbp.copy()
    if "game_id" not in left.columns or "play_id" not in left.columns:
        meta["status"] = "PBP_MISSING_KEYS"
        return {"meta": meta, "joined": None}
    ftn = ftn.rename(columns={"nflverse_game_id": "game_id", "nflverse_play_id": "play_id"})
    # play_id types
    left["play_id"] = pd.to_numeric(left["play_id"], errors="coerce")
    ftn["play_id"] = pd.to_numeric(ftn["play_id"], errors="coerce")
    j = left.merge(ftn[["game_id", "play_id", "n_blitzers", "n_pass_rushers", "date_pulled"]], on=["game_id", "play_id"], how="left")
    j["is_blitz_ftn"] = j["n_blitzers"].fillna(0) >= 1
    j["ftn_joined"] = j["n_blitzers"].notna()
    meta["n_pbp"] = int(len(left))
    meta["n_joined"] = int(j["ftn_joined"].sum())
    meta["join_rate"] = float(j["ftn_joined"].mean())
    meta["date_pulled_sample"] = str(j["date_pulled"].dropna().iloc[0]) if j["date_pulled"].notna().any() else None
    return {"meta": meta, "joined": j}


def explosive_tables(df: pd.DataFrame) -> dict[str, Any]:
    """Offensive explosive rates + defensive explosives allowed (when team is defteam)."""
    out = {
        "definitions": {
            "explosive_pass_yards": EXPLOSIVE_PASS_YARDS,
            "explosive_rush_yards": EXPLOSIVE_RUSH_YARDS,
        },
        "offense": {},
        "defense_allowed": {},
    }
    for team, g in df.groupby("posteam"):
        passes = g[g["play_type"] == "pass"]
        runs = g[g["play_type"] == "run"]
        exp_p = passes[pd.to_numeric(passes["yards_gained"], errors="coerce").fillna(0) >= EXPLOSIVE_PASS_YARDS]
        exp_r = runs[pd.to_numeric(runs["yards_gained"], errors="coerce").fillna(0) >= EXPLOSIVE_RUSH_YARDS]
        out["offense"][team] = {
            "pass_attempts": int(len(passes)),
            "explosive_passes": int(len(exp_p)),
            "p_explosive_pass": float(len(exp_p) / len(passes)) if len(passes) else None,
            "rush_attempts": int(len(runs)),
            "explosive_rushes": int(len(exp_r)),
            "p_explosive_rush": float(len(exp_r) / len(runs)) if len(runs) else None,
            "status": "OK" if len(passes) + len(runs) >= 30 else "SPARSE",
        }
    # defense allowed: need defteam on rows — offense df is posteam-filtered; use games via full involvements if present
    if "defteam" in df.columns:
        for team, g in df.groupby("defteam"):
            if team not in ("JAX", "BAL"):
                continue
            passes = g[g["play_type"] == "pass"]
            runs = g[g["play_type"] == "run"]
            exp_p = passes[pd.to_numeric(passes["yards_gained"], errors="coerce").fillna(0) >= EXPLOSIVE_PASS_YARDS]
            exp_r = runs[pd.to_numeric(runs["yards_gained"], errors="coerce").fillna(0) >= EXPLOSIVE_RUSH_YARDS]
            out["defense_allowed"][team] = {
                "pass_attempts_faced": int(len(passes)),
                "explosive_passes_allowed": int(len(exp_p)),
                "p_exp_pass_allowed": float(len(exp_p) / len(passes)) if len(passes) else None,
                "rush_attempts_faced": int(len(runs)),
                "explosive_rushes_allowed": int(len(exp_r)),
                "p_exp_rush_allowed": float(len(exp_r) / len(runs)) if len(runs) else None,
                "status": "OK" if len(passes) + len(runs) >= 30 else "SPARSE",
                "note": "Only plays where this team was defteam in team-filtered rows; if offense-only filter, use games_df",
            }
    return out


def qb_completion_splits(joined: pd.DataFrame) -> dict[str, Any]:
    """Overall + qb_hit PROXY + FTN blitz splits. Never label qb_hit as measured pressure."""
    passes = joined[joined["play_type"] == "pass"].copy()
    out = {"by_passer": {}, "labels": {
        "qb_hit": "PROXY_NOT_MEASURED_PRESSURE",
        "blitz": "FTN_n_blitzers_ge_1_when_joined",
        "true_pressure_charted": "MISSING_in_local_FTN_extract",
    }}
    if passes.empty:
        return out
    for (team, qb), g in passes.groupby(["posteam", "passer_player_name"]):
        if not isinstance(qb, str):
            continue
        def comp(x):
            if len(x) == 0 or "complete_pass" not in x.columns:
                return None, 0
            return float((x["complete_pass"] == 1).mean()), int(len(x))
        c_all, n_all = comp(g)
        hit = g[g.get("qb_hit", 0) == 1] if "qb_hit" in g.columns else g.iloc[0:0]
        nohit = g[g.get("qb_hit", 0) != 1] if "qb_hit" in g.columns else g
        c_hit, n_hit = comp(hit)
        c_nh, n_nh = comp(nohit)
        if "is_blitz_ftn" in g.columns and g["ftn_joined"].any():
            bl = g[g["is_blitz_ftn"] & g["ftn_joined"]]
            nbl = g[(~g["is_blitz_ftn"]) & g["ftn_joined"]]
            c_bl, n_bl = comp(bl)
            c_nbl, n_nbl = comp(nbl)
        else:
            c_bl = n_bl = c_nbl = n_nbl = None
        out["by_passer"][f"{team}:{qb}"] = {
            "n_att": n_all, "comp_pct": c_all,
            "n_qb_hit_proxy": n_hit, "comp_pct_qb_hit_proxy": c_hit,
            "n_no_qb_hit": n_nh, "comp_pct_no_qb_hit": c_nh,
            "n_blitz_ftn": n_bl, "comp_pct_blitz_ftn": c_bl,
            "n_no_blitz_ftn": n_nbl, "comp_pct_no_blitz_ftn": c_nbl,
            "status": "OK" if n_all >= 20 else "SPARSE",
        }
    return out


def recent_form_miss_audit(df: pd.DataFrame, *, last_n_games: int = 3) -> dict[str, Any]:
    """Scenario-first recent form: last N games PPG / explosive — audit only, no auto cut."""
    out = {"label": "SCENARIO_FIRST_MISS_AUDIT_NO_AUTO_CUT", "by_team": {}}
    if "game_id" not in df.columns:
        return out
    for team in ("JAX", "BAL"):
        # approximate: unique games where posteam==team ordered by week
        sub = df[df["posteam"] == team]
        if sub.empty:
            continue
        games = sub.groupby("game_id").agg(week=("week", "first"), plays=("play_id", "count")).sort_values("week")
        recent = games.tail(last_n_games)
        out["by_team"][team] = {
            "recent_game_ids": list(map(str, recent.index)),
            "n_games": int(len(recent)),
            "note": "Not used as automatic veto; scenario cross-check only",
        }
    return out

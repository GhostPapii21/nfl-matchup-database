"""Drive-length / plays-per-game realism vs team W1–8 actuals (development diagnostic)."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Sequence
import numpy as np
import pandas as pd
from simulate import PlayCatalog, simulate_one, build_catalog
from pbp_filter import load_involvement_plays, load_team_history
from adjustments import apply_forward_qb_filter


def actual_combined_snaps_per_game(
    pbp_path: str | Path,
    *,
    teams: Sequence[str],
    season: int,
    weeks: tuple[int, int],
) -> dict[str, Any]:
    """Apples-to-apples: for each involvement game, count pass+run snaps by BOTH offenses."""
    inv = load_involvement_plays(pbp_path, teams=list(teams), season=season, weeks=weeks)
    snaps = inv[inv["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike"])]
    # games involving focus teams
    games = inv.groupby("game_id").agg(
        week=("week", "first"), home=("home_team", "first"), away=("away_team", "first")
    )
    combined = snaps.groupby("game_id").size()
    per_team = snaps[snaps["posteam"].isin(teams)].groupby(["posteam", "game_id"]).size()
    drives = inv[inv["posteam"].isin(teams) & inv["drive"].notna()]
    drive_lens = drives.groupby(["posteam", "game_id", "drive"]).size()
    return {
        "n_games": int(len(combined)),
        "n_team_games": int(len(per_team)),
        "mean_combined_offense_snaps": float(combined.mean()) if len(combined) else None,
        "median_combined_offense_snaps": float(combined.median()) if len(combined) else None,
        "mean_per_team_offense_snaps": float(per_team.mean()) if len(per_team) else None,
        "drive_length_plays": {
            "mean": float(drive_lens.mean()) if len(drive_lens) else None,
            "median": float(drive_lens.median()) if len(drive_lens) else None,
            "n_drives": int(len(drive_lens)),
        },
        "definition": "combined = all pass/run/kneel/spike snaps in games involving listed teams (both offenses)",
    }


def compare_sim_vs_actual_pace(cfg: dict, *, pbp_path: str | Path, n_sims: int = 100, seed: int = 3) -> dict[str, Any]:
    teams = cfg["history"]["teams"]
    weeks = (cfg["history"]["weeks_inclusive"][0], cfg["history"]["weeks_inclusive"][-1])
    actual_combined = actual_combined_snaps_per_game(
        pbp_path, teams=teams, season=cfg["history"]["season"], weeks=weeks
    )
    hist = load_team_history(
        pbp_path, teams=teams, season=cfg["history"]["season"], weeks=weeks,
    )
    df = hist["df"]
    if cfg.get("adjustments", {}).get("enabled"):
        df, _ = apply_forward_qb_filter(df, cfg["adjustments"])
    cat, _prov = build_catalog(df, cfg, games_df=hist.get("games_df"))
    cat.set_empirical_clock(PlayCatalog.build_empirical_clock(df))
    cat.enable_defense_conditioning(True)
    rng = np.random.default_rng(seed)
    snap_counts, punt_counts, td_counts, sparse_rates, drive_lens = [], [], [], [], []
    for _ in range(n_sims):
        st = simulate_one(df, cat, cfg, np.random.default_rng(int(rng.integers(0, 2**31 - 1))))
        n_snap = sum(1 for e in st.events if e.get("type") == "snap")
        snap_counts.append(n_snap)
        punt_counts.append(sum(1 for e in st.events if e.get("type") == "punt"))
        td_counts.append(sum(1 for e in st.events if e.get("type") == "touchdown"))
        ends = sum(1 for e in st.events if e.get("type") in ("punt", "touchdown", "turnover", "turnover_on_downs", "safety", "field_goal", "fg_sparse_miss_default"))
        drive_lens.append(n_snap / max(1, ends))
        sparse_rates.append(1.0 if any("SPARSE" in f or "FALLBACK" in f for f in st.sparse_flags) else 0.0)
    sim = {
        "mean_snaps_per_game": float(np.mean(snap_counts)),
        "median_snaps_per_game": float(np.median(snap_counts)),
        "mean_punts": float(np.mean(punt_counts)),
        "mean_tds": float(np.mean(td_counts)),
        "approx_plays_per_drive": float(np.mean(drive_lens)),
        "drive_note": "approx = snaps / drive-ending events (half-end drives not counted as ends)",
        "sparse_game_rate": float(np.mean(sparse_rates)),
        "n_sims": n_sims,
        "empirical_clock": True,
        "defense_conditioning": True,
    }
    base = actual_combined["mean_combined_offense_snaps"]
    per_team = actual_combined.get("mean_per_team_offense_snaps")
    # Legacy `actual` alias kept for run_period_realism_grade / older tests
    actual_legacy = {
        "mean_offense_snaps_per_team_game": per_team,
        "n_team_games": actual_combined.get("n_team_games"),
        "drive_length_plays": actual_combined.get("drive_length_plays"),
        "note": "per-team offense snaps; prefer actual_combined_offense_snaps for apples-to-apples",
    }
    return {
        "label": "development_in_sample_diagnostic_not_accuracy",
        "actual_combined_offense_snaps": actual_combined,
        "actual": actual_legacy,
        "actual_both_offenses_snaps_approx": (
            (per_team * 2.0) if per_team is not None else None
        ),
        "sim": sim,
        "comparison": {
            "baseline": "combined_offense_snaps_per_involvement_game",
            "sim_minus_actual_combined": (
                sim["mean_snaps_per_game"] - base if base is not None else None
            ),
            "sim_snaps_minus_2x_team_snaps": (
                sim["mean_snaps_per_game"] - (per_team * 2.0)
                if per_team is not None else None
            ),
            "note": "Primary: sim joint snaps vs actual both-offense snaps in involvement games; 2x retained as approx diagnostic only",
        },
    }

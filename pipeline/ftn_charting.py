"""FTN charting already pulled into this checkout. Missing fields stay missing.

The release has ``n_blitzers`` and ``n_pass_rushers``. It does not have
``was_pressure``. A blitz count is not a pressure rate, and a null is not zero.
2026 coverage in this pull stops at week 11, so a week-12 play has no charting row.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

FTN_DIR = Path("data/historical/nflverse/ftn")
COLUMNS = ("nflverse_game_id", "nflverse_play_id", "season", "week", "n_blitzers", "n_pass_rushers", "date_pulled")


def coverage(repo: Path) -> dict:
    seasons = []
    for year in (2024, 2025, 2026):
        path = repo / FTN_DIR / f"ftn_charting_{year}.parquet"
        if not path.is_file():
            seasons.append({"season": year, "status": "UNAVAILABLE", "rows": 0})
            continue
        frame = pd.read_parquet(path, columns=list(COLUMNS))
        weeks = sorted(int(w) for w in frame["week"].dropna().unique())
        seasons.append({
            "season": year,
            "status": "PRESENT",
            "rows": int(len(frame)),
            "weeks": weeks,
            "max_week": weeks[-1] if weeks else None,
            "week_12_rows": int((frame["week"] == 12).sum()),
            "n_blitzers_null": int(frame["n_blitzers"].isna().sum()),
            "n_pass_rushers_null": int(frame["n_pass_rushers"].isna().sum()),
            "date_pulled_max": None if frame["date_pulled"].isna().all() else str(frame["date_pulled"].max()),
            "role": "training" if year < 2026 else "in_season_through_available_week",
        })
    return {
        "schema": "ftn-charting-audit/1",
        "license": "CC BY-SA 4.0",
        "join_keys": ["nflverse_game_id", "nflverse_play_id"],
        "was_pressure": "absent",
        "pressure_filled_with_zero": False,
        "blitz_is_not_pressure": True,
        "seasons": seasons,
        "week_12_2026": "unavailable",
        "projection_ready": False,
    }


def defense_rush_profile(repo: Path, plays: pd.DataFrame, team: str, game: dict) -> dict:
    """Prior-week blitz and four-man rush for one defense. Pressure stays unavailable."""
    season = int(game["season"])
    week = int(game["week"])
    path = repo / FTN_DIR / f"ftn_charting_{season}.parquet"
    unavailable_pressure = {
        "kind": "unavailable",
        "unavailable": True,
        "value": None,
        "evidence_tier": "unavailable",
        "definition": "FTN was_pressure",
        "reason": "The FTN release has no was_pressure column. n_pass_rushers was not used as pressure and nulls were not set to zero.",
    }
    if not path.is_file() or plays is None or plays.empty or "play_id" not in plays.columns:
        return {
            "pressure": unavailable_pressure,
            "rush_four_vs_blitz": {
                "kind": "unavailable",
                "unavailable": True,
                "evidence_tier": "unavailable",
                "reason": "FTN charting or play_id was not available for this join.",
            },
        }
    chart = pd.read_parquet(path, columns=list(COLUMNS))
    chart = chart[(chart["season"] == season) & (chart["week"] < week)]
    side = plays[plays["defteam"] == team][["game_id", "play_id"]].copy()
    side["play_id"] = pd.to_numeric(side["play_id"], errors="coerce")
    chart = chart.rename(columns={"nflverse_game_id": "game_id", "nflverse_play_id": "play_id"})
    merged = side.merge(chart[["game_id", "play_id", "n_blitzers", "n_pass_rushers"]], on=["game_id", "play_id"], how="left")
    both = merged["n_blitzers"].notna() & merged["n_pass_rushers"].notna()
    known = merged[both]
    blitz = int((known["n_blitzers"] > 0).sum()) if len(known) else 0
    rush4 = int(((known["n_pass_rushers"] == 4) & (known["n_blitzers"] == 0)).sum()) if len(known) else 0
    if known.empty:
        rush = {
            "kind": "unavailable",
            "unavailable": True,
            "evidence_tier": "unavailable",
            "joined_rows": 0,
            "missing_rows": int(len(merged)),
            "reason": "No prior-week FTN row joined on nflverse_game_id and nflverse_play_id. Missing rows were not counted as zero blitz.",
        }
    else:
        rush = {
            "kind": "measured",
            "unavailable": False,
            "evidence_tier": "measured",
            "joined_rows": int(len(known)),
            "missing_rows": int((~both).sum()),
            "blitz_plays": blitz,
            "rush_four_not_blitz_plays": rush4,
            "blitz_rate": round(blitz / len(known), 6),
            "rush_four_not_blitz_rate": round(rush4 / len(known), 6),
            "denominator": int(len(known)),
            "definition": "Among joined rows with both n_blitzers and n_pass_rushers present: blitz is n_blitzers > 0; rush-four is four rushers and zero blitzers. Nulls are excluded, not zero.",
            "downgrades_only_this_output": True,
        }
    return {"pressure": unavailable_pressure, "rush_four_vs_blitz": rush}

"""Inventory of sources already in this checkout. Missing files stay unavailable.

Nothing here downloads a feed or fills a blank with zero.
"""
from __future__ import annotations

import csv
from pathlib import Path


SHARP = "data/coverage/sharp_coverage_2026.csv"
BACKTEST = "calibration/simv56/engines/sim_v6_backtest.csv"
GAMES = "data/historical/nflverse/games.csv"
NFL_SCHEDULE = "data/schedule/nfl_official_schedule.json"
NGS = (
    "data/historical/nflverse/ngs_passing.parquet",
    "data/historical/nflverse/ngs_receiving.parquet",
    "data/historical/nflverse/ngs_rushing.parquet",
)
FTN = "data/historical/nflverse/ftn_charting.parquet"


def _csv_inventory(path: Path, role: str) -> dict:
    if not path.is_file():
        return {"path": role, "status": "UNAVAILABLE", "evidence_tier": "unavailable", "reason": "file is not in this checkout"}
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    return {
        "path": role,
        "status": "PRESENT",
        "evidence_tier": "measured",
        "fields": fields,
        "rows": len(rows),
        "bytes": path.stat().st_size,
    }


def inventory(repo: Path) -> dict:
    sharp = _csv_inventory(repo / SHARP, SHARP)
    if sharp["status"] == "PRESENT":
        updated = sorted({row.get("source_updated") or "" for row in csv.DictReader((repo / SHARP).open())})
        pulled = sorted({row.get("pulled_utc") or "" for row in csv.DictReader((repo / SHARP).open())})
        sharp["source_updated_values"] = updated
        sharp["pulled_utc_values"] = pulled
        sharp["joins"] = "team abbreviation to the pregame packet defense. Not a player coverage assignment."
        sharp["not_a_coverage_assignment"] = True
    backtest = _csv_inventory(repo / BACKTEST, BACKTEST)
    if backtest["status"] == "PRESENT":
        weeks = sorted({int(row["week"]) for row in csv.DictReader((repo / BACKTEST).open())})
        backtest["weeks"] = weeks
        backtest["identity"] = "committed sim_v6 W4-7 backtest file, not a new fit"
        backtest["holdout_scorecard"] = None
    games = _csv_inventory(repo / GAMES, GAMES)
    if games["status"] == "PRESENT":
        games["evidence_tier"] = "measured"
        games["authority"] = "nflverse games.csv, not an NFL.com schedule capture"
    ngs = []
    for rel in NGS:
        path = repo / rel
        ngs.append({
            "path": rel,
            "status": "PRESENT" if path.is_file() else "UNAVAILABLE",
            "evidence_tier": "measured" if path.is_file() else "unavailable",
        })
    ftn_path = repo / FTN
    nfl = repo / NFL_SCHEDULE
    return {
        "schema": "sunday-source-inventory/1",
        "projection_ready": False,
        "sharp_coverage": sharp,
        "sim_v6_backtest": backtest,
        "nflverse_games": games,
        "ngs": ngs,
        "ftn_charting": {
            "path": FTN,
            "status": "PRESENT" if ftn_path.is_file() else "UNAVAILABLE",
            "evidence_tier": "unavailable" if not ftn_path.is_file() else "measured",
            "reason": None if ftn_path.is_file() else "no ftn_charting parquet is in this checkout; pressure and coverage charting stay unavailable",
        },
        "nfl_official_schedule": {
            "path": NFL_SCHEDULE,
            "status": "PRESENT" if nfl.is_file() else "UNAVAILABLE",
            "evidence_tier": "unavailable" if not nfl.is_file() else "measured",
            "reason": None if nfl.is_file() else "no offline NFL.com schedule capture with retrieval and as-of metadata",
        },
        "main_adapter": {"status": "UNAVAILABLE", "reason": "no production Main implementation is in this repository"},
        "lightning_adapter": {"status": "UNAVAILABLE", "reason": "no Lightning implementation is in this repository"},
    }

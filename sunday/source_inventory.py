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


def _official_schedule(path: Path) -> dict:
    if not path.is_file():
        return {
            "path": NFL_SCHEDULE,
            "status": "UNAVAILABLE",
            "evidence_tier": "unavailable",
            "pregame_capture": False,
            "reason": "no offline NFL.com schedule capture with retrieval and as-of metadata",
        }
    import json
    body = json.loads(path.read_text())
    note = str(body.get("note") or "")
    return {
        "path": NFL_SCHEDULE,
        "status": "PRESENT",
        "evidence_tier": "measured",
        "games": len(body.get("games") or {}),
        "source": body.get("source"),
        "retrieved_utc": body.get("retrieved_utc"),
        "as_of": body.get("as_of"),
        "announcement_date": body.get("announcement_date"),
        "corroborating_source": body.get("corroborating_source"),
        "pregame_capture": "not a historical pregame capture" not in note.lower(),
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
    from pipeline.ftn_charting import coverage as ftn_coverage
    return {
        "schema": "sunday-source-inventory/1",
        "projection_ready": False,
        "sharp_coverage": sharp,
        "sim_v6_backtest": backtest,
        "nflverse_games": games,
        "ngs": ngs,
        "ftn_charting": ftn_coverage(repo),
        "nfl_official_schedule": _official_schedule(repo / NFL_SCHEDULE),
        "main_adapter": {"status": "UNAVAILABLE", "reason": "no production Main implementation is in this repository"},
        "lightning_adapter": {"status": "UNAVAILABLE", "reason": "no Lightning implementation is in this repository"},
    }

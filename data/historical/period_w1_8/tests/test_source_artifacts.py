"""Real-source checks must not pass vacuously on schema-only CSVs."""
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import polars as pl
import pytest

from test_builder import b

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.source


def load(name):
    with (ROOT / f"data/{name}_w1_8.csv").open() as f:
        return list(csv.DictReader(f))


@pytest.fixture
def real():
    status = json.loads((ROOT / "data/build_status.json").read_text())
    if not status["counts_verified"]:
        pytest.skip("Real schedule/PBP unavailable; see reviews/COUNTS.md (unit fixtures do not establish coverage)")
    return load("games"), load("period_scores"), load("coverage_ledger"), status


def test_source_acquisition_and_complete_coverage():
    status = json.loads((ROOT / "data/build_status.json").read_text())
    assert status["status"] == "COMPLETE", f"Actual coverage not complete: {status['status']}; see reviews/COUNTS.md"


def test_exact_completed_schedule_count(real):
    games, _, ledger, status = real
    manifest = json.loads((ROOT / "data/raw/manifest.json").read_text())
    item = manifest["fetches"]["schedules"]
    path = ROOT / "data/raw" / item["file"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
    source = pl.read_parquet(path).to_dicts()
    expected = {s["game_id"] for s in source if b.completed(s, datetime.fromisoformat(status["as_of_utc"]))}
    assert len(games) == len(expected) > 0
    assert {g["game_id"] for g in games} == expected == {l["game_id"] for l in ledger}
    assert status["expected_completed_games"] == len(expected)


def test_no_future_week_and_32_teams(real):
    games, _, _, _ = real
    assert all(int(g["season"]) == 2026 and 1 <= int(g["week"]) <= 8 for g in games)
    assert len({g[side] for g in games for side in ("home", "away")}) == 32


def test_periods_sum_and_ot_flag(real):
    games, periods, ledger, _ = real
    by_game = defaultdict(dict)
    for row in periods:
        assert row["period"] not in by_game[row["game_id"]]
        by_game[row["game_id"]][row["period"]] = row
    assert len(periods) == 8 * len(games)
    for g in games:
        p = by_game[g["game_id"]]
        assert set(p) == set(b.PERIODS)
        assert all(r["status"] == "PRESENT" for r in p.values())
        for side, score in (("home", "home_score"), ("away", "away_score")):
            get = lambda period: int(p[period][f"{side}_pts"])
            assert sum(get(q) for q in ("Q1", "Q2", "Q3", "Q4", "OT")) == int(g[score])
            assert get("H1") == get("Q1") + get("Q2")
            assert get("H2") == get("Q3") + get("Q4")
            assert get("REG") + get("OT") == int(g[score])
            assert int(p["OT"][f"cumulative_{side}"]) == int(g[score])
        assert g["overtime"] in ("True", "False")
        if g["overtime"] == "False": assert (get("OT"), int(p["OT"]["home_pts"])) == (0, 0)
    manifest = json.loads((ROOT / "data/raw/manifest.json").read_text())
    pbp = pl.read_parquet(ROOT / "data/raw" / manifest["fetches"]["pbp"]["file"])
    observed = set(pbp.filter(pl.col("qtr") > 4)["game_id"].to_list())
    built_ids = {g["game_id"] for g in games}
    assert {g["game_id"] for g in games if g["overtime"] == "True"} == observed & built_ids


def test_source_and_market_honesty(real):
    games, _, ledger, _ = real
    assert all(g["source"] == b.SOURCE for g in games)
    for row in ledger:
        assert row["pff_overview"] == "MISSING" and row["pff_source"] == ""
        assert row["pff_attempt_status"] == "NOT_ATTEMPTED"
        assert row["market_spread_grade"] == row["market_total_grade"] == "NOLINE"
        assert row["spread_result_home"] == row["total_result"] == ""
        assert row["market_missing_reason"] == "NO_VERIFIED_CLOSER_QUOTE"
        assert row["quote_source"] == b.URLS["schedules"]
        assert row["quote_timestamp"] == "" and row["quote_verified_closer"] == "False"

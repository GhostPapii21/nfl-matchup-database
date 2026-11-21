"""NFL-10 / NFL-47: source freshness is judged from the publisher's own update / data-through stamps, never from
when we fetched it; repeated gap rows are deduplicated; coverage/NGS/FTN effects stay disabled without an
authorized, verified source; the ledger is written into the package inventory."""
import json, sqlite3
from pathlib import Path

import source_gap_ledger as L

ROOT = Path(__file__).resolve().parent


def _db(rows_fetch, rows_gap, games=(("g1", "2026-10-26", "STATUS_FINAL"),)):
    c = sqlite3.connect(":memory:")
    c.executescript("""
      CREATE TABLE games(game_id TEXT PRIMARY KEY,date TEXT,status TEXT,data TEXT);
      CREATE TABLE external_fetches(fetch_id TEXT PRIMARY KEY,source_id TEXT,source_url TEXT,retrieved_at TEXT,source_updated_at TEXT,status TEXT,raw_hash TEXT,raw_path TEXT,detail TEXT);
      CREATE TABLE external_gaps(gap_id TEXT PRIMARY KEY,source_id TEXT,observed_at TEXT,reason TEXT,data TEXT);""")
    c.executemany("INSERT INTO games VALUES(?,?,?,'{}')", games)
    c.executemany("INSERT INTO external_fetches VALUES(?,?,?,?,?,?,NULL,NULL,NULL)", rows_fetch)
    c.executemany("INSERT INTO external_gaps VALUES(?,?,?,?,?)", rows_gap)
    return c


def test_fresh_fetch_of_old_publisher_data_is_stale():
    # Fetched today, but the publisher last updated before the latest final game: STALE.
    c = _db([("f1", "s", "u", "2026-11-21T12:00:00+00:00", "2026-10-20T13:38:00+00:00", "OK")], [])
    row = L.build(c)["sources"][0]
    assert row["freshness"] == "STALE_SOURCE_UPDATED_BEFORE_LAST_FINAL"
    assert row["freshness_basis"] == "source_updated_at"


def test_old_fetch_of_current_publisher_data_is_not_stale():
    c = _db([("f1", "s", "u", "2026-10-27T05:00:00+00:00", "2026-10-27T13:34:45+00:00", "OK")], [])
    row = L.build(c)["sources"][0]
    assert row["freshness"] == "UPDATED_AFTER_LAST_FINAL"
    assert row["data_through"] == "unknown"  # an update stamp is not a stated data-through cutoff


def test_missing_publisher_stamp_is_unknown_never_fresh():
    c = _db([("f1", "s", "u", "2026-11-21T12:00:00+00:00", None, "OK")], [])
    assert L.build(c)["sources"][0]["freshness"] == "UNKNOWN_NO_SOURCE_TIMESTAMP"


def test_fetch_error_latest_is_reported():
    c = _db([("f1", "s", "u", "2026-10-27T05:00:00+00:00", None, "FETCH_ERROR")], [])
    row = L.build(c)["sources"][0]
    assert row["latest_fetch_status"] == "FETCH_ERROR"
    assert row["freshness"] == "UNKNOWN_NO_SOURCE_TIMESTAMP"


def test_newest_publisher_stamp_wins_not_newest_fetch():
    c = _db([("f1", "s", "u", "2026-10-27T05:00:00+00:00", "2026-10-27T13:34:45+00:00", "OK"),
             ("f2", "s", "u", "2026-10-28T05:00:00+00:00", "2026-10-20T00:00:00+00:00", "OK")], [])
    row = L.build(c)["sources"][0]
    assert row["source_updated_at"] == "2026-10-27T13:34:45+00:00"


def test_gaps_deduplicated_by_source_and_reason():
    gaps = [(f"g{i}", "s", f"2026-10-2{i}T00:00:00+00:00", "FRESHNESS_STALE", "{}") for i in range(5)]
    gaps.append(("x", "s", "2026-10-25T00:00:00+00:00", "FETCH_ERROR", "{}"))
    c = _db([("f1", "s", "u", "2026-10-27T05:00:00+00:00", None, "OK")], gaps)
    out = L.build(c)
    g = {(r["source_id"], r["reason"]): r for r in out["gaps"]}
    assert len(out["gaps"]) == 2
    assert g[("s", "FRESHNESS_STALE")]["occurrences"] == 5
    assert g[("s", "FRESHNESS_STALE")]["first_observed_at"] == "2026-10-20T00:00:00+00:00"
    assert g[("s", "FRESHNESS_STALE")]["last_observed_at"] == "2026-10-24T00:00:00+00:00"
    assert out["raw_gap_rows"] == 6


def test_coverage_effects_disabled_without_authorized_verified_source():
    c = _db([], [])
    cov = L.build(c)["coverage_family"]
    assert cov and all(r["effects_enabled"] is False for r in cov)
    names = {r["family"] for r in cov}
    for need in ("FTN charting", "NGS coverage responsibility", "PFF coverage"):
        assert any(need in n for n in names)


def test_effects_enable_requires_both_authorized_and_verified():
    assert L.effects_enabled({"authorized": True, "verified": False}) is False
    assert L.effects_enabled({"authorized": False, "verified": True}) is False
    assert L.effects_enabled({"authorized": True, "verified": True}) is True


def test_committed_ledger_matches_database():
    p = ROOT / "inventory/SOURCE_GAP_LEDGER.json"
    committed = json.loads(p.read_text())
    fresh = L.build(L.open_db(ROOT / "nfl_matchups.sqlite.gz"))
    assert committed == fresh, "run: python3 source_gap_ledger.py --write"

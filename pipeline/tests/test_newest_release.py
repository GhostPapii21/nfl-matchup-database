"""Newest-release freshness rule (Rico 2026-11-22): latest asset + completed-game coverage.

GAP is distinct from STALE. NWS is current if updateTime matches the live grid. Live sources keep
pull-time windows. Inactives keep T-90. Public NGS matchup fields that do not exist are MISSING/unknown, not zero.
"""
from datetime import timedelta, timezone
from pathlib import Path

import pytest

from pipeline import coverage, freshness as F, ngs_matchup
from pipeline.tests.test_pipeline import KO, iso, packet
from pipeline.tests.test_source_asof import rows


@pytest.fixture(autouse=True)
def _isolate_committed_inactives(tmp_path_factory, monkeypatch):
    """Hermetic: committed phase15/inactives evidence must not leak into these tests."""
    from phase15 import official_inactives as _OI
    monkeypatch.setattr(_OI, "OUT", tmp_path_factory.mktemp("no_inactives"))


def test_cadence_table_covers_every_policy_and_hooked_source():
    from pipeline import cadence
    assert set(F.POLICY) <= set(cadence.CADENCE)
    assert set(F.HOOKED) <= set(cadence.HOOKED_CADENCE)
    assert cadence.rule_for("snap_counts") == "latest_release"
    assert cadence.rule_for("news_injuries") == "live_window"
    assert cadence.rule_for("weather") == "nws_live_grid"
    assert cadence.rule_for("official_inactives") == "t90"
    assert cadence.coverage_for("pfr_defense") == "completed_games"
    assert cadence.coverage_for("rosters") is None


def test_latest_release_old_stamp_is_fresh_not_stale():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    pk["sources"]["snap_counts"]["source_updated_at"] = iso(now - timedelta(hours=50))
    r = rows(pk, now)["snap_counts"]
    assert r["status"] == "FRESH" and r["cadence"] == "latest_release"
    assert r["age_minutes"] == pytest.approx(50 * 60, abs=0.1)


def test_latest_release_superseded_by_newer_asset_is_stale():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    del pk["sources"]["snap_counts"]["source_updated_at"]
    asof = {"snap_counts": {"source_updated_at": None, "as_of_basis": "UNKNOWN_NO_SOURCE_TIMESTAMP",
                            "reason": "asset was re-published after our pull; our copy is superseded and its publish time is unknown",
                            "evidence": {"api": "https://api.github.com/repos/nflverse/nflverse-data/releases/tags/snap_counts"}}}
    r = rows(pk, now, source_asof=asof)["snap_counts"]
    assert r["status"] == "STALE" and "not the latest published asset" in r["reason"]
    assert "superseded" in r["reason"]
    assert r in F.blocking([r])


def test_latest_release_missing_completed_game_is_gap_not_stale():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    completed = lambda p: [{"game_id": "2026_11_IND_HOU", "week": 11, "teams": ["IND", "HOU"]}]

    def cov(name, rec, p):
        if name == "pfr_defense":
            return {"has_game_id": True, "game_ids": {"2026_10_WAS_NYG"}, "has_week_team": False,
                    "weeks": set(), "week_teams": set(), "columns": ["game_id"]}
        return None

    r = rows(pk, now, completed_games=completed, source_coverage=cov)["pfr_defense"]
    assert r["status"] == "GAP" and "2026_11_IND_HOU" in r["reason"]
    assert r["status"] != "STALE"
    assert r in F.blocking([r])


def test_latest_release_with_all_completed_games_is_fresh():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    completed = lambda p: [{"game_id": "2026_10_WAS_NYG", "week": 10, "teams": ["WAS", "NYG"]}]
    cov = lambda name, rec, p: {"has_game_id": True, "game_ids": {"2026_10_WAS_NYG"}, "has_week_team": False,
                                "weeks": set(), "week_teams": set(), "columns": ["game_id"]}
    r = rows(pk, now, completed_games=completed, source_coverage=cov)["snap_counts"]
    assert r["status"] == "FRESH"


def test_nws_old_update_time_is_fresh_when_it_matches_the_grid():
    now = KO - timedelta(hours=2)  # would have been STALE under the old 90 min / 3 h / 6 h clocks
    pk = packet(now)
    pk["weather"]["source_updated_at"] = iso(now - timedelta(hours=10))
    r = rows(pk, now)["weather"]
    assert r["status"] == "FRESH" and r["cadence"] == "nws_live_grid"
    assert r["age_minutes"] == pytest.approx(10 * 60, abs=0.1)


def test_nws_superseded_grid_is_not_fresh():
    now = KO - timedelta(hours=2)
    pk = packet(now)
    del pk["weather"]["source_updated_at"]
    asof = {"weather": {"source_updated_at": None, "as_of_basis": "UNKNOWN_NO_SOURCE_TIMESTAMP",
                        "reason": "forecast regenerated after our pull; our copy's issue time is unknown",
                        "evidence": {"url": "https://api.weather.gov/gridpoints/PHI/50,76/forecast/hourly"}}}
    r = rows(pk, now, source_asof=asof)["weather"]
    assert r["status"] == "STALE" and "regenerated after our pull" in r["reason"]


def test_live_windows_still_apply_to_odds_espn_and_schedule():
    now = KO - timedelta(hours=1)
    pk = packet(now - timedelta(minutes=50))  # 50 min old pull; odds limit is 20, news is 45
    rr = rows(pk, now)
    assert rr["odds"]["status"] == "STALE" and rr["odds"]["cadence"] == "live_window"
    assert rr["news_injuries"]["status"] == "STALE"  # 45 min limit inside 2 h
    assert rr["schedule"]["status"] == "FRESH"  # 24 h window, 50 min old
    # schedule 25 h old is STALE
    pk2 = packet(now)
    pk2["sources"]["games"]["source_updated_at"] = iso(now - timedelta(hours=25))
    assert rows(pk2, now)["schedule"]["status"] == "STALE"


def test_inactives_t90_unchanged():
    now = KO - timedelta(hours=3)
    assert rows(packet(now), now)["official_inactives"]["status"] == "NOT_YET"
    now2 = KO - timedelta(minutes=60)
    assert rows(packet(now2), now2)["official_inactives"]["status"] == "MISSING"


def test_blocking_includes_gap_and_not_fresh():
    rows_ = [
        {"source": "a", "status": "FRESH", "reason": "ok"},
        {"source": "b", "status": "GAP", "reason": "missing game"},
        {"source": "c", "status": "NOT_REQUIRED", "reason": "indoor"},
    ]
    bad = F.blocking(rows_)
    assert [r["source"] for r in bad] == ["b"]


def test_ngs_sources_are_in_the_gate():
    now = KO - timedelta(hours=30)
    rr = rows(packet(now), now)
    for s in ("ngs_passing", "ngs_receiving", "ngs_rushing"):
        assert s in F.POLICY and rr[s]["status"] == "FRESH" and rr[s]["cadence"] == "latest_release"
    assert "ngs_defender_matchup" in rr


def test_ngs_defender_check_lists_wanted_fields_missing_not_zero():
    inv = ngs_matchup.field_inventory({})
    wanted = {m["field"] for m in inv["missing"] if m.get("source") == "public_ngs"}
    assert wanted == set(ngs_matchup.WANTED)
    assert all(m["status"] == "MISSING" and m["value"] == "unknown" for m in inv["missing"] if m.get("source") == "public_ngs")
    assert all(m.get("value") != 0 and m.get("value") != "0" for m in inv["missing"])
    # public aggregates are listed as available in the dictionary
    avail = {a["field"] for a in inv["available"]}
    assert "avg_separation" in avail and "completion_percentage_above_expectation" in avail
    assert "rush_yards_over_expected" in avail


def test_ngs_defender_row_missing_without_files_does_not_invent_zeros():
    now = KO - timedelta(hours=30)
    r = rows(packet(now), now)["ngs_defender_matchup"]
    ev = r["as_of_evidence"] or {}
    missing = [m for m in (ev.get("fields") or {}).get("missing", []) if m.get("source") == "public_ngs"]
    assert missing and all(m["value"] == "unknown" for m in missing)
    assert "route" in r["reason"].lower() or "MISSING" in r["reason"]


def test_ngs_coverage_gap_for_a_completed_week_team(tmp_path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    week = pa.array([10, 10], type=pa.int32())
    team = pa.array(["WAS", "NYG"])
    t = pa.table({"week": week, "team_abbr": team, "player_display_name": ["A", "B"],
                  "avg_separation": [0.1, 0.2]})
    path = tmp_path / "ngs_receiving.parquet"
    pq.write_table(t, path)
    found = coverage.ids_in_file(path)
    completed = [{"game_id": "2026_11_IND_HOU", "week": 11, "teams": ["IND", "HOU"]}]
    assert coverage.missing_completed(completed, found) == ["week 11"]
    now = KO - timedelta(hours=30)
    pk = packet(now)
    pk["sources"]["ngs_receiving"]["path"] = str(path)
    r = rows(pk, now, completed_games=lambda p: completed,
             source_coverage=lambda name, rec, p: found if name.startswith("ngs_") else None)["ngs_receiving"]
    assert r["status"] == "GAP" and "week 11" in r["reason"]


def test_coverage_completed_games_from_schedule_scores(tmp_path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    t = pa.table({
        "game_id": ["2026_11_IND_HOU", "2026_11_PIT_PHI"],
        "week": pa.array([11, 11], type=pa.int32()),
        "season": pa.array([2026, 2026], type=pa.int32()),
        "away_team": ["IND", "PIT"],
        "home_team": ["HOU", "PHI"],
        "away_score": pa.array([16, None], type=pa.int32()),
        "home_score": pa.array([20, None], type=pa.int32()),
    })
    path = tmp_path / "games.parquet"
    pq.write_table(t, path)
    got = coverage.completed_games_from_schedule(path)
    assert len(got) == 1 and got[0]["game_id"] == "2026_11_IND_HOU"
    assert got[0]["teams"] == ["IND", "HOU"]



def test_ngs_defender_row_is_missing_when_no_public_ngs_records():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    for k in ("ngs_passing", "ngs_receiving", "ngs_rushing"):
        del pk["sources"][k]
    r = rows(pk, now)["ngs_defender_matchup"]
    assert r["status"] == "MISSING"
    ev = r["as_of_evidence"] or {}
    missing = [m for m in (ev.get("fields") or {}).get("missing", []) if m.get("source") == "public_ngs"]
    assert {m["field"] for m in missing} == set(ngs_matchup.WANTED)
    assert all(m["value"] == "unknown" for m in missing)
    assert r in F.blocking([r])


def test_coverage_unknown_is_not_invented_as_a_gap():
    # No schedule file, no hook: cannot assert a gap.
    assert coverage.missing_completed(None, {"has_game_id": True, "game_ids": set(), "has_week_team": False,
                                             "weeks": set(), "week_teams": set(), "columns": []}) == []
    assert coverage.missing_completed([{"game_id": "x"}], None) == []


def test_completed_games_filtered_to_packet_season(tmp_path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    t = pa.table({
        "game_id": ["2025_11_IND_HOU", "2026_11_IND_HOU", "2026_11_PIT_PHI"],
        "week": pa.array([11, 11, 11], type=pa.int32()),
        "season": pa.array([2025, 2026, 2026], type=pa.int32()),
        "game_type": ["REG", "REG", "REG"],
        "away_team": ["IND", "IND", "PIT"],
        "home_team": ["HOU", "HOU", "PHI"],
        "away_score": pa.array([16, 16, None], type=pa.int32()),
        "home_score": pa.array([20, 20, None], type=pa.int32()),
    })
    path = tmp_path / "games.parquet"
    pq.write_table(t, path)
    all_seasons = coverage.completed_games_from_schedule(path)
    assert {g["game_id"] for g in all_seasons} == {"2025_11_IND_HOU", "2026_11_IND_HOU"}
    only_2026 = coverage.completed_games_from_schedule(path, season=2026, season_type="REG")
    assert [g["game_id"] for g in only_2026] == ["2026_11_IND_HOU"]


def test_ngs_same_week_in_another_season_is_not_coverage(tmp_path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    t = pa.table({
        "week": pa.array([11, 11], type=pa.int32()),
        "season": pa.array([2025, 2025], type=pa.int32()),
        "team_abbr": ["IND", "HOU"],
        "player_display_name": ["A", "B"],
        "avg_separation": [0.1, 0.2],
    })
    path = tmp_path / "ngs_receiving.parquet"
    pq.write_table(t, path)
    found = coverage.ids_in_file(path)
    completed = [{"game_id": "2026_11_IND_HOU", "season": 2026, "week": 11, "teams": ["IND", "HOU"]}]
    miss = coverage.missing_completed(completed, found)
    assert miss == ["week 11 (2026)"]


def test_ngs_partial_team_list_for_a_published_week_is_not_a_gap(tmp_path):
    """Public NGS omits some team-weeks (minimums; LA vs LAR). The week is still covered."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    t = pa.table({
        "week": pa.array([11, 11], type=pa.int32()),
        "season": pa.array([2026, 2026], type=pa.int32()),
        "team_abbr": ["IND", "LAR"],
        "player_display_name": ["A", "B"],
        "avg_time_to_throw": [2.5, 2.6],
    })
    path = tmp_path / "ngs_passing.parquet"
    pq.write_table(t, path)
    found = coverage.ids_in_file(path)
    completed = [{"game_id": "2026_11_IND_HOU", "season": 2026, "week": 11, "teams": ["IND", "HOU"]},
                 {"game_id": "2026_11_SF_LA", "season": 2026, "week": 11, "teams": ["SF", "LA"]}]
    assert coverage.missing_completed(completed, found) == []

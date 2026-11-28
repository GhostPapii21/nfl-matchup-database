"""The Nov 29 acceptance gaps: joined inputs, sim_v6 refusal, and a local job store."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sunday.joinflow import build_joined_decision_input, hashes_match
from sunday.jobs import JobStore
from sunday.player_board import _situational_block
from sunday.script_models import _scoring_conservation
from tools.sim_v6 import acceptance_receipt, bias_status


def test_pressure_proxy_is_inferred_and_coverage_stays_unavailable():
    block = _situational_block({"pressure_targets": 2, "team_pressure_targets": 4})
    assert block["pressure_targets"]["evidence_tier"] == "inferred"
    assert block["pressure_targets"]["charting"] == "unavailable"
    assert block["coverage_route_access"]["evidence_tier"] == "unavailable"
    empty = _situational_block(None)
    assert empty["coverage_route_access"]["evidence_tier"] == "unavailable"
    assert empty["pressure_targets"]["evidence_tier"] == "unavailable"


def test_touchdown_conservation_is_measured_only_from_the_box():
    missing = _scoring_conservation(None)
    assert missing["status"] == "UNAVAILABLE"
    assert missing["evidence_tier"] == "unavailable"
    measured = _scoring_conservation({
        "reconciliation": {"failures": 0, "trials": 4, "checks": ["off_td_eq_engine_td_events"]},
    })
    assert measured["status"] == "MEASURED"
    assert measured["failures"] == 0


def test_sim_v6_nine_cell_run_is_refused_without_a_fallback():
    receipt = acceptance_receipt()
    assert receipt["status"] == "REFUSED"
    assert receipt["trials_executed"] == 0
    assert receipt["trials_required"] == 900_000
    assert receipt["cells_required"] == 9
    assert receipt["fallback_used"] is False
    assert receipt["scripts_in_recovered_source"] == []
    assert receipt["methods_in_recovered_source"] == ["mc", "bias", "gr"]
    assert receipt["projection_ready"] is False
    assert bias_status(None)["status"] == "REFUSED"
    assert bias_status({"multipliers": {"bias": {}}})["calibration_status"] == "EXPERIMENTAL_UNVALIDATED"
    assert bias_status({"holdout_scorecard": {"as_of": "2026-11-01"}})["status"] == "READY"


def test_joined_packet_keeps_hashes_and_blocks_a_late_as_of():
    assert hashes_match({"research": "a"}, {"research": "b"}) is False
    packet = build_joined_decision_input(
        game={"game_id": "2026_12_DEN_PIT", "home": "PIT", "away": "DEN"},
        kickoff_utc="2026-11-29T18:00:00+00:00",
        kickoff_verification="VERIFIED",
        as_of=datetime(2026, 11, 30, tzinfo=timezone.utc),
        research={"game_id": "2026_12_DEN_PIT"},
        script={"models": []},
        players={
            "player_count": 1,
            "teams": [{
                "players": [{
                    "player": "Bo Nix",
                    "pos": "QB",
                    "projections": {},
                    "situational": {
                        "pressure_targets": {"evidence_tier": "inferred"},
                        "coverage_route_access": {"evidence_tier": "unavailable"},
                    },
                }],
            }],
        },
        market_packet={},
        hashes={"research": "abc", "script": "def", "player_board": "ghi"},
        base_packet={"theses": [], "lines": []},
    )
    assert packet["projection_ready"] is False
    assert any("after the authoritative kickoff" in item for item in packet["joined"]["problems"])
    thesis = packet["theses"][0]
    assert thesis["subject"] == "Bo Nix"
    assert thesis["joined_evidence"]["coverage_assignment"]["evidence_tier"] == "unavailable"
    assert thesis["joined_evidence"]["pressure_targets"]["evidence_tier"] == "inferred"
    assert thesis["sample_quality"]["blocks_reads"] is True


def test_sources_locks_and_the_replacement_are_not_sim_v6():
    from sunday.lock_ledger import ledger
    from sunday.replacement_triad import empirical_cell, receipt, walk_forward
    from sunday.source_inventory import inventory
    repo = Path(__file__).resolve().parents[2]
    sources = inventory(repo)
    assert sources["nfl_official_schedule"]["status"] == "PRESENT"
    assert sources["nfl_official_schedule"]["pregame_capture"] is False
    assert sources["sharp_coverage"]["rows"] > 0
    assert sources["sharp_coverage"]["not_a_coverage_assignment"] is True
    assert sources["ftn_charting"]["was_pressure"] == "absent"
    assert sources["ftn_charting"]["week_12_2026"] == "unavailable"
    assert sources["main_adapter"]["status"] == "UNAVAILABLE"
    scored = walk_forward(repo)
    assert scored["rows"] == 1096
    assert scored["refit"] is False
    assert max(scored["weeks"]) <= 7
    locks_before = (repo / "snapshots" / "2026_12_DEN_PIT" / "20261127T111648Z" / "LOCK.json").read_bytes()
    book = ledger(repo)
    assert book["locks_rewritten"] is False
    assert book["new_locks_created"] == 0
    assert book["games"] == 16
    assert book["previously_scored_count"] == 14
    assert book["training_rows_are_locks"] is False
    assert book["training_game_rows"] > 0
    from pipeline.ftn_charting import coverage, defense_rush_profile
    import pandas as pd
    chart = coverage(repo)
    season_2026 = next(row for row in chart["seasons"] if row["season"] == 2026)
    assert season_2026["max_week"] == 11
    assert season_2026["week_12_rows"] == 0
    assert chart["was_pressure"] == "absent"
    assert chart["pressure_filled_with_zero"] is False
    blank = defense_rush_profile(repo, pd.DataFrame({"game_id": ["g"], "play_id": [1], "defteam": ["DEN"]}), "DEN", {"season": 2026, "week": 12})
    assert blank["pressure"]["value"] is None
    assert book["games"] >= 1
    assert all(row["rewritten"] is False for row in book["rows"])
    assert (repo / "snapshots" / "2026_12_DEN_PIT" / "20261127T111648Z" / "LOCK.json").read_bytes() == locks_before
    cell = empirical_cell([1.0, -2.0, 4.0], seed=1, n=100_000)
    assert cell["trials_executed"] == 100_000
    assert cell["scripts_assigned"] is False
    assert cell["not_sim_v6"] is True
    body = receipt(repo, season=2026, week=12)
    assert body["not_sim_v6"] is True
    assert body["schema"] == "sunday-replacement-triad/1"
    possession = next(row for row in body["methods"] if row["identity"] == "core.possession_engine_v0")
    assert possession["trials_executed"] == 0
    assert possession["committed_benchmark"]["runtime_sec"] == 819.2


def test_ngs_file_read_stops_before_week_12_and_scheduler_runs():
    from sunday.jobs import research_handler
    from sunday.ngs_verify import verify
    from sunday.td_outputs import collect
    repo = Path(__file__).resolve().parents[2]
    ngs = verify(repo)
    assert ngs["projection_ready"] is False
    assert ngs["certification"] is False
    assert ngs["feeds"]["passing"]["max_week_2026"] == 9
    assert ngs["feeds"]["passing"]["week_12_rows"] == 0
    assert "route" in ngs["feeds"]["passing"]["fields_absent"]
    script = Path(repo / "sunday" / "tests" / "_td_fixture")
    branch = script / "branches" / "possession_engine_v0"
    branch.mkdir(parents=True)
    (branch / "favorite_controls.json").write_text(json.dumps({
        "engine_id": "possession_engine_v0",
        "branch": "favorite_controls",
        "n_trials": 24,
        "players": [{
            "team": "DEN",
            "player": "Bo Nix",
            "td_opportunity": {"pass_td": {"mean": 1.5}, "rush_td": {"mean": 0.2}},
        }],
    }))
    try:
        td = collect(script)
    finally:
        import shutil
        shutil.rmtree(script)
    assert td["players_with_pass_td"] == 1
    assert td["players_with_rush_td"] == 1
    assert td["pooled"] is False
    store = JobStore(Path(repo / "sunday" / "tests" / "_jobs.sqlite"))
    try:
        now = datetime(2026, 11, 28, 12, tzinfo=timezone.utc)
        store.enqueue(game_id="2026_12_DEN_PIT", window="research", idempotency_key="den-research")
        outcomes = store.dispatch(research_handler(repo), now)
    finally:
        store.close()
        Path(repo / "sunday" / "tests" / "_jobs.sqlite").unlink(missing_ok=True)
    assert outcomes[0]["status"] == "done"
    assert "projection_ready=false" in outcomes[0]["result"]
    assert "ngs_2026_max_week=9" in outcomes[0]["result"]
    assert "certification=false" in outcomes[0]["result"]


def test_dispatch_isolates_a_failure_and_marks_a_missed_deadline(tmp_path):
    store = JobStore(tmp_path / "jobs.sqlite")
    now = datetime(2026, 11, 29, 18, tzinfo=timezone.utc)
    store.enqueue(
        game_id="2026_12_LATE", window="pregame", idempotency_key="late",
        deadline=now - timedelta(minutes=5),
    )
    store.enqueue(game_id="2026_12_BAD", window="pregame", idempotency_key="bad")
    store.enqueue(game_id="2026_12_OK", window="pregame", idempotency_key="ok")

    def handler(job):
        if job["game_id"] == "2026_12_BAD":
            raise RuntimeError("handler failed")
        return "ran"

    outcomes = store.dispatch(handler, now)
    by_key = {row["idempotency_key"]: row for row in outcomes}
    assert by_key["late"]["status"] == "missed"
    assert by_key["bad"]["status"] == "failed"
    assert by_key["ok"]["status"] == "done"
    assert "handler failed" in by_key["bad"]["result"]
    store.close()


def test_job_store_is_idempotent_and_recovers_a_crashed_lease(tmp_path):
    store = JobStore(tmp_path / "jobs.sqlite")
    now = datetime(2026, 11, 29, 16, tzinfo=timezone.utc)
    first = store.enqueue(game_id="2026_12_DEN_PIT", window="pregame", idempotency_key="DENPIT:pregame")
    second = store.enqueue(game_id="2026_12_DEN_PIT", window="pregame", idempotency_key="DENPIT:pregame")
    assert second["duplicate"] is True
    assert second["idempotency_key"] == first["idempotency_key"]
    leased = store.claim("worker-a", now, lease_seconds=30)
    assert leased["status"] == "leased"
    assert store.recover_expired(now + timedelta(seconds=31)) == 1
    again = store.claim("worker-b", now + timedelta(seconds=31), lease_seconds=30)
    assert again["attempts"] == 2
    assert again["lease_owner"] == "worker-b"
    done = store.complete(again["idempotency_key"], "worker-b")
    assert done["status"] == "done"
    assert done["projection_ready"] is False
    store.lock_inactives("2026_12_DEN_PIT", now)
    refused = store.enqueue(
        game_id="2026_12_DEN_PIT", window="inactive_refresh", idempotency_key="DENPIT:inactive",
    )
    assert refused["status"] == "REFUSED"
    store.close()

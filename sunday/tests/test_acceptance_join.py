"""The Nov 29 acceptance gaps: joined inputs, sim_v6 refusal, and a local job store."""
from datetime import datetime, timedelta, timezone

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

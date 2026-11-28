"""The one Sunday path calls the registered components and does not relabel a refusal as a run."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from sunday import kickoff, stack  # noqa: E402

AS_OF = datetime(2026, 11, 29, 12, 0, tzinfo=timezone.utc)
THREE = {
    "2026_12_LV_CLE": "2026-11-30T01:20:00+00:00",
    "2026_12_TEN_JAX": "2026-11-29T18:00:00+00:00",
    "2026_12_NE_LAC": "2026-11-29T21:05:00+00:00",
}


@pytest.mark.parametrize("game_id,agreed", list(THREE.items()))
def test_official_schedule_is_canonical_and_not_a_pregame_capture(game_id, agreed):
    paths = list((ROOT / "core/possession_engine_v0/config").glob("*2026-11-29_data_only_nfl43.json"))
    snapshots = {p: p.read_bytes() for p in paths}
    packet = json.loads((ROOT / "pregame" / "packets" / game_id / "packet.json").read_text())
    got = kickoff.resolve(ROOT, game_id, packet)
    assert got["authoritative_source"] == "nfl_official_schedule"
    assert got["authoritative_status"] == "OK"
    assert got["verification"] == "VERIFIED"
    assert got["resolved"] is True
    assert got["source"] == "nfl_official_schedule"
    assert got["canonical_kickoff_utc"] == agreed
    assert got["pregame_capture"] is False
    assert got["capture_before_this_kickoff"] is True
    assert got["originals"]["espn_event_date"]["kickoff_utc"] == agreed
    assert got["originals"]["possession_config"]["kickoff_utc"] == agreed
    assert got["originals"]["nflverse_games_csv"]["kickoff_utc"] != agreed
    assert any({row["left"], row["right"]} == {"nflverse_games_csv", "nfl_official_schedule"} for row in got["conflicts"])
    assert got["config_file_rewritten"] is False
    for path, raw in snapshots.items():
        assert path.read_bytes() == raw


def test_nfl_schedule_capture_is_the_only_canonical_clock(tmp_path):
    capture = tmp_path / "nfl_official_schedule.json"
    capture.write_text(json.dumps({
        "source": "https://www.nfl.com/schedules/2026/by-week/week-12",
        "retrieved_utc": "2026-11-28T12:00:00+00:00",
        "as_of": "2026-11-28T12:00:00+00:00",
        "games": {"2026_12_LV_CLE": "2026-11-30T01:20:00+00:00"},
    }))
    packet = json.loads((ROOT / "pregame" / "packets" / "2026_12_LV_CLE" / "packet.json").read_text())
    got = kickoff.resolve(ROOT, "2026_12_LV_CLE", packet, nfl_schedule_path=capture)
    assert got["verification"] == "VERIFIED"
    assert got["source"] == "nfl_official_schedule"
    assert got["canonical_kickoff_utc"] == "2026-11-30T01:20:00+00:00"
    assert any(row["left"] == "nflverse_games_csv" for row in got["conflicts"])


def test_blocked_component_is_not_executed_or_pass(tmp_path):
    rows = [
        stack._row("schedule", "sunday.kickoff", "resolve", "identity", "EXECUTED", "ok",
                   AS_OF, AS_OF, [], []),
        stack._row("orchestrator", "pipeline.orchestrator.runner", "run_games", "orchestration", "REFUSED",
                   "freshness", AS_OF, AS_OF, [], []),
        stack._row("script_models", "sunday.script_models", "run_historical_replay", "analytical", "BLOCKED",
                   "entrypoint absent", AS_OF, AS_OF, [], []),
    ]
    for row in rows:
        if row["status"] != "EXECUTED":
            assert row["analytical_execution"] is False
            assert row["status"] != "EXECUTED"
    manifest = stack._manifest(tmp_path, "2026_12_AAA_BBB", AS_OF, "python -m sunday game",
                              {"source": "test", "canonical_kickoff_utc": None, "originals": {}, "conflicts": []},
                              rows, tmp_path / "out", blocked=False)
    assert manifest["result"] == "PARTIAL"
    assert manifest["result"] != "PASS"
    assert manifest["counts"]["REFUSED"] == 1
    assert manifest["counts"]["BLOCKED"] == 1
    assert manifest["projection_ready"] is False


def test_nested_refusal_cannot_pass():
    children = stack._child_rows([
        {"module_id": "freshness_check", "execution_class": "freshness", "status": "PARTIAL", "analytical_executed": False},
        {"module_id": "phase_ledger", "execution_class": "freshness", "status": "PASS", "analytical_executed": False},
        {"module_id": "ngs_matchup", "execution_class": "adapter", "status": "MISSING", "analytical_executed": False},
        {"module_id": "sim100k_preflight", "execution_class": "gate", "status": "REFUSED", "analytical_executed": False},
        {"module_id": "sim_v6_contract", "execution_class": "stub", "status": "BLOCKED", "analytical_executed": False},
        {"module_id": "matchup_edges", "execution_class": "analytical", "status": "PASS", "analytical_executed": True},
    ])
    parent = stack._row("orchestrator", "pipeline.orchestrator.runner", "run_games", "orchestration",
                        "EXECUTED", "the fan-out returned", AS_OF, AS_OF, [], [])
    schedule = stack._row("schedule", "sunday.kickoff", "resolve", "identity", "BLOCKED",
                          "NFL schedule capture unavailable", AS_OF, AS_OF, [], [])
    components = [schedule, parent, *children]
    assert stack.acceptance_result(components) == "BLOCKED"
    assert stack.acceptance_result(components) != "PASS"
    by_id = {row["id"]: row for row in children}
    assert by_id["orchestrator.ngs_matchup"]["status"] == "MISSING"
    assert by_id["orchestrator.sim100k_preflight"]["status"] == "REFUSED"
    assert by_id["orchestrator.sim_v6_contract"]["status"] == "BLOCKED"
    assert by_id["orchestrator.freshness_check"]["kind"] == "check"
    assert by_id["orchestrator.freshness_check"]["analytical_execution"] is False
    assert by_id["orchestrator.phase_ledger"]["analytical_execution"] is False
    verified = [stack._row("schedule", "sunday.kickoff", "resolve", "identity", "EXECUTED", "ok", AS_OF, AS_OF, [], []),
                parent, *children]
    assert stack.acceptance_result(verified) == "PARTIAL"


def test_missing_module_is_not_registered(tmp_path):
    state, payload, err = stack._call("sunday.not_a_registered_component", "run")
    assert state == "NOT_REGISTERED" and payload is None and err


def test_matchup_hash_ignores_clock_and_thread_names():
    left = {"generated_utc": "2026-11-28T01:00:00+00:00", "sections": {"coverage": 1},
            "receipts": [{"section": "coverage", "elapsed_ms": 10, "thread": "matchup_0", "status": "OK"}]}
    right = {"generated_utc": "2026-11-28T02:00:00+00:00", "sections": {"coverage": 1},
             "receipts": [{"section": "coverage", "elapsed_ms": 99, "thread": "matchup_3", "status": "OK"}]}
    assert stack._stable_research(left, AS_OF) == stack._stable_research(right, AS_OF)


def test_registered_components_import():
    import pipeline.orchestrator as orch
    import pipeline.matchup_research.build as research
    import sunday.script_models as scripts
    import sunday.player_board as board
    import sunday.decision.board as decision
    for fn in (orch.run_games, research.build_packet, scripts.run_historical_replay, board.from_packet, decision.build_board):
        assert callable(fn)

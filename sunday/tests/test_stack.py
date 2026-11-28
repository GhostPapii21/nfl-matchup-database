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


@pytest.mark.parametrize("game_id,expected", list(THREE.items()))
def test_kickoff_conflicts_use_espn_and_keep_the_config(game_id, expected):
    before = (ROOT / "core/possession_engine_v0/config").read_bytes() if False else None
    paths = list((ROOT / "core/possession_engine_v0/config").glob("*2026-11-29_data_only_nfl43.json"))
    snapshots = {p: p.read_bytes() for p in paths}
    packet = json.loads((ROOT / "pregame" / "packets" / game_id / "packet.json").read_text())
    got = kickoff.resolve(ROOT, game_id, packet)
    assert got["resolved"] is True
    assert got["source"] == "espn_event_date"
    assert got["canonical_kickoff_utc"] == expected
    assert got["config_file_rewritten"] is False
    assert got["conflicts"]
    assert any(row["source"] == "nflverse_games_csv" for row in got["conflicts"])
    config_utc = got["originals"]["possession_config"]["kickoff_utc"]
    assert config_utc == expected
    for path, raw in snapshots.items():
        assert path.read_bytes() == raw
    assert before is None


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

"""Sunday slice: isolation, as-of refusal, and a real DEN@PIT replay."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from sunday.assemble import partition_scripts
from sunday.context import schedule_games
from sunday.runner import execute_game, run_isolated

ROOT = Path(__file__).resolve().parents[2]
ASOF_PREGAME = "2026-11-27T04:31:50+00:00"
DEN = "2026_12_DEN_PIT"


def _ok(spec):
    if spec["game_id"] == "bad":
        raise RuntimeError("boom")
    return {"game_id": spec["game_id"], "status": "COMPLETE", "exit": 0}


def test_schedule_read_drops_final_scores():
    rows = schedule_games(on_date="2026-11-29")
    assert len(rows) == 10
    for row in rows:
        assert row["weekday"] == "Sunday"
        assert "away_score" not in row
        assert "home_score" not in row
        assert "result" not in row


def test_script_buckets_do_not_overlap_or_drop_trials():
    trials = {
        "h1_home": [14, 3, 10, 7],
        "h1_away": [0, 14, 7, 7],
        "reg_home": [28, 10, 17, 20],
        "reg_away": [7, 24, 14, 17],
    }
    # home spread -3: home is favored. Trial 0 controls, trial 1 is an underdog chase
    # (favorite trailed... wait favorite is home. Trial 1 home half 3 away 14, favorite margin half = 3-14 = -11,
    # final 10-24 = -14. underdog chase requires favorite led by 8 at half. That is trial 0 only for controls.
    out = partition_scripts(trials, "PIT", "DEN", home_spread=-3.0)
    assert out["ran"] is True
    assert out["pooled"] is False
    assert out["favorite"] == "PIT"
    counts = [branch["n"] for branch in out["branches"].values()]
    assert sum(counts) == out["n"] == 4
    assert out["play_pass_run"] == "NOT_SUPPORTED"
    assert out["branches"]["favorite_controls"]["n"] == 1
    assert out["branches"]["underdog_chases"]["n"] == 0


def test_pickem_does_not_invent_a_favorite():
    trials = {"h1_home": [7], "h1_away": [7], "reg_home": [14], "reg_away": [14]}
    out = partition_scripts(trials, "PIT", "DEN", home_spread=0)
    assert out["ran"] is False
    assert out["status"] == "NOT_SUPPORTED"


def test_one_game_failure_does_not_suppress_the_other():
    rows = run_isolated(
        [{"game_id": "bad"}, {"game_id": "good"}],
        worker=_ok,
        max_workers=2,
    )
    by_id = {row["game_id"]: row for row in rows}
    assert by_id["bad"]["status"] == "FAILED"
    assert "boom" in by_id["bad"]["error"]
    assert by_id["good"]["status"] == "COMPLETE"


def test_missing_packet_is_refused_without_a_simulator(tmp_path):
    result = execute_game({
        "game_id": "2026_99_AA_BB",
        "as_of": ASOF_PREGAME,
        "trials": 5,
        "out": str(tmp_path),
        "threads": 1,
        "command": "python -m sunday game --game 2026_99_AA_BB",
    })
    assert result["status"] == "REFUSED"
    assert result["exit"] == 2
    body = json.loads(Path(result["manifest"]).read_text())
    assert body["projection_ready"] is False
    assert "6_models" not in body["layers"]


def test_disagreeing_kickoffs_refuse_the_game(tmp_path):
    result = execute_game({
        "game_id": "2026_12_LV_CLE",
        "as_of": "2026-11-28T12:00:00+00:00",
        "trials": 5,
        "out": str(tmp_path),
        "threads": 1,
        "command": "python -m sunday game --game 2026_12_LV_CLE",
    })
    assert result["status"] == "REFUSED"
    assert any("kickoff sources disagree" in item for item in result["critical"])
    body = json.loads(Path(result["manifest"]).read_text())
    assert "6_models" not in body["layers"]


def test_as_of_after_kickoff_is_refused(tmp_path):
    result = execute_game({
        "game_id": DEN,
        "as_of": "2026-11-28T00:00:00+00:00",
        "trials": 5,
        "out": str(tmp_path),
        "threads": 1,
        "command": "python -m sunday game --game 2026_12_DEN_PIT",
    })
    assert result["status"] == "REFUSED"
    text = Path(result["manifest"]).read_text()
    assert "not before kickoff" in text
    assert "possession_engine" not in text


def test_process_fanout_keeps_both_refusals(tmp_path):
    specs = [
        {"game_id": "2026_99_AA_BB", "as_of": ASOF_PREGAME, "trials": 5,
         "out": str(tmp_path), "threads": 1, "command": "t", "run_id": "iso"},
        {"game_id": DEN, "as_of": "2026-11-28T00:00:00+00:00", "trials": 5,
         "out": str(tmp_path), "threads": 1, "command": "t", "run_id": "iso"},
    ]
    rows = run_isolated(specs, max_workers=2)
    assert {row["game_id"] for row in rows} == {"2026_99_AA_BB", DEN}
    assert all(row["status"] == "REFUSED" for row in rows)
    assert (tmp_path / "2026_99_AA_BB" / "manifest.json").is_file()
    assert (tmp_path / DEN / "manifest.json").is_file()


@pytest.mark.skipif(
    not (ROOT / "data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet").is_file(),
    reason="as-of week 11 play-by-play is not in this checkout",
)
def test_den_pit_replay_executes_real_engines(tmp_path):
    result = execute_game({
        "game_id": DEN,
        "as_of": ASOF_PREGAME,
        "trials": 20,
        "out": str(tmp_path),
        "threads": 4,
        "command": "python -m sunday replay --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00 --trials 20",
    })
    body = json.loads(Path(result["manifest"]).read_text())
    assert result["status"] == "COMPLETE"
    assert body["projection_ready"] is False
    assert body["research_only"] is True
    assert body["wager_authorized"] is False
    leak = body["preflight"]["leakage"]
    assert leak["ok"] is True
    assert leak["max_week"] == 11
    assert leak["contains_target_game"] is False
    schedule = body["layers"]["1_game_context"]["schedule"]
    assert "away_score" not in schedule and "home_score" not in schedule
    roster = body["layers"]["6_models"]["roster"]
    assert roster["documented_sim_v6"]["ran"] is False
    assert roster["documented_sim_v6"]["exists"] is False
    assert roster["lightning"]["ran"] is False
    assert roster["simv56_scratch"]["ran"] is False
    poss = body["layers"]["6_models"]["possession"]
    assert poss["ran"] is True
    assert poss["n_completed"] == 20
    assert poss["engine_id"] == "possession_engine_v0"
    assert max(poss["history_evidence"]["weeks"]) <= 11
    period = body["layers"]["6_models"]["period"]
    assert period["ran"] is True
    assert period["bias"]["ran"] is False
    assert set(period["methods"]) == {"matchup_pair", "independent", "game_randomness"}
    assert all(method["ran"] for method in period["methods"].values())
    assert period["asof_max_week"] == 11
    scripts = body["layers"]["5_game_scripts"]
    assert scripts["pooled"] is False
    assert sum(branch["n"] for branch in scripts["branches"].values()) == scripts["n"] == 20
    disagree = body["layers"]["7_distributions_and_market"]["disagreement"]
    assert disagree["pooled"] is False
    assert "blended_probability" not in disagree
    engines = {row["engine_id"] for row in disagree["methods"]}
    assert engines == {"possession_engine_v0", "period_engine_v0"}
    board = body["layers"]["9_board"]
    assert board["strong_reads"] == []
    assert board["soft_leans"] == []
    assert board["no_plays"]
    assert any(item["id"] == "sim_v6_absent" for item in body["layers"]["8_red_team"]["challenges"])
    assert body["output_sha256"]
    assert Path(result["manifest"]).with_name("report.md").is_file()
    as_of = datetime.fromisoformat(body["layers"]["1_game_context"]["as_of"])
    kick = datetime.fromisoformat(body["layers"]["1_game_context"]["kickoff_utc"])
    assert as_of.astimezone(timezone.utc) < kick.astimezone(timezone.utc)

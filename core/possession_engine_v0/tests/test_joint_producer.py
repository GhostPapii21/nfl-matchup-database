"""Tiny synthetic plumbing fixtures, never TNF fit/validation or measured roles."""
import copy
import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from joint_inputs import canonical, digest, freeze_run, trial_seed
from joint_accounting import validate_trial, finalize_validation
from joint_producer import (OT_PROFILE, STAT_PROFILE, OpportunityModel, missing_features,
                            simulate_joint_games, simulate_trial, write_forecast)
from simulate import simulate_games


WIRE_ROOT = Path(__file__).resolve().parents[3] / "research/nfl_sim_integration_2026-11-06/integration/wire"
FROZEN_WIRE_SHA256 = '50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd'


def frozen_wire_example():
    # Required authority fixture: never skip, regenerate, or normalize its bytes.
    data = (WIRE_ROOT / 'producer_joint_trial_example_v1.jsonl').read_bytes()
    assert hashlib.sha256(data).hexdigest() == FROZEN_WIRE_SHA256
    assert len(data.splitlines()) == 1
    return json.loads(data)


def test_frozen_producer_wire_v1_exact_bytes():
    frozen_wire_example()


def test_export_preserves_documented_producer_wire_v1_shapes(tmp_path):
    example = frozen_wire_example()
    meta = json.loads((WIRE_ROOT / 'WIRE_SCHEMA_V1_META.json').read_text())
    assert meta['wire_schema_id'] == 'nfl-sim-joint-trial-producer-wire'
    assert meta['wire_version'] == '1.0.0-producer'
    assert meta['example_jsonl_sha256'] == FROZEN_WIRE_SHA256
    spec, root, inputs, _, _ = fixture_inputs(tmp_path)
    output = simulate_joint_games(spec, input_root=root, inputs=inputs, n=1, seed=123,
                                  output_root=tmp_path / 'exports')
    exported = Path(output['artifact_directory']) / 'trials.jsonl'
    rows = [json.loads(line) for line in exported.read_text().splitlines()]
    assert exported.read_bytes() == b''.join(canonical(t) + b'\n' for t in output['trials'])
    assert len(rows) == 1
    trial = rows[0]
    assert set(trial) == set(example) == set(meta['top_level_keys'])
    assert isinstance(trial['status'], dict)
    assert set(trial['status']) == set(example['status']) == {
        'state', 'completion_reason', 'terminal_state', 'went_ot',
        'adapter_projection_allowed', 'projection_blockers'}
    assert isinstance(trial['status']['state'], str)
    assert isinstance(trial['status']['completion_reason'], str)
    assert isinstance(trial['status']['terminal_state'], dict)
    assert type(trial['status']['went_ot']) is bool
    assert trial['status']['adapter_projection_allowed'] is False
    assert isinstance(trial['status']['projection_blockers'], list)
    assert not {'completion_reason', 'terminal_state', 'went_ot'} & set(trial)
    assert set(trial['freeze']) == set(example['freeze']) == set(meta['freeze_keys'])
    assert trial['freeze']['input_manifest_digest'] == output['input_content_hash']
    assert 'input_manifest_hash' not in trial['freeze']
    assert set(trial['engine']) == set(example['engine']) == set(meta['engine_keys'])
    assert isinstance(trial['engine']['component_version'], str)
    assert set(trial['engine']['dependencies']) == {'python', 'numpy'}
    assert all(isinstance(v, str) and v for v in trial['engine']['dependencies'].values())
    assert not {'component_versions', 'dependency_versions'} & set(trial['engine'])
    assert trial['team_periods']
    for row in trial['team_periods']:
        assert set(row) == set(example['team_periods'][0]) == set(meta['team_period_sample_keys'])
        assert set(row['stats']) == set(example['team_periods'][0]['stats'])
        assert type(row['stats']['points']) is int
        assert 'points' not in row


def fixture_inputs(tmp_path, terminal="designed_rush", catch="COMPLETE", elapsed=900, yards=None):
    root = tmp_path / "frozen"
    root.mkdir(parents=True)
    game = {"game_id": "0001", "game_id_namespace": "synthetic_test", "season": 2026,
            "season_type": "TEST", "week": 1, "home_team_id": "HOME", "away_team_id": "AWAY",
            "team_id_namespace": "synthetic_test", "kickoff_utc": "2026-11-07T18:00:00Z", "crosswalk_ref": "registry"}
    players = [{"record_id": team + role, "team_id": team, "player_id_namespace": "synthetic_test",
                "player_id": team + "00" + str(i), "evidence_ref": "synthetic_roster_fixture"}
               for team in ("HOME", "AWAY") for i, role in enumerate(("P", "T", "R", "ZERO"))]
    registry = {"game": game, "players": players, "evidence_refs": ["synthetic_schedule_fixture"],
                "alias_map_version": "synthetic-v1", "team_alias_map": {"HOME": "HOME", "AWAY": "AWAY"}, "crosswalk": [
                    {"entity": "player", "source_namespace": "synthetic_source", "source_id": p["record_id"],
                     "canonical_namespace": p["player_id_namespace"], "canonical_id": p["player_id"],
                     "evidence_ref": "synthetic_roster_fixture"} for p in players]}
    roles = {team: [{"weight": 1, "value": {"state_id": "available_test", "available": [team + role for role in ("P", "T", "R", "ZERO")],
              "depth_chart_state": {"status": "MODELED", "label": "synthetic_joint_depth_state"},
              "rotation_weights": {"passer": {team + "P": 1}, "target": {team + "T": 1}, "carry": {team + "R": 1}},
              "target_depth_distribution": [{"value": 7, "weight": 1}]}}] for team in ("HOME", "AWAY")}
    default_yards = -4 if terminal == "sack" else 3 if terminal in {"designed_rush", "scramble", "kneel", "credited_aborted_rush"} else 8 if terminal.endswith("targeted_pass") and catch == "COMPLETE" else 0
    outcome = {"yards": default_yards if yards is None else yards, "elapsed_seconds": elapsed}
    if terminal == "punt":
        outcome["punt_net_yards"] = 40
    if terminal == "field_goal":
        outcome["made"] = True
    model = {"schema_version": "1", "model_version": "synthetic-tables-v1", "uses_market": False, "lineage_modes": ["data_only"],
             "provenance_refs": ["model", "registry"], "sample_size": None, "sample_size_reason": "SYNTHETIC_TEST; no observed sample",
             "flags": ["SCENARIO_ONLY"], "ot_rule_profile": OT_PROFILE, "stat_credit_profile": STAT_PROFILE,
             "environments": [{"value": {"environment_id": "synthetic_shared"}, "weight": 1}],
             "role_states": roles, "usage_cells": [{"cell_id": "synthetic_default", "when": {},
                         "terminals": [{"value": terminal, "weight": 1}]}],
             "catch_distributions": {terminal: [{"value": catch, "weight": 1}]},
             "outcome_cells": [{"cell_id": "synthetic_outcome", "when": {}, "distribution": [{"value": outcome, "weight": 1}]}],
             "try_points": [{"value": 1, "weight": 1}]}
    splits = {"split_manifest_id": "synthetic-unassigned-v1", "policy_version": "1", "status": "UNASSIGNED",
              "created_at_utc": "2026-11-05T10:00:00Z", "train_game_ids": None, "dev_game_ids": None, "holdout_game_ids": None}
    spec = {"game": game, "mode": "data_only", "config_id": "synthetic-only", "purpose": "SYNTHETIC_TEST",
            "cutoff_utc": "2026-11-06T10:00:00Z", "frozen_at_utc": "2026-11-06T10:00:00Z",
            "generated_at_utc": "2026-11-06T10:01:00Z", "max_steps": 12}
    inputs = [{"logical_input_id": key, "path": key + ".json", "source": "synthetic_fixture",
               "selected_record_ids": ["synthetic_all"], "schema_version": "1", "usage": "PREDICTIVE",
               "source_event_time_utc": "2026-11-05T10:00:00Z", "available_at_utc": "2026-11-05T10:00:00Z",
               "retrieved_at_utc": "2026-11-05T11:00:00Z", "asof_evidence_ref": "synthetic_fixed_bytes"}
              for key in ("registry", "model", "splits")]
    data = {"registry": registry, "model": model, "splits": splits}
    def save():
        for key, value in data.items():
            (root / (key + ".json")).write_bytes(canonical(value))
    save()
    return spec, root, inputs, data, save


def frozen_fixture(tmp_path, **kwargs):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, **kwargs)
    return freeze_run(spec, root, inputs, n=1, seed=123)


def assert_valid(trial):
    result = validate_trial(trial)
    assert result["status"] == "PASS", [c for c in result["checks"] if not c["pass"]][:8]
    assert trial["status"]["state"] == "COMPLETE", trial["validation"]["failed_invariants"][:8]


@pytest.mark.parametrize("terminal", ["targeted_pass", "non_dropback_targeted_pass", "throwaway", "spike",
    "other_untargeted_attempt", "sack", "scramble", "aborted_dropback_no_attempt", "designed_rush", "kneel",
    "credited_aborted_rush", "no_play", "punt", "field_goal"])
def test_terminal_conservation_per_period_and_aggregate(tmp_path, terminal):
    trial = simulate_trial(frozen_fixture(tmp_path, terminal=terminal), 0)
    assert_valid(trial)
    assert all(type(v) is int for row in trial["team_periods"] for v in row["stats"].values())
    zero = [r for r in trial["player_periods"] if r["player_id"].endswith("003")]
    assert zero and all(all(v == 0 for v in r["stats"].values()) for r in zero)


@pytest.mark.parametrize("terminal", ["targeted_pass", "designed_rush", "scramble", "kneel"])
def test_opportunities_increment_in_execution_before_catch_or_yard_draw(tmp_path, terminal):
    frozen = frozen_fixture(tmp_path, terminal=terminal)
    seen = []
    class Spy(OpportunityModel):
        def outcome(self, op):
            stat = "eligible_target_attempts" if terminal == "targeted_pass" else "rush_attempts"
            assert self.live_team[op["team"]][stat] >= 1
            assert op["team_credits"][stat] == 1
            assert op["team_credits"]["gross_pass_yards"] == 0
            assert op["team_credits"]["rush_yards"] == 0
            assert [r["generation_stage"] for r in op["trace"]] == ["PRE_SNAP", "OPPORTUNITY"]
            assert any(r["stats"]["targets" if terminal == "targeted_pass" else "carries"] == 1 for r in op["players"].values())
            seen.append(op["team"])
            return super().outcome(op)
    assert_valid(simulate_trial(frozen, 0, model_class=Spy))
    assert seen


@pytest.mark.parametrize("catch", ["INCOMPLETE", "INTERCEPTION"])
def test_targeted_failure_has_target_zero_catch_zero_yards(tmp_path, catch):
    trial = simulate_trial(frozen_fixture(tmp_path, terminal="targeted_pass", catch=catch), 0)
    assert_valid(trial)
    for e in trial["events"]:
        if e["type"] == "snap":
            t = e["team_credits"][e["acting_team_id"]]
            assert t["eligible_target_attempts"] == 1
            assert t["completions"] == t["gross_pass_yards"] == 0


def test_unknown_receiver_unassigned_not_fake_player(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, terminal="targeted_pass", catch="INTERCEPTION")
    for team, roles in data["model"]["role_states"].items():
        roles[0]["value"]["rotation_weights"]["target"] = {"UNASSIGNED": 1}
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert_valid(trial)
    assert "PLAYER_ID_UNRESOLVED" in trial["status"]["projection_blockers"]
    assert any(r["stats"]["unassigned_targets"] for r in trial["team_periods"])
    assert all(e["assignments"]["receiver"] is None for e in trial["events"] if e["type"] == "snap")


def test_clocks_boundary_continuity_halftime_ot_and_linked_try(tmp_path):
    trial = simulate_trial(frozen_fixture(tmp_path, terminal="designed_rush", yards=75), 0)
    assert_valid(trial)
    assert trial["status"]["went_ot"]
    assert sum(e["elapsed_clock_seconds"] for e in trial["events"] if e["period_kind"] == "REG") == 3600
    assert all(0 <= e["post_period_seconds_remaining"] <= e["pre_period_seconds_remaining"] for e in trial["events"])
    tries = [e for e in trial["events"] if e["type"] == "try"]
    assert tries and all(e["elapsed_clock_seconds"] == 0 and e["pre_period_seconds_remaining"] == 0 for e in tries)
    half = next(e for e in trial["events"] if e.get("possession_end_cause") == "halftime")
    assert half["post_possession"] == "HOME"
    for p in trial["possessions"]:
        assert p["clock_seconds"] == sum(s["clock_seconds"] for s in p["period_segments"])


def test_quarter_boundary_does_not_force_new_possession(tmp_path):
    trial = simulate_trial(frozen_fixture(tmp_path, terminal="no_play"), 0)
    assert_valid(trial)
    starts = {e["period_id"]: e for e in trial["events"] if e["type"] == "period_start"}
    assert starts["Q1"]["possession_id"] == starts["Q2"]["possession_id"]
    assert starts["Q3"]["possession_id"] == starts["Q4"]["possession_id"]
    assert starts["Q2"]["possession_id"] != starts["Q3"]["possession_id"]


def test_no_ot_has_known_zero_ot_stats(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, terminal="field_goal")
    # Three pre-Q4 made FGs; a Q4 no-play leaves the regulation score unequal.
    data["model"]["usage_cells"].insert(0, {"cell_id": "q4_no_play", "when": {"period_id": "Q4"},
                                               "terminals": [{"value": "no_play", "weight": 1}]})
    data["model"]["outcome_cells"].insert(0, {"cell_id": "no_play", "when": {"terminal": "no_play"},
                                                 "distribution": [{"value": {"yards": 0, "elapsed_seconds": 900}, "weight": 1}]})
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert_valid(trial)
    assert not trial["status"]["went_ot"]
    assert all(all(v == 0 for v in r["stats"].values()) for r in trial["aggregates"]["team"] if r["period_id"] == "OT")


def test_cap_is_incomplete_blocks_projection_without_filling_future_quarters(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    spec["max_steps"] = 1
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert trial["status"]["state"] == "INCOMPLETE"
    assert not trial["status"]["adapter_projection_allowed"]
    assert {r["period_id"] for r in trial["team_periods"]} == {"Q1"}
    assert all(r["stats"] is None for r in trial["aggregates"]["team"] if r["period_id"] in {"REG", "FG"})


def test_shared_state_role_depth_rotation_are_explicit_and_conditional(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, terminal="targeted_pass")
    for team, states in data["model"]["role_states"].items():
        state = states[0]["value"]
        state["available"].remove(team + "T")
        state["rotation_weights"]["target"][team + "R"] = 0.5
        state["target_depth_distribution"] = [{"value": 4, "weight": 0.5}, {"value": 15, "weight": 0.5}]
        state["depth_chart_state"] = {"label": "synthetic_backup_active", "flags": ["MODELED", "SCENARIO_ONLY"]}
    data["model"]["usage_cells"].insert(0, {"cell_id": "late_state", "when": {"regulation_seconds_remaining_max": 900, "down": 1},
                      "terminals": [{"value": "kneel", "weight": 1}]})
    data["model"]["outcome_cells"].insert(0, {"cell_id": "kneel", "when": {"terminal": "kneel"},
               "distribution": [{"value": {"yards": -1, "elapsed_seconds": 900}, "weight": 1}]})
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert_valid(trial)
    snaps = [e for e in trial["events"] if e["type"] == "snap"]
    assert any(e["generation_trace"][0]["usage_cell_id"] == "late_state" for e in snaps)
    assert all(e["assignments"]["receiver"]["player_id"].endswith("002") for e in snaps if e["terminal_category"] == "targeted_pass")
    assert all("roles" in trial["latent_state"] for _ in [0])


def test_lateral_and_signed_credit_adjustment_are_explicit(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, terminal="targeted_pass")
    # Model an explicit receiving credit difference, without changing player yards to reconcile.
    data["model"]["outcome_cells"] = []
    for team in ("HOME", "AWAY"):
        outcome = {"yards": 8, "field_advance_yards": 6, "elapsed_seconds": 900,
                   "receiving_credits": [{"player_ref": team + "T", "yards": 4}, {"player_ref": team + "R", "yards": 6}],
                   "pass_receiving_credit_adjustment": -2, "credit_explanation": "synthetic provider/lateral credit fixture",
                   "credit_provenance_refs": ["model"]}
        data["model"]["outcome_cells"].append({"cell_id": team + "_lateral", "when": {"team_id": team},
                                    "distribution": [{"value": outcome, "weight": 1}]})
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=2), 0)
    assert_valid(trial)
    snap = next(e for e in trial["events"] if e["type"] == "snap")
    lateral = next(p for p in snap["player_credits"] if p["player_id"].endswith("002"))
    assert lateral["stats"]["rec_yards"] == 6
    assert lateral["stats"]["targets"] == lateral["stats"]["catches"] == 0
    assert snap["credit_adjustments"][0]["signed_pass_receiving_adjustment"] == -2


@pytest.mark.parametrize("mutation", ["target", "clock", "score", "stages", "missingness", "event_key", "period", "negative", "schema"])
def test_deliberate_corruption_fails_closed(tmp_path, mutation):
    trial = simulate_trial(frozen_fixture(tmp_path, terminal="targeted_pass"), 0)
    assert_valid(trial)
    event = next(e for e in trial["events"] if e["type"] == "snap")
    if mutation == "target":
        event["team_credits"][event["acting_team_id"]]["eligible_target_attempts"] += 1
    elif mutation == "clock":
        event["post_period_seconds_remaining"] = -1
    elif mutation == "score":
        trial["team_periods"][0]["stats"]["points"] += 1
    elif mutation == "stages":
        event["generation_trace"][1], event["generation_trace"][3] = event["generation_trace"][3], event["generation_trace"][1]
    elif mutation == "missingness":
        trial["feature_availability"]["coverage"]["value"] = "zone"
    elif mutation == "event_key":
        event["event_id"] = trial["events"][0]["event_id"]
    elif mutation == "period":
        trial["player_periods"].append(trial["player_periods"][0])
    elif mutation == "negative":
        event["player_credits"][0]["stats"]["pass_attempts"] = -1
    elif mutation == "schema":
        del trial["possessions"]
    finalize_validation(trial)
    assert trial["validation"]["status"] == "INVALID"
    assert trial["status"]["state"] == "INVALID"
    assert not trial["status"]["adapter_projection_allowed"]


def test_empty_trial_never_false_pass():
    assert validate_trial({})["status"] == "INVALID"


def test_joint_ids_replay_seed_derivation_and_batch_extension(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    frozen = freeze_run(spec, root, inputs, n=2, seed=123)
    extended = freeze_run(spec, root, inputs, n=3, seed=123)
    assert frozen["forecast_id"] != extended["forecast_id"]
    assert trial_seed(frozen, 0) == trial_seed(extended, 0)
    expected = int.from_bytes(hashlib.sha256(canonical([frozen["run_spec"]["rng"]["seed_derivation_version"], "123", "synthetic_test", "0001", 0])).digest()[:8], "big")
    assert trial_seed(frozen, 0) == str(expected)
    one = simulate_trial(frozen, 1)
    zero = simulate_trial(frozen, 0)
    assert one == simulate_trial(frozen, 1)
    assert zero["trial_id"] == frozen["forecast_id"] + "/trial/0"
    assert zero["rng"]["trial_seed"] != one["rng"]["trial_seed"]
    assert {zero["trial_id"], one["trial_id"]} == {frozen["forecast_id"] + "/trial/" + str(i) for i in (0, 1)}
    assert zero["aggregates"] == simulate_trial(extended, 0)["aggregates"]


def test_manifest_durable_dispatch_and_cutoff_versioning(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    cfg = {"mode": spec["mode"], "config_id": spec["config_id"], "joint_producer": {
        "spec": spec, "input_root": root, "inputs": inputs, "output_root": tmp_path / "outputs"}}
    output = simulate_games(cfg, pbp_path="unused", n=2, seed=7)
    assert output["n_requested"] == output["n_completed"] == 2
    assert output["n_invalid"] == output["n_incomplete"] == 0
    assert output["n_usable"] == 0  # synthetic-only never actionable
    assert len(output["excluded_trials"]) == 2
    folder = Path(output["artifact_directory"])
    manifest = json.loads((folder / "input_manifest.json").read_text())
    assert digest(manifest) == output["input_content_hash"]
    ledger = json.loads((folder / "forecast_ledger.json").read_text())
    assert ledger["trial_ids"] == [t["trial_id"] for t in output["trials"]]
    assert ledger["result_evidence_ids"] == []
    for t in output["trials"]:
        assert t["feature_availability"] == missing_features()
        assert t["freeze"]["cutoff_utc"] == spec["cutoff_utc"]
        assert t["freeze"]["input_content_hash"] == output["input_content_hash"]
        assert t["engine"]["engine_version"] and t["engine"]["dirty_patch_hash"]
    frozen = freeze_run(spec, root, inputs, n=2, seed=7)
    assert write_forecast(tmp_path / "outputs", frozen, output["trials"]) == str(folder)
    bad = copy.deepcopy(output["trials"])
    bad[0]["flags"].append("CHANGED")
    with pytest.raises(ValueError, match="immutable artifact conflict"):
        write_forecast(tmp_path / "outputs", frozen, bad)
    spec["cutoff_utc"] = "2026-11-06T09:00:00Z"
    revised = freeze_run(spec, root, inputs, n=2, seed=7)
    assert revised["forecast_id"] != frozen["forecast_id"]


@pytest.mark.parametrize("problem", ["post_cutoff", "late_unverified", "market", "postgame", "identity", "ambiguous", "split_overlap", "inspected_holdout"])
def test_freeze_blocks_bad_evidence_or_contamination(tmp_path, problem):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    if problem == "post_cutoff":
        inputs[0]["available_at_utc"] = "2026-11-07T10:00:00Z"
    elif problem == "late_unverified":
        spec["frozen_at_utc"] = spec["generated_at_utc"] = "2026-11-06T12:00:00Z"
        inputs[0]["retrieved_at_utc"] = "2026-11-06T11:00:00Z"
    elif problem == "market":
        inputs[0]["usage"] = "MARKET"
    elif problem == "postgame":
        inputs[0]["usage"] = "EVIDENCE_ONLY_POSTGAME"
    elif problem == "identity":
        spec["game"]["game_id"] = None
    elif problem == "ambiguous":
        data["registry"]["crosswalk"].append(data["registry"]["crosswalk"][0])
    else:
        split = data["splits"]
        row = {"namespace": "synthetic_test", "game_id": "0001"}
        split.update(status="FROZEN", frozen_before_selection=True, train_game_ids=[], dev_game_ids=[], holdout_game_ids=[row])
        if problem == "split_overlap":
            split["train_game_ids"] = [row]
        else:
            split["inspected_game_ids"] = [row]
    save()
    with pytest.raises(ValueError):
        freeze_run(spec, root, inputs, n=1, seed=1)


def test_modes_are_distinct_and_cannot_silently_relabel_market_model(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    independent = freeze_run(spec, root, inputs, n=1, seed=1)
    adjusted_spec = {**spec, "mode": "script_adjusted"}
    assert freeze_run(adjusted_spec, root, inputs, n=1, seed=1)["forecast_id"] != independent["forecast_id"]
    data["model"]["uses_market"] = True
    save()
    with pytest.raises(ValueError, match="market lineage"):
        freeze_run(spec, root, inputs, n=1, seed=1)
    market_spec = {**spec, "mode": "market_informed"}
    with pytest.raises(ValueError, match="frozen market input"):
        freeze_run(market_spec, root, inputs, n=1, seed=1)
    inputs[1]["usage"] = "MARKET"
    market = freeze_run(market_spec, root, inputs, n=1, seed=1)
    assert market["forecast_id"] != independent["forecast_id"]
    assert market["input_content_hash"] != independent["input_content_hash"]


def test_unsupported_category_or_official_ot_profile_blocks_run(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    data["model"]["ot_rule_profile"] = {"id": "official_unverified"}
    save()
    with pytest.raises(ValueError, match="UNSUPPORTED OT"):
        simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)


def test_legacy_accounting_cannot_claim_contract_pass(tmp_path, monkeypatch):
    from validation import accounting
    import numpy as np
    from state import GameState
    fake = {"arrays": {k: np.array([0]) for k in ("q1_home", "q2_home", "q3_home", "q4_home", "h1_home", "h2_home", "reg_home", "fg_home", "ot_home",
        "q1_away", "q2_away", "q3_away", "q4_away", "h1_away", "h2_away", "reg_away", "fg_away", "ot_away", "went_ot")},
            "evidence_summary": {"sparse_rate": 0}, "player_joint": {}}
    monkeypatch.setattr(accounting, "simulate_games", lambda *a, **kw: fake)
    monkeypatch.setattr(accounting, "load_team_history", lambda *a, **kw: {"df": None})
    monkeypatch.setattr(accounting, "build_catalog", lambda *a, **kw: (None, None))
    monkeypatch.setattr(accounting, "simulate_one", lambda *a, **kw: GameState.new_game("HOME", "AWAY"))
    cfg = {"config_id": "synthetic-only", "history": {"teams": ["HOME", "AWAY"], "season": 2026, "weeks_inclusive": [1]}}
    result = accounting.run_accounting_checks(cfg, pbp_path="unused", n=1)
    assert result["overall_status"] != "PASS"
    assert next(c for c in result["checks"] if c["name"] == "reg_clock_target_declared_3600")["ok"] is False


def test_stopped_clock_is_ordered_and_cap_is_not_false_complete(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, terminal="spike", elapsed=0)
    spec["max_steps"] = 2
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert trial["status"]["state"] == "INCOMPLETE"
    assert trial["validation"]["status"] == "PASS"
    snaps = [e for e in trial["events"] if e["type"] == "snap"]
    assert len(snaps) == 2 and all(e["elapsed_clock_seconds"] == 0 for e in snaps)
    assert snaps[0]["event_seq"] < snaps[1]["event_seq"]
    assert all(r["stats"] is None for r in trial["aggregates"]["team"])


def test_explicit_period_end_runoff_is_not_a_snap_or_attempt(tmp_path):
    trial = simulate_trial(frozen_fixture(tmp_path, terminal="period_end_runoff"), 0)
    assert_valid(trial)
    assert not any(e["type"] == "snap" for e in trial["events"])
    assert sum(e["elapsed_clock_seconds"] for e in trial["events"] if e["period_kind"] == "REG") == 3600
    assert all(r["stats"]["dropbacks"] == r["stats"]["rush_attempts"] == 0 for r in trial["team_periods"])


@pytest.mark.parametrize("rush_design", ["direct_snap", "end_around", "qb_designed"])
def test_non_rb_designed_runs_keep_explicit_classification(tmp_path, rush_design):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    for team, states in data["model"]["role_states"].items():
        states[0]["value"]["rotation_weights"]["carry"] = {team + "T": 1}
    data["model"]["outcome_cells"][0]["distribution"][0]["value"]["rush_design"] = rush_design
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert_valid(trial)
    assert all(e["orthogonal_flags"]["rush_design"] == rush_design for e in trial["events"] if e["type"] == "snap")


def test_non_qb_throw_keeps_credited_passer_and_non_dropback_attempt(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, terminal="non_dropback_targeted_pass")
    for team, states in data["model"]["role_states"].items():
        states[0]["value"]["rotation_weights"]["passer"] = {team + "R": 1}
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert_valid(trial)
    for e in trial["events"]:
        if e["type"] == "snap":
            assert e["assignments"]["passer"]["player_id"].endswith("002")
            stats = e["team_credits"][e["acting_team_id"]]
            assert stats["non_dropback_pass_attempts"] == 1 and stats["dropbacks"] == 0


def test_unknown_passer_sack_and_completed_target_stay_in_residuals(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, terminal="targeted_pass")
    for team, states in data["model"]["role_states"].items():
        states[0]["value"]["rotation_weights"]["passer"] = {"UNASSIGNED": 1}
        states[0]["value"]["rotation_weights"]["target"] = {"UNASSIGNED": 1}
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert_valid(trial)
    e = next(e for e in trial["events"] if e["type"] == "snap")
    t = e["team_credits"][e["acting_team_id"]]
    assert t["unassigned_catches"] == t["unassigned_targets"] == t["unassigned_pass_attempts"] == 1
    assert t["unassigned_rec_yards"] == t["unassigned_pass_yards"] == 8
    assert e["player_credits"] == []


def test_fumble_preserves_stat_yards_and_ends_possession(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    data["model"]["outcome_cells"][0]["distribution"][0]["value"]["fumble_lost"] = True
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert_valid(trial)
    snap = next(e for e in trial["events"] if e["type"] == "snap")
    assert snap["orthogonal_flags"]["fumble_lost"]
    assert snap["team_credits"]["AWAY"]["rush_yards"] == 3
    assert snap["team_credits"]["AWAY"]["turnovers"] == 1
    assert trial["possessions"][0]["end_cause"] == "turnover"


@pytest.mark.parametrize("mutation", ["loaded", "spec", "manifest", "population", "unassigned_index"])
def test_prepared_freeze_cannot_be_mutated_or_shuffled(tmp_path, mutation):
    frozen = frozen_fixture(tmp_path)
    if mutation == "loaded":
        frozen["loaded"]["model"]["uses_market"] = True
    elif mutation == "spec":
        frozen["spec"]["mode"] = "market_informed"
    elif mutation == "manifest":
        frozen["input_manifest"]["entries"][0]["sha256"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError):
        if mutation == "population":
            write_forecast(tmp_path / "out", frozen, [])
        else:
            simulate_trial(frozen, 3 if mutation == "unassigned_index" else 0)


def test_late_verified_extraction_and_creation_times_do_not_change_forecast_identity(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    first = freeze_run(spec, root, inputs, n=1, seed=1)
    spec["frozen_at_utc"] = spec["generated_at_utc"] = "2026-11-06T12:00:00Z"
    assert freeze_run(spec, root, inputs, n=1, seed=1)["forecast_id"] == first["forecast_id"]
    inputs[0].update(retrieved_at_utc="2026-11-06T11:00:00Z", asof_verified=True)
    later = freeze_run(spec, root, inputs, n=1, seed=1)
    assert later["input_content_hash"] != first["input_content_hash"]


def test_input_byte_revision_changes_content_and_forecast_ids(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    first = freeze_run(spec, root, inputs, n=1, seed=1)
    path = root / "model.json"
    path.write_bytes(path.read_bytes() + b"\n")  # same JSON value, distinct exact source bytes
    revised = freeze_run(spec, root, inputs, n=1, seed=1)
    assert first["input_content_hash"] != revised["input_content_hash"]
    assert first["forecast_id"] != revised["forecast_id"]


@pytest.mark.parametrize("field", ["penalty", "untimed_down", "defensive_return_yards"])
def test_unsupported_rule_effects_are_blocked_not_silently_approximated(tmp_path, field):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    data["model"]["outcome_cells"][0]["distribution"][0]["value"][field] = 1
    save()
    with pytest.raises(ValueError, match="UNSUPPORTED"):
        simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)


def test_corrupted_yard_stage_and_seed_cannot_hide_behind_balanced_credits(tmp_path):
    trial = simulate_trial(frozen_fixture(tmp_path, terminal="targeted_pass"), 0)
    snap = next(e for e in trial["events"] if e["type"] == "snap")
    snap["generation_trace"][3]["realized_yards"] += 1
    assert validate_trial(trial)["status"] == "INVALID"
    snap["generation_trace"][3]["realized_yards"] -= 1
    trial["rng"]["trial_seed"] = "123"
    assert validate_trial(trial)["status"] == "INVALID"


def test_lineage_cannot_relabel_market_derived_model_as_independent(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    data["model"]["lineage_modes"] = ["market_informed"]
    save()
    with pytest.raises(ValueError, match="market lineage"):
        freeze_run(spec, root, inputs, n=1, seed=1)


def test_null_identity_has_explicit_status_and_no_named_projection(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    unresolved = data["registry"]["players"][2]
    old_id = unresolved["player_id"]
    unresolved.update(player_id=None, identity_status="UNRESOLVED")
    data["registry"]["crosswalk"] = [r for r in data["registry"]["crosswalk"] if r["canonical_id"] != old_id]
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert_valid(trial)
    assert "PLAYER_ID_UNRESOLVED" in trial["status"]["projection_blockers"]
    assert not any(r["player_id"] == old_id for r in trial["player_periods"])
    assert any(r["stats"]["unassigned_carries"] > 0 for r in trial["team_periods"])


def test_invalid_draw_is_persisted_and_counted_without_filtering(tmp_path, monkeypatch):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    import joint_producer
    original = joint_producer.OpportunityModel.outcome
    def corrupt_after_allocation(self, op):
        catch, outcome = original(self, op)
        op["team_credits"]["dropbacks"] += 1
        return catch, outcome
    monkeypatch.setattr(joint_producer.OpportunityModel, "outcome", corrupt_after_allocation)
    result = simulate_joint_games(spec, input_root=root, inputs=inputs, n=2, seed=1, output_root=tmp_path / "out")
    assert result["n_invalid"] == result["n_requested"] == 2
    assert result["n_usable"] == result["n_completed"] == 0
    assert len(result["trials"]) == 2
    assert len((Path(result["artifact_directory"]) / "trials.jsonl").read_text().splitlines()) == 2


def test_safety_credits_opponent_and_negative_rush_yards_without_offensive_points(tmp_path):
    trial = simulate_trial(frozen_fixture(tmp_path, terminal="designed_rush", yards=-25), 0)
    assert_valid(trial)
    snap = next(e for e in trial["events"] if e["type"] == "snap")
    assert snap["team_credits"]["AWAY"]["rush_yards"] == -25
    assert snap["team_credits"]["AWAY"]["points"] == 0
    assert snap["team_credits"]["HOME"]["points"] == 2
    assert snap["score_delta"] == {"HOME": 2, "AWAY": 0}
    assert trial["possessions"][0]["end_cause"] == "safety"


def test_required_types_and_latent_evidence_cannot_be_missing(tmp_path):
    trial = simulate_trial(frozen_fixture(tmp_path), 0)
    trial["latent_state"] = None
    assert validate_trial(trial)["status"] == "INVALID"


def test_cap_cannot_be_relabelled_complete(tmp_path):
    spec, root, inputs, data, save = fixture_inputs(tmp_path)
    spec["max_steps"] = 4
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=1), 0)
    assert trial["status"]["state"] == "INCOMPLETE"
    trial["status"].update(state="COMPLETE", completion_reason="regulation_complete")
    validation = validate_trial(trial)
    assert validation["status"] == "INVALID"
    assert "termination_event" in validation["failed_invariants"]


@pytest.mark.parametrize('terminal,catch', [('targeted_pass', 'INCOMPLETE'), ('punt', 'NA'), ('field_goal', 'NA')])
def test_zero_yard_terminal_plays_conserve_through_ot(tmp_path, terminal, catch):
    spec, root, inputs, data, save = fixture_inputs(tmp_path, terminal=terminal, catch=catch, yards=0)
    if terminal == 'field_goal':
        data['model']['outcome_cells'][0]['distribution'][0]['value']['made'] = False
    save()
    trial = simulate_trial(freeze_run(spec, root, inputs, n=1, seed=123), 0)
    assert_valid(trial)
    assert trial['status']['went_ot']
    assert any(e['period_kind'] == 'OT' for e in trial['events'])
    for e in trial['events']:
        for credits in e['team_credits'].values():
            assert credits['gross_pass_yards'] == credits['rush_yards'] == 0


def test_forecast_identity_ignores_generated_replay_sources(tmp_path):
    import joint_inputs
    original = joint_inputs.source_files
    package = tmp_path / 'package'
    package.mkdir()
    (package / 'runtime.py').write_text('x = 1\n')
    first = {p.relative_to(package).as_posix(): p.read_bytes() for p in original(package)}
    for directory in ('runs/replay/engine_source', 'artifacts/replay/engine_source'):
        target = package / directory
        target.mkdir(parents=True)
        (target / 'runtime.py').write_text('old replay source\n')
    second = {p.relative_to(package).as_posix(): p.read_bytes() for p in original(package)}
    assert first == second == {'runtime.py': b'x = 1\n'}


def test_replay_bytes_are_stable_across_python_hash_seeds(tmp_path):
    import os
    import subprocess
    import sys
    spec, root, inputs, _, _ = fixture_inputs(tmp_path, terminal='targeted_pass')
    payload = tmp_path / 'replay.json'
    payload.write_text(json.dumps({'spec': spec, 'root': str(root), 'inputs': inputs}))
    code = """
import json, sys
from joint_inputs import freeze_run, digest
from joint_producer import simulate_trial
p = json.load(open(sys.argv[1]))
f = freeze_run(p['spec'], p['root'], p['inputs'], n=1, seed=123)
print(digest(simulate_trial(f, 0)))
"""
    env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1]))
    outputs = [subprocess.check_output([sys.executable, '-c', code, str(payload)],
               env=dict(env, PYTHONHASHSEED=str(seed)), text=True) for seed in (1, 2)]
    assert outputs[0] == outputs[1]

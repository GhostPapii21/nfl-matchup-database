from copy import deepcopy
import json
from pathlib import Path
import pytest
from research.market_calibration.joint_trial_adapter import adapt_joint_trials, contract_info
from research.market_calibration.manifest import validate_manifest

ROOT = Path(__file__).resolve().parents[1]


def trial():
    """Synthetic transport fixture only, not a real frozen producer forecast."""
    from hashlib import sha256
    row = dict(
        contract_version="1.0.0", forecast_id="sha256:" + "a" * 64,
        trial_id="sha256:" + "a" * 64 + "/trial/0", trial_index=0,
        game=dict(game_id="canonical-fixture", game_id_namespace="test", season=2026,
                  season_type="REG", week=9, home_team_id="BAL", away_team_id="JAX",
                  kickoff_utc="2026-11-06T01:15:00Z", crosswalk_ref="fixture-crosswalk"),
        freeze=dict(cutoff_utc="2026-11-05T20:00:00Z", frozen_at_utc="2026-11-05T20:00:00Z",
                    generated_at_utc="2026-11-05T20:01:00Z", input_content_hash="sha256:" + "b" * 64,
                    input_manifest_ref="fixture-manifest", input_manifest_hash="sha256:" + "c" * 64,
                    mode="data_only", config_id="fixture", split_manifest_id="fixture-splits",
                    split_manifest_hash="sha256:" + "d" * 64),
        engine=dict(engine_version="e" * 40, component_versions={}, dependency_versions={},
                    ot_rule_profile="fixture-no-official-rules-claim", stat_credit_profile="fixture",
                    limitations=["SYNTHETIC_SCORE_TRANSPORT_FIXTURE"]),
        rng=dict(seed="31", rng_algorithm="fixture", rng_version="fixture", seed_derivation_version="v1"),
        status="COMPLETE", completion_reason="fixture", terminal_state="final", went_ot=False,
        latent_state={}, events=[], possessions=[], team_periods=[], player_periods=[], aggregates={},
        feature_availability={k: dict(status="UNKNOWN" if k == "coverage" else "MISSING",
            value=None, allows_sim_effect=False) for k in
            ("coverage", "routes", "personnel_11", "personnel_12", "personnel_13")},
        provenance={"fixture": True}, flags=[], validation={"status": "NOT_RUN"})
    material = ["v1", "31", "test", "canonical-fixture", row["freeze"]["input_content_hash"], 0]
    row["rng"]["trial_seed"] = str(int.from_bytes(sha256(json.dumps(material, separators=(",", ":"),
        sort_keys=True).encode()).digest()[:8], "big"))
    for quarter, home, away in [("Q1", 3, 10), ("Q2", 0, 7), ("Q3", 0, 3), ("Q4", 17, 0)]:
        row["team_periods"].extend([dict(team_id="BAL", period_id=quarter, points=home),
                                    dict(team_id="JAX", period_id=quarter, points=away)])
    return row


def test_adapter_retains_joint_trial_and_seed_without_player_targets():
    source = trial()
    rows = adapt_joint_trials([source])
    assert rows[0].trial_id == source["trial_id"] and rows[0].seed == "31"
    assert rows[0].trial_seed == source["rng"]["trial_seed"]
    assert rows[0].forecast_id == source["forecast_id"]
    assert rows[0].scorecard.points("H1") == (3, 17)
    assert not hasattr(rows[0], "player_targets")
    assert rows[0].source["feature_availability"] == source["feature_availability"]
    assert rows[0].actionable_status == "NOLINE"
    assert rows[0].interface_status == "CONTRACT_SCORE_TRANSPORT_ONLY"
    info = contract_info()
    assert info["status"] == "CONTRACT_SCORE_TRANSPORT_ONLY"
    assert info["sha256"]


@pytest.mark.parametrize("field,value", [("trial_id", None), ("trial_index", True),
    ("rng", {}), ("team_periods", []), ("status", "INCOMPLETE"), ("game", {})])
def test_adapter_rejects_incomplete_or_invalid_trials(field, value):
    row = trial()
    row[field] = value
    with pytest.raises(ValueError):
        adapt_joint_trials([row])


def test_duplicate_trial_ids_refused_even_with_other_seed():
    other = trial()
    other["rng"]["seed"] = "32"
    with pytest.raises(ValueError):
        adapt_joint_trials([trial(), other])


def test_seed_derivation_and_forecast_population():
    row = trial()
    row["rng"]["trial_seed"] = "0"
    with pytest.raises(ValueError):
        adapt_joint_trials([row])
    with pytest.raises(ValueError):
        adapt_joint_trials([trial()], expected_trial_ids=["absent"])


def test_missing_ot_is_not_zero_and_duplicate_period_rejected():
    row = trial()
    row["went_ot"] = True
    with pytest.raises(ValueError):
        adapt_joint_trials([row])
    row = trial()
    row["team_periods"].append(row["team_periods"][0])
    with pytest.raises(ValueError):
        adapt_joint_trials([row])


def test_actual_manifest_is_honest():
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    validate_manifest(manifest, ROOT)
    assert manifest["calibration"]["status"] == "UNIMPLEMENTED_NO_FITTED_CALIB"
    assert manifest["anchored"]["status"] == "PENDING_VALIDATION"
    assert manifest["data_policy"]["weeks_1_8_2026"] == "development_inspected"


@pytest.mark.parametrize("section", ["calibration", "anchored", "validation", "adapter"])
@pytest.mark.parametrize("claim", ["FITTED", "OK", "VALIDATED"])
def test_manifest_cannot_claim_absent_success(section, claim):
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    manifest[section]["status"] = claim
    with pytest.raises(ValueError):
        validate_manifest(manifest, ROOT)


def test_manifest_missing_artifacts_and_mislabelled_holdout_refused():
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    broken = deepcopy(manifest)
    broken["artifacts"].append("artifacts/does-not-exist.json")
    with pytest.raises(ValueError):
        validate_manifest(broken, ROOT)
    broken = deepcopy(manifest)
    broken["data_policy"]["weeks_1_8_2026"] = "untouched_holdout"
    with pytest.raises(ValueError):
        validate_manifest(broken, ROOT)

"""Adversarial second review after the first green run: no performance claims."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest
from market_calibration.calibration import CalibrationBias, separate_outputs, score_predictions, validate_splits
from market_calibration.manifest import validate_manifest
from market_calibration.quotes import load_saved_quotes, match_quote
from market_calibration.joint_trial_adapter import adapt_joint_trials
from test_quotes import request
from test_calibration import provenance
from test_contract_manifest import trial

ROOT = Path(__file__).resolve().parents[1]


def raw_for(match):
    q = next(q for q in match.quotes if q.side == match.requested_side)
    identity = {k: getattr(q, k) for k in ("game_id", "market", "period", "side", "line", "settlement", "team")}
    identity["game_id_namespace"] = "saved_csv_game_id"
    return {"p_win": .7, "probability_basis": match.comparison_basis, "market_identity": identity}


@pytest.mark.parametrize("changes", [{"period": "H1"}, {"side": "BAL"}, {"line": -6.5},
    {"game_id": "OTHER"}, {"game_id_namespace": "canonical"}, {"settlement": "winner_3way"}])
def test_unrelated_raw_cannot_be_anchored(changes):
    matched = match_quote(load_saved_quotes(), request())
    raw = raw_for(matched)
    raw["market_identity"].update(changes)
    assert separate_outputs(raw, matched, raw_weight=.3)["market_anchored_output"]["p_win"] is None


def test_missing_raw_identity_and_probability_basis_blocked():
    matched = match_quote(load_saved_quotes(), request())
    raw = raw_for(matched)
    raw.pop("market_identity")
    assert separate_outputs(raw, matched, raw_weight=.3)["market_anchored_output"]["p_win"] is None
    raw = raw_for(matched)
    raw["probability_basis"] = "three_way_unconditional"
    assert separate_outputs(raw, matched, raw_weight=.3)["market_anchored_output"]["p_win"] is None


def test_fit_refuses_development_inspected_and_tnf_even_when_requested_as_train():
    for p in (provenance(split="development"), provenance(week=8),
              provenance(game_id="401873037"), provenance(inspected=True)):
        with pytest.raises(ValueError, match="train"):
            CalibrationBias().fit([p])


def test_scoring_rejects_anchored_family_and_mixed_split():
    p = provenance(prediction_family="MARKET_ANCHORED")
    with pytest.raises(ValueError):
        score_predictions([(.7, 1, p)], scoring_label="baseline")
    with pytest.raises(ValueError):
        score_predictions([(.7, 1, provenance()), (.7, 1, provenance(game_id="other", split="holdout"))],
                          scoring_label="baseline")


def test_same_game_cannot_escape_split_gate_through_changed_season():
    with pytest.raises(ValueError):
        validate_splits([provenance(), provenance(season=2025, split="holdout")])


@pytest.mark.parametrize("section,key,value", [("quotes", "status", "OK"),
    ("adapter", "full_core_acceptance", "OK"), ("anchored", "predictions_provided", True),
    ("adapter", "contract_sha256", "a" * 64)])
def test_manifest_cannot_overclaim_in_other_fields(section, key, value):
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    manifest[section][key] = value
    with pytest.raises(ValueError):
        validate_manifest(manifest, ROOT)


@pytest.mark.parametrize("mutation", ["missing_feature", "false_missingness_effect", "mixed_seed", "null_profile"])
def test_trial_transport_preserves_missingness_and_freeze_consistency(mutation):
    row = trial()
    if mutation == "missing_feature":
        del row["feature_availability"]["routes"]
    elif mutation == "false_missingness_effect":
        row["feature_availability"]["routes"]["allows_sim_effect"] = True
    elif mutation == "null_profile":
        row["engine"]["stat_credit_profile"] = None
    else:
        other = deepcopy(row)
        other["trial_index"] = 1
        other["trial_id"] = other["forecast_id"] + "/trial/1"
        other["rng"]["seed"] = "32"
        from market_calibration.joint_trial_adapter import derive_trial_seed
        other["rng"]["trial_seed"] = derive_trial_seed(other)
        with pytest.raises(ValueError):
            adapt_joint_trials([row, other])
        return
    with pytest.raises(ValueError):
        adapt_joint_trials([row])


def test_valid_ot_remains_separate_and_metadata_is_copied():
    source = trial()
    source["went_ot"] = True
    source["team_periods"].extend([dict(team_id="BAL", period_id="OT1", points=0),
                                   dict(team_id="JAX", period_id="OT1", points=3)])
    projected = adapt_joint_trials([source])[0]
    assert projected.scorecard.points("REG") == (20, 20)
    assert projected.scorecard.points("FG") == (20, 23)
    source["team_periods"][0]["points"] = 90
    assert projected.scorecard.points("H1") == (3, 17)
    assert projected.source["team_periods"][0]["points"] == 3

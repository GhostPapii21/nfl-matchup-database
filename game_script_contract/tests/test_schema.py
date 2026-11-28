"""Scenario-output schema: structure plus semantic coherence (no faked or missing dimensions)."""
import copy

import jsonschema
import pytest

from game_script_contract.allocation import assert_valid, errors, validate_payload, ContractError
from game_script_contract.schema import BRANCH_IDS, DIMENSIONS, ScenarioOutput, load_json_schema
from game_script_contract.tests._synthetic import fresh


def codes(f):
    return {x.code for x in errors(f)}


def test_schema_is_valid_draft_2020_12():
    jsonschema.Draft202012Validator.check_schema(load_json_schema())


def test_schema_requires_all_ten_dimensions():
    s = load_json_schema()
    assert set(s["$defs"]["dimension_status"]["required"]) == set(DIMENSIONS) and len(DIMENSIONS) == 10
    assert set(s["properties"]["branches"]["required"]) == set(BRANCH_IDS)
    assert s["properties"]["branches"]["additionalProperties"] is False


def test_well_formed_differentiated_payload_passes():
    p = fresh()
    assert validate_payload(p) == []
    assert_valid(p)
    obj = ScenarioOutput.from_dict(p)
    assert set(obj.branches) == set(BRANCH_IDS)
    assert obj.branches["competitive"].players[0].targets.samples


def test_schema_rejects_missing_branch_and_extra_fields():
    p = fresh(); del p["branches"]["underdog_chases"]
    assert "SCHEMA" in codes(validate_payload(p))
    p = fresh(); p["branches"]["blowout"] = copy.deepcopy(p["branches"]["competitive"])
    assert "SCHEMA" in codes(validate_payload(p))
    p = fresh(); p["branches"]["competitive"]["pooled_mean"] = 1.0
    assert "SCHEMA" in codes(validate_payload(p))


def test_distribution_must_be_priceable():
    p = fresh()
    p["branches"]["competitive"]["players"][0]["targets"] = {"mean": 5.0}    # point estimate only
    assert "SCHEMA" in codes(validate_payload(p))


def test_not_modeled_dimension_cannot_carry_values():
    p = fresh()
    p["branches"]["competitive"]["dimension_status"]["pressure_coverage"] = {"status": "not_modeled", "reason": "x", "source": None}
    assert "FAKED_DIMENSION" in codes(validate_payload(p))


def test_modeled_dimension_cannot_be_null():
    p = fresh()
    for t in p["branches"]["favorite_controls"]["teams"].values():
        t["sec_per_play"] = None
    assert "MISSING_DIMENSION_OUTPUT" in codes(validate_payload(p))


def test_every_branch_carries_the_same_players():
    p = fresh()
    p["branches"]["underdog_chases"]["players"].pop()
    assert "PLAYER_SET_MISMATCH" in codes(validate_payload(p))


def test_samples_must_come_from_the_branch_trials():
    p = fresh()
    pl = p["branches"]["competitive"]["players"][0]
    pl["targets"]["samples"] = pl["targets"]["samples"][:-3]
    assert "SAMPLE_COUNT_MISMATCH" in codes(validate_payload(p))


def test_hold_threshold_must_match_one_score():
    p = fresh()
    p["branch_definition"]["one_score_max_deficit"] = 7   # hold still 9; 7+1 != 9
    assert "DEFINITION_HOLD_INCONSISTENT" in codes(validate_payload(p))


def test_schema_rejects_nonpositive_q3_threshold_and_underdog_ahead_outside_b():
    p = fresh()
    p["branch_definition"]["q3_control_margin"] = 0
    assert "SCHEMA" in codes(validate_payload(p))
    p = fresh()
    p["branch_definition"]["competitive_includes_underdog_ahead"] = False
    assert "SCHEMA" in codes(validate_payload(p))


def test_assert_valid_raises():
    p = fresh(); p["branches"]["competitive"]["probability"] = 0.9
    with pytest.raises(ContractError):
        assert_valid(p)

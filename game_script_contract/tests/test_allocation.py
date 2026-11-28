"""Probability-allocation contract: exactly three branches whose probabilities total 100%."""
import json
import math

import pytest

from game_script_contract.allocation import (TOLERANCE, ContractError, errors, loads_strict, validate_allocation)
from game_script_contract.tests._synthetic import fresh

OK = {"favorite_controls": 0.35, "competitive": 0.45, "underdog_chases": 0.20}


def codes(f):
    return {x.code for x in errors(f)}


def test_valid_allocation_totals_100_percent():
    assert validate_allocation(dict(OK)) == []
    p = fresh()
    assert errors(validate_allocation(p)) == []
    assert math.isclose(sum(b["probability"] for b in p["branches"].values()), 1.0, abs_tol=TOLERANCE)


@pytest.mark.parametrize("probs", [
    {"favorite_controls": 0.35, "competitive": 0.44, "underdog_chases": 0.20},   # 99%
    {"favorite_controls": 0.35, "competitive": 0.46, "underdog_chases": 0.20},   # 101%
    {"favorite_controls": 1 / 3, "competitive": 1 / 3, "underdog_chases": 1 / 3 + 2e-6},
])
def test_rejects_totals_other_than_100_percent(probs):
    assert "PROBABILITY_SUM" in codes(validate_allocation(probs))


def test_tolerance_boundary():
    assert validate_allocation({"favorite_controls": 0.35, "competitive": 0.45, "underdog_chases": 0.20 + 5e-7}) == []


@pytest.mark.parametrize("bad,code", [
    (-0.05, "PROBABILITY_NEGATIVE"), (float("nan"), "PROBABILITY_NOT_FINITE"), (float("inf"), "PROBABILITY_NOT_FINITE"),
    ("0.2", "PROBABILITY_NOT_FINITE"), (None, "PROBABILITY_NOT_FINITE"), (True, "PROBABILITY_NOT_FINITE"),
    (1.2, "PROBABILITY_ABOVE_ONE"),
])
def test_rejects_invalid_probability_values(bad, code):
    probs = dict(OK, underdog_chases=bad)
    assert code in codes(validate_allocation(probs))


def test_negative_branch_cannot_be_offset_by_another():
    probs = {"favorite_controls": 0.6, "competitive": 0.5, "underdog_chases": -0.1}   # sums to 1.0
    assert codes(validate_allocation(probs)) == {"PROBABILITY_NEGATIVE"}


def test_rejects_missing_branch():
    probs = {"favorite_controls": 0.5, "competitive": 0.5}
    assert "BRANCH_MISSING" in codes(validate_allocation(probs))


def test_rejects_extra_branch():
    probs = dict(OK, blowout=0.0)
    assert "BRANCH_EXTRA" in codes(validate_allocation(probs))


def test_rejects_fourth_branch_even_when_three_named_total_100():
    probs = {"favorite_controls": 0.3, "competitive": 0.4, "underdog_chases": 0.3, "garbage_time": 0.0}
    assert "BRANCH_EXTRA" in codes(validate_allocation(probs))


def test_rejects_duplicate_branch_key_in_json():
    text = '{"favorite_controls": 0.3, "competitive": 0.4, "competitive": 0.4, "underdog_chases": 0.3}'
    with pytest.raises(ContractError, match="duplicate key"):
        loads_strict(text)
    assert loads_strict(json.dumps(OK)) == OK


def test_branch_id_must_match_key():
    p = fresh()
    p["branches"]["competitive"]["branch_id"] = "favorite_controls"
    assert "BRANCH_ID_MISMATCH" in codes(validate_allocation(p))


def test_trial_partition_probabilities_match_counts():
    p = fresh()
    p["branches"]["competitive"]["probability"] += 0.01
    p["branches"]["underdog_chases"]["probability"] -= 0.01
    assert "COUNT_PROBABILITY_MISMATCH" in codes(validate_allocation(p))
    p = fresh()
    p["branches"]["competitive"]["n_trials"] += 5
    assert "COUNT_TOTAL_MISMATCH" in codes(validate_allocation(p))

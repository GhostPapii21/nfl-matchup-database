"""Duplicated scenario outputs: shared objects, identical / near-identical payloads, copied dimensions."""
import copy

from game_script_contract.allocation import detect_duplicate_branches, errors
from game_script_contract.tests._synthetic import fresh


def codes(f):
    return {x.code for x in errors(f)}


def test_clean_payload_has_no_duplicates():
    assert errors(detect_duplicate_branches(fresh())) == []


def test_same_branch_object_reused():
    p = fresh()
    p["branches"]["underdog_chases"] = p["branches"]["competitive"]
    assert p["branches"]["underdog_chases"] is p["branches"]["competitive"]
    assert "SHARED_BRANCH_OBJECT" in codes(detect_duplicate_branches(p))


def test_shared_sub_object_copy_by_reference():
    p = fresh()
    p["branches"]["underdog_chases"]["players"] = p["branches"]["competitive"]["players"]
    f = detect_duplicate_branches(p)
    assert any(x.code == "SHARED_SUBOBJECT" and "players" in x.message for x in f)


def test_deep_copied_identical_branch():
    p = fresh()
    p["branches"]["underdog_chases"] = copy.deepcopy(p["branches"]["competitive"])
    p["branches"]["underdog_chases"]["branch_id"] = "underdog_chases"
    assert "IDENTICAL_BRANCH_PAYLOAD" in codes(detect_duplicate_branches(p))


def test_identical_except_probability_and_counts():
    p = fresh()
    dup = copy.deepcopy(p["branches"]["competitive"])
    dup.update(branch_id="favorite_controls", probability=p["branches"]["favorite_controls"]["probability"],
               n_trials=p["branches"]["favorite_controls"]["n_trials"])
    p["branches"]["favorite_controls"] = dup
    assert "IDENTICAL_BRANCH_PAYLOAD" in codes(detect_duplicate_branches(p))


def test_near_identical_branch():
    p = fresh()
    dup = copy.deepcopy(p["branches"]["competitive"])
    dup["branch_id"] = "underdog_chases"
    dup["teams"]["FAV"]["points"]["samples"][0] *= (1 + 1e-12)
    p["branches"]["underdog_chases"] = dup
    assert "NEAR_IDENTICAL_BRANCH_PAYLOAD" in codes(detect_duplicate_branches(p, rel_tol=1e-9))
    assert "NEAR_IDENTICAL_BRANCH_PAYLOAD" not in codes(detect_duplicate_branches(p, rel_tol=0.0))


def test_one_dimension_copied_between_branches():
    p = fresh()
    a, b = p["branches"]["favorite_controls"], p["branches"]["competitive"]
    for tm in ("FAV", "DOG"):
        b["teams"][tm]["sec_per_play"] = copy.deepcopy(a["teams"][tm]["sec_per_play"])
    f = detect_duplicate_branches(p)
    assert any(x.code == "DUPLICATED_DIMENSION" and x.location.endswith(":pace") for x in f)
    assert any(x.code == "DUPLICATED_FIELD" for x in f)

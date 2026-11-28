"""Branch pooling detectors: collapsed means, identical distributions, pooled scores, mis-ordered branches."""
import copy

from game_script_contract.allocation import detect_branch_pooling, errors, validate_payload
from game_script_contract.schema import BRANCH_IDS
from game_script_contract.tests._synthetic import fresh, payload


def codes(f):
    return {x.code for x in errors(f)}


def test_clean_payload_has_no_pooling():
    assert errors(detect_branch_pooling(fresh())) == []


def test_all_branches_replaced_by_pooled_distribution():
    p, t, _ = payload()
    pooled = list(map(float, t["players"]["fav_wr1"]["targets"]))
    for b in BRANCH_IDS:
        pl = next(x for x in p["branches"][b]["players"] if x["player_id"] == "fav_wr1")
        pl["targets"] = {"samples": list(pooled)}
    f = detect_branch_pooling(p)
    assert any(x.code == "BRANCH_DISTRIBUTIONS_IDENTICAL" and x.location == "players.fav_wr1.targets" for x in f)


def test_branch_means_collapsed_to_overall_mean():
    p = fresh()
    for b, shape in zip(BRANCH_IDS, ([6, 8], [5, 9], [4, 10])):   # same mean 7, different shapes
        pl = next(x for x in p["branches"][b]["players"] if x["player_id"] == "dog_wr1")
        pl["targets"] = {"pmf": {str(shape[0]): 0.5, str(shape[1]): 0.5}}
    assert any(x.code == "BRANCH_MEANS_COLLAPSED" for x in detect_branch_pooling(p))


def test_pooled_score_samples_violate_branch_definition():
    p, t, _ = payload()
    br = p["branches"]["competitive"]
    n = br["n_trials"]
    # First n unfiltered trials include A and C games, so they violate the competitive definition.
    for team, q in (("FAV", t["qf"]), ("DOG", t["qd"])):
        for k in range(4):
            br["teams"][team]["quarter_points"][f"q{k + 1}"] = {"samples": q[:n, k].astype(float).tolist()}
        br["teams"][team]["points"] = {"samples": q[:n].sum(1).astype(float).tolist()}
    assert "SCORE_OUTSIDE_BRANCH" in codes(detect_branch_pooling(p))


def test_mislabeled_branches_out_of_order():
    p = fresh()
    a, c = p["branches"]["favorite_controls"], p["branches"]["underdog_chases"]
    a["teams"], c["teams"] = c["teams"], a["teams"]
    assert {"SCORE_OUTSIDE_BRANCH", "BRANCH_ORDER_VIOLATION"} <= codes(detect_branch_pooling(p))


def test_derived_behaviour_is_visible_as_warning():
    p = fresh()
    p["branches"]["competitive"]["dimension_status"]["pass_run"]["status"] = "derived"
    f = detect_branch_pooling(p)
    assert any(x.code == "DERIVED_NOT_MODELED" and x.severity == "warning" for x in f)
    assert errors(f) == []


def test_validate_payload_surfaces_pooling():
    p, t, _ = payload()
    pooled = list(map(float, t["fav_pass"]))
    for b in BRANCH_IDS:
        p["branches"][b]["teams"]["FAV"]["pass_attempts"] = {"samples": copy.copy(pooled)}
    c = codes(validate_payload(p))
    assert "BRANCH_DISTRIBUTIONS_IDENTICAL" in c and "SAMPLE_COUNT_MISMATCH" in c

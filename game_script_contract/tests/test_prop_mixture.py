"""Prop probabilities are per-branch mixtures, never computed from an averaged (pooled) stat line."""
import math

import numpy as np
import pytest

from game_script_contract.allocation import ContractError, check_prop_probability, dist_mean, prop_probability
from game_script_contract.schema import BRANCH_IDS
from game_script_contract.tests._synthetic import fresh, payload


def test_mixture_is_probability_weighted_sum_of_branch_conditionals():
    p = fresh()
    r = prop_probability(p, player_id="dog_wr1", stat="targets", line=8.5, side="over")
    manual = 0.0
    for b in BRANCH_IDS:
        s = np.asarray(next(x for x in p["branches"][b]["players"] if x["player_id"] == "dog_wr1")["targets"]["samples"])
        manual += p["branches"][b]["probability"] * float((s > 8.5).mean())
    assert math.isclose(r["probability"], manual, abs_tol=1e-12)
    assert r["method"] == "branch_mixture_v1"


def test_mixture_equals_unconditional_rate_for_a_trial_partition():
    p, t, labels = payload()
    r = prop_probability(p, player_id="fav_rb1", stat="carries", line=15.5, side="over")
    assert math.isclose(r["probability"], float((t["players"]["fav_rb1"]["carries"] > 15.5).mean()), abs_tol=1e-12)


def test_branches_give_different_conditionals():
    r = prop_probability(fresh(), player_id="fav_rb1", stat="carries", line=15.5)
    c = {b: v["conditional"] for b, v in r["per_branch"].items()}
    assert c["favorite_controls"] > c["competitive"] > c["underdog_chases"]


def _pooled_poisson(p, pid, stat, line):
    mu = sum(b["probability"] * dist_mean(next(x for x in b["players"] if x["player_id"] == pid)[stat])
             for b in p["branches"].values())
    return 1 - sum(math.exp(k * math.log(mu) - mu - math.lgamma(k + 1)) for k in range(int(math.floor(line)) + 1))


def test_prop_from_averaged_stat_line_is_detected():
    p = fresh()
    pooled = _pooled_poisson(p, "fav_rb1", "carries", 19.5)
    mix = prop_probability(p, player_id="fav_rb1", stat="carries", line=19.5)["probability"]
    assert abs(pooled - mix) > 0.005, "fixture must make pooling matter"
    f = check_prop_probability(p, pooled, player_id="fav_rb1", stat="carries", line=19.5)
    assert [x.code for x in f] == ["PROP_NOT_BRANCH_MIXTURE"] and "Poisson(pooled mean)" in f[0].message
    assert check_prop_probability(p, mix, player_id="fav_rb1", stat="carries", line=19.5) == []


def test_pricing_off_one_branch_is_detected():
    p = fresh()
    one = prop_probability(p, player_id="dog_wr1", stat="targets", line=8.5)["per_branch"]["competitive"]["conditional"]
    f = check_prop_probability(p, one, player_id="dog_wr1", stat="targets", line=8.5)
    assert f and "single branch competitive only" in f[0].message


def test_point_estimate_vs_line_is_detected():
    p = fresh()
    f = check_prop_probability(p, 1.0, player_id="fav_rb1", stat="carries", line=10.5)
    assert f and "indicator(pooled mean vs line)" in f[0].message


def test_refuses_to_borrow_another_branch_when_distribution_missing():
    p = fresh()
    next(x for x in p["branches"]["underdog_chases"]["players"] if x["player_id"] == "fav_rb1")["carries"] = None
    with pytest.raises(ContractError, match="refusing to borrow"):
        prop_probability(p, player_id="fav_rb1", stat="carries", line=15.5)


def test_refuses_invalid_allocation():
    p = fresh(); p["branches"]["competitive"]["probability"] = 0.0
    with pytest.raises(ContractError, match="allocation invalid"):
        prop_probability(p, player_id="fav_rb1", stat="carries", line=15.5)


def test_team_props_and_push_handling():
    p = fresh()
    over = prop_probability(p, team="FAV", stat="points", line=24, side="over")
    under = prop_probability(p, team="FAV", stat="points", line=24, side="under")
    assert math.isclose(over["probability"] + under["probability"] + over["push"], 1.0, abs_tol=1e-9)

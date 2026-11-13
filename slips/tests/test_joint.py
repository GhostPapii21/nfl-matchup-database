"""Deterministic tests for slips.joint (item 8 / Phase 6). Synthetic trials with exactly known answers."""
import math
import numpy as np
import pytest

from slips.joint import Leg, leg_hits, joint_from_hits, slip_probability, actual_hits, wilson


def sim_from(home, away, players):
    return {"arrays": {"fg_home": np.asarray(home), "fg_away": np.asarray(away)}, "player_samples": players}


def test_perfectly_correlated_legs_joint_equals_marginal_not_product():
    # QB and WR yards move together: both hit in exactly the same 5 of 10 trials
    ps = [{"pass_yards|NYG|QB": 300.0, "rec_yards|NYG|WR": 100.0} if i < 5 else
          {"pass_yards|NYG|QB": 150.0, "rec_yards|NYG|WR": 20.0} for i in range(10)]
    r = slip_probability(sim_from([0] * 10, [0] * 10, ps),
                         [Leg("pass_yards", "NYG|QB", ">=", 250), Leg("rec_yards", "NYG|WR", ">=", 60)])
    assert r["p_joint"] == 0.5
    assert r["p_independent"] == 0.25
    assert r["lift_joint_over_independent"] == 2.0


def test_mutually_exclusive_legs_joint_zero():
    r = slip_probability(sim_from([30, 10, 30, 10], [10, 30, 10, 30], []),
                         [Leg("game", "home_margin", ">", 0), Leg("game", "home_margin", "<", 0)])
    assert r["p_joint"] == 0.0 and r["p_independent"] == 0.25


def test_independent_grid_joint_equals_product():
    # 4 trials covering every (A, B) combination once: joint = product exactly
    h, a = [20, 20, 40, 40], [20, 40, 20, 40]
    r = slip_probability(sim_from(h, a, []), [Leg("game", "home_pts", ">", 30), Leg("game", "away_pts", ">", 30)])
    assert r["p_joint"] == r["p_independent"] == 0.25


def test_game_keys_and_ops():
    s = sim_from([24, 17], [20, 21], [])
    assert leg_hits(s, [Leg("game", "total", "<", 40.5)]).ravel().tolist() == [False, True]
    assert leg_hits(s, [Leg("game", "total", "<=", 38)]).ravel().tolist() == [False, True]
    assert leg_hits(s, [Leg("game", "home_margin", ">=", 4)]).ravel().tolist() == [True, False]


def test_player_missing_from_some_trials_counts_zero():
    ps = [{"rush_yards|WAS|RB": 80.0}, {}]
    h = leg_hits(sim_from([0, 0], [0, 0], ps), [Leg("rush_yards", "WAS|RB", "<", 10)])
    assert h.ravel().tolist() == [False, True]


def test_player_missing_from_every_trial_raises():
    with pytest.raises(KeyError):
        leg_hits(sim_from([0], [0], [{}]), [Leg("rec_yards", "NYG|Ghost", ">=", 1)])


def test_bad_legs_rejected():
    with pytest.raises(ValueError):
        Leg("game", "spread", ">", 0)
    with pytest.raises(ValueError):
        Leg("rec_yards", "Nabers", ">", 0)
    with pytest.raises(ValueError):
        Leg("rec_yards", "NYG|Nabers", "=", 0)
    with pytest.raises(ValueError):
        joint_from_hits(np.zeros((0, 2), dtype=bool))


def test_wilson_bounds():
    lo, hi = wilson(50, 100)
    assert lo < 0.5 < hi and math.isclose(lo + hi, 1.0, abs_tol=1e-12)
    assert wilson(0, 10)[0] == 0.0


def test_actual_hits_and_void():
    legs = [Leg("game", "total", "<", 54.5), Leg("rec_yards", "NYG|WR", ">=", 40)]
    act = {"home_pts": 24, "away_pts": 21, "players": {"rec_yards|NYG|WR": 44.0}}
    assert actual_hits(act, legs) == [True, True]
    assert actual_hits({**act, "players": {}}, legs) is None  # did not play -> void


def test_deterministic_for_fixed_trials():
    rng = np.random.default_rng(7)
    ps = [{"rec_yards|NYG|WR": float(x)} for x in rng.integers(0, 120, 500)]
    s = sim_from(rng.integers(0, 40, 500), rng.integers(0, 40, 500), ps)
    legs = [Leg("rec_yards", "NYG|WR", ">=", 40), Leg("game", "total", "<", 45.5)]
    assert slip_probability(s, legs) == slip_probability(s, legs)

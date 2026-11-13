"""Integration: slip probability straight from a real (tiny, seeded) engine run. Deterministic for a fixed seed."""
import pytest
from calibration.common import PBP, engine_path, make_cfg
from slips.joint import Leg, slip_probability

pytestmark = pytest.mark.skipif(not PBP.exists(), reason="nflverse PBP parquet not present")


def _run(seed):
    engine_path()
    import simulate
    return simulate.simulate_games(make_cfg("NYG", "WAS", 10), pbp_path=str(PBP), n=12, seed=seed)


def test_engine_joint_vs_independent_and_reproducible():
    o = _run(20261113)
    qb = max(((k.split("|", 2)[2], v) for t in o["player_samples"] for k, v in t.items() if k.startswith("pass_yards|NYG|")),
             key=lambda kv: kv[1])[0]
    legs = [Leg("pass_yards", f"NYG|{qb}", ">=", 150), Leg("game", "home_pts", ">=", 17)]
    r1 = slip_probability(o, legs)
    r2 = slip_probability(_run(20261113), legs)
    assert r1 == r2
    assert r1["n_trials"] == 12 and 0.0 <= r1["p_joint"] <= min(r1["marginals"])
    assert abs(r1["p_independent"] - r1["marginals"][0] * r1["marginals"][1]) < 1e-12

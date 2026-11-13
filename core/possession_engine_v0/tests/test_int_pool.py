"""NFL-75 Phase 2b: opt-in team INT pooling (int_pool.py). Written before the backtest.

1. Default (int_pool=None) is bit-identical to main: golden digests from main 6bc0c54 (same harness as
   test_opportunity.py) and no "int_pool" block.
2. m = 0 (p* = the team's own rate, q_up = q_down = 0) draws only from int_pool's own RNG: every output block is
   byte-identical to the default run.
3. A team with no INT row in its pool throws interceptions once pooled (the engine-level cap is removed), at about
   the pooled rate; a team above the league rate is pulled down.
4. Guards: refused from a config, refused above the research cap, refused by lock.run_sim, schema/range checks.
Research only. projection_ready stays false."""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _opportunity_golden as G  # noqa: E402

needs_pbp = pytest.mark.skipif(not __import__("_player_box_golden").PBP.exists(),
                               reason="committed nflverse W1-9 PBP missing")
GOLD = json.loads((Path(__file__).resolve().parent / "opportunity_golden_main_6bc0c54.json").read_text())
SPEC = {"schema": "nfl75-int-pool/1", "league_rate": 0.022, "m": 1200.0}
_CACHE: dict = {}


def _run(name, seed, ip=None, n=None):
    key = (name, seed, json.dumps(ip, sort_keys=True), n)
    if key not in _CACHE:
        kw = {"int_pool": ip} if ip is not None else {}
        _CACHE[key] = G.run(name, n or G.N, seed, **kw)
    return _CACHE[key]


@needs_pbp
@pytest.mark.parametrize("name", G.VARIANTS)
def test_default_is_bit_identical_to_main(name):
    seed = G.SEEDS[0]
    out = _run(name, seed)
    assert "int_pool" not in out
    assert G.digest(out) == GOLD["digests"][f"{name}|{seed}"]


@needs_pbp
def test_m_zero_draws_only_its_own_rng():
    seed = G.SEEDS[0]
    out = _run("was_nyg_lock", seed, {**SPEC, "m": 0.0})
    assert G.digest(out) == GOLD["digests"][f"was_nyg_lock|{seed}"]
    assert out["int_pool"]["counts"]["to_int"] == 0 and out["int_pool"]["counts"]["to_incomplete"] == 0
    assert out["int_pool"]["counts"]["attempts_seen"] > 0


def _pool(n_att, n_int):
    rows = [{"play_type": "pass", "sack": 0, "interception": 1 if i < n_int else 0, "complete_pass": 0 if i < n_int else 1,
             "yards_gained": 0.0 if i < n_int else 7.0, "touchdown": 0, "fumble_lost": 0,
             "interception_player_name": "D.Back" if i < n_int else None} for i in range(n_att)]
    rows += [{"play_type": "run", "sack": 0, "interception": 0, "complete_pass": 0, "yards_gained": 4.0,
              "touchdown": 0, "fumble_lost": 0, "interception_player_name": None}] * 50
    rows += [{"play_type": "pass", "sack": 1, "interception": 0, "complete_pass": 0, "yards_gained": -6.0,
              "touchdown": 0, "fumble_lost": 0, "interception_player_name": None}] * 10
    return pd.DataFrame(rows)


class _St:
    def __init__(self, team):
        self.possession = team


def test_zero_int_team_can_throw_one_and_rates_hit_target():
    from int_pool import IntPool
    ip = IntPool({"schema": "nfl75-int-pool/1", "league_rate": 0.025, "m": 400.0},
                 {"CLEAN": _pool(200, 0), "SLOPPY": _pool(100, 10)}, np.random.default_rng(1))
    t = ip.table
    assert t["CLEAN"]["att"] == 200 and t["CLEAN"]["int"] == 0  # sacks are not attempts
    assert t["CLEAN"]["p_star"] == pytest.approx(400 * 0.025 / 600)
    assert t["SLOPPY"]["p_star"] == pytest.approx((10 + 400 * 0.025) / 500)
    for team in ("CLEAN", "SLOPPY"):
        pool = _pool(t[team]["att"], t[team]["int"])
        att = pool[(pool.play_type == "pass") & (pool.sack != 1)]
        rows = [att.iloc[i] for i in range(len(att))]
        draws = [ip.apply(_St(team), rows[i % len(rows)]) for i in range(100_000)]
        rate = np.mean([int(r["interception"]) for r in draws])
        assert rate == pytest.approx(t[team]["p_star"], abs=0.003)
        conv = [r for r in draws if int(r["interception"]) == 1 and r["interception_player_name"] is None]
        if team == "CLEAN":  # converted rows: an INT at the line of scrimmage with no defender credit
            assert conv and all(r["yards_gained"] == 0.0 and r["complete_pass"] == 0 for r in conv)


def test_runs_and_sacks_are_never_touched_and_draw_nothing():
    from int_pool import IntPool
    rng = np.random.default_rng(5)
    ip = IntPool({**SPEC, "m": 1e9}, {"T": _pool(10, 0)}, rng)
    state = rng.bit_generator.state
    p = _pool(10, 0)
    for _, row in pd.concat([p[p.play_type == "run"].head(5), p[p.sack == 1].head(5)]).iterrows():
        assert ip.apply(_St("T"), row) is row
    assert rng.bit_generator.state == state


def test_spec_validation():
    from int_pool import validate
    with pytest.raises(ValueError):
        validate({"schema": "x", "league_rate": 0.02, "m": 1})
    with pytest.raises(ValueError):
        validate({**SPEC, "league_rate": 0.7})
    with pytest.raises(ValueError):
        validate({**SPEC, "m": -1})


@needs_pbp
def test_opt_in_changes_ints_and_is_labelled():
    seed = G.SEEDS[0]
    out = _run("was_nyg_lock", seed, {**SPEC, "m": 1e9})
    b = out["int_pool"]
    assert b["label"].startswith("UNACCEPTED_RESEARCH_ONLY")
    assert b["counts"]["to_int"] + b["counts"]["to_incomplete"] > 0
    assert set(b["teams"]) >= {"WAS", "NYG"}


def test_int_pool_refused_above_research_cap_and_from_config():
    import simulate
    cfg, _ = __import__("_player_box_golden").variant_cfg("was_nyg_lock")
    with pytest.raises(ValueError, match="never 100k"):
        simulate.simulate_games(cfg, pbp_path=str(G.PBG.PBP), n=simulate.RESEARCH_MAX_N + 1, seed=1, int_pool=SPEC)
    c = dict(cfg)
    c["int_pool"] = SPEC
    with pytest.raises(ValueError, match="UNSUPPORTED"):
        simulate.simulate_games(c, pbp_path=str(G.PBG.PBP), n=2, seed=1)


def test_lock_path_refuses_int_pool():
    import inspect
    sys.path.insert(0, str(REPO))
    from snapshots import lock
    assert "int_pool" not in inspect.signature(lock.run_sim).parameters
    cfg, _ = __import__("_player_box_golden").variant_cfg("was_nyg_lock")
    c = dict(cfg)
    c["int_pool"] = SPEC
    with pytest.raises(ValueError, match="UNSUPPORTED"):
        lock.run_sim(c, str(G.PBG.PBP), 2, 1, 1)
    assert "int_pool" not in (REPO / "pipeline/sim100k.py").read_text()

import json

import numpy as np
import pytest

from engines.sim_v7 import data as D
from engines.sim_v7 import engine as E
from engines.sim_v7 import cli

REQUIRED = {"game_id", "player_id", "market", "method", "scenario", "trial_count", "seed", "distribution",
            "line_probabilities", "calibration_status", "input_hash", "source_cutoff", "execution_status"}
GAME = "2026_12_NO_CIN"


@pytest.fixture(scope="module")
def doc():
    return cli.simulate_game(GAME, n=3000, seed=11, batch=15_000, log=lambda *_: None)


def test_scenarios_disjoint():
    rng = np.random.default_rng(0)
    H, F = rng.integers(-30, 30, 50_000), rng.integers(-40, 40, 50_000)
    m = E.classify(H, F)
    tot = sum(v.astype(int) for v in m.values())
    assert tot.max() == 1


def test_no_future_leakage():
    cut = "2026-11-24"
    ctx = D.team_context("CIN", cut)
    P = D.load_pbp()
    dates = P[P.game_id.isin(ctx.game_ids)].game_date
    assert (dates < cut).all()
    assert set(ctx.drives.game_id) <= set(ctx.game_ids)
    lg = D.league_params(cut)
    assert lg["cutoff"] == cut


def test_recalibration_identity_is_noop_and_monotone():
    rng = np.random.default_rng(3)
    x = rng.gamma(2.0, 20.0, 20_000)  # float64: no ties
    y = E.apply_recalibration(x, np.linspace(0, 1, 101), np.random.default_rng(1))
    assert np.allclose(np.sort(x), np.sort(y))
    g = np.linspace(0, 1, 101) ** 1.3
    z = E.apply_recalibration(x, g, np.random.default_rng(1))
    o = np.argsort(x, kind="stable")
    assert np.all(np.diff(z[o]) >= -1e-6)       # monotone in x -> joint structure preserved
    assert np.median(z) < np.median(x)


def test_contract_fields_and_counts(doc):
    recs = doc["records"]
    assert recs and all(REQUIRED <= set(r) for r in recs)
    cells = {(r["method"], r["scenario"]) for r in recs}
    assert len(cells) == 9
    for r in recs:
        if r["execution_status"] == "OK":
            assert r["trial_count"] == 3000


def test_methods_are_distinct(doc):
    """Same player-market, same scenario: MC and GR must not be the same sampler."""
    by = {}
    for r in doc["records"]:
        if r["market"] in ("rec_yds", "rush_yds", "pass_yds") and r["scenario"] == "competitive":
            by.setdefault((r["player_id"], r["market"]), {})[r["method"]] = r["distribution"]
    diffs = [abs(v["mc"]["mean"] - v["gr"]["mean"]) + abs(v["mc"]["sd"] - v["gr"]["sd"]) for v in by.values() if "mc" in v and "gr" in v]
    assert len(diffs) > 5 and np.mean(diffs) > 1.0
    if cli.load_calib():
        bd = [abs(v["mc"]["median"] - v["bias"]["median"]) + abs(v["mc"]["p90"] - v["bias"]["p90"]) for v in by.values() if "bias" in v]
        assert np.mean(bd) > 0.1


def test_deterministic_seed():
    a = cli.simulate_game(GAME, n=1000, seed=5, batch=8000, methods=("mc", "gr"), log=lambda *_: None)
    b = cli.simulate_game(GAME, n=1000, seed=5, batch=8000, methods=("mc", "gr"), log=lambda *_: None)
    assert json.dumps(a["records"], default=float) == json.dumps(b["records"], default=float)


def test_player_production_tied_to_team_scoring():
    cfg, _ = cli.game_config(GAME)
    run = E.run_cells(cfg, methods=("mc", "gr"), scenarios=("competitive",), n=4000, batch=20_000, log=lambda *_: None)
    qb = run["ctxs"]["CIN"].players.gsis.iloc[0]
    for m in ("mc", "gr"):
        X = run["results"][m]["cells"]["competitive"]["X"]
        r = np.corrcoef(X[f"{qb}|passtd"], X["CIN|pts"])[0, 1]
        assert r > 0.2, (m, r)

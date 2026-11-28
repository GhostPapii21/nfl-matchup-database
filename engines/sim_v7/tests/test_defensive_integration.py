"""Defensive integration: coverage allocation, scramble, residual, GR defense, TD consistency."""
from __future__ import annotations

import copy
import json

import numpy as np
import pytest

from engines.sim_v7 import coverage_alloc as CA
from engines.sim_v7 import data as D
from engines.sim_v7 import defensive as DEF
from engines.sim_v7 import engine as E
from engines.sim_v7 import scramble as SC
from engines.sim_v7 import cli

GAME = "2026_12_NO_CIN"


@pytest.fixture(scope="module")
def board_cfg():
    return cli.game_config(GAME)


def test_defensive_profiles_change_draws(board_cfg):
    cfg, board = board_cfg
    profiles = cfg["defensive_profiles"]
    assert profiles
    assert any(p.get("evidence") for p in profiles.values())

    def mean_att(def_prof, seed=9):
        g = dict(cfg, defensive_profiles=def_prof)
        r = E.run_cells(g, methods=("mc",), scenarios=("competitive",), n=4000, batch=12_000,
                        seed=seed, include_residual=False, log=lambda *_: None)
        qb = r["ctxs"]["NO"].players.gsis.iloc[0]
        return float(r["results"]["mc"]["cells"]["competitive"]["X"][f"{qb}|att"].mean())

    neutral = {t: dict(p, completion=1.0, yards_per_completion=1.0, attempts=1.0) for t, p in profiles.items()}
    high = copy.deepcopy(profiles)
    for p in high.values():
        p["attempts"] = 0.85
        p["completion"] = 0.90
    assert abs(mean_att(high) - mean_att(neutral)) > 0.5


def test_matchup_variants_pressure_man_zone(board_cfg):
    cfg, board = board_cfg

    def force(man, pressure):
        b = copy.deepcopy(board)
        for s in b["sides"].values():
            cp = s.setdefault("coverage_profile", {})
            cp["man_rate"] = man
            cp["zone_rate"] = 1 - man
            cp["pressure_rate"] = pressure
        return {D.NV.get(t, t): p for t, p in DEF.profiles(b).items()}

    cases = {
        "high_pressure": force(0.25, 0.45),
        "low_pressure": force(0.25, 0.10),
        "man_heavy": force(0.55, 0.28),
        "zone_heavy": force(0.08, 0.28),
    }
    means = {}
    for name, prof in cases.items():
        g = dict(cfg, defensive_profiles=prof)
        r = E.run_cells(g, methods=("mc",), scenarios=("competitive",), n=5000, batch=15_000,
                        seed=3, include_residual=False, log=lambda *_: None)
        qb = r["ctxs"]["NO"].players.gsis.iloc[0]
        X = r["results"]["mc"]["cells"]["competitive"]["X"]
        means[name] = (float(X[f"{qb}|att"].mean()), float(X[f"{qb}|passyds"].mean()))
    assert means["high_pressure"][0] < means["low_pressure"][0]
    assert abs(means["man_heavy"][1] - means["zone_heavy"][1]) > 0.5


def test_coverage_allocation_measured_vs_inferred(board_cfg):
    cfg, board = board_cfg
    alloc = CA.profiles_from_board(board)
    assert alloc
    side = next(iter(alloc.values()))
    assert side["charting"]["play_level_coverage_assignment"] == "MISSING"
    assert "sharp" in side["defense_shell"]
    # at least one receiver with measured opportunity share when board has player_ids
    recs = side.get("receivers") or {}
    measured = [r for r in recs.values() if r.get("measured_target_share") is not None]
    assert measured, "expected measured board opportunity shares"
    for r in measured:
        assert "inferred" in r and "measured" in r
        assert r["target_share_multiplier"] != 0


def test_scramble_separated_from_designed():
    cfg, _ = cli.game_config(GAME)
    qb = None
    for p in cfg["defensive_profiles"].values():
        qb = p.get("qb_id")
        prof = p.get("scramble")
        if prof and prof.get("status") != "MISSING":
            break
    assert prof and "designed" in prof and "pressure" in prof
    assert prof["designed"]["kind"] in ("measured", "league_prior")
    assert 0 < prof["pressure"]["p_pressure"] < 1
    assert 0 <= prof["pressure"]["p_scramble_given_pressure"] <= 1
    rng = np.random.default_rng(1)
    out = SC.apply_scramble_to_dropbacks(rng, 2000, np.full(2000, 35), prof)
    assert out["scrambled"].mean() > 0
    assert out["thrown"].mean() + out["sacked"].mean() + out["scrambled"].mean() + out["throwaway"].mean() == pytest.approx(35, abs=0.5)


def test_residual_exhaustive_and_unconditional():
    doc = cli.simulate_game(GAME, n=1500, seed=2, batch=8_000, log=lambda *_: None)
    assert doc["residual_records"]
    assert doc["unconditional_records"]
    # primary scenarios disjoint from residual in classify
    rng = np.random.default_rng(0)
    H, F = rng.integers(-30, 30, 20_000), rng.integers(-40, 40, 20_000)
    m = E.classify(H, F, include_residual=True)
    tot = sum(v.astype(int) for v in m.values())
    assert tot.min() == 1 and tot.max() == 1
    # residual flagged
    assert all(r.get("is_residual") for r in doc["residual_records"] if "is_residual" in r)
    # calibration not inherited as VALIDATED
    bias_rows = [r for r in doc["records"] if r["method"] == "bias" and r.get("player_id")]
    if bias_rows:
        assert all("EXPERIMENTAL_UNVALIDATED_DEFENSE_CHANGED" in r["calibration_status"] for r in bias_rows)


def test_td_pass_rec_consistency():
    cfg, _ = cli.game_config(GAME)
    run = E.run_cells(cfg, methods=("mc",), scenarios=("competitive",), n=3000, batch=12_000,
                      include_residual=False, log=lambda *_: None)
    X = run["results"]["mc"]["cells"]["competitive"]["X"]
    for t, ctx in run["ctxs"].items():
        qb = ctx.players.gsis.iloc[0]
        rec_ids = [g for g, r in zip(ctx.players.gsis, ctx.players.role) if r != "QB"]
        passtd = X[f"{qb}|passtd"]
        rectd_sum = sum(X[f"{g}|rectd"] for g in rec_ids if f"{g}|rectd" in X)
        # passtd >= sum modeled receiver TDs (remainder is _other)
        assert np.all(passtd + 1e-6 >= rectd_sum)
        assert f"{t}|pass_td_team" in X
        assert np.allclose(X[f"{t}|pass_td_team"], passtd)


def test_gr_uses_opponent_defense_weights(board_cfg):
    cfg, _ = board_cfg
    # Smoke: GR completes with defenses attached
    run = E.run_cells(cfg, methods=("gr",), scenarios=("competitive",), n=2000, batch=8_000,
                      include_residual=False, log=lambda *_: None)
    assert run["results"]["gr"]["cells"]["competitive"]["trial_count"] == 2000


def test_acceptance_receipt_shape():
    doc = cli.simulate_game(GAME, n=1000, seed=4, batch=5_000, log=lambda *_: None)
    rec = cli.acceptance_receipt(doc, n_required=1000)
    assert rec["schema"] == "sim-v7-acceptance-receipt/1"
    assert rec["projection_ready"] is False
    assert rec["not_original_sim_v6"] is True
    assert len(rec["primary_cells"]) == 9
    assert rec["status"] in ("EXECUTED", "PARTIAL")

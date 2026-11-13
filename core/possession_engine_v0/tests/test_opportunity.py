"""NFL-75 Phase 2: player opportunity model (opportunity.py), opt-in. Written BEFORE the model.

1. Default is bit-identical to main 6bc0c54: every output block, including the name-locked player_box, matches the
   golden digests computed on main before this module existed (4 configs x 2 seeds).
2. Opt-in is still observational: with a model on, every one of those blocks is byte-identical too (the model has its
   own RNG stream) and a new player_box_opportunity block appears.
3. Reconciliation per trial: player lines sum to team lines, and the opportunity team ledger equals the name-locked
   team ledger for every stat (opportunities are only moved between players of the same team).
4. Fixes: role (an Out / stale QB gets no dropbacks; the starter owns them) and history caps (EB likelihood > 0 for
   events missing from a player's own rows, so Daniels can throw an interception).
5. Redistribution rule and determinism.
Research only. projection_ready stays false."""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _opportunity_golden as G  # noqa: E402

needs_pbp = pytest.mark.skipif(not __import__("_player_box_golden").PBP.exists(),
                               reason="committed nflverse W1-9 PBP missing")
GOLD = json.loads((Path(__file__).resolve().parent / "opportunity_golden_main_6bc0c54.json").read_text())
MODELS = REPO / "research/runs/2026-11-13_opportunity_phase2/models"
MODEL_FOR = {"was_nyg_lock": "model_2026_w10_WAS_NYG.json", "was_nyg_h2h_legacy": "model_2026_w10_WAS_NYG.json",
             "was_nyg_rare_research": "model_2026_w10_WAS_NYG.json", "def_allowed_w05": "model_2026_w09_JAX_BAL.json"}
_CACHE: dict = {}


def model(name):
    return json.loads((MODELS / MODEL_FOR[name]).read_text())


def _run(name, seed, opp=False, n=None):
    key = (name, seed, opp, n)
    if key not in _CACHE:
        kw = {"opportunity_model": model(name)} if opp else {}
        _CACHE[key] = G.run(name, n or G.N, seed, **kw)
    return _CACHE[key]


# ------------------------------------------------------------------ 1-2. bit-identical
@needs_pbp
@pytest.mark.parametrize("name", G.VARIANTS)
@pytest.mark.parametrize("seed", G.SEEDS)
def test_default_is_bit_identical_to_main(name, seed):
    out = _run(name, seed)
    assert "player_box_opportunity" not in out
    assert G.digest(out) == GOLD["digests"][f"{name}|{seed}"]


@needs_pbp
@pytest.mark.parametrize("name", G.VARIANTS)
@pytest.mark.parametrize("seed", G.SEEDS)
def test_opt_in_leaves_every_existing_block_bit_identical(name, seed):
    out = _run(name, seed, opp=True)
    assert "player_box_opportunity" in out
    assert G.digest(out) == GOLD["digests"][f"{name}|{seed}"]


@needs_pbp
def test_opt_in_requires_recorder_and_schema():
    import simulate
    cfg, ru = __import__("_player_box_golden").variant_cfg("was_nyg_lock")
    with pytest.raises(ValueError):
        simulate.simulate_games(cfg, pbp_path=str(G.PBG.PBP), n=2, seed=1, record_players=False,
                                opportunity_model=model("was_nyg_lock"))
    with pytest.raises(ValueError):
        simulate.simulate_games(cfg, pbp_path=str(G.PBG.PBP), n=2, seed=1, opportunity_model={"schema": "x"})


# ------------------------------------------------------------------ 3. reconciliation
@needs_pbp
@pytest.mark.parametrize("name", G.VARIANTS)
def test_every_trial_reconciles_and_team_ledger_unchanged(name):
    out = _run(name, 20261112, opp=True)
    ob, nb = out["player_box_opportunity"], out["player_box"]
    rec = ob["reconciliation"]
    assert rec["trials"] == G.N and rec["failures"] == 0, rec.get("first_failures")
    assert "team_ledger_eq_name_locked" in rec["checks"]
    # independent recomputation from the stored matrices
    nix = {tuple(c): j for j, c in enumerate(nb["team_columns"])}
    for j, (t, s) in enumerate(ob["team_columns"]):
        if s in ("rz_targets", "i5_targets", "rz_carries", "i5_carries"):
            continue
        ref = nb["team_values"][:, nix[(t, s)]] if (t, s) in nix else np.zeros(G.N)
        assert np.array_equal(ob["team_values"][:, j], ref), (t, s)
    sums: dict = {}
    for j, (t, p, s) in enumerate(ob["columns"]):
        sums[(t, s)] = sums.get((t, s), 0) + ob["values"][:, j]
    oix = {tuple(c): j for j, c in enumerate(ob["team_columns"])}
    for k, v in sums.items():
        assert np.array_equal(v, ob["team_values"][:, oix[k]]), k


@needs_pbp
def test_deterministic_for_same_seed():
    a = G.run("was_nyg_lock", 30, 11, opportunity_model=model("was_nyg_lock"))
    b = G.run("was_nyg_lock", 30, 11, opportunity_model=model("was_nyg_lock"))
    assert np.array_equal(a["player_box_opportunity"]["values"], b["player_box_opportunity"]["values"])
    assert a["player_box_opportunity"]["columns"] == b["player_box_opportunity"]["columns"]


# ------------------------------------------------------------------ 4. the two engine gaps
def _col(box, team, player, stat):
    for j, c in enumerate(box["columns"]):
        if tuple(c) == (team, player, stat):
            return box["values"][:, j]
    return np.zeros(box["values"].shape[0])


@needs_pbp
def test_role_gap_fixed_mccarthy_owns_nyg_dropbacks():
    out = _run("was_nyg_lock", 20261112, opp=True)
    ob, nb = out["player_box_opportunity"], out["player_box"]
    mc = _col(ob, "NYG", "J.McCarthy", "pass_att").mean()
    wi = _col(ob, "NYG", "J.Winston", "pass_att").mean()
    team = sum(ob["team_values"][:, j].mean() for j, c in enumerate(ob["team_columns"]) if tuple(c) == ("NYG", "pass_att"))
    assert mc > 0.75 * team and mc > 4 * wi
    # the name-locked recorder (main) is the gap being fixed: Winston out-attempts McCarthy there
    assert _col(nb, "NYG", "J.Winston", "pass_att").mean() > _col(nb, "NYG", "J.McCarthy", "pass_att").mean()


@needs_pbp
def test_history_cap_fixed_daniels_can_throw_int():
    out = _run("was_nyg_lock", 20261112, opp=True, n=400)
    assert _col(out["player_box"], "WAS", "J.Daniels", "int_thrown").sum() == 0  # name-locked: never
    assert (_col(out["player_box_opportunity"], "WAS", "J.Daniels", "int_thrown") > 0).mean() > 0


def test_eb_likelihood_positive_for_unseen_event():
    import opportunity as O
    prior = {"op|int": 0.02, "op|comp": 0.6, "op|inc": 0.38}
    lk = O.eb_lik({"op|comp": 30, "op|inc": 20}, prior, m=20.0)
    assert lk["op|int"] > 0 and abs(sum(lk.values()) - 1) < 1e-12
    assert lk["op|int"] == pytest.approx(20 * 0.02 / 70)


# ------------------------------------------------------------------ 5. redistribution rule
def test_redistribute_rule():
    import opportunity as O
    s = [0.5, 0.2, 0.2, 0.1]
    pos = ["WR", "WR", "TE", O.UNLISTED]
    r = O.redistribute(s, pos, [True, False, False, False], alpha=1.0)
    assert r[0] == 0 and r.sum() == pytest.approx(1) and r[1] == pytest.approx(0.7)  # all to the other WR
    r = O.redistribute(s, pos, [True, False, False, False], alpha=0.0)
    assert r[1] == pytest.approx(0.4) and r[2] == pytest.approx(0.4) and r[3] == pytest.approx(0.2)  # proportional
    r = O.redistribute(s, pos, [False] * 4, alpha=0.5)
    assert np.allclose(r, s)


def test_feature_cells_match_fitter():
    import opportunity as O
    sys.path.insert(0, str(REPO))
    from calibration import opportunity_fit as F
    assert O.feat_target(3, 12, True, True, False) in F.feature_cells("target")
    assert O.feat_carry(50, -2, False) in F.feature_cells("carry")
    assert O.feat_dropback(15, "sack") in F.feature_cells("dropback")


def test_model_files_are_point_in_time():
    for f in sorted(MODELS.glob("model_*.json")):
        m = json.loads(f.read_text())
        meta = m["meta"]
        assert meta["projection_ready"] is False
        assert meta["params"]["data_max_week_used"]["week"] < meta["eval_week"]

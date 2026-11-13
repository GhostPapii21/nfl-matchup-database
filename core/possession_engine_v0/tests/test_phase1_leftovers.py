"""Phase 1 leftovers (refs NFL-75): deterministic regression tests written BEFORE the engine change.

(a) Residual excess snaps: _clock_cost returned int(max(3, N(mu, 4))). int() truncates, so every pass/run/punt clock
    event is charged about 0.5 s less than the as-of mean it targets (W1-9: pass 21.40 vs 21.87 s, run 33.73 vs
    34.11 s; calibration/outputs/phase1_reconcile_*). Opt-in fix: accounting.clock_rounding = "round".
(c) Punt rate: the 4th-down decision cell "mid" spans yardline 36-60, so a 4th down at the opponent 40 samples the
    same punt-heavy mix as one at the own 45. Sim mix at 36-45: punt 0.65 / FG 0.12 vs actual 0.29 / 0.34.
    Opt-in fix: accounting.fourth_down_yl_buckets = "v1_fringe" (adds a 36-45 "fringe" cell; same coarsening chain).
Defaults are unchanged (golden hash below captured on main 3dad900 before any edit). Nothing is fitted to scores or
lines; no weights change. Research only, not validated."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import simulate  # noqa: E402
from simulate import (_clock_cost, accounting_from_cfg, _fourth_down_decision, yl4_bucket,  # noqa: E402
                      ACCOUNTING_DEFAULTS, ACCOUNTING_LEGACY, ACCOUNTING_PRE_WP12)

REPO = HERE.parents[1]
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
CFG = HERE / "config/was_nyg_2026-11-12_data_only_nfl43.json"
GOLDEN_MAIN_3DAD900 = "d18e19271d666c3b"  # WAS@NYG data-only config, n=30, seed 20261113, default accounting


def _run(accounting=None, n=30, seed=20261113):
    cfg = json.loads(CFG.read_text())
    if accounting is not None:
        cfg["accounting"] = accounting
    o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=n, seed=seed)
    A = o["arrays"]
    return hashlib.sha256(np.asarray(A["fg_home"], dtype=np.int64).tobytes()
                          + np.asarray(A["fg_away"], dtype=np.int64).tobytes()).hexdigest()[:16]


# ---------------------------------------------------------------- defaults unchanged
@pytest.mark.skipif(not PBP.exists(), reason="PBP parquet not present")
def test_default_output_matches_main_golden():
    assert _run() == GOLDEN_MAIN_3DAD900


def test_accounting_defaults_keep_old_behaviour():
    a = accounting_from_cfg({})
    assert a["clock_rounding"] == "truncate" and a["fourth_down_yl_buckets"] == "v0"
    for preset in ("legacy", "pre_wp12"):
        p = accounting_from_cfg({"accounting": preset})
        assert p["clock_rounding"] == "truncate" and p["fourth_down_yl_buckets"] == "v0"
    for d in (ACCOUNTING_DEFAULTS, ACCOUNTING_LEGACY, ACCOUNTING_PRE_WP12):
        assert d["clock_rounding"] == "truncate" and d["fourth_down_yl_buckets"] == "v0"


def test_accounting_rejects_unknown_values():
    with pytest.raises(ValueError):
        accounting_from_cfg({"accounting": {"clock_rounding": "ceil"}})
    with pytest.raises(ValueError):
        accounting_from_cfg({"accounting": {"fourth_down_yl_buckets": "v9"}})


# ---------------------------------------------------------------- (a) clock rounding
def _mean_cost(mu, rounding, n=200_000, seed=11):
    rng = np.random.default_rng(seed)
    kw = {} if rounding is None else {"rounding": rounding}
    return float(np.mean([_clock_cost("pass", rng, {"pass": mu}, **kw) for _ in range(n)]))


@pytest.mark.parametrize("mu", [21.867, 28.0, 34.107])
def test_truncate_default_is_half_second_short(mu):
    # characterizes the bug: the default keeps it so old runs reproduce
    assert abs(_mean_cost(mu, None) - (mu - 0.5)) < 0.03
    assert _mean_cost(mu, None) == _mean_cost(mu, "truncate")


@pytest.mark.parametrize("mu", [21.867, 28.0, 34.107])
def test_round_is_unbiased(mu):
    assert abs(_mean_cost(mu, "round") - mu) < 0.03


def test_rounding_consumes_identical_rng_stream():
    r1, r2 = np.random.default_rng(5), np.random.default_rng(5)
    for _ in range(50):
        _clock_cost("run", r1, {"run": 30.0}, rounding="truncate")
        _clock_cost("run", r2, {"run": 30.0}, rounding="round")
    assert r1.bit_generator.state == r2.bit_generator.state


def test_round_keeps_three_second_floor():
    rng = np.random.default_rng(3)
    assert min(_clock_cost("field_goal", rng, {"field_goal": 1.0}, rounding="round") for _ in range(2000)) == 3


# ---------------------------------------------------------------- (c) 4th-down field-position cells
def test_v1_bucket_boundaries():
    from simulate import yl4_bucket_v1
    assert [yl4_bucket_v1(y) for y in (35, 36, 45, 46, 60, 61)] == ["fg_range", "fringe", "fringe", "mid", "mid", "own"]
    assert [yl4_bucket(y) for y in (35, 36, 45, 46, 60, 61)] == ["fg_range", "mid", "mid", "mid", "mid", "own"]


def _toy_catalog(scheme):
    rows = ([dict(posteam="AAA", down=4, yardline_100=40, ydstogo=8, play_type="field_goal")] * 6
            + [dict(posteam="AAA", down=4, yardline_100=55, ydstogo=8, play_type="punt")] * 30)
    f4 = pd.DataFrame(rows)
    cat = SimpleNamespace(min_n=5, _f4=f4, fourth_down_yl_buckets=scheme, fourth_cells={})
    f4 = f4.assign(_y4=f4.yardline_100.map(yl4_bucket), _t4="long")
    for team, g in f4.groupby("posteam"):
        cat.fourth_cells[(team,)] = g
        for y, gy in g.groupby("_y4"):
            cat.fourth_cells[(team, y)] = gy
            for tg, gt in gy.groupby("_t4"):
                cat.fourth_cells[(team, y, tg)] = gt
    return cat


def _decisions(scheme, n=400):
    rng = np.random.default_rng(42)
    cat = _toy_catalog(scheme)
    out = []
    for _ in range(n):
        st = SimpleNamespace(possession="AAA", yardline_100=40, ydstogo=8, sparse_flags=[])
        out.append(_fourth_down_decision(rng, cat, st))
    return pd.Series(out).value_counts(normalize=True).to_dict()


def test_v0_mixes_own_side_punts_into_opponent_40():
    d = _decisions("v0")
    assert d.get("punt", 0) > 0.7  # 30 punts at the 45 vs 6 FGs at the opp 40 share one "mid" cell


def test_v1_fringe_cell_separates_opponent_40():
    d = _decisions("v1_fringe")
    assert d == {"field_goal": 1.0}


def test_v1_is_deterministic_for_fixed_seed():
    assert _decisions("v1_fringe") == _decisions("v1_fringe")


# ---------------------------------------------------------------- opt-ins are wired (and only when enabled)
@pytest.mark.skipif(not PBP.exists(), reason="PBP parquet not present")
def test_opt_ins_change_output_only_when_enabled():
    assert _run({"clock_rounding": "round"}) != GOLDEN_MAIN_3DAD900
    assert _run({"fourth_down_yl_buckets": "v1_fringe"}) != GOLDEN_MAIN_3DAD900
    assert _run({"clock_rounding": "truncate", "fourth_down_yl_buckets": "v0"}) == GOLDEN_MAIN_3DAD900

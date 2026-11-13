"""NFL-75 (refs NFL-75): QB rush YPC prior + kneel model fix, opt-in via leg qb_rush_prior=True.

Covers: the QB prior is the league QB non-kneel YPC (not the RB-dominated all-rusher mean), kneels are excluded from
the YPC sample and carry counts, the separate kneel model, and that non-QB legs / flag-off legs are unchanged
(the Phase 4 W8-9 reproduction in test_simv56_pmodel.py covers flag-off bit-for-bit)."""
from __future__ import annotations

import hashlib
import inspect
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE_DIR = ROOT / "calibration" / "simv56" / "engines"
sys.dont_write_bytecode = True                                  # never leave __pycache__ in the sha-pinned engine dir
sys.path.insert(0, str(ENGINE_DIR))
import qb_rush_prior as QRP  # noqa: E402

from calibration import simv56_pmodel as SV  # noqa: E402


def _ru():
    """Synthetic league: RBs 4.0 YPC (200 carries), QB 'Q1' 7.0 YPC on 20 scrambles + 6 kneels (-1), QB 'Q2' 5.0."""
    rows = []
    for i in range(200):
        rows.append(dict(game_id=f"g{i % 4}", posteam="AAA", defteam="BBB" if i % 2 else "CCC", rusher_player_id="R1",
                         pg="RB", rushing_yards=4.0, qb_kneel=0))
    for i in range(20):
        rows.append(dict(game_id=f"g{i % 4}", posteam="AAA", defteam="BBB", rusher_player_id="Q1", pg="QB",
                         rushing_yards=7.0, qb_kneel=0))
    for i in range(6):
        rows.append(dict(game_id=f"g{i % 2}", posteam="AAA", defteam="BBB", rusher_player_id="Q1", pg="QB",
                         rushing_yards=-1.0, qb_kneel=1))
    for i in range(20):
        rows.append(dict(game_id="g9", posteam="DDD", defteam="CCC", rusher_player_id="Q2", pg="QB",
                         rushing_yards=5.0, qb_kneel=0))
    return pd.DataFrame(rows)


def test_qb_prior_is_league_qb_ypc_not_rb_dominated_mean():
    ru = _ru()
    qr = QRP.qb_rush_inputs(ru, "Q1", "BBB", ["g0", "g1", "g2", "g3"])
    assert qr["lg_qb"] == pytest.approx(6.0)                        # (20*7 + 20*5) / 40, kneels out
    lg_all = ru.rushing_yards.mean()                                 # the old target (all rushers incl kneels)
    assert lg_all < 4.4
    pm, n = float(qr["ypc"].mean()), len(qr["ypc"])
    new = pm * QRP.ypc_factor(pm, n, qr["lg_qb"], 1.0)
    w = n / (n + 100)
    old = w * pm + (1 - w) * lg_all
    assert new == pytest.approx(w * 7.0 + (1 - w) * 6.0)
    assert new > qr["lg_qb"] > old                                   # pulled to the QB mean, not toward the RB mean
    # same K=100 weight as the engines (weights unchanged)
    assert QRP.K_YPC == 100


def test_kneels_excluded_from_ypc_sample_and_carries():
    ru = _ru()
    qr = QRP.qb_rush_inputs(ru, "Q1", "BBB", ["g0", "g1", "g2", "g3"])
    assert len(qr["ypc"]) == 20 and (qr["ypc"] == 7.0).all()       # the six -1 kneels are not in the YPC sample
    assert list(qr["car"]) == [5, 5, 5, 5]                           # non-kneel carries per game (kneels were g0/g1)
    assert qr["n_kneels_player"] == 6
    # opponent factor over non-kneel rushes only
    nk = ru[ru.qb_kneel != 1]
    assert qr["opp_ratio"] == pytest.approx(nk[nk.defteam == "BBB"].rushing_yards.mean() / nk.rushing_yards.mean())


def test_ypc_factor_guards():
    assert QRP.ypc_factor(0.0, 0, 6.0, 1.1) == 1.0                   # no sample
    assert QRP.ypc_factor(-0.5, 3, 6.0, 1.1) == pytest.approx(1.1)   # non-positive mean: opponent factor only
    assert QRP.ypc_factor(5.0, 10, float("nan"), 0.9) == pytest.approx(0.9)


def _tg_and_kneels():
    tg = pd.DataFrame(dict(game_id=[f"g{i}" for i in range(8)] * 2, posteam=["AAA"] * 8 + ["BBB"] * 8,
                           margin=[7, 3, 10, 14, -7, -3, -10, -14] + [-7, -3, -10, -14, 7, 3, 10, 14]))
    rows = []
    for gid, team, m in tg.itertuples(index=False):
        for _ in range(3 if m > 0 else (1 if m == -3 else 0)):
            rows.append(dict(game_id=gid, posteam=team, rushing_yards=-1.0, qb_kneel=1))
    rows.append(dict(game_id="g0", posteam="AAA", rushing_yards=5.0, qb_kneel=0))
    return tg, pd.DataFrame(rows)


def test_kneel_model_table_and_game_state():
    tg, ru = _tg_and_kneels()
    t = QRP.kneel_table(ru, tg)
    assert sorted(t["lead"]) == [3] * 8 and sorted(t["other"]) == [0, 0, 0, 0, 0, 0, 1, 1]
    assert (t["yards"] == -1.0).all() and len(t["yards"]) == 26     # the non-kneel 5-yd run is not a kneel
    n = 20000
    fav = QRP.sim_kneel_yards(np.random.default_rng(1), -14.0, n, t)
    dog = QRP.sim_kneel_yards(np.random.default_rng(1), 14.0, n, t)
    assert (fav <= 0).all() and (dog <= 0).all()
    assert fav.mean() < dog.mean() - 1.0                            # leading teams kneel more
    p_lead = 0.5 * (1 + math.erf(14 / 13.5 / 2 ** 0.5))          # P(margin > 0), margin ~ N(14, 13.5)
    assert fav.mean() == pytest.approx(-(3 * p_lead + 0.25 * (1 - p_lead)), abs=0.05)
    again = QRP.sim_kneel_yards(np.random.default_rng(1), -14.0, n, t)
    assert np.array_equal(fav, again)                               # deterministic for a seed
    assert not QRP.sim_kneel_yards(np.random.default_rng(1), 0.0, 10, dict(lead=[], other=[], yards=[])).any()


def test_kneel_rng_is_a_separate_stream():
    a = QRP.kneel_rng(20261101, "X", "rushyds", "mc").random(5)
    b = np.random.default_rng(20261101 + int(hashlib.md5(b"X|rushyds|mc").hexdigest()[:6], 16)).random(5)
    assert not np.allclose(a, b)


_PROBE = r"""
import json, sys, warnings; warnings.filterwarnings('ignore')
sys.path.insert(0, sys.argv[1]); import cc_sim_v6 as M
E = M.Engine(cutoff='2026-10-29', calib=None, n=4000)
out = {}
for key, leg in json.loads(sys.argv[2]).items():
    o, info = E.sim(leg)
    out[key] = dict(p={m: o[m]['rungs'][str(leg['rungs'][0])] for m in o}, mean={m: o[m]['mean'] for m in o},
                    A_ypc=info['A_ypc'], w_car=info['w_car'], qrp=info.get('qb_rush_prior'))
print(json.dumps(out))
"""


@pytest.fixture(scope="module")
def probe():
    legs = {}
    base = dict(player="Drake Maye", team="NE", opp="MIA", market="rushyds", spread=-7.0, rungs=[23.5])
    legs["maye_off"] = base
    legs["maye_on"] = dict(base, qb_rush_prior=True)
    rb = dict(player="Derrick Henry", team="BAL", opp="BUF", market="rushyds", spread=-1.5, rungs=[77.5])
    legs["rb_off"] = rb
    legs["rb_on"] = dict(rb, qb_rush_prior=True)
    with tempfile.TemporaryDirectory(dir="/tmp") as td:
        src = SV.make_src(Path(td) / "src")
        env = dict(os.environ, CC_OPP="0.5", CC_SRC=str(src), CC_CUTOFF="2026-10-29", SIMV6_SRC=str(src),
                   PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, "-c", _PROBE, str(ENGINE_DIR), json.dumps(legs)], env=env,
                           capture_output=True, text=True, cwd=ENGINE_DIR, timeout=300)
    assert r.returncode == 0, r.stderr[-800:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_engine_qb_leg_uses_qb_prior_and_kneel_free_carries(probe):
    on, off = probe["maye_on"], probe["maye_off"]
    q = on["qrp"]
    assert off["qrp"] is None
    assert q["lg_qb"] > 5.0 > 4.4 > q["lg_all_nk"] - 0.01 > 4.0     # QB prior ~5.8 vs all-rusher ~4.3 (W1-7 PBP)
    assert q["n_kneels"] > 0 and on["w_car"] < off["w_car"]          # kneels no longer counted as carries
    assert on["A_ypc"] > off["A_ypc"]                                # scramble QB is no longer pulled toward RB YPC
    assert on["mean"]["mc"] != off["mean"]["mc"]


def test_engine_non_qb_leg_unchanged_by_flag(probe):
    assert probe["rb_on"] == probe["rb_off"]


def test_run_all_passes_flag_only_when_asked(tmp_path):
    legs = pd.DataFrame([dict(player="Drake Maye", gsis=None, team="NE", opp="MIA", market="rushyds", spread=-7.0,
                              line=23.5)])
    src = SV.make_src(tmp_path / "src")
    SV.run_all(legs, week=8, src=src, workdir=tmp_path / "off", n=500)
    SV.run_all(legs, week=8, src=src, workdir=tmp_path / "on", n=500, qb_rush_prior=True)
    off = json.loads((tmp_path / "off" / "engine_legs.json").read_text())
    on = json.loads((tmp_path / "on" / "engine_legs.json").read_text())
    assert "qb_rush_prior" not in off[0] and on[0]["qb_rush_prior"] is True
    p_off = pd.read_csv(tmp_path / "off" / "sim_v6_opp0.5_w8.csv").p_mc.iloc[0]
    p_on = pd.read_csv(tmp_path / "on" / "sim_v6_opp0.5_w8.csv").p_mc.iloc[0]
    assert p_off != p_on


def test_run_cli_has_no_qb_rush_prior_switch():
    """A probability file stamped prob_source=sim_v5_v6_ensemble (the Phase 4 fit inputs) cannot carry the fix."""
    assert "qb_rush_prior" not in inspect.getsource(SV.main)

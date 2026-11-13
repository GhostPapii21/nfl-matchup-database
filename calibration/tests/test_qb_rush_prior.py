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


# ------------------------------------------------------------------ component model (qb_rush_prior="components")
def _ru_components():
    rows = []
    for i in range(300):
        rows.append(dict(game_id=f"g{i % 6}", posteam="AAA", defteam="BBB", rusher_player_id="R1", pg="RB",
                         rushing_yards=float(i % 9 - 2), qb_kneel=0, qb_scramble=0))
    scr = [6, 9, 12, 4, 15, 8, 0, 22, 7, 11]          # player's longest scramble = 22
    for i, y in enumerate(scr):
        rows.append(dict(game_id=f"g{i % 4}", posteam="AAA", defteam="BBB", rusher_player_id="Q1", pg="QB",
                         rushing_yards=float(y), qb_kneel=0, qb_scramble=1))
    for i, y in enumerate([1, 2, -1, 3, 0, 1]):
        rows.append(dict(game_id=f"g{i % 3}", posteam="AAA", defteam="BBB", rusher_player_id="Q1", pg="QB",
                         rushing_yards=float(y), qb_kneel=0, qb_scramble=0))
    for i in range(4):
        rows.append(dict(game_id=f"g{i}", posteam="AAA", defteam="BBB", rusher_player_id="Q1", pg="QB",
                         rushing_yards=-1.0, qb_kneel=1, qb_scramble=0))
    for i in range(60):                                 # league QB pool incl. a few long scrambles
        rows.append(dict(game_id="g9", posteam="DDD", defteam="CCC", rusher_player_id="Q2", pg="QB",
                         rushing_yards=float([5, 8, 3, 41, 10, -2][i % 6]), qb_kneel=0, qb_scramble=int(i % 2 == 0)))
    return pd.DataFrame(rows)


def test_components_split_scrambles_designed_and_drop_kneels():
    qc = QRP.component_inputs(_ru_components(), "Q1", "BBB", ["g0", "g1", "g2", "g3"])
    assert list(qc["scr_car"]) == [3, 3, 2, 2] and list(qc["des_car"]) == [2, 2, 2, 0]   # kneels in no component
    assert qc["scr"]["n"] == 10 and qc["des"]["n"] == 6 and qc["n_kneels_player"] == 4
    assert qc["scr"]["mu"] != qc["des"]["mu"]                                          # separate yard models
    assert (qc["des"]["neg_pool"] <= 0).all() and 0 < qc["des"]["p0"] < 1


def test_component_yards_have_a_heavy_right_tail_past_the_players_longest_run():
    qc = QRP.component_inputs(_ru_components(), "Q1", "BBB", ["g0", "g1", "g2", "g3"])
    y = QRP.draw_yards(np.random.default_rng(3), qc["scr"], 200_000)
    assert (y > 22).mean() > 0.01                    # beyond his longest observed scramble (a resampler gives 0)
    assert (y > 50).mean() > 0                       # 50+ yard spikes are reachable
    assert (y <= 0).mean() == pytest.approx(qc["scr"]["p0"], abs=0.005)               # explicit non-positive atom
    assert y.max() > 3 * np.median(y[y > 0])


def test_component_rush_zero_volume_component_is_zero_not_an_error():
    qc = QRP.component_inputs(_ru_components(), "Q1", "BBB", ["g0", "g1", "g2", "g3"])
    rng = np.random.default_rng(0)
    out = QRP.component_rush(rng, lambda c: np.full(100, 2), dict(scr=False, des=False), qc, 1.0, 100)
    assert not out.any()


@pytest.fixture(scope="module")
def probe_components():
    base = dict(player="Drake Maye", team="NE", opp="MIA", market="rushyds", spread=-7.0, rungs=[80.0])
    rb = dict(player="Derrick Henry", team="BAL", opp="BUF", market="rushyds", spread=-1.5, rungs=[77.5])
    legs = dict(maye_prior=dict(base, qb_rush_prior=True), maye_comp=dict(base, qb_rush_prior="components"),
                rb_off=rb, rb_comp=dict(rb, qb_rush_prior="components"))
    with tempfile.TemporaryDirectory(dir="/tmp") as td:
        src = SV.make_src(Path(td) / "src")
        env = dict(os.environ, CC_OPP="0.5", CC_SRC=str(src), CC_CUTOFF="2026-10-29", SIMV6_SRC=str(src),
                   PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, "-c", _PROBE, str(ENGINE_DIR), json.dumps(legs)], env=env,
                           capture_output=True, text=True, cwd=ENGINE_DIR, timeout=300)
    assert r.returncode == 0, r.stderr[-800:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_engine_components_reach_spike_games(probe_components):
    # P(Maye >= 80) with his own-carry resampler is ~0.3%; the component tail makes such a game several times likelier
    assert probe_components["maye_comp"]["p"]["mc"] > 3 * probe_components["maye_prior"]["p"]["mc"]
    assert probe_components["rb_comp"] == probe_components["rb_off"]                    # non-QB unchanged


def test_run_all_rejects_unknown_mode(tmp_path):
    legs = pd.DataFrame([dict(player="Drake Maye", gsis=None, team="NE", opp="MIA", market="rushyds", spread=-7.0,
                              line=23.5)])
    with pytest.raises(SV.SimV56Error):
        SV.run_all(legs, week=8, src=tmp_path, workdir=tmp_path / "w", n=10, qb_rush_prior="tail")


# ------------------------------------------------------------------ flag allowlist (True / "prior" / "components" only)
@pytest.mark.parametrize("val", [None, False, "false", "False", "off", "", 0, "True", 1, "yes"])
def test_flag_allowlist_stays_off(val):
    assert QRP.flag_on(val) is False


@pytest.mark.parametrize("val", [True, "prior", "components"])
def test_flag_allowlist_turns_on(val):
    assert QRP.flag_on(val) is True


def test_engines_use_flag_allowlist_not_bool_truthiness():
    """The string 'false' must not enable the fix; engines call flag_on, not bool(leg.get(...))."""
    for name in ("cc_sim_v5.py", "cc_sim_v6.py", "cc_sim_v6_fix.py"):
        src = (ENGINE_DIR / name).read_text()
        assert "bool(leg.get('qb_rush_prior'))" not in src
        assert "QRP.flag_on(leg.get('qb_rush_prior'))" in src


# ------------------------------------------------------------------ kneels-only QB (v5 nb() NaN crash; Mullens / Tyrod / Mac Jones)
def _kneels_only_src(dest: Path) -> Path:
    """Tiny synthetic PBP: 'Kneel Only' is a QB whose only carries are kneels. League has a starter QB,
    RBs and enough pass/rush volume for the engines' polyfit and opponent-adjustment paths."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    pl = pd.DataFrame([
        dict(gsis_id="K1", display_name="Kneel Only", latest_team="AAA", position_group="QB"),
        dict(gsis_id="Q1", display_name="Starter QB", latest_team="AAA", position_group="QB"),
        dict(gsis_id="R1", display_name="Team RB", latest_team="AAA", position_group="RB"),
        dict(gsis_id="W1", display_name="Team WR", latest_team="AAA", position_group="WR"),
        dict(gsis_id="Q2", display_name="Other QB", latest_team="BBB", position_group="QB"),
        dict(gsis_id="R2", display_name="Other RB", latest_team="BBB", position_group="RB"),
        dict(gsis_id="W2", display_name="Other WR", latest_team="BBB", position_group="WR"),
    ])
    games = [
        ("g0", "2026-09-13", 28, 10),
        ("g1", "2026-09-20", 21, 17),
        ("g2", "2026-09-27", 14, 24),
        ("g3", "2026-10-04", 31, 7),
        ("g4", "2026-10-11", 17, 20),
        ("g5", "2026-10-18", 24, 14),
    ]
    rows = []

    def add(**kw):
        base = dict(season_type="REG", two_point_attempt=0, sack=0, pass_attempt=0, rush_attempt=0,
                    play_type="run", complete_pass=0, receiving_yards=0.0, passing_yards=0.0,
                    rushing_yards=0.0, qb_kneel=0, qb_scramble=0, home_team="AAA",
                    rusher_player_id=None, receiver_player_id=None, passer_player_id=None)
        base.update(kw)
        rows.append(base)

    for gid, date, hs, aws in games:
        common = dict(game_id=gid, game_date=date, home_score=hs, away_score=aws)
        for _ in range(15):
            add(**common, posteam="AAA", defteam="BBB", play_type="pass", pass_attempt=1,
                passer_player_id="Q1", receiver_player_id="W1", complete_pass=1,
                passing_yards=8.0, receiving_yards=8.0)
        for _ in range(12):
            add(**common, posteam="AAA", defteam="BBB", play_type="run", rush_attempt=1,
                rusher_player_id="R1", rushing_yards=4.0)
        for _ in range(3):
            add(**common, posteam="AAA", defteam="BBB", play_type="run", rush_attempt=1,
                rusher_player_id="Q1", rushing_yards=7.0, qb_scramble=1)
        for _ in range(2):
            add(**common, posteam="AAA", defteam="BBB", play_type="run", rush_attempt=1,
                rusher_player_id="K1", rushing_yards=-1.0, qb_kneel=1)
        # a few QB receptions so v5 oppadj(pg=QB) is not a divide-by-zero
        add(**common, posteam="AAA", defteam="BBB", play_type="pass", pass_attempt=1,
            passer_player_id="Q1", receiver_player_id="Q2", complete_pass=1,
            passing_yards=3.0, receiving_yards=3.0)
        for _ in range(12):
            add(**common, posteam="BBB", defteam="AAA", play_type="pass", pass_attempt=1,
                passer_player_id="Q2", receiver_player_id="W2", complete_pass=1,
                passing_yards=7.0, receiving_yards=7.0)
        for _ in range(10):
            add(**common, posteam="BBB", defteam="AAA", play_type="run", rush_attempt=1,
                rusher_player_id="R2", rushing_yards=4.0)
        add(**common, posteam="BBB", defteam="AAA", play_type="pass", pass_attempt=1,
            passer_player_id="Q2", receiver_player_id="Q1", complete_pass=1,
            passing_yards=2.0, receiving_yards=2.0)
    pd.DataFrame(rows).to_parquet(dest / "play_by_play_2026.parquet")
    pl.to_parquet(dest / "players.parquet")
    return dest


_KNEEL_PROBE = r"""
import json, sys, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, sys.argv[1])
engine, legs, n = sys.argv[2], json.loads(sys.argv[3]), int(sys.argv[4])
out = {}
if engine == 'v5':
    import cc_sim_v5 as M
    M.N = n
    def run(leg):
        return M.sim(leg)
elif engine == 'v6':
    import cc_sim_v6 as M
    E = M.Engine(cutoff='2026-10-29', calib=None, n=n)
    def run(leg):
        return E.sim(leg)
else:
    import cc_sim_v6_fix as M
    E = M.Engine(cutoff='2026-10-29', calib=None, n=n)
    def run(leg):
        return E.sim(leg)
for key, leg in legs.items():
    try:
        o, info = run(leg)
        out[key] = dict(ok=True, mean={m: float(o[m]['mean']) for m in o},
                        A_ypc=info['A_ypc'], w_car=info['w_car'], qrp=info.get('qb_rush_prior'))
    except Exception as ex:
        out[key] = dict(ok=False, error=repr(ex))
print(json.dumps(out))
"""


def _run_kneel_probe(src: Path, engine: str, legs: dict, n: int = 800) -> dict:
    env = dict(os.environ, CC_OPP="0.5", CC_SRC=str(src), CC_CUTOFF="2026-10-29", SIMV6_SRC=str(src),
               PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-c", _KNEEL_PROBE, str(ENGINE_DIR), engine, json.dumps(legs), str(n)],
                       env=env, capture_output=True, text=True, cwd=ENGINE_DIR, timeout=120)
    assert r.returncode == 0, r.stderr[-800:] or r.stdout[-800:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def _kneel_legs():
    base = dict(player="Kneel Only", gsis="K1", team="AAA", opp="BBB", market="rushyds",
                spread=-7.0, rungs=[0.5])
    starter = dict(player="Starter QB", gsis="Q1", team="AAA", opp="BBB", market="rushyds",
                   spread=-7.0, rungs=[20.5])
    return {
        "kneel_off": dict(base),
        "kneel_false": dict(base, qb_rush_prior="false"),
        "kneel_False": dict(base, qb_rush_prior="False"),
        "kneel_offstr": dict(base, qb_rush_prior="off"),
        "kneel_empty": dict(base, qb_rush_prior=""),
        "kneel_zero": dict(base, qb_rush_prior=0),
        "kneel_on": dict(base, qb_rush_prior=True),
        "kneel_prior": dict(base, qb_rush_prior="prior"),
        "kneel_comp": dict(base, qb_rush_prior="components"),
        "starter_off": dict(starter),
        "starter_false": dict(starter, qb_rush_prior="false"),
        "starter_on": dict(starter, qb_rush_prior=True),
    }


@pytest.mark.parametrize("engine", ["v5", "v6", "v6_fix"])
def test_kneels_only_qb_does_not_crash_when_flag_is_on(engine, tmp_path):
    """v5 used to hit NaN in nb() for a QB whose only carries are kneels (Mullens, Tyrod, Mac Jones)."""
    src = _kneels_only_src(tmp_path / "src")
    out = _run_kneel_probe(src, engine, _kneel_legs())
    for key, row in out.items():
        assert row.get("ok"), f"{engine} {key} crashed: {row}"
        assert all(math.isfinite(v) for v in row["mean"].values()), (engine, key, row)
    on, off = out["kneel_on"], out["kneel_off"]
    assert on["qrp"] is not None and off["qrp"] is None
    assert on["w_car"] == 0                                   # kneels removed from carry volume
    assert off["w_car"] > 0                                   # flag off still counts kneels as carries
    # allowlist: these stay on the unfixed path
    for key in ("kneel_false", "kneel_False", "kneel_offstr", "kneel_empty", "kneel_zero"):
        assert out[key]["qrp"] is None
        assert out[key]["mean"] == off["mean"]
        assert out[key]["w_car"] == off["w_car"]
    # True and "prior" both turn the QB-prior fix on (same mode)
    assert out["kneel_prior"]["mean"] == on["mean"]
    assert out["kneel_prior"]["qrp"] is not None
    assert out["kneel_comp"]["qrp"] is not None
    # "false" also leaves a scrambling QB on the unfixed path
    assert out["starter_false"]["mean"] == out["starter_off"]["mean"]
    assert out["starter_false"]["qrp"] is None
    assert out["starter_on"]["qrp"] is not None
    assert out["starter_on"]["mean"] != out["starter_off"]["mean"]

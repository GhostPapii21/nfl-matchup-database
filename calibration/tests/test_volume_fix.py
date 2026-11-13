"""NFL-75 opt-in volume fixes (outside-AI review memo B2, B3, B8, B9) for the vendored simv56 engines.
Default path must stay the Phase 4 ensemble (the 88-leg W8-9 reproduction in test_simv56_pmodel.py); volume_fix=True
must keep zero-carry games, let the spread move expected volume, lift the 2x boost cap and guard the YPC ratio.
Committed PBP + players table only; no network. Research only; projection_ready stays false."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from calibration import simv56_pmodel as SV  # noqa: E402

sys.path.insert(0, str(SV.ENGINE_DIR))
_dwb, sys.dont_write_bytecode = sys.dont_write_bytecode, True   # no __pycache__ inside the sha-pinned engines dir
import volume_fix as VFX  # noqa: E402
sys.dont_write_bytecode = _dwb

PBP = ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
# Week 8 Phase 4 legs (calibration/tests/fixtures/simv56_phase4_w8_w9_legs.csv)
STAFFORD = dict(player="Matthew Stafford", gsis="00-0026498", team="LA", opp="LAC", market="rushyds", spread=-6.5,
                line=0.5)
LOVE = dict(player="Jordan Love", gsis="00-0036264", team="GB", opp="CAR", market="rushyds", spread=-3.5, line=4.5)


def _fixture_leg(gsis):
    f = pd.read_csv(ROOT / "calibration/tests/fixtures/simv56_phase4_w8_w9_legs.csv", dtype={"gsis": str})
    return f[(f.week == 8) & (f.gsis == gsis)].iloc[0]


def test_fixture_legs_match():
    for leg in (STAFFORD, LOVE):
        r = _fixture_leg(leg["gsis"])
        assert (r.player, r.team, r.opp, r.spread, r.line) == (leg["player"], leg["team"], leg["opp"], leg["spread"],
                                                                leg["line"])


# ---------------------------------------------------------------- units
def test_active_games_keeps_played_zero_carry_games_only():
    d = pd.DataFrame(dict(game_id=["g1", "g2", "g3", "g4"], tgt=[0, 0, 0, 1], car=[3, 0, 0, 0]))
    pbp = pd.DataFrame(dict(game_id=["g1", "g2", "g3"], passer_player_id=["Q", "Q", "X"], pass_attempt=[1, 0, 1],
                            sack=[0, 1, 0]))
    assert list(VFX.active_games(d, pbp, "Q").game_id) == ["g1", "g2", "g4"]   # g2: sacked, 0 carries -> kept
    assert list(d[(d.tgt + d.car) > 0].game_id) == ["g1", "g4"]                # the old rule dropped g2


def test_committed_pbp_has_qb_games_the_old_rule_dropped():
    """Stafford had 0 carries in 2 of his 7 pre-W8 starts (memo B2), so the old rule biased P(over 0.5) upward."""
    P = pd.read_parquet(PBP, columns=["game_id", "game_date", "passer_player_id", "rusher_player_id", "rush_attempt",
                                      "pass_attempt", "sack"])
    P = P[P.game_date < SV.cutoff_for_week(8)]
    g = STAFFORD["gsis"]
    played = set(P[(P.passer_player_id == g) & ((P.pass_attempt == 1) | (P.sack == 1))].game_id)
    ran = set(P[(P.rusher_player_id == g) & (P.rush_attempt == 1)].game_id)
    assert len(played) == 7 and len(played - ran) == 2


def test_script_tv_moves_the_mean_with_the_spread_and_matches_history_at_history_script():
    rng = np.random.default_rng(0)
    n, b, tmean, mean, m_s, mbar = 200_000, 0.01, 28.0, 14.0, 0.5, 2.0
    pace = rng.lognormal(0, 0.15, n)
    z = rng.normal(0, 13.5, n)
    fav = VFX.script_tv(tmean, pace, b, -(-7.0) + z, -7.0, mean, m_s, mbar).mean()
    dog = VFX.script_tv(tmean, pace, b, -(7.0) + z, 7.0, mean, m_s, mbar).mean()
    ref = VFX.script_tv(tmean, pace, b, mbar + z, -mbar, mean, m_s, mbar).mean()
    assert ref == pytest.approx(mean / m_s, rel=1e-12)                       # history script -> history mean
    assert fav == pytest.approx(mean / m_s * np.exp(b * (7.0 - mbar)), rel=1e-12)
    assert dog == pytest.approx(mean / m_s * np.exp(b * (-7.0 - mbar)), rel=1e-12)
    # the old formula: identical mean at opposite spreads (memo B3)
    old = lambda s, M: (lambda tv: tv * (mean / (m_s * tv.mean())))(tmean * pace * np.exp(b * (M - (-s))) *
                                                                     np.exp(b * (-s)))
    assert old(-7.0, 7.0 + z).mean() == pytest.approx(old(7.0, -7.0 + z).mean(), rel=1e-12)


def test_scale_count_has_no_2x_cap():
    rng = np.random.default_rng(1)
    C = rng.poisson(10, 200_000)
    for m in (0.5, 1.0, 1.5, 2.0, 2.6, 3.0):
        assert VFX.scale_count(np.random.default_rng(2), C, m).mean() == pytest.approx(C.mean() * m, rel=5e-3)
    assert VFX.scale_count(np.random.default_rng(2), np.array([4]), 3.0)[0] == 12


@pytest.mark.parametrize("pm,ok", [(4.2, True), (0.0, False), (-1.5, False), (float("nan"), False)])
def test_ypc_ratio_guard(pm, ok):
    assert VFX.ypc_ratio_ok(pm) is ok


def test_bad_volume_fix_value_is_refused(tmp_path):
    with pytest.raises(SV.SimV56Error, match="volume_fix"):
        SV.run_all(pd.DataFrame([STAFFORD]), week=8, src=tmp_path, workdir=tmp_path, volume_fix="yes")


def test_volume_fix_is_pinned_in_sha256sums():
    sums = SV.verify_engines()
    assert "volume_fix.py" in sums and {"cc_sim_v5.py", "cc_sim_v6.py", "cc_sim_v6_fix.py"} <= set(sums)


# ---------------------------------------------------------------- engines, end to end
def _run(tmp_path, legs, name, **kw):
    src = SV.make_src(tmp_path / "src")
    return SV.run_all(pd.DataFrame(legs), week=8, src=src, workdir=tmp_path / name, **kw)


def test_default_path_is_unchanged_and_opt_in_lowers_stafford_over_half_yard(tmp_path):
    want = float(_fixture_leg(STAFFORD["gsis"]).phase4_p_model)
    base = _run(tmp_path, [STAFFORD], "base")
    assert abs(SV.ensemble(base).p_under.iloc[0] - want) <= 1e-12
    fix = _run(tmp_path, [STAFFORD], "fix", volume_fix=True)
    for e in SV.ENGINES:     # two kept 0-carry games: P(>= 0.5 yds) falls in every engine and every mode
        for m in ("mc", "bias", "gr"):
            assert fix[e][f"p_{m}"].iloc[0] < base[e][f"p_{m}"].iloc[0], (e, m)
    assert SV.ensemble(fix).p_under.iloc[0] > want


def test_spread_moves_gr_volume_only_with_the_opt_in(tmp_path):
    fav, dog = dict(LOVE, spread=-10.0), dict(LOVE, spread=10.0, gsis=LOVE["gsis"])
    b_f, b_d = _run(tmp_path, [fav], "bf"), _run(tmp_path, [dog], "bd")
    f_f, f_d = _run(tmp_path, [fav], "ff", volume_fix=True), _run(tmp_path, [dog], "fd", volume_fix=True)
    for e in SV.ENGINES:
        assert b_f[e].p_gr.iloc[0] == b_d[e].p_gr.iloc[0], e             # default: spread cancels (memo B3)
        assert b_f[e].p_mc.iloc[0] == b_d[e].p_mc.iloc[0], e
        assert f_f[e].p_gr.iloc[0] > f_d[e].p_gr.iloc[0], e              # favoured -> more carries -> higher P(over)

"""Regression tests from Ghost6 vet 2026-11-05 — written to FAIL on unfixed tree."""
import sys, hashlib, subprocess, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from reconstruct import load_pbp, period_table_from_pbp, as_of_mask
from monte_carlo import simulate_game, raw_probs_from_sim, stable_seed
from settlement import settle_spread_2way
from market import build_mirror


def test_fg_includes_ot_when_requested_NO_DET():
    """Ghost6: 2026_01_NO_DET engine FG 24-24 vs true final 31-30 (OT)."""
    pbp = load_pbp(Path(__file__).resolve().parents[1] / "data/play_by_play_2026.parquet")
    tab = period_table_from_pbp(pbp)
    row = tab[tab.game_id == "2026_01_NO_DET"].iloc[0]
    g = pbp[pbp.game_id == "2026_01_NO_DET"]
    true_h = int(g.total_home_score.max())
    true_a = int(g.total_away_score.max())
    assert true_h == 31 and true_a == 30
    # regulation-only columns
    assert row.reg_home == 24 and row.reg_away == 24
    # full/final including OT
    assert row.fg_home == true_h and row.fg_away == true_a
    assert row.score_scope_fg == "includes_ot"
    assert row.score_scope_reg == "regulation_only"


def test_2026_ot_mismatch_count_zero_for_fg_final():
    pbp = load_pbp(Path(__file__).resolve().parents[1] / "data/play_by_play_2026.parquet")
    tab = period_table_from_pbp(pbp)
    bad = 0
    for gid, g in pbp.groupby("game_id"):
        r = tab[tab.game_id == gid].iloc[0]
        if r.fg_home != int(g.total_home_score.max()) or r.fg_away != int(g.total_away_score.max()):
            bad += 1
    assert bad == 0


def test_raw_probs_expose_push_and_decisive():
    root = Path(__file__).resolve().parents[1]
    hist = pd.concat([
        period_table_from_pbp(load_pbp(root / "data/play_by_play_2025.parquet")),
        period_table_from_pbp(load_pbp(root / "data/play_by_play_2026.parquet")),
    ], ignore_index=True)
    asof = hist[as_of_mask(hist, 2026, 9)]
    sim = simulate_game(asof, "BAL", "JAX", n=5000, seed=1, apply_gr=False)
    out = raw_probs_from_sim(sim, period="h1", market="spread_2way", line=-3.0, side="home")
    assert "p_win" in out and "p_push" in out and "p_lose" in out
    assert abs(out["p_win"] + out["p_push"] + out["p_lose"] - 1.0) < 1e-9
    # decisive conditional (pushes refunded) for two-way no-vig compare
    assert "p_win_decisive" in out
    if out["p_push"] < 1:
        assert abs(out["p_win_decisive"] - out["p_win"] / (1 - out["p_push"])) < 1e-9
    # legacy key monte_carlo remains unconditional win rate (documented)
    assert out["monte_carlo"] == out["p_win"]


def test_stable_seed_cross_process():
    s1 = stable_seed(20261105, 5, "2026_05_BUF_LA")
    # subprocess fresh interpreter
    code = (
        "import sys; sys.path.insert(0,%r); from monte_carlo import stable_seed; "
        "print(stable_seed(20261105,5,'2026_05_BUF_LA'))"
    ) % str(Path(__file__).resolve().parents[1])
    out = subprocess.check_output([sys.executable, "-c", code], env={**os.environ, "PYTHONHASHSEED": "random"})
    s2 = int(out.decode().strip())
    assert s1 == s2
    # must NOT equal unstable builtin hash path in general (document)
    assert isinstance(s1, int)


def test_pin_status_not_ok_when_identity_flags():
    m = build_mirror(
        {"monte_carlo": 0.5},
        pinnacle_two_way=(-110, -110),
        identity_flags=["PERIOD_MISMATCH"],
    )
    assert m.pinnacle_status != "OK"
    assert "PERIOD_MISMATCH" in m.flags


def test_three_way_probs_sum():
    root = Path(__file__).resolve().parents[1]
    hist = pd.concat([
        period_table_from_pbp(load_pbp(root / "data/play_by_play_2025.parquet")),
        period_table_from_pbp(load_pbp(root / "data/play_by_play_2026.parquet")),
    ], ignore_index=True)
    asof = hist[as_of_mask(hist, 2026, 9)]
    sim = simulate_game(asof, "BAL", "JAX", n=3000, seed=2, apply_gr=False)
    out = raw_probs_from_sim(sim, period="h1", market="winner_3way", line=0.0, side="home")
    assert abs(out["p_side"] + out["p_opp"] + out["p_tie"] - 1.0) < 1e-9

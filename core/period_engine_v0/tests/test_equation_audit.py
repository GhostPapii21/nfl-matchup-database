"""Regressions for the 2026-11-11 equation audit (docs/EQUATION_AUDIT_2026-11-11.md)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import pytest
from market import american_to_implied, novig_two_way, novig_three_way
from monte_carlo import simulate_game, raw_probs_from_sim, team_game_matrix
from reconstruct import load_pbp, period_table_from_pbp, as_of_mask
from settlement import settle_spread_2way, settle_total_2way

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def asof():
    hist = pd.concat([period_table_from_pbp(load_pbp(ROOT / "data/play_by_play_2025.parquet")),
                      period_table_from_pbp(load_pbp(ROOT / "data/play_by_play_2026.parquet"))], ignore_index=True)
    return hist[as_of_mask(hist, 2026, 9)]


def test_gr_legacy_inflates_variance_and_correlation(asof):
    mc = simulate_game(asof, "BAL", "JAX", n=60000, seed=1)["arrays"]
    old = simulate_game(asof, "BAL", "JAX", n=60000, seed=1, apply_gr=True, gr_scale="legacy_total_cv")["arrays"]
    # Var(h*S) = Var(h)(2 + cv^2) with cv the total CV: sd ~1.45x, corr(home, away) ~ 1/(2+cv^2)
    assert old["reg_home"].std() / mc["reg_home"].std() > 1.3
    assert np.corrcoef(old["reg_home"], old["reg_away"])[0, 1] > 0.35


def test_gr_covariance_scale_keeps_marginals(asof):
    mc = simulate_game(asof, "BAL", "JAX", n=60000, seed=1)
    gr = simulate_game(asof, "BAL", "JAX", n=60000, seed=1, apply_gr=True)
    assert gr["status"]["gr_scale"] == "within_game_covariance"
    ratio = gr["arrays"]["reg_home"].std() / mc["arrays"]["reg_home"].std()
    assert 0.95 < ratio < 1.15
    corr = np.corrcoef(gr["arrays"]["reg_home"], gr["arrays"]["reg_away"])[0, 1]
    assert corr < 0.15


def test_matchup_pair_mixes_offence_and_opponent_defence(asof):
    Gh, Ga = team_game_matrix(asof, "BAL"), team_game_matrix(asof, "JAX")
    want = 0.5 * Gh[:, :4].sum(1).mean() + 0.5 * Ga[:, 4:].sum(1).mean()
    sim = simulate_game(asof, "BAL", "JAX", n=80000, seed=3, sampling="matchup_pair")
    assert sim["summaries"]["reg"]["home_mean"] == pytest.approx(want, abs=0.25)
    with pytest.raises(ValueError):
        simulate_game(asof, "BAL", "JAX", n=10, sampling="nope")


def test_team_game_matrix_matches_rowwise(asof):
    G = team_game_matrix(asof, "BAL")
    rows = []
    for _, r in asof.iterrows():
        if r.home_team == "BAL":
            rows.append([r.q1_home, r.q2_home, r.q3_home, r.q4_home, r.q1_away, r.q2_away, r.q3_away, r.q4_away])
        elif r.away_team == "BAL":
            rows.append([r.q1_away, r.q2_away, r.q3_away, r.q4_away, r.q1_home, r.q2_home, r.q3_home, r.q4_home])
    assert np.array_equal(G, np.asarray(rows, float))


def test_vectorised_settlement_equals_scalar_rules(asof):
    sim = simulate_game(asof, "BAL", "JAX", n=5000, seed=5)
    h, a = sim["arrays"]["h1_home"], sim["arrays"]["h1_away"]
    for line in (-3.0, -2.5, 0.0, 3.0):
        r = raw_probs_from_sim(sim, period="h1", market="spread_2way", line=line, side="home")
        ref = np.array([settle_spread_2way(float(m), line) for m in h - a])
        assert (r["p_win"], r["p_push"]) == ((ref == "win").mean(), (ref == "push").mean())
    for line, side in ((20.0, "over"), (20.5, "under")):
        r = raw_probs_from_sim(sim, period="h1", market="total_2way", line=line, side=side)
        ref = np.array([settle_total_2way(float(t), line, side) for t in h + a])
        assert (r["p_win"], r["p_push"]) == ((ref == "win").mean(), (ref == "push").mean())


def test_american_price_validation_and_power_novig():
    for bad in (-99, 0, 50, float("nan")):
        with pytest.raises(ValueError):
            american_to_implied(bad)
    assert american_to_implied(100) == american_to_implied(-100) == 0.5
    assert novig_two_way(-110, -110, "power") == pytest.approx((0.5, 0.5))
    pm, pp = novig_two_way(-400, 300), novig_two_way(-400, 300, "power")
    assert sum(pp) == pytest.approx(1.0) and pp[1] < pm[1]  # power takes more margin from the long shot
    assert sum(novig_three_way(150, 180, 500, "power")) == pytest.approx(1.0)

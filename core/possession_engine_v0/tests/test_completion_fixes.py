"""Completion-pass fixes: apples-to-apples pace, defense-conditioned sample, empirical clock."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from config_load import load_config
from validation.realism import compare_sim_vs_actual_pace, actual_combined_snaps_per_game
from simulate import PlayCatalog, simulate_one, _clock_cost
from pbp_filter import load_team_history
from effects.apply_supported import annotate_snaps, EffectsCatalog
from state import GameState, apply_kickoff

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_apples_to_apples_pace_uses_combined_game_snaps():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    act = actual_combined_snaps_per_game(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    assert act["n_games"] == 15
    assert act["mean_combined_offense_snaps"] > 80
    # must be closer to ~120 than to 59
    assert act["mean_combined_offense_snaps"] > 100
    rep = compare_sim_vs_actual_pace(cfg, pbp_path=PBP, n_sims=30, seed=1)
    assert "actual_combined_offense_snaps" in rep
    assert rep["comparison"]["baseline"] == "combined_offense_snaps_per_involvement_game"


def test_defense_conditioned_sampling_prefers_opponent_when_enough_n():
    hist = load_team_history(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    # Build synthetic: ensure JAX vs BAL exists? may not — use any defteam with enough n
    df = hist["df"]
    # pick a defense that JAX faced often
    jx = df[(df.posteam == "JAX") & (df.play_type.isin(["pass", "run"]))]
    top_def = jx["defteam"].value_counts().index[0]
    n_vs = int((jx["defteam"] == top_def).sum())
    assert n_vs >= 1
    cat = PlayCatalog(df, min_n=5)
    cat.enable_defense_conditioning(True)
    st = GameState.new_game(home=top_def if top_def != "JAX" else "BAL", away="JAX")
    # If home is defense when JAX has ball
    if st.home == "JAX":
        st.away = top_def
    st.possession = "JAX"
    st.down, st.ydstogo, st.yardline_100 = 1, 10, 60
    rng = np.random.default_rng(0)
    tags = []
    for _ in range(40):
        row, tag = cat.sample_snap(rng, st, False)
        tags.append(tag)
        if row is not None and n_vs >= 5:
            # when enough n, should often hit DEF_COND
            pass
    if n_vs >= 5:
        assert any("DEF_COND" in t for t in tags), tags[:10]


def test_empirical_clock_costs_from_pbp_when_available():
    hist = load_team_history(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    costs = PlayCatalog.build_empirical_clock(hist["df"])
    assert "pass" in costs and "run" in costs
    assert costs["pass"] != 22 or costs.get("source") == "empirical_median_delta"
    # _clock_cost accepts override map
    rng = np.random.default_rng(0)
    a = _clock_cost("pass", rng, cost_map={"pass": 15, "run": 20})
    assert 5 <= a <= 40

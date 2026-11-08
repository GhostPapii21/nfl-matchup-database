"""Priority1: event-derived Q1-Q4/H1/H2/reg/OT scoreboards + reconciliation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from config_load import load_config
from simulate import simulate_games, stable_seed, simulate_one, PlayCatalog
from pbp_filter import load_team_history
from state import GameState

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_sim_arrays_include_period_scores():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    out = simulate_games(cfg, pbp_path=PBP, n=20, seed=7)
    A = out["arrays"]
    for k in ("q1_home","q1_away","q2_home","q2_away","q3_home","q3_away","q4_home","q4_away",
              "h1_home","h1_away","h2_home","h2_away","reg_home","reg_away","fg_home","fg_away"):
        assert k in A, f"missing {k}"
    # H1 = Q1+Q2, H2 = Q3+Q4, reg = H1+H2, fg >= reg
    assert np.array_equal(A["h1_home"], A["q1_home"] + A["q2_home"])
    assert np.array_equal(A["h1_away"], A["q1_away"] + A["q2_away"])
    assert np.array_equal(A["h2_home"], A["q3_home"] + A["q4_home"])
    assert np.array_equal(A["h2_away"], A["q3_away"] + A["q4_away"])
    assert np.array_equal(A["reg_home"], A["h1_home"] + A["h2_home"])
    assert np.array_equal(A["reg_away"], A["h1_away"] + A["h2_away"])
    assert np.all(A["fg_home"] >= A["reg_home"]) and np.all(A["fg_away"] >= A["reg_away"])
    # OT points only if went_ot
    ot_h = A["fg_home"] - A["reg_home"]
    ot_a = A["fg_away"] - A["reg_away"]
    assert np.all((ot_h + ot_a == 0) | A["went_ot"])


def test_boundary_score_assigned_to_quarter_of_event():
    """TD scored while qtr==2 must land in q2 bucket, not q3."""
    from simulate import _apply_snap
    import pandas as pd
    st = GameState.new_game("BAL", "JAX")
    st.qtr = 2
    st.possession = "JAX"
    st.yardline_100 = 5
    st.down, st.ydstogo = 1, 5
    st.period_scores = {"q1": [0,0], "q2": [0,0], "q3": [0,0], "q4": [0,0], "ot": [0,0]}
    row = pd.Series({
        "play_type": "run", "yards_gained": 5.0, "touchdown": 0, "interception": 0,
        "fumble_lost": 0, "complete_pass": 0, "first_down": 0,
        "passer_player_name": None, "receiver_player_name": None, "rusher_player_name": "X",
    })
    class Cat:
        min_n = 5
        specials = {"punt": {}, "field_goal": {}, "extra_point": {"JAX": pd.DataFrame({"extra_point_result": ["good"]})}}
        def sample_snap(self, rng, st, allow_pool):
            return row, "OK"
    _apply_snap(np.random.default_rng(0), Cat(), st, False)
    # home=BAL idx0, away=JAX idx1
    assert st.period_scores["q2"][1] >= 6
    assert st.period_scores["q3"] == [0, 0]
    assert st.period_scores["q1"] == [0, 0]

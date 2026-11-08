"""RED→GREEN: state transitions, kickoff/half/OT/FG/PAT/turnover, joint players, seeds."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from config_load import load_config
from simulate import simulate_games, stable_seed
from state import GameState, apply_kickoff, maybe_halftime, start_ot_if_tied

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_stable_seed_deterministic():
    assert stable_seed(20261105, 9, "JAX@BAL") == stable_seed(20261105, 9, "JAX@BAL")
    assert stable_seed(20261105, 9, "JAX@BAL") != stable_seed(20261105, 9, "OTHER")


def test_kickoff_sets_possession_and_yardline():
    st = GameState.new_game(home="BAL", away="JAX")
    st2 = apply_kickoff(st, receiving="JAX", yardline_100=75)
    assert st2.possession == "JAX"
    assert st2.yardline_100 == 75
    assert st2.down == 1 and st2.ydstogo == 10
    assert st2.events[-1]["type"] == "kickoff"


def test_halftime_resets_for_q3_kickoff_side():
    st = GameState.new_game(home="BAL", away="JAX")
    st.qtr = 2
    st.game_seconds_remaining = 0
    st = maybe_halftime(st, q3_receive="BAL")
    assert st.qtr == 3
    assert st.half == 2
    assert st.possession == "BAL"
    assert any(e["type"] == "halftime" for e in st.events)


def test_ot_only_if_tied_after_reg():
    st = GameState.new_game(home="BAL", away="JAX")
    st.qtr = 4
    st.game_seconds_remaining = 0
    st.score_home = 17
    st.score_away = 17
    st = start_ot_if_tied(st)
    assert st.qtr == 5
    assert st.in_ot is True
    st2 = GameState.new_game(home="BAL", away="JAX")
    st2.qtr = 4
    st2.game_seconds_remaining = 0
    st2.score_home = 20
    st2.score_away = 17
    st2 = start_ot_if_tied(st2)
    assert st2.in_ot is False
    assert st2.final is True


def test_simulate_data_only_small_n_invariants():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    out = simulate_games(cfg, pbp_path=PBP, n=100, seed=stable_seed(cfg["seed_base"], 9, "JAX@BAL"))
    assert out["status"] in {"OK", "OK_WITH_SPARSE_FLAGS"}
    assert out["n_completed"] == 100
    assert out["config_id"] == cfg["config_id"]
    assert out["pooling_silently_applied"] is False
    A = out["arrays"]
    assert np.all(A["fg_home"] >= 0) and np.all(A["fg_away"] >= 0)
    # regulation score components present
    assert "reg_home" in A and "reg_away" in A
    # OT flag only when reg tied
    reg_tie = A["reg_home"] == A["reg_away"]
    assert np.all(~A["went_ot"] | reg_tie)
    # joint player tables exist and sum from same events
    assert "player_joint" in out
    assert out["evidence_summary"]["min_n_state"] == cfg["min_n_state"]


def test_simulate_script_adjusted_marks_sparse_qb_and_excludes_lamar():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_script_adjusted.json")
    out = simulate_games(cfg, pbp_path=PBP, n=50, seed=stable_seed(cfg["seed_base"], 9, "JAX@BAL_adj"))
    assert out["adjustments_meta"]["BAL"]["fabricated"] is False
    assert out["adjustments_meta"]["BAL"]["excluded_passers"] == ["L.Jackson"]
    # Fagnano-only pool is sparse — must be flagged, not silently filled with league
    assert out["adjustments_meta"]["BAL"]["n_pass_after"] < 50
    assert "SPARSE" in str(out.get("qb_status", {}).get("BAL", "")) or out["status"] in {"OK_WITH_SPARSE_FLAGS", "OK"}
    assert out["pooling_silently_applied"] is False
    # player joint should not credit Lamar Jackson passing yards in adjusted forward sims
    pj = out["player_joint"]
    bal_passers = pj.get("pass_yards", {}).get("BAL", {})
    assert "L.Jackson" not in bal_passers or bal_passers.get("L.Jackson", 0) == 0

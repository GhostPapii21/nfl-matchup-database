"""Regressions from Codex review of e041e95 (2026-11-05 18:32 EST)."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
import simulate as sim
from effects.apply_supported import EffectsCatalog, annotate_snaps
from test_complete_pass2 import _row, _st


def test_defense_players_not_credited_to_offense():
    offense = pd.DataFrame([_row() for _ in range(5)])
    defense = pd.DataFrame([_row(posteam="CCC", rusher_player_name="CCC_RB") for _ in range(5)])
    cat = sim.PlayCatalog(offense, 3, defense); cat.enable_defense_allowed(1)
    st = _st()
    sim._apply_snap(np.random.default_rng(0), cat, st, False)
    assert "CCC_RB" not in st.player_counts.get("rush_yards", {}).get("AAA", {})


def test_touchdown_credit_cannot_exceed_distance_to_goal():
    df = pd.DataFrame([_row(yards_gained=60) for _ in range(5)])
    st = _st(yardline_100=10)
    sim._apply_snap(np.random.default_rng(0), sim.PlayCatalog(df, 3), st, False)
    assert st.player_counts["rush_yards"]["AAA"]["RB"] == 10


def test_defense_mixture_not_bypassed_by_h2h():
    offense = pd.DataFrame([_row() for _ in range(5)])
    defense = pd.DataFrame([_row(posteam="CCC") for _ in range(5)])
    cat = sim.PlayCatalog(offense, 3, defense); cat.enable_defense_allowed(1); cat.enable_defense_conditioning(True)
    _, tag = cat.sample_snap(np.random.default_rng(0), _st(), False)
    assert tag.startswith("DEF_ALLOWED")


def test_effect_coarsening_is_visible_to_summary():
    df = pd.DataFrame([_row(down=1, play_type="pass") for _ in range(5)] + [_row(down=2, play_type="pass") for _ in range(5)])
    ann = annotate_snaps(df); ann["ftn_joined"] = True; ann["is_blitz_ftn"] = ann.down == 2
    cat = EffectsCatalog(sim.PlayCatalog(df, 3), ann, enable_blitz_strata=True); cat.blitz_rate["AAA"] = 1
    st = _st()
    sim._apply_snap(np.random.default_rng(0), cat, st, False)
    assert any(f.startswith("COARSE") for f in st.sparse_flags), st.sparse_flags
    assert any(f.startswith("EFFECT_") for f in st.sparse_flags), st.sparse_flags


def test_simulate_games_enforces_target_week():
    cfg = {"history": {"teams": ["AAA", "BBB"], "season": 2026, "weeks_inclusive": [1, 2]},
           "game": {"week_asof_exclusive": 2}, "min_n_state": 5, "config_id": "x", "mode": "x"}
    with pytest.raises(ValueError):
        sim.simulate_games(cfg, pbp_path="unused", n=1, seed=0)


def test_fg_bootstrap_resamples_games():
    from run_complete_pass2 import paired_game_diffs
    g = pd.DataFrame({"game_id": ["a", "b"], "abs_err_home": [0, 20], "abs_err_away": [0, 20],
                      "baseline_abs_err_home": [10, 10], "baseline_abs_err_away": [10, 10]})
    d = paired_game_diffs(g)
    assert len(d) == 2 and list(d) == [-10, 10]

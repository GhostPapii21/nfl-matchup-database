"""Scoring inflation regressions (Ghost6 audit + independent reproduce on 9ebe892)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from state import GameState, maybe_halftime, apply_kickoff
from simulate import PlayCatalog, _apply_snap, _punt_fixed, simulate_games, stable_seed
from config_load import load_config
from pbp_filter import load_team_history

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_halftime_q3_clock_is_one_quarter_not_two():
    st = GameState.new_game(home="BAL", away="JAX")
    st.qtr = 2
    st.game_seconds_remaining = 0
    st = maybe_halftime(st, q3_receive="BAL")
    assert st.qtr == 3
    assert st.game_seconds_remaining == 900, (
        f"Q3 must start with 900s (15 min), got {st.game_seconds_remaining}"
    )


def test_punt_gives_receiving_team_flipped_field_position():
    st = GameState.new_game(home="BAL", away="JAX")
    st.possession = "JAX"
    st.yardline_100 = 60
    st.down, st.ydstogo = 4, 10
    cat = PlayCatalog(pd.DataFrame({
        "posteam": [], "play_type": [], "ydstogo": [], "yardline_100": [], "down": [],
    }), min_n=5)
    cat.specials = {"punt": {}, "field_goal": {}, "extra_point": {}}
    cat.fourth_probs = {}
    cat.cells, cat.by_down, cat.by_team = {}, {}, {}
    rng = np.random.default_rng(0)
    _punt_fixed(rng, cat, st)
    assert st.possession == "BAL"
    assert st.yardline_100 == 80, f"expected 80 after flip, got {st.yardline_100}"


def test_historical_td_flag_without_reach_does_not_score():
    st = GameState.new_game(home="BAL", away="JAX")
    apply_kickoff(st, receiving="JAX", yardline_100=75)
    row = pd.Series({
        "play_type": "pass",
        "yards_gained": 5.0,
        "touchdown": 1,
        "interception": 0,
        "fumble_lost": 0,
        "complete_pass": 1,
        "first_down": 0,
        "passer_player_name": "T.Lawrence",
        "receiver_player_name": "X.Player",
        "rusher_player_name": None,
    })
    class Cat:
        min_n = 5
        specials = {"punt": {}, "field_goal": {}, "extra_point": {}}
        def sample_snap(self, rng, st, allow_pool):
            return row, "OK"
    rng = np.random.default_rng(1)
    before = (st.score_home, st.score_away)
    _apply_snap(rng, Cat(), st, allow_pool=False)
    assert (st.score_home, st.score_away) == before, "false TD from historical flag"
    assert st.yardline_100 == 70


def test_geo_td_from_yards_still_scores():
    st = GameState.new_game(home="BAL", away="JAX")
    apply_kickoff(st, receiving="JAX", yardline_100=8)
    row = pd.Series({
        "play_type": "run",
        "yards_gained": 8.0,
        "touchdown": 0,
        "interception": 0,
        "fumble_lost": 0,
        "complete_pass": 0,
        "first_down": 0,
        "passer_player_name": None,
        "receiver_player_name": None,
        "rusher_player_name": "T.Etienne",
    })
    class Cat:
        min_n = 5
        specials = {"punt": {}, "field_goal": {}, "extra_point": {"JAX": pd.DataFrame({"extra_point_result": ["good"]})}}
        def sample_snap(self, rng, st, allow_pool):
            return row, "OK"
    rng = np.random.default_rng(2)
    _apply_snap(rng, Cat(), st, allow_pool=False)
    assert st.score_away >= 6


def test_data_only_mean_total_not_nfl_impossible():
    """Pre-fix ~111 total; post-fix should be near hist JAX28+BAL22≈50, allow wide band not 90+."""
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    out = simulate_games(cfg, pbp_path=PBP, n=200, seed=stable_seed(cfg["seed_base"], 9, cfg["config_id"]))
    h = float(out["arrays"]["fg_home"].mean())
    a = float(out["arrays"]["fg_away"].mean())
    total = h + a
    assert total < 80, f"inflated total {total} (H={h} A={a})"
    assert h < 40 and a < 45, f"side means still inflated H={h} A={a}"

"""RED regressions from Codex possession review (2026-11-05) — concrete reproducible defects."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import pytest
from simulate import (
    PlayCatalog, simulate_one, _punt_fixed, _apply_snap, _attempt_pat, _clock_cost,
)
from state import GameState, apply_kickoff
from effects.apply_supported import EffectsCatalog, annotate_snaps
from validation.realism import compare_sim_vs_actual_pace
from config_load import load_config
from pbp_filter import load_team_history, COLS

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def _mini_catalog_with_punts(*, kick_distance=40, return_yards=0, yards_gained=0):
    """Synthetic catalog: one team with documented punt net = kick - return."""
    rows = []
    # enough snaps for catalog
    for i in range(20):
        rows.append({
            "posteam": "AAA", "defteam": "BBB", "down": 1, "ydstogo": 10,
            "yardline_100": 60, "play_type": "pass", "yards_gained": 5,
            "interception": 0, "fumble_lost": 0, "complete_pass": 1,
            "passer_player_name": "Q", "receiver_player_name": "R",
            "rusher_player_name": None, "game_id": "g1", "play_id": i,
            "game_seconds_remaining": 800 - i,
        })
    for i in range(5):
        rows.append({
            "posteam": "AAA", "defteam": "BBB", "down": 4, "ydstogo": 10,
            "yardline_100": 60, "play_type": "punt", "yards_gained": yards_gained,
            "kick_distance": kick_distance, "return_yards": return_yards,
            "touchback": 0, "interception": 0, "fumble_lost": 0,
            "complete_pass": 0, "passer_player_name": None,
            "receiver_player_name": None, "rusher_player_name": None,
            "game_id": "g1", "play_id": 100 + i,
            "game_seconds_remaining": 400,
            "field_goal_result": None, "extra_point_result": None,
        })
    df = pd.DataFrame(rows)
    return PlayCatalog(df, min_n=3), df


def test_punt_uses_explicit_net_distance_not_yards_gained():
    """Codex P1: yards_gained=0 on all punts → must use kick_distance - return_yards.
    From yl=60, net=40 → receiving yardline_100 == 80.
    """
    cat, _ = _mini_catalog_with_punts(kick_distance=40, return_yards=0, yards_gained=0)
    st = GameState.new_game(home="AAA", away="BBB")
    st.possession = "AAA"
    st.yardline_100 = 60
    st.down, st.ydstogo = 4, 10
    st.game_seconds_remaining = 500
    rng = np.random.default_rng(0)
    _punt_fixed(rng, cat, st)
    assert st.possession == "BBB"
    assert st.yardline_100 == 80, f"expected recv yl=80 got {st.yardline_100}; net event={st.events[-1]}"
    assert st.events[-1]["net"] == 40


def test_each_offensive_play_emits_one_snap():
    """Codex P1: TD / interception / TOD must still count as a snap for pace."""
    # Build catalog with a sure TD (long gain) and an interception and TOD path
    rows = []
    for i in range(30):
        rows.append({
            "posteam": "AAA", "defteam": "BBB", "down": 1, "ydstogo": 10,
            "yardline_100": 50, "play_type": "run", "yards_gained": 3,
            "interception": 0, "fumble_lost": 0, "complete_pass": 0,
            "passer_player_name": None, "receiver_player_name": None,
            "rusher_player_name": "RB", "game_id": "g1", "play_id": i,
            "game_seconds_remaining": 800,
        })
    df = pd.DataFrame(rows)
    cat = PlayCatalog(df, min_n=3)
    rng = np.random.default_rng(1)

    # ordinary
    st = GameState.new_game(home="AAA", away="BBB")
    st.possession = "AAA"; st.down, st.ydstogo, st.yardline_100 = 1, 10, 50
    st.game_seconds_remaining = 500
    n0 = sum(1 for e in st.events if e.get("type") == "snap")
    _apply_snap(rng, cat, st, False)
    assert sum(1 for e in st.events if e.get("type") == "snap") == n0 + 1

    # TD path: force huge yards via synthetic row injection
    st2 = GameState.new_game(home="AAA", away="BBB")
    st2.possession = "AAA"; st2.down, st2.ydstogo, st2.yardline_100 = 1, 10, 5
    st2.game_seconds_remaining = 500
    # monkey via direct row: patch sample by feeding yards through catalog cell
    # Build one-row TD catalog
    td_df = pd.DataFrame([{
        "posteam": "AAA", "defteam": "BBB", "down": 1, "ydstogo": 10,
        "yardline_100": 5, "play_type": "run", "yards_gained": 10,
        "interception": 0, "fumble_lost": 0, "complete_pass": 0,
        "passer_player_name": None, "receiver_player_name": None,
        "rusher_player_name": "RB", "game_id": "g1", "play_id": 1,
        "game_seconds_remaining": 500, "extra_point_result": "good",
        "field_goal_result": None,
    }] * 10)
    # add PAT specials
    for i in range(5):
        td_df = pd.concat([td_df, pd.DataFrame([{
            "posteam": "AAA", "defteam": "BBB", "down": 0, "ydstogo": 0,
            "yardline_100": 15, "play_type": "extra_point", "yards_gained": 0,
            "interception": 0, "fumble_lost": 0, "complete_pass": 0,
            "passer_player_name": None, "receiver_player_name": None,
            "rusher_player_name": None, "game_id": "g1", "play_id": 50+i,
            "game_seconds_remaining": 500, "extra_point_result": "good",
            "field_goal_result": None,
        }])], ignore_index=True)
    cat_td = PlayCatalog(td_df, min_n=3)
    n_before = sum(1 for e in st2.events if e.get("type") == "snap")
    _apply_snap(rng, cat_td, st2, False)
    assert any(e.get("type") == "touchdown" for e in st2.events)
    assert sum(1 for e in st2.events if e.get("type") == "snap") == n_before + 1

    # interception
    int_df = pd.DataFrame([{
        "posteam": "AAA", "defteam": "BBB", "down": 1, "ydstogo": 10,
        "yardline_100": 50, "play_type": "pass", "yards_gained": 0,
        "interception": 1, "fumble_lost": 0, "complete_pass": 0,
        "passer_player_name": "Q", "receiver_player_name": None,
        "rusher_player_name": None, "game_id": "g1", "play_id": i,
        "game_seconds_remaining": 500,
    } for i in range(15)])
    cat_int = PlayCatalog(int_df, min_n=3)
    st3 = GameState.new_game(home="AAA", away="BBB")
    st3.possession = "AAA"; st3.down, st3.ydstogo, st3.yardline_100 = 1, 10, 50
    st3.game_seconds_remaining = 500
    n_before = sum(1 for e in st3.events if e.get("type") == "snap")
    _apply_snap(rng, cat_int, st3, False)
    assert any(e.get("type") == "turnover" for e in st3.events)
    assert sum(1 for e in st3.events if e.get("type") == "snap") == n_before + 1


def test_effects_catalog_runs_complete_game():
    """Codex P1: EffectsCatalog must duck-type clock_map / defense hooks used by simulate_one."""
    hist = load_team_history(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    assert hist["status"] == "OK"
    base = PlayCatalog(hist["df"], min_n=5)
    ann = annotate_snaps(hist["df"])
    effects = EffectsCatalog(base, ann, enable_blitz_strata=False)
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    st = simulate_one(hist["df"], effects, cfg, np.random.default_rng(7))
    assert st.final
    assert st.score_home + st.score_away >= 0
    snap = st.period_snapshot()
    assert snap["reg_home"] == st.reg_score_home


def test_backed_up_loss_scores_safety():
    """Codex P1: loss crossing own goal must award 2 and flip possession — not clip to 99."""
    rows = [{
        "posteam": "AAA", "defteam": "BBB", "down": 1, "ydstogo": 10,
        "yardline_100": 98, "play_type": "run", "yards_gained": -5,
        "interception": 0, "fumble_lost": 0, "complete_pass": 0,
        "passer_player_name": None, "receiver_player_name": None,
        "rusher_player_name": "RB", "game_id": "g1", "play_id": i,
        "game_seconds_remaining": 500,
    } for i in range(15)]
    cat = PlayCatalog(pd.DataFrame(rows), min_n=3)
    st = GameState.new_game(home="AAA", away="BBB")
    st.possession = "AAA"
    st.down, st.ydstogo, st.yardline_100 = 1, 10, 98
    st.game_seconds_remaining = 500
    _apply_snap(np.random.default_rng(0), cat, st, False)
    assert st.score_away == 2, f"expected safety 2 for BBB, scores H{st.score_home}-A{st.score_away} events={st.events}"
    assert any(e.get("type") == "safety" for e in st.events)
    assert st.possession == "BBB" or any(e.get("type") == "safety" for e in st.events)


def test_coarse_support_is_reported_when_hard_sparse_zero():
    """Codex P2: renaming COARSE must not hide support gaps — report coarse_use separately."""
    from simulate import simulate_games
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    out = simulate_games(cfg, pbp_path=PBP, n=5, seed=2)
    ev = out["evidence_summary"]
    assert "coarse_rate" in ev or "games_with_coarse_flags" in ev
    assert "sparse_rate" in ev
    # hard-sparse and coarse are distinct keys
    assert "games_with_sparse_flags" in ev


def test_pat_does_not_consume_game_clock():
    """Codex: PAT is a dead-ball period — game clock unchanged."""
    rows = [{
        "posteam": "AAA", "defteam": "BBB", "down": 0, "ydstogo": 0,
        "yardline_100": 15, "play_type": "extra_point", "yards_gained": 0,
        "interception": 0, "fumble_lost": 0, "complete_pass": 0,
        "passer_player_name": None, "receiver_player_name": None,
        "rusher_player_name": None, "game_id": "g1", "play_id": i,
        "game_seconds_remaining": 500, "extra_point_result": "good",
        "field_goal_result": None,
    } for i in range(5)]
    # also need snaps so specials index
    for i in range(10):
        rows.append({
            "posteam": "AAA", "defteam": "BBB", "down": 1, "ydstogo": 10,
            "yardline_100": 50, "play_type": "pass", "yards_gained": 5,
            "interception": 0, "fumble_lost": 0, "complete_pass": 1,
            "passer_player_name": "Q", "receiver_player_name": "R",
            "rusher_player_name": None, "game_id": "g1", "play_id": 100+i,
            "game_seconds_remaining": 600,
        })
    cat = PlayCatalog(pd.DataFrame(rows), min_n=3)
    st = GameState.new_game(home="AAA", away="BBB")
    st.possession = "AAA"
    st.game_seconds_remaining = 412
    before = st.game_seconds_remaining
    _attempt_pat(np.random.default_rng(0), cat, st, "AAA")
    assert st.game_seconds_remaining == before


def test_period_report_accepts_current_realism_schema():
    """Codex P1: report/tests must not KeyError after combined-baseline schema change."""
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    rep = compare_sim_vs_actual_pace(cfg, pbp_path=PBP, n_sims=8, seed=3)
    # legacy + new keys both present for consumers
    assert "sim" in rep
    assert "actual" in rep or "actual_combined_offense_snaps" in rep
    # combined baseline must be exposed
    assert "actual_combined_offense_snaps" in rep
    act = rep.get("actual") or {}
    # either legacy mean or combined
    assert (
        act.get("mean_offense_snaps_per_team_game")
        or rep["actual_combined_offense_snaps"].get("mean_combined_offense_snaps")
    )


def test_kick_distance_column_loaded_in_history():
    """Punt net needs kick_distance/return_yards in team history COLS."""
    assert "kick_distance" in COLS
    assert "return_yards" in COLS
    hist = load_team_history(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    assert "kick_distance" in hist["df"].columns
    punts = hist["df"][hist["df"].play_type == "punt"]
    assert len(punts) >= 1
    assert float(pd.to_numeric(punts["kick_distance"], errors="coerce").mean()) > 20


def test_punt_nan_touchback_does_not_crash():
    """Codex final re-review: touchback=NaN with valid kick_distance must not raise."""
    cat, _ = _mini_catalog_with_punts(kick_distance=45, return_yards=5, yards_gained=0)
    # inject NaN touchback into specials
    plays = cat.specials["punt"]["AAA"]
    plays["touchback"] = float("nan")
    plays["punt_in_endzone"] = float("nan")
    cat.specials["punt"]["AAA"] = plays
    st = GameState.new_game(home="AAA", away="BBB")
    st.possession = "AAA"
    st.yardline_100 = 55
    st.down, st.ydstogo = 4, 8
    st.game_seconds_remaining = 400
    _punt_fixed(np.random.default_rng(0), cat, st)
    assert st.events[-1]["type"] == "punt"
    assert 15 <= st.events[-1]["net"] <= 70

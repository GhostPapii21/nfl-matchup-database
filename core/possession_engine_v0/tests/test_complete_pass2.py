"""RED-first regressions for completion pass 2 (Rico 2026-11-05 18:11 EST)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from simulate import PlayCatalog, simulate_games, _fourth_down_decision, _attempt_fg, _apply_snap, build_catalog
from state import GameState
from effects.apply_supported import EffectsCatalog, annotate_snaps
from config_load import load_config
from validation.realism import actual_combined_snaps_per_game

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"
CFG = ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json"


def _row(**kw):
    base = dict(posteam="AAA", defteam="BBB", down=1, ydstogo=10, yardline_100=50, play_type="run",
                yards_gained=3, interception=0, fumble_lost=0, complete_pass=0, sack=0,
                passer_player_name=None, receiver_player_name=None, rusher_player_name="RB",
                game_id="g1", play_id=0, game_seconds_remaining=500,
                field_goal_result=None, extra_point_result=None, kick_distance=np.nan)
    base.update(kw)
    return base


def _st(**kw):
    st = GameState.new_game(home="AAA", away="BBB")
    st.possession = "AAA"; st.down = 1; st.ydstogo = 10; st.yardline_100 = 50; st.game_seconds_remaining = 500
    for k, v in kw.items():
        setattr(st, k, v)
    return st


def test_blitz_strata_preserves_run_selection():
    rows = [_row(play_id=i, play_type="run") for i in range(40)]
    rows += [_row(play_id=100 + i, play_type="pass", down=2) for i in range(20)]
    df = pd.DataFrame(rows)
    ann = annotate_snaps(df)
    ann["ftn_joined"] = True
    ann["is_blitz_ftn"] = ann.index % 2 == 0
    eff = EffectsCatalog(PlayCatalog(df, min_n=3), ann, enable_blitz_strata=True)
    eff.blitz_rate["AAA"] = 1.0
    rng = np.random.default_rng(0)
    st = _st(down=1)
    types = [str(eff.sample_snap(rng, st, False)[0]["play_type"]) for _ in range(50)]
    assert all(t == "run" for t in types), types


def test_blitz_strata_only_conditions_called_pass():
    rows = [_row(play_id=i, play_type="pass", down=1, yards_gained=(20 if i % 2 == 0 else 1)) for i in range(40)]
    df = pd.DataFrame(rows)
    ann = annotate_snaps(df); ann["ftn_joined"] = True; ann["is_blitz_ftn"] = ann.index % 2 == 0
    eff = EffectsCatalog(PlayCatalog(df, min_n=3), ann, enable_blitz_strata=True)
    eff.blitz_rate["AAA"] = 1.0
    rng = np.random.default_rng(1)
    rows_out = [eff.sample_snap(rng, _st(), False) for _ in range(30)]
    assert all(r[0]["yards_gained"] == 20 for r in rows_out)
    assert all("BLITZ" in r[1] for r in rows_out)


def test_fourth_down_conditions_on_field_position():
    rows = []
    # deep own territory: always punt; opp 20: always FG
    for i in range(10):
        rows.append(_row(play_id=i, down=4, ydstogo=8, yardline_100=80, play_type="punt", kick_distance=45))
        rows.append(_row(play_id=50 + i, down=4, ydstogo=8, yardline_100=20, play_type="field_goal",
                         kick_distance=38, field_goal_result="made"))
    rows += [_row(play_id=200 + i) for i in range(10)]
    cat = PlayCatalog(pd.DataFrame(rows), min_n=3)
    rng = np.random.default_rng(0)
    deep = {_fourth_down_decision(rng, cat, _st(down=4, ydstogo=8, yardline_100=80)) for _ in range(40)}
    red = {_fourth_down_decision(rng, cat, _st(down=4, ydstogo=8, yardline_100=20)) for _ in range(40)}
    assert deep == {"punt"}, deep
    assert red == {"field_goal"}, red


def test_fourth_down_sparse_fallback_flagged():
    rows = [_row(play_id=i) for i in range(10)]
    rows += [_row(play_id=50 + i, down=4, ydstogo=8, yardline_100=80, play_type="punt", kick_distance=45) for i in range(6)]
    cat = PlayCatalog(pd.DataFrame(rows), min_n=3)
    st = _st(down=4, ydstogo=1, yardline_100=30)
    _fourth_down_decision(np.random.default_rng(0), cat, st)
    assert any("4TH" in f for f in st.sparse_flags), st.sparse_flags


def test_fg_make_rate_conditioned_on_distance():
    rows = [_row(play_id=i) for i in range(10)]
    for i in range(10):
        rows.append(_row(play_id=100 + i, play_type="field_goal", kick_distance=25, field_goal_result="made", down=4))
        rows.append(_row(play_id=200 + i, play_type="field_goal", kick_distance=58, field_goal_result="missed", down=4))
    cat = PlayCatalog(pd.DataFrame(rows), min_n=3)
    makes = 0
    for s in range(30):
        st = _st(down=4, yardline_100=7)  # ~25-yd kick
        _attempt_fg(np.random.default_rng(s), cat, st)
        makes += st.score_home
    assert makes == 90


def test_missed_fg_spot_of_kick_rule():
    rows = [_row(play_id=i) for i in range(10)]
    rows += [_row(play_id=100 + i, play_type="field_goal", kick_distance=50, field_goal_result="missed", down=4) for i in range(10)]
    cat = PlayCatalog(pd.DataFrame(rows), min_n=3)
    st = _st(down=4, yardline_100=32)  # spot of kick = 39 → opp yl 61
    _attempt_fg(np.random.default_rng(0), cat, st)
    assert st.possession == "BBB" and st.yardline_100 == 61, st.yardline_100
    st2 = _st(down=4, yardline_100=5)  # spot 12 → inside 20 → opp yl 80
    rows2 = [_row(play_id=i) for i in range(10)] + [_row(play_id=100 + i, play_type="field_goal", kick_distance=23, field_goal_result="missed", down=4) for i in range(10)]
    _attempt_fg(np.random.default_rng(0), PlayCatalog(pd.DataFrame(rows2), min_n=3), st2)
    assert st2.yardline_100 == 80


def test_simulate_games_wires_effects_with_provenance():
    cfg = load_config(CFG)
    out = simulate_games(cfg, pbp_path=PBP, n=5, seed=3)
    prov = out["effects_provenance"]
    assert prov["catalog_class"] == "EffectsCatalog"
    assert prov["ftn_join"]["status"] in ("OK", "MISSING_FTN")
    assert "blitz_strata_events" in out["evidence_summary"]


def test_def_allowed_interaction_used_for_jaxbal_when_enabled():
    cfg = load_config(CFG)
    cfg["defense_interaction"] = {"mode": "opponent_allowed", "weight": 0.5}
    out = simulate_games(cfg, pbp_path=PBP, n=5, seed=3)
    assert out["evidence_summary"]["def_interaction_events"] > 0
    assert out["effects_provenance"]["defense_interaction"]["label"].startswith("STRUCTURAL_ASSUMPTION")


def test_data_only_default_has_no_def_allowed_mixing():
    out = simulate_games(load_config(CFG), pbp_path=PBP, n=3, seed=3)
    assert out["evidence_summary"]["def_interaction_events"] == 0


def test_player_credit_negative_completion_and_fumble_rush():
    df = pd.DataFrame([_row(play_id=i, play_type="pass", complete_pass=1, yards_gained=-3,
                            passer_player_name="Q", receiver_player_name="R", rusher_player_name=None) for i in range(10)])
    st = _st()
    _apply_snap(np.random.default_rng(0), PlayCatalog(df, min_n=3), st, False)
    assert st.player_counts["pass_yards"]["AAA"]["Q"] == -3
    assert st.player_counts["rec_yards"]["AAA"]["R"] == -3
    df2 = pd.DataFrame([_row(play_id=i, yards_gained=6, fumble_lost=1) for i in range(10)])
    st2 = _st()
    _apply_snap(np.random.default_rng(0), PlayCatalog(df2, min_n=3), st2, False)
    assert st2.player_counts["rush_yards"]["AAA"]["RB"] == 6


def test_player_joint_samples_exported():
    out = simulate_games(load_config(CFG), pbp_path=PBP, n=4, seed=3)
    assert len(out["player_samples"]) == 4
    assert isinstance(out["player_samples"][0], dict)


def test_realism_n_team_games_is_group_count():
    act = actual_combined_snaps_per_game(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    assert act["n_team_games"] >= 15
    assert "n_team_games" in act

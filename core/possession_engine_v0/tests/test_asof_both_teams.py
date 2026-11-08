"""Priority2: both teams' as-of histories for target games; W1 skip; no league/prior-year pool."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation.asof_grade import build_asof_history_for_game, grade_week_games, list_jaxbal_games

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_w2_game_loads_both_teams_prior_plays():
    # 2026_02_JAX_DEN — JAX and DEN each need prior week-1 plays (DEN may have W1)
    hist = build_asof_history_for_game(PBP, home="DEN", away="JAX", season=2026, week=2)
    assert hist["status"] == "OK"
    assert set(hist["df"]["posteam"].unique()) <= {"DEN", "JAX"}
    assert hist["df"]["week"].max() < 2
    assert hist["evidence"]["n_plays_home"] > 0 and hist["evidence"]["n_plays_away"] > 0
    assert hist["evidence"].get("prior_year_pooled") is False
    assert hist["evidence"].get("league_pooled") is False


def test_w1_still_ungradable():
    rows = grade_week_games(PBP, weeks=[1], n_sims=5, seed_base=1)
    assert all(r["grade_status"] == "UNGRADEABLE_NO_OWN_SEASON_HISTORY" for r in rows)


def test_w3_plus_can_grade_full_not_opponent_out_of_scope():
    rows = grade_week_games(PBP, weeks=[3], n_sims=20, seed_base=20261105)
    assert len(rows) == 2
    for r in rows:
        assert r["grade_status"] == "GRADED_FULL", r
        assert r["pred_home_mean"] is not None
        assert r["silent_pool_applied"] is False

"""Period grading vs reconstructed actuals for as-of GRADED_FULL games."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from validation.period_grade import reconstruct_actual_periods, grade_periods_for_games
from validation.asof_grade import list_jaxbal_games, grade_week_games

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_reconstruct_actual_periods_jax_den():
    act = reconstruct_actual_periods(PBP, "2026_02_JAX_DEN")
    assert act["status"] == "OK"
    assert act["h1_home"] == 3 and act["h1_away"] == 10
    assert act["reg_home"] == 20 and act["fg_home"] == 20
    assert act["q1_home"] + act["q2_home"] == act["h1_home"]


def test_period_grade_includes_mae_separate_from_fg():
    # small n for speed — week 2 only (2 games, both should grade)
    rows = grade_week_games(PBP, weeks=[2], n_sims=30, seed_base=20261105)
    assert all(r["grade_status"] == "GRADED_FULL" for r in rows)
    out = grade_periods_for_games(PBP, rows, n_sims=30, seed_base=20261105)
    assert "by_game" in out and len(out["by_game"]) == 2
    assert "metrics" in out
    m = out["metrics"]
    for k in ("mae_h1_home", "mae_h1_away", "mae_fg_home", "mae_fg_away", "brier_h1_home_win"):
        assert k in m
    # period metrics distinct keys from fg
    assert m["mae_h1_home"] is not None

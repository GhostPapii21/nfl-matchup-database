"""Validation/grading contracts — failures/skips are valid outcomes."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation.accounting import run_accounting_checks
from validation.asof_grade import list_jaxbal_games, grade_week_games, build_asof_history
from config_load import load_config

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_accounting_reports_reg_clock_and_sparse():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    rep = run_accounting_checks(cfg, pbp_path=PBP, n=30, seed=11)
    assert "regulation_clock_sec_target" in rep
    assert rep["regulation_clock_sec_target"] == 3600
    assert "mean_plays_approx" in rep
    assert "sparse_rate" in rep
    assert "checks" in rep
    # must not claim PASS overall without evidence fields
    assert rep["overall_status"] in {"PASS", "FAIL", "MIXED"}


def test_w1_games_are_ungradable_no_own_season_history():
    games = list_jaxbal_games(PBP)
    w1 = [g for g in games if g["week"] == 1]
    assert len(w1) == 2
    rows = grade_week_games(PBP, weeks=[1], n_sims=10, seed_base=20261105)
    assert len(rows) == 2
    for r in rows:
        assert r["grade_status"].startswith("UNGRADEABLE")
        assert "NO_OWN_SEASON_HISTORY" in r["grade_status"] or "NO_ASOF" in r["skip_reason"]


def test_w3_opponent_prior_plays_graded_no_league_pool():
    """Rico 4:09: historical opponents allowed via each team's own prior plays — not league pool."""
    rows = grade_week_games(PBP, weeks=[3], n_sims=10, seed_base=20261105)
    assert len(rows) >= 1
    for r in rows:
        assert r["grade_status"] == "GRADED_FULL", r
        assert r.get("silent_pool_applied") is False
        assert r.get("league_pooled") is False
        assert r.get("prior_year_pooled") is False


def test_asof_history_excludes_future_weeks_and_prior_year():
    hist = build_asof_history(PBP, teams=["JAX", "BAL"], season=2026, before_week=4)
    assert hist["status"] == "OK"
    assert hist["df"]["week"].max() < 4
    assert hist["df"]["season"].eq(2026).all()
    assert set(hist["df"]["posteam"].unique()) <= {"JAX", "BAL"}
    # week 1 before_week=1 empty
    empty = build_asof_history(PBP, teams=["JAX", "BAL"], season=2026, before_week=1)
    assert empty["status"] == "EMPTY_ASOF"

"""Drive-length / plays-per-game realism diagnostics (development label)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation.realism import compare_sim_vs_actual_pace
from config_load import load_config

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_realism_report_has_denominators():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    rep = compare_sim_vs_actual_pace(cfg, pbp_path=PBP, n_sims=40, seed=3)
    assert rep["label"] == "development_in_sample_diagnostic_not_accuracy"
    assert "actual" in rep and "sim" in rep
    assert rep["actual"]["mean_offense_snaps_per_team_game"] > 0
    assert rep["sim"]["mean_snaps_per_game"] > 0
    assert "drive_length_plays" in rep["actual"]

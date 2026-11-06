"""Candidate is importable and flagged exploratory; must not be imported by walkforward."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "candidates"))
import walkforward
import joint_residual_v0 as jr
from reconstruct import load_pbp, period_table_from_pbp, as_of_mask
import pandas as pd


def test_candidate_marked_exploratory_and_unused_by_walkforward():
    src = Path(walkforward.__file__).read_text()
    assert "joint_residual" not in src
    assert "candidates" not in src
    root = Path(__file__).resolve().parents[1]
    hist = pd.concat([
        period_table_from_pbp(load_pbp(root / "data/play_by_play_2025.parquet")),
        period_table_from_pbp(load_pbp(root / "data/play_by_play_2026.parquet")),
    ], ignore_index=True)
    asof = hist[as_of_mask(hist, 2026, 9)]
    out = jr.simulate_joint_totals(asof, "BAL", "JAX", "fg", n=2000, seed=1)
    assert out.get("exploratory") is True
    assert out.get("not_in_walkforward") is True
    assert out.get("status") == "CANDIDATE_UNVALIDATED"

"""Kickoff starting field position comes from as-of data, not a fixed own-25 (equation audit 2026-11-11)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from simulate import kickoff_start_yardlines
from state import GameState, apply_kickoff, kickoff_spot, maybe_halftime, LEGACY_KICKOFF_YL


def _df():
    return pd.DataFrame({
        "game_id": ["g"] * 9, "play_id": range(1, 10),
        "play_type": ["kickoff", "run", "pass", "kickoff", "pass", "kickoff", "kickoff", "pass", "run"],
        "posteam": ["A", "A", "A", "B", "B", "A", "B", "A", "A"],
        "yardline_100": [35, 65, 60, 35, 72, 35, 35, 50, 45],
        "kickoff_attempt": [1, 0, 0, 1, 0, 1, 1, 0, 0],
    })


def test_kickoff_starts_use_receiving_teams_first_snap():
    # 3rd kickoff is followed by another kickoff (e.g. re-kick after penalty): skipped.
    # 4th: receiving B, but A snaps next (onside recovery) -> excluded.
    assert kickoff_start_yardlines(_df()).tolist() == [65, 72]


def test_kickoff_starts_missing_columns_is_none():
    assert kickoff_start_yardlines(_df().drop(columns=["kickoff_attempt"])) is None


def test_kickoff_spot_uses_sampler_else_legacy():
    st = GameState.new_game(home="BAL", away="JAX")
    assert kickoff_spot(st) == LEGACY_KICKOFF_YL == 75
    st.kickoff_sampler = lambda: 65
    apply_kickoff(st, receiving="JAX", yardline_100=kickoff_spot(st))
    assert st.yardline_100 == 65
    st.qtr, st.game_seconds_remaining = 2, 0
    maybe_halftime(st, q3_receive="BAL")
    assert st.possession == "BAL" and st.yardline_100 == 65


def test_real_2026_kickoffs_start_near_own_31():
    pbp = Path(__file__).resolve().parents[2] / "period_engine_v0/data/play_by_play_2026.parquet"
    d = pd.read_parquet(pbp, columns=["game_id", "play_id", "play_type", "posteam", "yardline_100", "kickoff_attempt", "week"])
    k = kickoff_start_yardlines(d[d.week <= 8])
    assert len(k) > 1000
    assert 66 < k.mean() < 72  # 2025 rule: touchbacks to the 35 (yl 65); legacy engine used 75

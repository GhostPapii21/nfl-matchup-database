"""Regressions from Codex final review of 8a4ce01 (2026-11-05 18:45 EST)."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
import numpy as np
import pandas as pd
import simulate as sim
from test_complete_pass2 import _row, _st
from test_codex_p1_regressions import _mini_catalog_with_punts


def test_turnover_on_downs_preserves_spot():
    df = pd.DataFrame([_row(down=4, yards_gained=0) for _ in range(5)])
    st = _st(down=4, ydstogo=1, yardline_100=1)
    sim._apply_snap(np.random.default_rng(0), sim.PlayCatalog(df, 3), st, False)
    assert (st.possession, st.yardline_100) == ("BBB", 99)


def test_punt_preserves_inside_five_spot():
    cat, _ = _mini_catalog_with_punts(kick_distance=45, return_yards=0)
    st = _st(down=4, yardline_100=50)
    sim._punt_fixed(np.random.default_rng(0), cat, st)
    assert st.yardline_100 == 95


def test_snap_event_uses_realized_yards():
    df = pd.DataFrame([_row(yards_gained=60) for _ in range(5)])
    st = _st(yardline_100=10)
    sim._apply_snap(np.random.default_rng(0), sim.PlayCatalog(df, 3), st, False)
    snap = next(e for e in st.events if e["type"] == "snap")
    assert snap["yards"] == 10 and snap["hist_yards"] == 60


def test_interception_spot_not_clipped_to_10():
    df = pd.DataFrame([_row(play_type="pass", interception=1, yards_gained=0) for _ in range(5)])
    st = _st(yardline_100=95)  # INT at own 5 -> opponent at its... yl 5
    sim._apply_snap(np.random.default_rng(0), sim.PlayCatalog(df, 3), st, False)
    assert st.possession == "BBB" and st.yardline_100 == 5


def test_inferred_punt_touchback_event():
    cat, _ = _mini_catalog_with_punts(kick_distance=45, return_yards=0)
    st = _st(down=4, yardline_100=40)
    sim._punt_fixed(np.random.default_rng(0), cat, st)
    assert st.yardline_100 == 80
    ev = st.events[-1]
    assert (ev["touchback"], ev["net"]) == (True, 20)

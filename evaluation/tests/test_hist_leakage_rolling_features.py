"""Historical leakage audit: rolling / trailing features must use only games before the target game.

Targets the shared trailing-mean helper used for the player-yard dispersion fit and its walk-forward backtest
(market_calibration/fit_dispersion_nflverse.py), plus the walk-forward fit window. xfail = real finding.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from market_calibration import fit_dispersion_nflverse as F  # noqa: E402


def _pg(n=12, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for pid in ("p1", "p2"):
        for i in range(n):
            season, week = (2025, i + 10) if i < 6 else (2026, i - 5)
            rows.append(dict(stat="rec", pid=pid, season=season, week=week, yards=float(rng.integers(0, 120))))
    return pd.DataFrame(rows).sort_values(["stat", "pid", "season", "week"]).reset_index(drop=True)


def test_trailing_mean_never_includes_current_game():
    pg = _pg()
    tm = F.trailing_mean(pg)
    for pid, g in pg.assign(tm=tm).groupby("pid"):
        y = g.yards.tolist()
        for i, v in enumerate(g.tm.tolist()):
            prev = y[max(0, i - F.TRAIL_N):i]
            if len(prev) < F.TRAIL_MIN:
                assert np.isnan(v)
            else:
                assert v == pytest.approx(np.mean(prev))


def test_trailing_mean_unchanged_when_future_games_change():
    pg = _pg()
    a = F.trailing_mean(pg)
    pg2 = pg.copy()
    last = pg2.groupby("pid").tail(1).index
    pg2.loc[last, "yards"] = 10_000.0
    b = F.trailing_mean(pg2)
    pd.testing.assert_series_equal(a.drop(last), b.drop(last))


@pytest.mark.xfail(strict=True, reason=(
    "LATENT RISK (LOW): fit_dispersion_nflverse.trailing_mean (line 97-101) relies on the caller having sorted rows by "
    "season/week (it is, at line 92). Fed unsorted rows, shift(1) picks up FUTURE games. The helper should sort itself "
    "or assert order."))
def test_trailing_mean_is_order_independent():
    pg = _pg()
    a = F.trailing_mean(pg)
    shuffled = pg.sample(frac=1.0, random_state=3)
    b = F.trailing_mean(shuffled).reindex(pg.index)
    pd.testing.assert_series_equal(a, b)


def test_walk_forward_mask_excludes_target_week():
    df = pd.DataFrame({"season": [2025, 2026, 2026, 2026], "week": [18, 3, 4, 5]})
    m = F._mask_train(df, 2026, 3)
    assert m.tolist() == [True, True, False, False]


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED, population): fit_dispersion_nflverse builds player-games from play-by-play only (docstring lines "
    "20-21): a player with no target/carry has no row, so p0 (share of games <= 0 yards) is conditional on >= 1 "
    "opportunity and inactive / zero-touch games never enter the fit or the wk4-9 player-level backtest."))
def test_dispersion_player_games_include_zero_opportunity_games():
    src = (ROOT / "market_calibration/fit_dispersion_nflverse.py").read_text()
    assert "Player-games with no target/carry do not appear" not in src

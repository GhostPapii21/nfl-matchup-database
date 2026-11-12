"""NFL-49 B accounting fixes: mean clock (not median of a bimodal delta), same-quarter deltas over all as-of rows,
kneels/spikes out of the snap pool, kickoffs run the clock. cfg accounting="legacy" reproduces the old engine.
Research only, not validated."""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import simulate  # noqa: E402
from simulate import PlayCatalog, accounting_from_cfg, ACCOUNTING_DEFAULTS, ACCOUNTING_LEGACY  # noqa: E402

REPO = HERE.parents[1]
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
CFG = HERE / "config/was_nyg_2026-11-12_data_only_nfl43.json"


def test_accounting_defaults_and_legacy():
    assert accounting_from_cfg({}) == ACCOUNTING_DEFAULTS
    assert accounting_from_cfg({"accounting": "legacy"}) == ACCOUNTING_LEGACY
    with pytest.raises(ValueError):
        accounting_from_cfg({"accounting": {"clock": "mode"}})
    assert accounting_from_cfg({"accounting": {"clock": "legacy_median"}})["kickoff_clock"] is False


def _toy_clock_df():
    # one game, one quarter: run deltas alternate 40 s (clock running) and 6 s (stopped) -> mean 23, median 23 or 40
    rows, t = [], 3600
    for i, dt in enumerate([40, 6, 40, 40, 6] * 8):
        rows.append(dict(game_id="g", play_id=i, qtr=1, play_type="run", game_seconds_remaining=t)); t -= dt
    rows.append(dict(game_id="g", play_id=998, qtr=1, play_type="punt", game_seconds_remaining=t))
    rows.append(dict(game_id="g", play_id=999, qtr=2, play_type="run", game_seconds_remaining=t - 5))
    return pd.DataFrame(rows)


def test_mean_clock_is_the_mean_not_the_median():
    df = _toy_clock_df()
    m = PlayCatalog.build_empirical_clock(df, stat="mean")
    assert m["source"] == "empirical_mean_delta_same_qtr"
    assert m["run"] == pytest.approx((40 * 3 + 6 * 2) / 5)
    legacy = PlayCatalog.build_empirical_clock(df)
    assert legacy["run"] == 40.0  # median of the bimodal deltas


def test_mean_clock_ignores_cross_quarter_delta():
    df = _toy_clock_df()
    df.loc[df.play_id == 998, "play_type"] = "run"  # its 5 s delta crosses into Q2 and must not count
    assert PlayCatalog.build_empirical_clock(df, stat="mean")["run"] == pytest.approx(26.4)


def test_kneels_and_spikes_excluded_from_snap_pool_by_default():
    df = pd.DataFrame([dict(posteam="A", defteam="B", play_type=pt, down=1, ydstogo=10, yardline_100=50, yards_gained=0)
                       for pt in ["pass", "run", "qb_kneel", "qb_spike"] * 3])
    assert set(PlayCatalog(df, min_n=1, exclude_clock_mgmt=True).snaps.play_type) == {"pass", "run"}
    assert "qb_kneel" in set(PlayCatalog(df, min_n=1).snaps.play_type)


@pytest.mark.skipif(not PBP.exists(), reason="committed W1-9 PBP missing")
def test_real_sim_default_vs_legacy_accounting():
    cfg = json.loads(CFG.read_text())
    cfg.pop("semantics", None)
    new = simulate.simulate_games(cfg, pbp_path=str(PBP), n=60, seed=11)
    assert new["effects_provenance"]["accounting"] == ACCOUNTING_DEFAULTS
    cfg["accounting"] = "legacy"
    old = simulate.simulate_games(cfg, pbp_path=str(PBP), n=60, seed=11)
    assert old["effects_provenance"]["accounting"] == ACCOUNTING_LEGACY
    tot = lambda o: float((o["arrays"]["fg_home"] + o["arrays"]["fg_away"]).mean())
    # mean clock gives more snaps -> more scoring than the median clock on the same data (direction only)
    assert tot(new) > tot(old)

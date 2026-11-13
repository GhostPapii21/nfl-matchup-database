"""NFL-75 Phase 2 fitter guards: point in time, frozen params, holdout refusal. Skips when the uncommitted 2025 PBP /
players table (NFLVERSE_PBP_DIR, default /tmp/nflverse_pbp) are absent."""
from __future__ import annotations
import json

import pytest

from calibration import opportunity_fit as F
from calibration import opportunity_backtest as BT

needs_data = pytest.mark.skipif(not (F.SOURCES["pbp_2025"]["path"].exists() and F.SOURCES["players"]["path"].exists()),
                                reason="uncommitted nflverse 2025 PBP / players table missing")


def test_holdout_weeks_refused():
    with pytest.raises(SystemExit):
        BT.main(["--weeks", "10"])
    with pytest.raises(SystemExit):
        BT.main(["--weeks", "9", "--n", "20001"])


def test_frozen_params_never_read_eval_week():
    for f in sorted((BT.OUT / "params").glob("params_2026_w*.json")):
        p = json.loads(f.read_text())
        assert p["data_max_week_used"]["week"] == p["eval_week"] - 1
        for slot, v in p["slots"].items():
            assert v["train_team_games"] > 0


@needs_data
def test_sources_sha256():
    F.verify_sources()


@needs_data
def test_train_and_inputs_point_in_time():
    tr = F.train_set(2026, 6, "target")
    assert all(not (x["season"] == 2026 and (x["week"] >= 6 or max(x["weeks"]) >= 6)) for x in tr)
    x = F.team_game_inputs(2026, "NYG", 10, "dropback")
    assert max(x["weeks"]) <= 9
    rows = F.lik_rows(2026, 6)
    assert not ((rows["season"] == 2026) & (rows["week"] >= 6)).any()


@needs_data
def test_depth_qb1_uses_snapshot_before_game_day():
    import pandas as pd
    d = pd.read_csv(F.SOURCES["depth_qb1"]["path"], dtype={"gsis_id": str})
    gd = F._gamedays()[(2026, 10, "NYG")]
    q = F.depth_qb1(2026, "NYG", 10)
    sub = d[(d.season == 2026) & (d.team == "NYG") & (d.dt < f"{gd}T04:00:00Z")]
    assert q == sub.sort_values("dt").iloc[-1]["gsis_id"]

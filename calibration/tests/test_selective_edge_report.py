"""Phase 4 reporting helpers: position split of STRONG UNDER, and the freeze_v2 live-leg adapter (reads a committed
price freeze; never fills a missing price). Research only."""
from __future__ import annotations
import glob

import numpy as np
import pandas as pd

from calibration import selective_edge as se
from calibration import selective_edge_report as RP
from calibration import selective_edge_live as LV


def test_position_groups():
    df = pd.DataFrame(dict(position=["QB", "RB", "FB", "WR", None]))
    assert RP.position_group(df.position).tolist() == ["QB", "RB", "RB", "other", "other"]


def test_strong_under_by_position_counts():
    rows = []
    for i, pos in enumerate(["QB"] * 3 + ["RB"] * 2):
        rows.append(dict(label=se.STRONG_UNDER, market="rushyds", side="Under", position=pos, game_id=f"g{i}",
                         dec=1.91, win=1.0 if i % 2 == 0 else 0.0, push=0))
    t = RP.strong_under_by_position(pd.DataFrame(rows), B=200)
    assert dict(zip(t.position_group, t.n)) == {"QB": 3, "RB": 2}


def test_freeze_v2_adapter_reads_real_prices_only():
    f = sorted(glob.glob(str(LV.ROOT / "pregame/price_freezes/2026-11-12_WAS@NYG/freeze_v2_*.json")))[-1]
    legs = LV.legs_from_freeze_v2(f)
    ru = legs[(legs.market == "rushyds") & (legs.side == "Under")]
    assert len(ru) >= 1 and (ru.week == 10).all() and (ru.kind == "main").all()
    priced = ru[ru.dec.notna()]
    assert (priced.dec > 1).all() and priced.price_source.str.contains("freeze_v2").all()
    assert ru[ru.dec.isna()].price_source.isna().all()
    assert legs.p_model.isna().all()  # adapter never invents a model probability

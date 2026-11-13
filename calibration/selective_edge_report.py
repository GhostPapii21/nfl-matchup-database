"""NFL-75 Phase 4 reporting (read-only on graded outputs; not part of the frozen classifier).

    python3 -m calibration.selective_edge_report   # after selective_edge_run eval

Writes the STRONG UNDER split by position group (QB / RB / other) for Weeks 4-7 and 8-9, and the gated-RB rush-yds
under row with no edge filter, so the "60%+ carry backs" claim can be checked against what the label actually holds.
Research only; projection_ready stays false."""
from __future__ import annotations

import pandas as pd

from calibration import selective_edge as se


def position_group(pos: pd.Series) -> pd.Series:
    p = pos.fillna("").astype(str)
    return p.where(p.eq("QB"), p.isin(se.RB_POSITIONS).map({True: "RB", False: "other"}))


def strong_under_by_position(df: pd.DataFrame, B: int = se.BOOT_B) -> pd.DataFrame:
    s = df[df.label == se.STRONG_UNDER].copy()
    s["position_group"] = position_group(s.position)
    return se.table(s, by=("market", "position_group"), B=B)


def main():
    from calibration.selective_edge_freeze import RUN, load_params
    from calibration.selective_edge_run import WORK
    params = load_params()
    L = pd.read_csv(WORK / "legs_w4_9.csv", low_memory=False)
    I = se.settle(se.classify(L[L.week.isin(se.TRAIN_WEEKS)].reset_index(drop=True), params))
    E = pd.read_csv(WORK / "graded_w8_9.csv", low_memory=False)
    out = []
    for name, d in (("IS W4-7", I), ("OOS W8-9", E)):
        out.append(strong_under_by_position(d).assign(set=name, view="STRONG UNDER (edge >= 0)"))
        rb = d[(d.kind == "main") & (d.market == "rushyds") & d.position.isin(se.RB_POSITIONS)
               & ~d.reason.isin(["do_not_play_rb_carry_lt_60", "carry_history_unknown"])]
        out.append(pd.DataFrame([dict(set=name, view="gated RB rush-yds unders, no edge filter", market="rushyds",
                                      position_group="RB", **se.summarize(rb))]))
        fail = d[(d.kind == "main") & (d.market == "rushyds") & (d.reason == "do_not_play_rb_carry_lt_60")]
        out.append(pd.DataFrame([dict(set=name, view="RB rush-yds unders FAILING the 60% gate", market="rushyds",
                                      position_group="RB", **se.summarize(fail))]))
    R = pd.concat(out, ignore_index=True)
    R.to_csv(RUN / "results_rush_under_by_position.csv", index=False)
    c = ["set", "view", "position_group", "n", "W", "L", "hit", "be", "margin", "margin_lo", "margin_hi"]
    print(R[c].round(3).to_string(index=False))


if __name__ == "__main__":
    main()

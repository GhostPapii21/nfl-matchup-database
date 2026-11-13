"""NFL-75 Phase 4: grade Weeks 10-12 (holdout / live) legs with the FROZEN selective-edge classifier.

Refuses any week outside 10-12, checks the freeze manifest for every week BEFORE any outcome is read, never refits.
Prices must be real (graded side decimal + price_source); missing prices are INSUFFICIENT EVIDENCE, never filled.

    python3 -m calibration.selective_edge_live --legs legs_w10.csv --pbp <nflverse pbp through the prior week> \
        [--oos <W8-9 graded csv from selective_edge_run eval>] --out <dir>

Legs CSV columns: week, game_id, player, gsis, position, market (rushyds|recyds|rec|rushrec|pass*), side, kind
(main|alt), line, dec (graded-side decimal price), p_nv, p_model (graded-side probability), defender_verified,
price_source, actual (blank until final). `legs_from_freeze_v2` builds main-line rows from a committed
pregame/price_freezes/*/freeze_v2_*.json (read only). Research only; projection_ready stays false."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from calibration import selective_edge as se
from calibration.selective_edge_freeze import ROOT, check_freeze, load_params

FREEZE_MARKETS = {"rushing_yards": "rushyds", "receiving_yards": "recyds", "receptions": "rec",
                  "rush_reception_yards": "rushrec", "passing_yards": "passyds"}


class LiveGradeError(RuntimeError):
    pass


def grade_live(legs: pd.DataFrame, pbp: pd.DataFrame, context: pd.DataFrame | None = None,
               root: Path = ROOT) -> pd.DataFrame:
    weeks = sorted(int(w) for w in pd.Series(legs.week).dropna().unique())
    if not weeks or any(w not in se.HOLDOUT_WEEKS for w in weeks):
        raise LiveGradeError(f"live grader accepts only weeks 10-12 (holdout); got {weeks}")
    for w in weeks:
        check_freeze(w, root=root)
    params = load_params(root)
    if context is not None:
        legs = pd.concat([legs.reset_index(drop=True), context.reset_index(drop=True)], axis=1)
    else:
        if len(pbp) and (pd.to_numeric(pbp.week, errors="coerce") >= min(weeks)).any():
            pbp = pbp[pd.to_numeric(pbp.week, errors="coerce") < min(weeks)]  # point in time: prior weeks only
        legs = se.attach_context(legs, pbp)
    out = se.settle(se.classify(legs, params))
    out["source"] = out.get("source", "live")
    out["projection_ready"] = False
    return out


def legs_from_freeze_v2(path: str, roster: pd.DataFrame | None = None) -> pd.DataFrame:
    """Main-line two-sided prop legs from a price-freeze/2 JSON: graded price = best retail price for that side at the
    consensus line; p_nv = consensus no-vig. Skips a market whose best price is at a different line than consensus."""
    d = json.loads(Path(path).read_text())
    meta = d["meta"]
    rows = []
    for key, mk in d["markets"].items():
        stat, _, player = key.partition("|")
        if stat not in FREEZE_MARKETS or not player:
            continue
        cons = (d.get("consensus", {}).get(key) or {})
        cons = cons.get("consensus") if isinstance(cons, dict) else None
        cons = cons if isinstance(cons, dict) else {}  # "no consensus" -> no line, no price
        line = cons.get("line")
        for side in ("Over", "Under"):
            best = (mk.get("best_retail_price") or {}).get(side) or {}
            ok = best.get("price") is not None and line is not None and best.get("line") == line
            rows.append(dict(week=int(meta["game_id"].split("_")[1]), game_id=meta["game_id"], player=player,
                             market=FREEZE_MARKETS[stat], side=side, kind="main", line=line,
                             dec=float(se.american_to_decimal(best["price"])) if ok else np.nan,
                             p_nv=(cons.get("no_vig") or {}).get(side, np.nan) if ok else np.nan,
                             price_source=(f"freeze_v2 {Path(path).name} {best.get('book')} pulled "
                                           f"{meta.get('pulled_utc')}") if ok else None,
                             p_model=np.nan, defender_verified=False, actual=np.nan, source="live"))
    df = pd.DataFrame(rows)
    if roster is not None and len(df):
        r = roster.rename(columns={"full_name": "player", "gsis_id": "gsis"})[["player", "gsis", "position"]]
        df = df.merge(r.drop_duplicates("player", keep=False), on="player", how="left")
    for c in ("gsis", "position"):
        if c not in df:
            df[c] = np.nan
    return df


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--legs", required=True)
    ap.add_argument("--pbp", required=True)
    ap.add_argument("--oos", help="graded W8-9 OOS csv to show the combined (backtest_oos + live) view")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    legs = pd.read_csv(a.legs)
    for w in sorted(legs.week.unique()):          # refuse before reading anything else
        if int(w) not in se.HOLDOUT_WEEKS:
            raise LiveGradeError(f"live grader accepts only weeks 10-12; got {w}")
        check_freeze(int(w))
    g = grade_live(legs, pd.read_parquet(a.pbp))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    g.to_csv(out / "live_graded.csv", index=False)
    views = {"live_only": se.graduation(g, sources=("live",))}
    if a.oos:
        o = pd.read_csv(a.oos)
        views["backtest_oos_plus_live"] = se.graduation(pd.concat([o, g], ignore_index=True),
                                                        sources=("backtest_oos", "live"))
    for k, v in views.items():
        v.to_csv(out / f"graduation_{k}.csv", index=False)
        print(f"== graduation ({k}); report only, projection_ready stays false")
        print(v.round(3).to_string(index=False) if len(v) else "(no candidate legs)")


if __name__ == "__main__":
    main()

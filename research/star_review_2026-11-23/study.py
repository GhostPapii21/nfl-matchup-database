"""Star review after Week 11 (2026-11-22): which star groups are accurate, and do the pregame reasons behind this
week's misses improve the 80-yard star model on past seasons?

Base: the board's star model (research/watch_model_2026-11-16/fit.py), fit 2022-24, held out 2025-26.
Candidates (all known before kickoff):
  receivers  true_backup  team starts a QB who is not its usual starter and has under 8 starts in two seasons
             vet_new      ...who is not its usual starter but is a veteran (8+ starts)
             fav          team's point spread (favoured by), the run-heavy-favourite case (Rice, Burden)
  backs      split        another back on the team also came in averaging 10+ carries (Swift/Monangai)
             mate_car     that other back's carries a game
             true_backup  as above
A candidate is kept only if it lowers held-out log loss and Brier and its weight is clear of zero (|z| >= 2).

    python3 research/star_review_2026-11-23/study.py --data DIR     # DIR as for research/game_types_2026-11-16/test_rb.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research" / "watch_model_2026-11-16"))
sys.path.insert(0, str(ROOT / "research" / "game_types_2026-11-16"))
sys.path.insert(0, str(ROOT / "research" / "qb_script_2026-11-22"))
import fit as F  # noqa: E402
import study as Q  # noqa: E402
import test_rb as T  # noqa: E402

RX = ["l_tgt", "l_yds", "implied", "team_pass", "l_ex", "g80_pg"]
BX = ["l_car", "l_ypc", "spread", "implied", "l_d"]
CUTS = {"3": 0.50, "2": 0.40, "1": 0.30}


def qb_flags():
    t = Q.team_games(Q.games())
    return t[["season", "week", "team", "backup_true", "backup_vet"]].rename(columns={"backup_true": "true_backup", "backup_vet": "vet_new"})


def evaluate(d, X, extra, y="hit80"):
    tr, te = d[d.season <= 2024], d[d.season >= 2025]
    def run(cols):
        m = sm.GLM(tr[y], sm.add_constant(tr[cols].astype(float)), family=sm.families.Binomial()).fit()
        p = m.predict(sm.add_constant(te[cols].astype(float), has_constant="add")).clip(1e-4, 1 - 1e-4)
        ll = float(-(te[y] * np.log(p) + (1 - te[y]) * np.log(1 - p)).mean())
        return m, p, {"logloss": round(ll, 5), "brier": round(float(((p - te[y]) ** 2).mean()), 5)}
    m0, p0, s0 = run(X)
    out = {"base": s0, "n_train": int(len(tr)), "n_test": int(len(te)), "candidates": {}}
    for c in extra:
        m1, p1, s1 = run(X + [c])
        z = float(m1.params[c] / m1.bse[c])
        out["candidates"][c] = {**s1, "coef": round(float(m1.params[c]), 4), "z": round(z, 2), "rows_with_flag_test": int(te[c].astype(float).gt(0).sum()),
                                "keep": bool(s1["logloss"] < s0["logloss"] and s1["brier"] < s0["brier"] and abs(z) >= 2)}
    return out, te.assign(p=p0)


def record(te_parts):
    a = pd.concat(te_parts)
    weeks = a.groupby(["season", "week"]).ngroups
    out = {}
    for lab, lo, hi in (("3", CUTS["3"], 2), ("2", CUTS["2"], CUTS["3"]), ("1", CUTS["1"], CUTS["2"])):
        x = a[(a.p >= lo) & (a.p < hi)]
        se = float(np.sqrt(x.hit80.mean() * (1 - x.hit80.mean()) / max(len(x), 1)))
        out[lab] = {"players": int(len(x)), "per_week": round(len(x) / weeks, 1), "predicted": round(float(x.p.mean()), 3),
                    "hit80": round(float(x.hit80.mean()), 3), "hit80_ci95": [round(float(x.hit80.mean()) - 1.96 * se, 3), round(float(x.hit80.mean()) + 1.96 * se, 3)],
                    "gap_points": round(100 * float(x.hit80.mean() - x.p.mean()), 1)}
        for kind in ("rec", "rush"):
            k = x[x.kind == kind]
            out[lab][kind] = {"players": int(len(k)), "predicted": round(float(k.p.mean()), 3) if len(k) else None, "hit80": round(float(k.hit80.mean()), 3) if len(k) else None}
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); a = ap.parse_args()
    qf = qb_flags()
    r = F.receivers()
    r = r.merge(qf, on=["season", "week", "team"], how="left")
    r[["true_backup", "vet_new"]] = r[["true_backup", "vet_new"]].fillna(False).astype(int)
    r["fav"] = r.spread.fillna(0)
    rec, te_r = evaluate(r, RX, ["true_backup", "vet_new", "fav"])

    D = Path(a.data)
    b = pd.concat([T.season(y, D) for y in (2022, 2023, 2024, 2025, 2026)]).dropna(subset=["implied"]).reset_index(drop=True)
    b["l_car"], b["l_ypc"], b["l_d"] = np.log(0.6 * b.car_pg + 0.4 * b.car_l3), np.log(b.ypc), np.log(b.d_yds_pg)
    b["hit80"] = (b.y_yds >= 80).astype(int)
    mates = b.groupby(["season", "week", "team"]).car_pg.agg(list).rename("cars").reset_index()
    b = b.merge(mates, on=["season", "week", "team"])
    b["mate_car"] = [max([c for c in cs if c != me] or [0]) if cs.count(me) == 1 else max(cs) for cs, me in zip(b.cars, b.car_pg)]
    b["split"] = (b.mate_car >= 10).astype(int)
    b = b.merge(qf, on=["season", "week", "team"], how="left")
    b[["true_backup", "vet_new"]] = b[["true_backup", "vet_new"]].fillna(False).astype(int)
    rush, te_b = evaluate(b, BX, ["split", "mate_car", "true_backup"])
    _, te_b2 = evaluate(b, BX + ["mate_car"], [])
    cols = ["season", "week", "p", "hit80", "kind"]
    res = {"receivers": rec, "backs": rush,
           "star_groups_heldout_2025_26": record([te_r.assign(kind="rec")[cols], te_b.assign(kind="rush")[cols]]),
           "star_groups_heldout_2025_26_with_mate_car": record([te_r.assign(kind="rec")[cols], te_b2.assign(kind="rush")[cols]])}
    full = sm.GLM(b.hit80, sm.add_constant(b[BX + ["mate_car"]].astype(float)), family=sm.families.Binomial()).fit()
    full100 = sm.GLM((b.y_yds >= 100).astype(int), sm.add_constant(b[BX + ["mate_car"]].astype(float)), family=sm.families.Binomial()).fit()
    res["rusher_weights_all_seasons_with_mate_car"] = {"80": {k: round(float(v), 4) for k, v in full.params.items()},
                                                       "100": {k: round(float(v), 4) for k, v in full100.params.items()}}
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

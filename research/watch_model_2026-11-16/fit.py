"""Fit the 80-yard watch models and write dashboard/watch_model.json.

Receivers (WR/TE), 2022 to week 9 of 2026, pre-game inputs only:
  ln targets (0.6 season + 0.4 last-three share x team targets), ln yards per game, team implied total,
  team pass volume (targets a game), the defense's rate of 20+ yard completions allowed (relative to league),
  and how many 80+ yard games the defense has allowed to his position per game.
Every factor is in the fit, so the data sets its weight; factors that do not predict get a weight near zero.
Running backs: research/game_types_2026-11-16/test_rb.py (carries, yards per carry, spread, team total, RB yards allowed).

    python3 research/watch_model_2026-11-16/fit.py --data DIR      # DIR as for test_rb.py
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research" / "game_types_2026-11-16"))


def receivers():
    r = pd.read_parquet(ROOT / "research" / "receiver_volatility_2026-11-14" / "rows.parquet")
    r = r[r.pos.isin(["WR", "TE"]) & (r.games_prior >= 3) & r.implied.notna() & (r.share > 0)].copy()
    r["team_pass"] = r.tgt_pg / r.share
    r["l_tgt"] = np.log((0.6 * r.tgt_pg + 0.4 * r.share_l3 * r.team_pass).clip(0.5))
    r["l_yds"] = np.log(r.yds_avg.clip(1))
    r["l_ex"] = np.log(r.opp_ex_rate.clip(0.5, 2.0))
    r["hit80"] = (r.y_yds >= 80).astype(int)
    key = ["season", "opp", "pos"]
    g = r.groupby(key + ["week"]).agg(n80=("hit80", "sum")).reset_index().sort_values(key + ["week"])
    g["cum"] = g.groupby(key).n80.cumsum() - g.n80
    g["gp"] = g.groupby(key).cumcount()
    g["g80_pg"] = g.cum / g.gp.clip(lower=1)
    r = r.merge(g[key + ["week", "g80_pg", "gp"]], on=key + ["week"], how="left")
    r = r[r.gp >= 3]
    return r


def fit_block(r, X, label):
    tr, te = r[r.season <= 2024], r[r.season >= 2025]
    out = {"label": label, "n": int(len(r)), "features": X, "models": {}}
    for k in (80, 100):
        y = (r.y_yds >= k).astype(int)
        m_tr = sm.GLM(y[tr.index], sm.add_constant(tr[X]), family=sm.families.Binomial()).fit()
        p = m_tr.predict(sm.add_constant(te[X], has_constant="add"))
        q = pd.qcut(p, 5, labels=False, duplicates="drop")
        cal = [{"predicted": round(float(p[q == i].mean()), 3), "happened": round(float(y[te.index][q == i].mean()), 3), "n": int((q == i).sum())} for i in sorted(set(q))]
        m = sm.GLM(y, sm.add_constant(r[X]), family=sm.families.Binomial()).fit()          # final weights: all seasons
        out["models"][str(k)] = {"coef": {a: round(float(b), 4) for a, b in m.params.items()},
                                 "z": {a: round(float(m.params[a] / m.bse[a]), 2) for a in m.params.index},
                                 "holdout_auc": round(float(roc_auc_score(y[te.index], p)), 3), "holdout_calibration": cal}
    sd = r[X].std()
    out["effect_per_sd_80"] = {a: round(float(np.exp(out["models"]["80"]["coef"][a] * sd[a]) - 1) * 100, 1) for a in X}
    return out


def star_record(r, X, b, XB, cuts):
    """What the stars did on 2025-26 with weights fitted on 2022-24 only (receivers and backs together)."""
    parts = []
    for d, cols, y in ((r, X, "hit80"), (b.assign(hit80=(b.y_yds >= 80).astype(int)), XB, "hit80")):
        tr, te = d[d.season <= 2024], d[d.season >= 2025]
        m = sm.GLM(tr[y], sm.add_constant(tr[cols]), family=sm.families.Binomial()).fit()
        parts.append(te.assign(p=m.predict(sm.add_constant(te[cols], has_constant="add")))[["season", "week", "p", "hit80", "y_yds"]])
    a = pd.concat(parts)
    weeks = a.groupby(["season", "week"]).ngroups
    out = {"weeks": int(weeks), "seasons": "2025-2026", "all_80_games": int(a.hit80.sum())}
    for lab, lo, hi in (("3", cuts["3"], 2), ("2", cuts["2"], cuts["3"]), ("1", cuts["1"], cuts["2"])):
        x = a[(a.p >= lo) & (a.p < hi)]
        out[lab] = {"per_week": round(len(x) / weeks, 1), "predicted": round(float(x.p.mean()), 3), "hit80": round(float(x.hit80.mean()), 3), "hit100": round(float((x.y_yds >= 100).mean()), 3)}
    s = a[a.p >= cuts["1"]]
    out["all_stars"] = {"per_week": round(len(s) / weeks, 1), "hit80": round(float(s.hit80.mean()), 3), "share_of_all_80_games_caught": round(float(s.hit80.sum() / a.hit80.sum()), 3)}
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); a = ap.parse_args()
    res = {"fitted": "2022 to 2026 (weights), checked on 2025-2026 with weights from 2022-2024"}
    r = receivers()
    res["receiver"] = fit_block(r, ["l_tgt", "l_yds", "implied", "team_pass", "l_ex", "g80_pg"], "WR/TE receiving yards")
    import test_rb as T
    D = Path(a.data)
    b = pd.concat([T.season(y, D) for y in (2022, 2023, 2024, 2025, 2026)]).dropna(subset=["implied"]).reset_index(drop=True)
    b["l_car"], b["l_ypc"], b["l_d"] = np.log(0.6 * b.car_pg + 0.4 * b.car_l3), np.log(b.ypc), np.log(b.d_yds_pg)
    res["rusher"] = fit_block(b, ["l_car", "l_ypc", "spread", "implied", "l_d"], "RB rushing yards")
    res["stars"] = {"3": 0.50, "2": 0.40, "1": 0.30}
    res["star_record"] = star_record(r, ["l_tgt", "l_yds", "implied", "team_pass", "l_ex", "g80_pg"], b, ["l_car", "l_ypc", "spread", "implied", "l_d"], res["stars"])
    old = ROOT / "dashboard" / "watch_model.json"
    if old.exists() and "book_grade" in json.loads(old.read_text()):      # written by grade_vs_books.py; keep it
        res["book_grade"] = json.loads(old.read_text())["book_grade"]
    old.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

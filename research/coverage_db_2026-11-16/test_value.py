"""Does a defense's coverage record add to the pregame 80-yard projection? (fit 2022-2024, holdout 2025-2026)

Base: targets (blended), season yards per game, team implied total (the three inputs that carry the projection).
Added, all from games before the one predicted:
  team_g80     receivers at his position with 80+ yards against this defense, per game
  cb_ypt       charted yards per target allowed by the defense's cornerbacks (PFR)
  weak_ypt     the worst regular cornerback's charted yards per target (30+ targets... scaled by weeks; the "weak link")
  cb_g70       share of the cornerbacks' games in which one of them was charged with 70+ yards
  cover_ypt    for tight ends: the same for linebackers and safeties

    python3 research/coverage_db_2026-11-16/test_value.py --data DIR   # DIR holds advdef_<y>.parquet and snaps_<y>.parquet
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROWS = ROOT / "research" / "receiver_volatility_2026-11-14" / "rows.parquet"
CB, SLB = {"CB", "DB"}, {"S", "FS", "SS", "LB", "ILB", "OLB", "MLB"}


def features(data: Path) -> pd.DataFrame:
    out = []
    for y in (2022, 2023, 2024, 2025, 2026):
        a = pd.read_parquet(data / f"advdef_{y}.parquet")
        s = pd.read_parquet(data / f"snaps_{y}.parquet")
        posn = s.sort_values("week").groupby("pfr_player_id").position.last()
        a["position"] = a.pfr_player_id.map(posn)
        for c in ("def_targets", "def_yards_allowed"):
            a[c] = a[c].fillna(0)
        for team, g in a.groupby("team"):
            for w in sorted(g.week.unique()) + [int(g.week.max()) + 1]:
                pr = g[g.week < w]
                if pr.week.nunique() < 3:
                    continue
                cb, sl = pr[pr.position.isin(CB)], pr[pr.position.isin(SLB)]
                per = cb.groupby("pfr_player_id").agg(t=("def_targets", "sum"), y=("def_yards_allowed", "sum"), g=("week", "nunique"))
                reg = per[per.t >= 3 * pr.week.nunique()]                       # regulars: 3+ targets a game
                out.append({"season": y, "opp": team, "week": w,
                            "cb_ypt": cb.def_yards_allowed.sum() / max(cb.def_targets.sum(), 1),
                            "weak_ypt": (reg.y / reg.t).max() if len(reg) else np.nan,
                            "cb_g70": (cb.def_yards_allowed >= 70).mean() if len(cb) else np.nan,
                            "cover_ypt": sl.def_yards_allowed.sum() / max(sl.def_targets.sum(), 1)})
    return pd.DataFrame(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    a = ap.parse_args(argv)
    r = pd.read_parquet(ROWS)
    r = r[r.pos.isin(["WR", "TE"]) & (r.games_prior >= 3) & r.implied.notna() & (r.share > 0)].copy()
    r["tgt_blend"] = 0.6 * r.tgt_pg + 0.4 * r.share_l3 * (r.tgt_pg / r.share)
    r["hit"] = (r.y_yds >= 80).astype(int)
    # receivers with 80+ against the defense before this week, per game, same position
    key = ["season", "opp", "pos"]
    g = r.groupby(key + ["week"]).agg(n80=("hit", "sum")).reset_index().sort_values(key + ["week"])
    g["cum80"] = g.groupby(key).n80.cumsum() - g.n80
    g["gp"] = g.groupby(key).cumcount()
    g["team_g80"] = g.cum80 / g.gp.clip(lower=1)
    r = r.merge(g[key + ["week", "team_g80", "gp"]], on=key + ["week"], how="left")
    r = r.merge(features(Path(a.data)), on=["season", "opp", "week"], how="left")
    r["cover"] = np.where(r.pos == "WR", r.cb_ypt, r.cover_ypt)
    r = r.dropna(subset=["cover", "team_g80", "weak_ypt", "cb_g70"])
    r = r[r.gp >= 3]
    base = ["l_tgt", "l_yds", "implied"]
    r["l_tgt"], r["l_yds"] = np.log(r.tgt_blend.clip(0.5)), np.log(r.yds_avg.clip(1))
    for c in ("team_g80", "cover", "weak_ypt", "cb_g70"):
        r["z_" + c] = (r[c] - r[c].mean()) / r[c].std()
    tr, te = r[r.season <= 2024], r[r.season >= 2025]
    res = {"n_train": int(len(tr)), "n_test": int(len(te)), "base_rate_80": round(float(r.hit.mean()), 3)}

    def run(cols, d_tr=tr, d_te=te):
        m = sm.GLM(d_tr.hit, sm.add_constant(d_tr[cols]), family=sm.families.Binomial()).fit()
        p = m.predict(sm.add_constant(d_te[cols], has_constant="add"))
        return m, float(roc_auc_score(d_te.hit, p)), p

    m0, auc0, p0 = run(base)
    res["base_auc"] = round(auc0, 4)
    res["added"] = {}
    for c in ("z_team_g80", "z_cover", "z_weak_ypt", "z_cb_g70"):
        m, auc, _ = run(base + [c])
        res["added"][c] = {"auc": round(auc, 4), "coef": round(float(m.params[c]), 3), "se": round(float(m.bse[c]), 3),
                           "odds_change_per_sd": round(float(np.exp(m.params[c])), 3)}
    m, auc, pall = run(base + ["z_team_g80", "z_cover", "z_weak_ypt", "z_cb_g70"])
    res["all_four_auc"] = round(auc, 4)
    # Top candidates only (the question asked): among players the base model rates 35%+, split by the defense's record
    te = te.assign(p0=p0.values)
    top = te[te.p0 >= 0.35]
    res["top_candidates"] = {"n": int(len(top)), "hit_rate": round(float(top.hit.mean()), 3)}
    for c, lab in (("team_g80", "80+ games allowed per game to his position"), ("cover", "charted yards per target by the coverage group"),
                   ("weak_ypt", "worst regular cornerback's yards per target")):
        q = pd.qcut(top[c], 3, labels=["lowest third", "middle", "highest third"], duplicates="drop")
        res["top_candidates"][lab] = {str(k): {"n": int(len(v)), "hit_80": round(float(v.hit.mean()), 3), "hit_100": round(float((v.y_yds >= 100).mean()), 3),
                                               "avg_value": round(float(v[c].mean()), 2)} for k, v in top.groupby(q, observed=True)}
    allr = r.assign(p0=m0.predict(sm.add_constant(r[base], has_constant="add")))
    top_all = allr[allr.p0 >= 0.35]
    res["top_candidates_all_seasons"] = {"n": int(len(top_all)), "hit_rate": round(float(top_all.hit.mean()), 3)}
    for c, lab in (("team_g80", "80+ games allowed per game to his position"), ("cover", "charted yards per target by the coverage group"),
                   ("weak_ypt", "worst regular cornerback's yards per target")):
        q = pd.qcut(top_all[c], 3, labels=["lowest third", "middle", "highest third"], duplicates="drop")
        res["top_candidates_all_seasons"][lab] = {str(k): {"n": int(len(v)), "hit_80": round(float(v.hit.mean()), 3),
                                                           "hit_100": round(float((v.y_yds >= 100).mean()), 3)} for k, v in top_all.groupby(q, observed=True)}
    (HERE / "value_results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

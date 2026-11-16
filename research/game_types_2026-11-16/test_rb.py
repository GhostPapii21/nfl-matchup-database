"""Do a defense's tackling numbers predict a running back's rushing yards? (2022 to week 10 of 2026)

One row per lead-back game: a back averaging 10+ carries over 3+ games coming in. Everything on the right-hand side is
from earlier games that season. Fit 2022-2024, held out 2025-2026.

    python3 research/game_types_2026-11-16/test_rb.py --data DIR
DIR: advrush_<y>.parquet, advdef_<y>.parquet for 2022-2026, pbp_2026.parquet, games.parquet (nflverse).
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "pregame" / ".cache"


def season(y, D):
    f = D / f"pbp_{y}.parquet"
    p = pd.read_parquet(f if f.exists() else C / f"play_by_play_{y}.parquet")
    p = p[(p.season_type == "REG") & (p.two_point_attempt != 1)]
    ro = pd.read_parquet(C / f"roster_weekly_{y}.parquet")
    pos = dict(zip(ro.gsis_id, ro.position))
    r = p[(p.rush_attempt == 1) & (p.qb_kneel != 1) & p.rusher_player_id.notna()].copy()
    r["pos"] = r.rusher_player_id.map(pos)
    r = r[r.pos == "RB"]
    r["y"] = r.rushing_yards.fillna(0)
    pg = r.groupby(["game_id", "week", "posteam", "defteam", "rusher_player_id"]).agg(car=("y", "size"), yds=("y", "sum"), long=("y", "max"),
                                                                                         r10=("y", lambda s: int((s >= 10).sum()))).reset_index()
    dg = r.groupby(["defteam", "week"]).agg(d_car=("y", "size"), d_yds=("y", "sum"), d_r10=("y", lambda s: int((s >= 10).sum()))).reset_index()
    ar = pd.read_parquet(D / f"advrush_{y}.parquet"); ar = ar[ar.game_type == "REG"] if "game_type" in ar else ar
    bt = ar.groupby(["opponent", "week"]).agg(bt=("rushing_broken_tackles", "sum"), yac=("rushing_yards_after_contact", "sum"), ybc=("rushing_yards_before_contact", "sum"),
                                              a_car=("carries", "sum")).reset_index().rename(columns={"opponent": "defteam"})
    ad = pd.read_parquet(D / f"advdef_{y}.parquet"); ad = ad[ad.game_type == "REG"] if "game_type" in ad else ad
    mt = ad.groupby(["team", "week"]).agg(mt=("def_missed_tackles", "sum")).reset_index().rename(columns={"team": "defteam"})
    d = dg.merge(bt, on=["defteam", "week"], how="left").merge(mt, on=["defteam", "week"], how="left")
    gm = pd.read_parquet(D / "games.parquet"); gm = gm[(gm.season == y) & (gm.game_type == "REG")].set_index("game_id")
    lg = {"ypc": r.y.sum() / len(r)}
    rows = []
    for (pid, tm), h in pg.groupby(["rusher_player_id", "posteam"]):
        h = h.sort_values("week")
        for i in range(3, len(h)):
            pr, cur = h.iloc[:i], h.iloc[i]
            if pr.car.mean() < 10:
                continue
            dd = d[(d.defteam == cur.defteam) & (d.week < cur.week)]
            if len(dd) < 3 or cur.game_id not in gm.index:
                continue
            g = gm.loc[cur.game_id]
            home = g.home_team == tm
            spread = g.spread_line if home else -g.spread_line
            rows.append({"season": y, "week": int(cur.week), "player": pid, "team": tm, "opp": cur.defteam, "car_pg": pr.car.mean(), "car_l3": pr.tail(3).car.mean(),
                         "ypc": (pr.yds.sum() + lg["ypc"] * 40) / (pr.car.sum() + 40), "yds_pg": pr.yds.mean(),
                         "implied": g.total_line / 2 + spread / 2, "spread": spread, "total": g.total_line,
                         "d_ypc": dd.d_yds.sum() / dd.d_car.sum(), "d_yds_pg": dd.d_yds.mean(), "d_r10_pg": dd.d_r10.mean(),
                         "d_mt_pg": dd.mt.mean(), "d_bt_pg": dd.bt.mean(), "d_yac_pc": dd.yac.sum() / max(dd.a_car.sum(), 1), "d_ybc_pc": dd.ybc.sum() / max(dd.a_car.sum(), 1),
                         "y_car": int(cur.car), "y_yds": float(cur.yds), "y_long": float(cur.long), "y_r10": int(cur.r10)})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); a = ap.parse_args()
    D = Path(a.data)
    r = pd.concat([season(y, D) for y in (2022, 2023, 2024, 2025, 2026)]).dropna(subset=["implied", "d_mt_pg", "d_bt_pg"])
    r["hit80"], r["hit100"] = (r.y_yds >= 80).astype(int), (r.y_yds >= 100).astype(int)
    r["l_car"], r["l_ypc"] = np.log(0.6 * r.car_pg + 0.4 * r.car_l3), np.log(r.ypc)
    feats = {"d_mt_pg": "missed tackles a game", "d_bt_pg": "tackles broken by backs a game", "d_yac_pc": "yards after contact per carry allowed",
             "d_ybc_pc": "yards before contact per carry allowed", "d_ypc": "yards per carry allowed to backs", "d_yds_pg": "RB rushing yards allowed a game",
             "d_r10_pg": "runs of 10+ allowed a game"}
    for c in feats:
        r["z_" + c] = (r[c] - r[c].mean()) / r[c].std()
    tr, te = r[r.season <= 2024], r[r.season >= 2025]
    base = ["l_car", "l_ypc", "spread", "implied"]
    out = {"n": int(len(r)), "n_train": int(len(tr)), "n_test": int(len(te)), "per_week": round(len(r) / r.groupby(["season", "week"]).ngroups, 1),
           "hit80": round(float(r.hit80.mean()), 3), "hit100": round(float(r.hit100.mean()), 3), "yards": round(float(r.y_yds.mean()), 1), "added": {}}

    def run(cols, y="hit80"):
        m = sm.GLM(tr[y], sm.add_constant(tr[cols]), family=sm.families.Binomial()).fit()
        return m, float(roc_auc_score(te[y], m.predict(sm.add_constant(te[cols], has_constant="add"))))

    m0, auc0 = run(base)
    out["base"] = {"auc": round(auc0, 4), "coef": {k: round(float(v), 3) for k, v in m0.params.items()}}
    # yards model (Poisson) for the size of each effect
    for c, lab in feats.items():
        m, auc = run(base + ["z_" + c])
        my = sm.GLM(tr.y_yds, sm.add_constant(tr[base + ["z_" + c]]), family=sm.families.Poisson()).fit(scale="X2")
        out["added"][lab] = {"auc": round(auc, 4), "odds_80_per_sd": round(float(np.exp(m.params["z_" + c])), 3), "z": round(float(m.params["z_" + c] / m.bse["z_" + c]), 2),
                             "yards_pct_per_sd": round(float(np.exp(my.params["z_" + c]) - 1) * 100, 1), "yards_z": round(float(my.params["z_" + c] / my.bse["z_" + c]), 2)}
    m, auc = run(base + ["z_" + c for c in feats])
    out["all_auc"] = round(auc, 4)

    def split(x, col):
        q = pd.qcut(x[col], 3, labels=["lowest third", "middle", "highest third"], duplicates="drop")
        return {str(k): {"n": int(len(v)), "yards": round(float(v.y_yds.mean()), 1), "carries": round(float(v.y_car.mean()), 1), "ypc": round(float(v.y_yds.sum() / v.y_car.sum()), 2),
                         "hit80": round(float(v.hit80.mean()), 3), "hit100": round(float(v.hit100.mean()), 3), "avg": round(float(v[col].mean()), 2)} for k, v in x.groupby(q, observed=True)}

    out["splits_all_lead_backs"] = {lab: split(r, c) for c, lab in feats.items()}
    out["splits_environment"] = {"spread (his team favored by)": split(r, "spread"), "team implied total": split(r, "implied"), "his carries a game": split(r, "car_pg")}
    wk = r[r.car_pg >= 15]
    out["workhorses_15_plus"] = {"n": int(len(wk)), "hit80": round(float(wk.hit80.mean()), 3), "hit100": round(float(wk.hit100.mean()), 3),
                                 "by_missed_tackles": split(wk, "d_mt_pg"), "by_rb_yards_allowed": split(wk, "d_yds_pg"), "by_spread": split(wk, "spread")}
    fav_soft = wk[(wk.spread >= 3) & (wk.d_yds_pg >= wk.d_yds_pg.quantile(0.6))]
    dog_tough = wk[(wk.spread <= -3) & (wk.d_yds_pg <= wk.d_yds_pg.quantile(0.4))]
    out["workhorse_combo"] = {"favored by 3+ against a soft run defense": {"n": int(len(fav_soft)), "hit80": round(float(fav_soft.hit80.mean()), 3), "hit100": round(float(fav_soft.hit100.mean()), 3), "yards": round(float(fav_soft.y_yds.mean()), 1)},
                              "underdog by 3+ against a tough run defense": {"n": int(len(dog_tough)), "hit80": round(float(dog_tough.hit80.mean()), 3), "hit100": round(float(dog_tough.hit100.mean()), 3), "yards": round(float(dog_tough.y_yds.mean()), 1)}}
    # how stable is each defense number? first half vs second half of a season
    stab = {}
    (HERE / "rb_results.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

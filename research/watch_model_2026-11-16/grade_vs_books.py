"""Grade the 80-yard watch model against FanDuel's real alt-over prices (2026 weeks 8-9, T-90 minutes before kickoff).

Data: data/odds_history/alt_ladders_wk8_9/backtest/graded_rungs.csv (5,138 graded rungs, FanDuel overs only, prices include
vig; "be" is the break-even chance at the price). The 79.5 and 99.5 rungs are the 80+ and 100+ yard markets.
Model weights are fitted on 2022-2025 only, so weeks 8-9 of 2026 were never seen. Inputs are pre-game (rows.parquet,
test_rb.py). Players the model has no row for (under 3 games or no share) are reported as "not covered".

    python3 research/watch_model_2026-11-16/grade_vs_books.py --data DIR
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / "research" / "game_types_2026-11-16"))
import fit as F          # noqa: E402
import test_rb as T      # noqa: E402

RX = ["l_tgt", "l_yds", "implied", "team_pass", "l_ex", "g80_pg"]
BX = ["l_car", "l_ypc", "spread", "implied", "l_d"]


def logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); a = ap.parse_args()
    g = pd.read_csv(ROOT / "data" / "odds_history" / "alt_ladders_wk8_9" / "backtest" / "graded_rungs.csv")
    r = F.receivers()
    b = pd.concat([T.season(y, Path(a.data)) for y in (2022, 2023, 2024, 2025, 2026)]).dropna(subset=["implied"]).reset_index(drop=True)
    b["l_car"], b["l_ypc"], b["l_d"] = np.log(0.6 * b.car_pg + 0.4 * b.car_l3), np.log(b.ypc), np.log(b.d_yds_pg)
    out = {"source": "FanDuel alt ladders, 2026 weeks 8-9, T-90 min; weights from 2022-2025 only"}
    rows = []
    for market, d, X, rung_sets in (("rec", r, RX, (79.5, 99.5)), ("rush", b, BX, (79.5, 99.5))):
        tr = d[d.season <= 2025]
        te = d[(d.season == 2026) & d.week.isin([8, 9])]
        models = {}
        for k, rung in ((80, 79.5), (100, 99.5)):
            y = (tr.y_yds >= k).astype(int)
            models[rung] = sm.GLM(y, sm.add_constant(tr[X]), family=sm.families.Binomial()).fit()
        te = te.copy()
        for rung, m in models.items():
            te[f"p{int(rung)}"] = m.predict(sm.add_constant(te[X], has_constant="add"))
        for rung in rung_sets:
            gg = g[(g.market == market) & (g.rung == rung)]
            j = gg.merge(te[["player", "week", f"p{int(rung)}"]].rename(columns={"player": "gsis_id", f"p{int(rung)}": "p"}), on=["gsis_id", "week"], how="left")
            j["rung_set"], j["mkt"] = rung, market
            rows.append(j)
    J = pd.concat(rows)
    res = {}
    for (mk, rung), x in J.groupby(["mkt", "rung_set"]):
        cov = x[x.p.notna()]
        row = {"rungs": int(len(x)), "covered": int(len(cov)), "coverage": round(len(cov) / len(x), 3),
               "uncovered_hit": round(float(x[x.p.isna()].win.mean()), 3) if x.p.isna().any() else None,
               "book_be": round(float(cov.be.mean()), 3), "hit": round(float(cov.win.mean()), 3), "model_p": round(float(cov.p.mean()), 3)}
        brier = lambda p: float(np.mean((p - cov.win) ** 2))
        row["brier"] = {"model": round(brier(cov.p), 4), "book_price": round(brier(cov.be), 4), "always_base_rate": round(brier(np.full(len(cov), cov.win.mean())), 4)}
        # blend: does the model add information beyond the book price? logistic of the result on both logits
        if len(cov) >= 40:
            m = sm.GLM(cov.win, sm.add_constant(pd.DataFrame({"model": logit(cov.p), "book": logit(cov.be)})), family=sm.families.Binomial()).fit()
            row["blend"] = {"coef_model": round(float(m.params["model"]), 2), "z_model": round(float(m.params["model"] / m.bse["model"]), 2),
                            "coef_book": round(float(m.params["book"]), 2), "z_book": round(float(m.params["book"] / m.bse["book"]), 2)}
        pick = {}
        for gap in (0.0, 0.03, 0.06):
            s = cov[cov.p - cov.be >= gap]
            pick[f"model_above_price_by_{int(gap * 100)}pts"] = {"n": int(len(s)), "hit": round(float(s.win.mean()), 3) if len(s) else None,
                                                                 "be": round(float(s.be.mean()), 3) if len(s) else None, "roi": round(float(s.profit.mean()), 3) if len(s) else None}
        row["bets"] = pick
        s = cov[cov.p >= 0.30]
        row["starred_30plus"] = {"n": int(len(s)), "hit": round(float(s.win.mean()), 3) if len(s) else None, "model_p": round(float(s.p.mean()), 3) if len(s) else None,
                                 "be": round(float(s.be.mean()), 3) if len(s) else None, "roi": round(float(s.profit.mean()), 3) if len(s) else None}
        res[f"{mk}_{'80' if rung == 79.5 else '100'}"] = row
    out["results"] = res
    # pooled 80 and 100 rungs, receiving and rushing: Brier of the model, the book's price, the price with the vig taken off
    # (one logit scale fitted on the other week) and an even blend of the model and the de-vigged price (leave-one-week-out)
    C = J[J.p.notna()].copy()
    br = {"model": [], "book_price": [], "book_devig": [], "blend": []}
    for wk in (8, 9):
        tr, te = C[C.week != wk], C[C.week == wk]
        m = sm.GLM(tr.win, sm.add_constant(pd.DataFrame({"b": logit(tr.be)})), family=sm.families.Binomial()).fit()
        dv = m.predict(sm.add_constant(pd.DataFrame({"b": logit(te.be)}), has_constant="add"))
        bl = 1 / (1 + np.exp(-(0.5 * logit(te.p) + 0.5 * logit(dv))))
        for k, v in (("model", te.p), ("book_price", te.be), ("book_devig", dv), ("blend", bl)):
            br[k].append(((v - te.win) ** 2).values)
    st = C[C.p >= 0.30]
    out["pooled"] = {"rungs": int(len(C)), "brier": {k: round(float(np.concatenate(v).mean()), 4) for k, v in br.items()},
                     "starred_30plus": {"n": int(len(st)), "hit": round(float(st.win.mean()), 3), "model_p": round(float(st.p.mean()), 3),
                                        "be": round(float(st.be.mean()), 3), "roi": round(float(st.profit.mean()), 3)},
                     "model_above_price_by_3pts": {"n": int((C.p - C.be >= 0.03).sum()), "roi": round(float(C[C.p - C.be >= 0.03].profit.mean()), 3)}}
    mp = ROOT / "dashboard" / "watch_model.json"
    mj = json.loads(mp.read_text())
    mj["book_grade"] = {"source": out["source"], "rungs": out["pooled"]["rungs"], **{k: out["pooled"][k] for k in ("brier", "starred_30plus", "model_above_price_by_3pts")}}
    mp.write_text(json.dumps(mj, indent=1) + "\n")
    J.to_csv(HERE / "graded_vs_books.csv", index=False)
    (HERE / "book_grade.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

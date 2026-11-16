"""Q1: is a receiver's explosive game predictable pregame? Leave-one-season-out logistic models, Brier and log loss."""
import numpy as np, pandas as pd, json
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import brier_score_loss, log_loss
import statsmodels.api as sm
H = Path(__file__).resolve().parent
d = pd.read_parquet(H / "rows.parquet")
d = d[d.games_prior >= 3].copy()
d["y100"] = (d.y_yds >= 100).astype(int); d["y30"] = (d.y_ex30 >= 1).astype(int); d["y2x20"] = (d.y_ex20 >= 2).astype(int)
d["l_tgt"] = np.log(d.tgt_pg); d["hot"] = d.ex20_l3 / 3 - d.ex20_rate * d.tgt_pg; d["form"] = d.yds_l3 - d.yds_avg
d["outdoor_wind"] = np.where(d.roof.isin(["dome", "closed"]), 0, d.wind.fillna(0))
for P in ("WR", "TE", "RB"): d["is_" + P] = (d.pos == P).astype(int)
d["implied"] = d.implied.fillna(d.implied.mean())
d["opp_pos_ypg"] = d.opp_pos_ypg.fillna(d.opp_pos_ypg.mean())
BASE = ["l_tgt", "share", "ypt", "is_WR", "is_TE"]
SETS = {"base (volume + efficiency)": BASE, "+ hot hand": BASE + ["hot", "ex20_l2", "form"], "+ deep profile": BASE + ["adot", "deep_rate", "ex20_rate", "ex30_rate", "air_share"],
        "+ matchup": BASE + ["opp_ex_rate", "opp_ypa", "implied", "outdoor_wind"], "all": BASE + ["hot", "ex20_l2", "form", "adot", "deep_rate", "ex20_rate", "ex30_rate", "air_share", "opp_ex_rate", "opp_ypa", "implied", "outdoor_wind"]}
out = {}
for y in ("y100", "y30", "y2x20"):
    res = {}
    for name, cols in SETS.items():
        ps, ys = [], []
        for s in sorted(d.season.unique()):
            tr, te = d[d.season != s], d[d.season == s]
            m = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000)).fit(tr[cols], tr[y])
            ps.append(m.predict_proba(te[cols])[:, 1]); ys.append(te[y].values)
        p, yy = np.concatenate(ps), np.concatenate(ys)
        res[name] = {"brier": round(brier_score_loss(yy, p), 5), "logloss": round(log_loss(yy, p), 5)}
    base_rate = d[y].mean(); res["no model (base rate)"] = {"brier": round(brier_score_loss(d[y], np.full(len(d), base_rate)), 5)}
    out[y] = {"rate": round(float(d[y].mean()), 4), "models": res}
    print(y, "rate", round(d[y].mean(), 3)); [print("  ", k, v) for k, v in res.items()]
# hot-hand coefficient with clustered SE, controlling for volume, efficiency and season explosive rate
X = sm.add_constant(d[BASE + ["ex20_rate", "deep_rate", "adot", "hot", "ex20_l2", "opp_ex_rate", "implied", "outdoor_wind"]])
for y in ("y100", "y30"):
    m = sm.Logit(d[y], X).fit(disp=0, cov_type="cluster", cov_kwds={"groups": pd.factorize(d.game_id)[0]})
    print("\n", y); print(m.summary2().tables[1][["Coef.", "Std.Err.", "P>|z|"]].round(4))
    out[y]["coef"] = {k: {"coef": round(float(m.params[k]), 4), "p": round(float(m.pvalues[k]), 4)} for k in m.params.index}
# decile check: does a 'hot' streak (2+ explosive catches in last 2 games) change next-game explosive rate within same season-rate band?
d["band"] = pd.qcut(d.ex20_rate * d.tgt_pg, 5, duplicates="drop")
t = d.groupby(["band", d.ex20_l2 >= 2], observed=True).agg(n=("y30", "size"), p30=("y30", "mean"), p100=("y100", "mean")).round(3)
print("\nexpected explosive catches per game band x hot last 2 games:\n", t)
out["hot_table"] = t.reset_index().astype(str).to_dict("records")
(H / "explosive_results.json").write_text(json.dumps(out, indent=1, default=str))

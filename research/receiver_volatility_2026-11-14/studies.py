"""Q1b discrimination; Q2 seesaw; Q3 QB change; Q4 position target share vs what the defense allows; team target-tree predictability."""
import numpy as np, pandas as pd, json
from pathlib import Path
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score
import statsmodels.formula.api as smf
H = Path(__file__).resolve().parent
d = pd.read_parquet(H / "rows.parquet"); d = d[d.games_prior >= 3].copy()
d["y100"] = (d.y_yds >= 100).astype(int); d["y30"] = (d.y_ex30 >= 1).astype(int)
d["l_tgt"] = np.log(d.tgt_pg); d["is_WR"] = (d.pos == "WR").astype(int); d["is_TE"] = (d.pos == "TE").astype(int); d["implied"] = d.implied.fillna(d.implied.mean())
R = {}
# ---- Q1b: how sharp can it get?
cols = ["l_tgt", "share", "ypt", "is_WR", "is_TE", "implied", "adot", "deep_rate"]
ps = []
for s in sorted(d.season.unique()):
    tr, te = d[d.season != s], d[d.season == s]
    for y in ("y100", "y30"):
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(tr[cols], tr[y])
        d.loc[te.index, "p_" + y] = m.predict_proba(te[cols])[:, 1]
q = {}
for y in ("y100", "y30"):
    d["dec"] = pd.qcut(d["p_" + y], 10, labels=False)
    t = d.groupby("dec").agg(pred=("p_" + y, "mean"), hit=(y, "mean"), n=(y, "size")).round(3)
    q[y] = {"auc": round(roc_auc_score(d[y], d["p_" + y]), 3), "deciles": t.reset_index().to_dict("records")}
    print(y, "AUC", q[y]["auc"]); print(t.T)
R["q1_sharpness"] = q
# ---- Q2: seesaw between a team's top two wide receivers (by prior target share)
wr = d[d.pos == "WR"].sort_values("share", ascending=False)
pairs = wr.groupby(["game_id", "team"]).head(2).groupby(["game_id", "team"]).filter(lambda x: len(x) == 2).sort_values(["game_id", "team", "share"], ascending=[True, True, False])
a, b = pairs.iloc[0::2].reset_index(drop=True), pairs.iloc[1::2].reset_index(drop=True)
for X in (a, b):
    X["yres"] = X.y_yds - X.yds_avg; X["tres"] = X.y_tgt - X.share * X.y_team_tgts; X["sh_g"] = X.y_tgt / X.y_team_tgts
seesaw = {"pairs": len(a), "corr_yards": round(a.y_yds.corr(b.y_yds), 3), "corr_yards_vs_their_average": round(a.yres.corr(b.yres), 3),
          "corr_target_share_in_game": round(a.sh_g.corr(b.sh_g), 3),
          "p_wr2_100": round(float((b.y_yds >= 100).mean()), 3), "p_wr2_100_when_wr1_100": round(float((b.y_yds[a.y_yds >= 100] >= 100).mean()), 3),
          "p_wr2_100_when_wr1_under40": round(float((b.y_yds[a.y_yds < 40] >= 100).mean()), 3),
          "p_wr1_100": round(float((a.y_yds >= 100).mean()), 3), "p_wr1_100_when_wr2_under40": round(float((a.y_yds[b.y_yds < 40] >= 100).mean()), 3)}
print("\nseesaw", seesaw)
# can the matchup tell which one booms? sign agreement of (a.yres - b.yres) with predicted difference using defense allowed? use target share difference prior vs result
diffpred = (a.share - b.share); diffact = (a.sh_g - b.sh_g)
seesaw["corr_prior_share_gap_vs_game_share_gap"] = round(diffpred.corr(diffact), 3)
named = {}
for tm, n1, n2 in (("CIN", "Ja'Marr Chase", "Tee Higgins"), ("GB", "Christian Watson", "Matthew Golden"), ("BUF", "Khalil Shakir", "Keon Coleman")):
    pass
R["q2_seesaw"] = seesaw
# ---- Q3: QB change. When this game's QB differs from the usual one and he has 2+ prior games, which share predicts targets better?
qc = d[(d.qb_changed == 1) & (d.games_same_qb >= 2) & d.share_same_qb.notna()].copy()
for c in ("share", "share_same_qb", "share_l3"):
    qc["pred_" + c] = qc[c] * qc.y_team_tgts
res3 = {c: round(float((qc["pred_" + c] - qc.y_tgt).abs().mean()), 3) for c in ("share", "share_same_qb", "share_l3")}
blend = 0.5 * qc.share + 0.5 * qc.share_same_qb
res3["50/50 blend"] = round(float((blend * qc.y_team_tgts - qc.y_tgt).abs().mean()), 3)
same = d[(d.qb_changed == 0)]
res3["n_games_with_new_qb"] = len(qc); res3["mean_abs_share_shift"] = round(float((qc.share_same_qb - qc.share).abs().mean()), 3)
print("\nQB change target MAE by share used:", res3)
R["q3_qb_change"] = res3
# ---- Q4: does what a defense allows to a position move that position group's target share?
g = d.groupby(["game_id", "team", "opp", "season", "week", "pos"]).agg(y_tgt=("y_tgt", "sum"), exp=("share", "sum"), team_tgts=("y_team_tgts", "first"), opp_pos_tpg=("opp_pos_tpg", "first"), opp_pos_ypg=("opp_pos_ypg", "first")).reset_index()
g["grp_share"] = g.y_tgt / g.team_tgts; g["dev"] = g.grp_share - g.exp
lg = g.groupby(["season", "pos"]).opp_pos_tpg.transform("mean")
g["opp_tgt_idx"] = g.opp_pos_tpg / lg - 1
g = g.dropna(subset=["dev", "opp_tgt_idx"])
res4 = {}
for P in ("WR", "TE", "RB"):
    x = g[g.pos == P]
    m = smf.ols("dev ~ opp_tgt_idx", data=x).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.game_id)[0]})
    res4[P] = {"slope": round(float(m.params["opp_tgt_idx"]), 4), "p": round(float(m.pvalues["opp_tgt_idx"]), 4), "n": len(x),
               "meaning": f"a defense that sees 20% more {P} targets than average moves this offense's {P} target share by {m.params['opp_tgt_idx'] * 0.2 * 100:+.2f} points"}
print("\nposition share vs defense targets allowed:", res4)
R["q4_position_share"] = res4
# ---- team target-tree predictability: how well prior share predicts game share for each team's main targets (2026)
d26 = d[(d.season == 2026)].copy(); d26["sh_g"] = d26.y_tgt / d26.y_team_tgts
top = d26[d26.share >= 0.12]
tt = top.groupby("team").apply(lambda x: pd.Series({"players": x.player.nunique(), "mad_share_pts": round(float((x.sh_g - x.share).abs().mean() * 100), 1),
       "corr": round(float(x.sh_g.corr(x.share)), 2)}), include_groups=False).sort_values("mad_share_pts")
print("\n2026 team target-tree predictability (lower miss = steadier):\n", tt.to_string())
R["team_tree"] = tt.reset_index().to_dict("records")
(H / "studies_results.json").write_text(json.dumps(R, indent=1, default=str))

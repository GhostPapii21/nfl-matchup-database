"""Reception lean vs yardage lean: does the starting QB's style move a receiver's catches and yards per catch?

Asked after Week 11: Malik Nabers had 12 targets and 7 catches but 55 yards with J.J. McCarthy (18 of 38). Volume and
catches held; yards per catch did not. Question: when the starter throws shorter (air yards per attempt, aDOT) or less
accurately (completion % over expected, CPOE) than the QB whose games built the receiver's averages, do his catch rate
and yards per catch move, and in opposite directions?

Rows: 2022-2026 regular-season WR/TE games with 4+ targets, 3+ earlier games that season. For each: the game's starter
(most dropbacks) and his aDOT and CPOE over his previous 600 attempts (any team, before this game); the "baseline QB"
mix = the receiver's earlier targets that season, weighted by who threw them. Outcomes: catch rate and yards per catch
in the game relative to the receiver's own prior averages. Fit 2022-24, check 2025-26.

    python3 research/rec_vs_yards_2026-11-23/study.py      # writes results.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
C = ROOT / "pregame" / ".cache"
COLS = ["game_id", "season", "week", "season_type", "posteam", "passer_player_id", "receiver_player_id", "pass_attempt", "sack",
        "complete_pass", "air_yards", "receiving_yards", "cpoe", "qb_dropback", "two_point_attempt"]


def load():
    fr = []
    for y in range(2021, 2027):
        f = C / f"play_by_play_{y}.parquet"
        if f.exists():
            p = pd.read_parquet(f, columns=COLS)
            fr.append(p[(p.season_type == "REG") & (p.pass_attempt == 1) & (p.sack != 1) & (p.two_point_attempt != 1)])
    return pd.concat(fr).sort_values(["season", "week"])


def qb_form(p):
    """Each QB's aDOT and CPOE over his previous 600 attempts before each game (any team)."""
    g = p.dropna(subset=["passer_player_id"]).groupby(["passer_player_id", "season", "week"]).agg(
        att=("pass_attempt", "sum"), air=("air_yards", "sum"), cpoe_sum=("cpoe", "sum"), cpoe_n=("cpoe", "count")).reset_index()
    g = g.sort_values(["passer_player_id", "season", "week"])
    out = []
    for q, h in g.groupby("passer_player_id"):
        a, ai, cs, cn = h.att.to_numpy(), h.air.to_numpy(), h.cpoe_sum.to_numpy(), h.cpoe_n.to_numpy()
        for i in range(len(h)):
            j = i - 1; A = AI = CS = CN = 0.0
            while j >= 0 and A < 600:
                A += a[j]; AI += ai[j]; CS += cs[j]; CN += cn[j]; j -= 1
            out.append((q, int(h.season.iloc[i]), int(h.week.iloc[i]), A, AI / A if A else np.nan, CS / CN if CN else np.nan))
    return pd.DataFrame(out, columns=["qb", "season", "week", "qb_prior_att", "qb_adot", "qb_cpoe"])


def main():
    p = load()
    form = qb_form(p)
    starter = (p.groupby(["game_id", "posteam", "passer_player_id"]).size().rename("n").reset_index()
               .sort_values("n").drop_duplicates(["game_id", "posteam"], keep="last").rename(columns={"passer_player_id": "qb"})[["game_id", "posteam", "qb"]])
    r = p.dropna(subset=["receiver_player_id"]).groupby(["season", "week", "game_id", "posteam", "receiver_player_id"]).agg(
        tgt=("pass_attempt", "sum"), rec=("complete_pass", "sum"), yds=("receiving_yards", "sum")).reset_index()
    # who threw each receiver's earlier targets (baseline QB mix)
    by_q = p.dropna(subset=["receiver_player_id", "passer_player_id"]).groupby(["season", "week", "receiver_player_id", "passer_player_id"]).size().rename("t").reset_index()
    by_q = by_q.merge(form.rename(columns={"qb": "passer_player_id"}), on=["passer_player_id", "season", "week"], how="left")
    r = r.merge(starter, on=["game_id", "posteam"]).merge(form, on=["qb", "season", "week"], how="left")
    r = r.sort_values(["receiver_player_id", "season", "week"])
    rows = []
    for (pid, s), h in r.groupby(["receiver_player_id", "season"]):
        bq = by_q[(by_q.receiver_player_id == pid) & (by_q.season == s)]
        for i in range(3, len(h)):
            pr, cur = h.iloc[:i], h.iloc[i]
            if cur.tgt < 4 or pr.rec.sum() < 8 or pd.isna(cur.qb_adot) or cur.qb_prior_att < 150:
                continue
            b = bq[bq.week < cur.week].dropna(subset=["qb_adot"])
            if b.t.sum() < 10:
                continue
            rows.append({"season": s, "week": int(cur.week), "player": pid, "team": cur.posteam, "tgt": cur.tgt, "rec": cur.rec, "yds": cur.yds,
                         "cr_prior": pr.rec.sum() / pr.tgt.sum(), "ypc_prior": pr.yds.sum() / pr.rec.sum(),
                         "adot_qb": cur.qb_adot, "cpoe_qb": cur.qb_cpoe,
                         "adot_base": float(np.average(b.qb_adot, weights=b.t)), "cpoe_base": float(np.average(b.qb_cpoe.fillna(0), weights=b.t))})
    d = pd.DataFrame(rows)
    d["d_adot"] = d.adot_qb - d.adot_base          # yards: starter throws deeper (+) or shorter (-) than his usual passers
    d["d_cpoe"] = d.cpoe_qb - d.cpoe_base          # points of completion % over expected
    d["shorter"] = (d.d_adot <= -1.0).astype(int)
    tr, te = d[d.season <= 2024], d[d.season >= 2025]
    res = {"rows": int(len(d)), "train": int(len(tr)), "test": int(len(te))}
    # catch rate: binomial (rec of tgt) with offset logit(cr_prior); yards per catch: gaussian on log ratio, weighted by catches
    for name, data in (("train_2022_24", tr), ("test_2025_26", te)):
        out = {}
        lo = np.log(data.cr_prior.clip(0.05, 0.95) / (1 - data.cr_prior.clip(0.05, 0.95)))
        m = sm.GLM(np.column_stack([data.rec, data.tgt - data.rec]), sm.add_constant(data[["d_adot", "d_cpoe"]]), family=sm.families.Binomial(), offset=lo).fit()
        out["catch_rate"] = {k: {"coef": round(float(m.params[k]), 4), "z": round(float(m.params[k] / m.bse[k]), 2)} for k in ("d_adot", "d_cpoe")}
        c = data[data.rec > 0]
        y = np.log((c.yds / c.rec).clip(1) / c.ypc_prior)
        m2 = sm.WLS(y, sm.add_constant(c[["d_adot", "d_cpoe"]]), weights=c.rec).fit()
        out["yards_per_catch_log"] = {k: {"coef": round(float(m2.params[k]), 4), "z": round(float(m2.params[k] / m2.bse[k]), 2)} for k in ("d_adot", "d_cpoe")}
        # plain buckets: starter throws 1+ yard shorter than the receiver's usual passers
        for lab, x in (("starter_1yd_shorter", data[data.d_adot <= -1]), ("similar", data[data.d_adot.abs() < 1]), ("starter_1yd_deeper", data[data.d_adot >= 1])):
            if len(x):
                cr_ratio = (x.rec.sum() / x.tgt.sum()) / float(np.average(x.cr_prior, weights=x.tgt))
                ypc_ratio = (x.yds.sum() / max(x.rec.sum(), 1)) / float(np.average(x.ypc_prior, weights=x.rec.clip(lower=1)))
                out[lab] = {"games": int(len(x)), "catch_rate_vs_his_norm": round(float(cr_ratio), 3), "yards_per_catch_vs_his_norm": round(float(ypc_ratio), 3)}
        res[name] = out
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

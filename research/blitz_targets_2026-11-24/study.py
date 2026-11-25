"""Does facing a blitz-heavy defense move targets to tight ends and backs and away from the WR1? (owner, after MNF
Nov 23, 2026: Washington blitzed Burrow all night; TEs and RBs got 65% of targets, Chase 31 yards.)

Data: Sharp Football Analysis advanced box scores, 2026 Weeks 1-10 (data_packages/sharp_advanced_2026_w1_10: per
team-game blitz faced, man faced, pressure allowed, time to throw, aDOT, deep rate) and nflverse play-by-play (targets by
receiver position). Each offense's game is compared with its OWN earlier games (target share by position, aDOT, deep
rate), so team style is taken out.

  1. Is blitzing a trait? Defense's blitz rate in earlier games vs its blitz rate this game.
  2. In-game: blitz rate faced this game vs the offense's RB+TE target share, WR1 share, aDOT and deep rate (vs its norm).
  3. Pregame (usable on the board): the DEFENSE's earlier blitz rate vs the same shifts. Same for man and pressure.

    python3 research/blitz_targets_2026-11-24/study.py      # writes results.json
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PKG = ROOT / "data_packages" / "sharp_advanced_2026_w1_10"


def sharp():
    rows = [json.loads(l) for l in open(PKG / "team_games.jsonl")]
    t = pd.DataFrame([{"week": r["week"], "team": r["team"], "opp": r["opponent"], **r["metrics"]} for r in rows])
    t["blitz_r"] = t.blitz / t.db
    t["man_r"] = t.man / t["cov"].replace(0, np.nan)
    t["prsr_r"] = t.prsr / t.db
    t["adot"] = t.air / t.att
    t["deep_r"] = t.deep / t.att
    t["ttt_s"] = t.ttt / t.ttt_n
    return t


def targets():
    f = sorted(glob.glob(str(ROOT / "data" / "historical" / "nflverse" / "pbp_2026_w1_10*.parquet")))[-1]
    p = pd.read_parquet(f, columns=["week", "season_type", "posteam", "pass_attempt", "receiver_player_id", "sack"])
    p = p[(p.season_type == "REG") & (p.pass_attempt == 1) & p.receiver_player_id.notna()]
    ro = pd.read_parquet(ROOT / "pregame" / ".cache" / "roster_weekly_2026.parquet", columns=["gsis_id", "position"]).drop_duplicates("gsis_id")
    p["pos"] = p.receiver_player_id.map(dict(zip(ro.gsis_id, ro.position))).fillna("?")
    p["grp"] = np.where(p.pos.isin(["RB", "FB"]), "RB", np.where(p.pos == "TE", "TE", np.where(p.pos == "WR", "WR", "OTH")))
    g = p.groupby(["week", "posteam", "grp"]).size().unstack(fill_value=0).reset_index().rename(columns={"posteam": "team"})
    for c in ("RB", "TE", "WR", "OTH"):
        if c not in g:
            g[c] = 0
    g["n"] = g[["RB", "TE", "WR", "OTH"]].sum(axis=1)
    # WR1 = the team's WR with the most targets in its EARLIER games
    w = p[p.grp == "WR"].groupby(["posteam", "week", "receiver_player_id"]).size().rename("t").reset_index()
    wr1 = []
    for (tm, wk), _ in g.set_index(["team", "week"]).iterrows():
        prior = w[(w.posteam == tm) & (w.week < wk)].groupby("receiver_player_id").t.sum()
        cur = w[(w.posteam == tm) & (w.week == wk)].set_index("receiver_player_id").t
        wr1.append({"team": tm, "week": wk, "wr1_t": int(cur.get(prior.idxmax(), 0)) if len(prior) else np.nan})
    return g.merge(pd.DataFrame(wr1), on=["team", "week"])


def prior_mean(df, key, cols, weight=None):
    df = df.sort_values([key, "week"]).copy()
    for c in cols:
        if weight:
            num = df.groupby(key)[c].transform(lambda s: s.shift().expanding().sum())
            den = df.groupby(key)[weight].transform(lambda s: s.shift().expanding().sum())
            df[c + "_prior"] = num / den
        else:
            df[c + "_prior"] = df.groupby(key)[c].transform(lambda s: s.shift().expanding().mean())
    df["k_" + key] = df.groupby(key).cumcount()
    return df


def slope(x, y, w):
    ok = x.notna() & y.notna() & w.notna()
    x, y, w = x[ok], y[ok], w[ok]
    X = np.column_stack([np.ones(len(x)), x])
    W = np.diag(w)
    b = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    r = y - X @ b
    s2 = (w * r ** 2).sum() / (w.sum() - 2)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ W @ X)))
    return {"per_10pts": round(float(b[1] * 0.10), 4), "z": round(float(b[1] / se[1]), 2), "n": int(len(x))}


def main():
    s, tg = sharp(), targets()
    d = s.merge(tg, on=["team", "week"], how="inner")
    for c in ("RB", "TE", "WR"):
        d[c + "_sh"] = d[c] / d.n
    d["rbte_sh"] = d.RB_sh + d.TE_sh
    d["wr1_sh"] = d.wr1_t / d.n
    # offense norms from its own earlier games (count-weighted shares)
    d["rbte_n"], d["wr1_n"] = d.RB + d.TE, d.wr1_t
    d = d.sort_values(["team", "week"])
    for c, num in (("rbte_norm", "rbte_n"), ("wr1_norm", "wr1_n")):
        d[c] = d.groupby("team")[num].transform(lambda s: s.shift().expanding().sum()) / d.groupby("team").n.transform(lambda s: s.shift().expanding().sum())
    for c in ("adot", "deep_r", "ttt_s"):
        d[c + "_norm"] = d.groupby("team")[c].transform(lambda s: s.shift().expanding().mean())
    d["k_off"] = d.groupby("team").cumcount()
    # defense's earlier rates (from the offenses it faced)
    dd = s[["week", "opp", "blitz", "db", "man", "cov", "prsr"]].rename(columns={"opp": "defense"}).sort_values(["defense", "week"])
    for c, den in (("blitz", "db"), ("man", "cov"), ("prsr", "db")):
        dd[f"def_{c}_prior"] = dd.groupby("defense")[c].transform(lambda x: x.shift().expanding().sum()) / dd.groupby("defense")[den].transform(lambda x: x.shift().expanding().sum())
    dd["k_def"] = dd.groupby("defense").cumcount()
    d = d.merge(dd[["week", "defense", "def_blitz_prior", "def_man_prior", "def_prsr_prior", "k_def"]], left_on=["week", "opp"], right_on=["week", "defense"])
    h = d[(d.k_off >= 2) & (d.k_def >= 2)].copy()
    for c in ("rbte", "wr1"):
        h[c + "_dev"] = h[c + "_sh"] - h[c + "_norm"]
    for c in ("adot", "deep_r", "ttt_s"):
        h[c + "_dev"] = h[c] - h[c + "_norm"]
    res = {"team_games": int(len(h)), "weeks": "2026 Weeks 3-10 (2+ earlier games for both teams)"}
    t = d[d.k_def >= 2].dropna(subset=["def_blitz_prior"])
    res["1_blitz_is_a_trait"] = {"corr_prior_vs_this_game": round(float(np.corrcoef(t.def_blitz_prior, t.blitz_r)[0, 1]), 3), "n": int(len(t))}
    outs = {"rbte_dev": "RB+TE target share vs norm", "wr1_dev": "WR1 target share vs norm", "adot_dev": "aDOT vs norm (yards)",
            "deep_r_dev": "deep-target rate vs norm", "ttt_s_dev": "time to throw vs norm (sec)"}
    res["2_in_game_blitz_faced"] = {lab: slope(h.blitz_r, h[c], h.n.astype(float)) for c, lab in outs.items()}
    res["3_pregame_defense_blitz"] = {lab: slope(h.def_blitz_prior, h[c], h.n.astype(float)) for c, lab in outs.items()}
    res["3b_pregame_defense_man"] = {lab: slope(h.def_man_prior, h[c], h.n.astype(float)) for c, lab in outs.items() if c in ("rbte_dev", "wr1_dev", "adot_dev")}
    res["3c_pregame_defense_pressure"] = {lab: slope(h.def_prsr_prior, h[c], h.n.astype(float)) for c, lab in outs.items() if c in ("rbte_dev", "wr1_dev", "adot_dev")}
    h["third"] = pd.qcut(h.def_blitz_prior.rank(method="first"), 3, labels=["blitzes least", "middle", "blitzes most"])
    res["3_by_defense_blitz_third"] = [{"defense": str(k), "games": int(len(x)), "def_blitz_prior": round(float(x.def_blitz_prior.mean()), 3),
                                        "blitz_faced": round(float(x.blitz_r.mean()), 3), "rbte_vs_norm_pts": round(100 * float(np.average(x.rbte_dev, weights=x.n)), 1),
                                        "wr1_vs_norm_pts": round(100 * float(np.average(x.wr1_dev.fillna(0), weights=x.n)), 1),
                                        "adot_vs_norm": round(float(x.adot_dev.mean()), 2), "ttt_vs_norm": round(float(x.ttt_s_dev.mean()), 3)}
                                       for k, x in h.groupby("third", observed=True)]
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

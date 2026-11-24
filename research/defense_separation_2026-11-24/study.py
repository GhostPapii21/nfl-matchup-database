"""Do some defenses take away receiver separation as a team trait, and does it predict receivers falling short?
(owner, after MNF Nov 23, 2026: Washington blanketed Ja'Marr Chase and Tee Higgins.)

Next Gen Stats weekly receiving (avg_separation at catch or incompletion), 2018-2026. For each receiver-week with 3+
targets: separation minus his own average in his earlier games that season (3+ games). A defense's "separation taken"
= the target-weighted mean of that gap for receivers who faced it in earlier weeks (3+ games). Questions:
  1. Is it a trait? Does a defense's earlier figure predict the gap receivers get against it this week?
  2. Does it predict 80-yard games beyond the star model (receivers; and WR1s, 22%+ target share)? Fit 2022-24, held
     out 2025-26, same bar as before (log loss and Brier both better, |z| >= 2).

    python3 research/defense_separation_2026-11-24/study.py      # writes results.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "pregame" / ".cache"
sys.path.insert(0, str(ROOT / "research" / "watch_model_2026-11-16"))
sys.path.insert(0, str(ROOT / "research" / "star_review_2026-11-23"))
import fit as F  # noqa: E402
import study as SR  # noqa: E402

AL = {"OAK": "LV", "SD": "LAC", "STL": "LA", "LAR": "LA"}


def defense_sep():
    n = pd.read_parquet(C / "ngs_receiving.parquet")
    n = n[(n.season_type == "REG") & (n.week > 0) & (n.season >= 2018) & (n.targets >= 3)].copy()
    n["team"] = n.team_abbr.replace(AL)
    g = pd.read_parquet(C / "games.parquet")
    g = g[g.game_type == "REG"]
    opp = pd.concat([g[["season", "week", "home_team", "away_team"]].rename(columns={"home_team": "team", "away_team": "opp"}),
                     g[["season", "week", "away_team", "home_team"]].rename(columns={"away_team": "team", "home_team": "opp"})])
    n = n.merge(opp, on=["season", "week", "team"], how="inner").sort_values(["player_gsis_id", "season", "week"])
    gp = n.groupby(["player_gsis_id", "season"])
    n["own_prior"] = gp.avg_separation.transform(lambda s: s.shift().expanding().mean())
    n["own_n"] = gp.cumcount()
    n = n[n.own_n >= 3].copy()
    n["gap"] = n.avg_separation - n.own_prior
    d = n.groupby(["opp", "season", "week"]).apply(lambda x: pd.Series({"gw": float((x.gap * x.targets).sum()), "w": float(x.targets.sum())}),
                                                   include_groups=False).reset_index().sort_values(["opp", "season", "week"])
    d["gw_td"] = d.groupby(["opp", "season"]).gw.transform(lambda s: s.shift().expanding().sum())
    d["w_td"] = d.groupby(["opp", "season"]).w.transform(lambda s: s.shift().expanding().sum())
    d["k"] = d.groupby(["opp", "season"]).cumcount()
    d["def_sep"] = np.where(d.k >= 3, d.gw_td / d.w_td, np.nan)
    return n, d[["opp", "season", "week", "def_sep", "gw", "w"]]


def main():
    n, d = defense_sep()
    res = {}
    # 1. persistence: earlier defense figure vs this week's gap
    t = d.dropna(subset=["def_sep"]).copy()
    t["this_week"] = t.gw / t.w
    res["trait"] = {"defense_weeks": int(len(t)), "corr_prior_vs_this_week": round(float(np.corrcoef(t.def_sep, t.this_week)[0, 1]), 3),
                    "slope": round(float(np.polyfit(t.def_sep, t.this_week, 1)[0]), 3),
                    "def_sep_sd": round(float(t.def_sep.std()), 3), "this_week_gap_sd": round(float(t.this_week.std()), 3)}
    # 2. star model test
    r = F.receivers()
    r = r.merge(d[["opp", "season", "week", "def_sep"]], on=["opp", "season", "week"], how="left")
    r["def_sep"] = r.def_sep.fillna(0.0)
    out, te = SR.evaluate(r, SR.RX, ["def_sep"])
    res["receivers_80plus"] = out
    w1 = r[r.share >= 0.22].copy()
    out1, _ = SR.evaluate(w1, SR.RX, ["def_sep"])
    res["wr1_80plus"] = out1
    # yards vs projection-free check: WR1 yards by defense third (held-out seasons)
    h = w1[w1.season >= 2025].copy()
    h["third"] = pd.qcut(h.def_sep.rank(method="first"), 3, labels=["takes away separation", "middle", "gives separation"])
    res["wr1_2025_26_by_defense_third"] = [{"defense": str(k), "games": int(len(x)), "yards_avg": round(float(x.y_yds.mean()), 1),
                                            "hit80": round(float((x.y_yds >= 80).mean()), 3), "his_avg_coming_in": round(float(x.yds_avg.mean()), 1)}
                                           for k, x in h.groupby("third", observed=True)]
    cur = d[(d.season == 2026)].sort_values("week").groupby("opp").tail(1)
    cur = cur.assign(def_sep_now=(cur.gw_td if "gw_td" in cur else cur.gw)).dropna(subset=["def_sep"]).sort_values("def_sep")
    res["2026_now_takes_away_most"] = [{"defense": a, "sep_vs_norm_yards": round(float(b), 2)} for a, b in zip(cur.opp, cur.def_sep)][:8]
    res["2026_now_gives_most"] = [{"defense": a, "sep_vs_norm_yards": round(float(b), 2)} for a, b in zip(cur.opp, cur.def_sep)][-8:]
    res["2026_WAS_CIN"] = {a: round(float(b), 2) for a, b in zip(cur.opp, cur.def_sep) if a in ("WAS", "CIN")}
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

"""Do alpha receivers do more against defenses that give up big plays, and in pass-heavy game types? (2022 to wk 9 2026)

Tiers use only what was known before each game:
  alpha   8+ targets a game and 70+ yards a game coming in
  tier B  7+ targets and 55+ yards a game (not alpha)
Defense, from earlier games that season:
  opp_ex_rate   20+ yard completions allowed per pass attempt, relative to the league
  lead_yds      average yards it allowed to the opposing team's lead receiver (top share, 7+ targets a game)
Game type:
  total         the betting total
  team_pass     the offense's own targets per game coming in

    python3 research/game_types_2026-11-16/test_tiers.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
r = pd.read_parquet(HERE.parents[1] / "research" / "receiver_volatility_2026-11-14" / "rows.parquet")
r = r[r.pos.isin(["WR", "TE"]) & (r.games_prior >= 3) & r.implied.notna() & (r.share > 0)].copy()
r["rank"] = r.groupby(["game_id", "team"]).share.rank(ascending=False, method="first")
r["total"] = r.implied * 2 - r.spread
r["team_pass"] = r.tgt_pg / r.share
r["tier"] = np.select([(r.tgt_pg >= 8) & (r.yds_avg >= 70), (r.tgt_pg >= 7) & (r.yds_avg >= 55)], ["alpha", "tier B"], "other")
lead = r[(r["rank"] == 1) & (r.tgt_pg >= 7)].sort_values(["season", "opp", "week"])
lead["cum"] = lead.groupby(["season", "opp"]).y_yds.cumsum() - lead.y_yds
lead["n"] = lead.groupby(["season", "opp"]).cumcount()
lead["lead_yds"] = lead.cum / lead.n.clip(lower=1)
allw = r[["season", "opp", "week"]].drop_duplicates().merge(lead[["season", "opp", "week", "cum", "n", "y_yds"]], on=["season", "opp", "week"], how="left").sort_values(["season", "opp", "week"])
allw["cum_all"] = allw.groupby(["season", "opp"]).y_yds.transform(lambda s: s.fillna(0).cumsum() - s.fillna(0))
allw["n_all"] = allw.groupby(["season", "opp"]).y_yds.transform(lambda s: s.notna().cumsum() - s.notna())
allw["lead_yds"] = allw.cum_all / allw.n_all.clip(lower=1)
r = r.merge(allw[["season", "opp", "week", "lead_yds", "n_all"]], on=["season", "opp", "week"], how="left")
out = {"tiers": {}}
for t in ("alpha", "tier B", "other"):
    x = r[r.tier == t]
    out["tiers"][t] = {"n": int(len(x)), "per_week": round(len(x) / r.groupby(["season", "week"]).ngroups, 1), "hit80": round(float((x.y_yds >= 80).mean()), 3),
                       "hit100": round(float((x.y_yds >= 100).mean()), 3), "yards": round(float(x.y_yds.mean()), 1), "explosive_pg": round(float(x.y_ex20.mean()), 2)}


def split(x, col, labels=("lowest third", "middle", "highest third")):
    q = pd.qcut(x[col], 3, labels=list(labels), duplicates="drop")
    return {str(k): {"n": int(len(v)), "hit80": round(float((v.y_yds >= 80).mean()), 3), "hit100": round(float((v.y_yds >= 100).mean()), 3),
                     "yards": round(float(v.y_yds.mean()), 1), "explosive_pg": round(float(v.y_ex20.mean()), 2), "avg": round(float(v[col].mean()), 2)}
            for k, v in x.groupby(q, observed=True)}


for t in ("alpha", "tier B"):
    x = r[r.tier == t]
    late = x[x.week >= 8]
    y = x[x.n_all >= 3]
    out[t] = {"by_defense_explosive_rate": split(x, "opp_ex_rate"), "by_defense_explosive_rate_week8_on": split(late, "opp_ex_rate"),
              "by_yards_allowed_to_lead_receivers": split(y, "lead_yds"), "by_game_total": split(x, "total"), "by_team_pass_volume": split(x, "team_pass"),
              "by_implied": split(x, "implied")}
    both = x[(x.opp_ex_rate >= x.opp_ex_rate.quantile(0.6)) & (x.total >= 46)]
    neither = x[(x.opp_ex_rate <= x.opp_ex_rate.quantile(0.4)) & (x.total <= 43)]
    out[t]["leaky_defense_and_high_total"] = {"n": int(len(both)), "hit80": round(float((both.y_yds >= 80).mean()), 3), "hit100": round(float((both.y_yds >= 100).mean()), 3)}
    out[t]["stingy_defense_and_low_total"] = {"n": int(len(neither)), "hit80": round(float((neither.y_yds >= 80).mean()), 3), "hit100": round(float((neither.y_yds >= 100).mean()), 3)}
    hold = x[x.season >= 2025]
    b2, n2 = hold[(hold.opp_ex_rate >= x.opp_ex_rate.quantile(0.6)) & (hold.total >= 46)], hold[(hold.opp_ex_rate <= x.opp_ex_rate.quantile(0.4)) & (hold.total <= 43)]
    out[t]["same_split_2025_26_only"] = {"leaky_high": {"n": int(len(b2)), "hit80": round(float((b2.y_yds >= 80).mean()), 3)},
                                         "stingy_low": {"n": int(len(n2)), "hit80": round(float((n2.y_yds >= 80).mean()), 3)}}
(HERE / "tier_results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))

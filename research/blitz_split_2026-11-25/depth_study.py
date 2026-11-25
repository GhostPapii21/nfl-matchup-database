"""Against blitz-heavy defenses, do deep receivers lose more yards per target than short ones? (owner, Nov 25, 2026)
Receiver-games 2026 Week 4+: his yards per target that game minus his own earlier yards per target, by his earlier aDOT
(deep 11+, middle 7-11, short <7) and the defense's earlier blitz rate (FTN). Also his target share vs his earlier share.

    python3 research/blitz_split_2026-11-25/depth_study.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
C = HERE.parents[1] / "pregame" / ".cache"
p = pd.read_parquet(C / "play_by_play_2026.parquet", columns=["season_type", "week", "game_id", "play_id", "posteam", "defteam", "qb_dropback",
                                                              "receiver_player_id", "pass_attempt", "sack", "air_yards", "receiving_yards"])
f = pd.read_parquet(C / "ftn_charting_2026.parquet", columns=["nflverse_game_id", "nflverse_play_id", "n_blitzers"])
p = p[(p.season_type == "REG") & (p.qb_dropback == 1)].merge(f, left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"], how="left")
p["bl"] = p.n_blitzers.fillna(0) > 0
t = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()].copy()
t["yds"] = t.receiving_yards.fillna(0)
g = t.groupby(["receiver_player_id", "week", "game_id", "posteam", "defteam"]).agg(tg=("yds", "size"), y=("yds", "sum"), ay=("air_yards", "sum")).reset_index()
team = t.groupby(["game_id", "posteam"]).size().rename("team_tg")
g = g.join(team, on=["game_id", "posteam"]).sort_values(["receiver_player_id", "week"])
cs = g.groupby("receiver_player_id")[["tg", "y", "ay", "team_tg"]].cumsum() - g[["tg", "y", "ay", "team_tg"]]
g["p_tg"], g["p_ypt"], g["p_adot"], g["p_share"] = cs.tg, cs.y / cs.tg, cs.ay / cs.tg, cs.tg / cs.team_tg
dbl = p.groupby(["defteam", "week"]).bl.agg(["sum", "size"]).reset_index().sort_values(["defteam", "week"])
dbl["prior"] = (dbl.groupby("defteam")["sum"].cumsum() - dbl["sum"]) / (dbl.groupby("defteam")["size"].cumsum() - dbl["size"])
g = g.merge(dbl[["defteam", "week", "prior"]], on=["defteam", "week"])
g = g[(g.week >= 4) & (g.p_tg >= 20) & g.prior.notna()].copy()
g["ypt_gap"] = g.y / g.tg - g.p_ypt
g["share_gap"] = g.tg / g.team_tg - g.p_share
g["depth"] = pd.cut(g.p_adot, [-99, 7, 11, 99], labels=["short (<7)", "middle (7-11)", "deep (11+)"])
g["defense"] = pd.cut(g.prior, [0, 0.25, 0.33, 1], labels=["blitz-light", "middle", "blitz-heavy (33%+)"])
out = []
for (dp, df), x in g.groupby(["depth", "defense"], observed=True):
    w = x.tg
    rng = np.random.default_rng(1)
    bs = [np.average(x.ypt_gap.values[i], weights=w.values[i]) for i in (rng.integers(0, len(x), len(x)) for _ in range(1000))]
    out.append({"receiver_depth": str(dp), "defense": str(df), "games": int(len(x)), "ypt_vs_own_norm": round(float(np.average(x.ypt_gap, weights=w)), 2),
                "ci95": [round(float(np.percentile(bs, 2.5)), 2), round(float(np.percentile(bs, 97.5)), 2)],
                "share_vs_own_norm_pts": round(100 * float(x.share_gap.mean()), 2)})
(HERE / "depth_results.json").write_text(json.dumps(out, indent=1) + "\n")
print(pd.DataFrame(out).to_string(index=False))

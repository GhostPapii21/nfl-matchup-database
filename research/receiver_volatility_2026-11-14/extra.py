import numpy as np, pandas as pd, json
from pathlib import Path
import statsmodels.formula.api as smf
C = Path("pregame/.cache"); H = Path(__file__).resolve().parent
d = pd.read_parquet(H / "rows.parquet"); d = d[d.games_prior >= 3].copy()
OUT = {}
# rematch: same player, same opponent twice in a season; does first-meeting residual predict the second?
d["res"] = d.y_yds - d.yds_avg
d = d.sort_values(["season", "player", "opp", "week"])
first = d.groupby(["season", "player", "opp"]).nth(0); second = d.groupby(["season", "player", "opp"]).nth(1)
m = first[["season", "player", "opp", "res", "y_yds"]].merge(second[["season", "player", "opp", "res", "y_yds"]], on=["season", "player", "opp"], suffixes=("_1", "_2"))
OUT["rematch"] = {"pairs": len(m), "corr_residual": round(float(m.res_1.corr(m.res_2)), 3),
                  "big_first_100_then_avg_second": round(float(m[m.y_yds_1 >= 100].y_yds_2.mean()), 1), "their_avg_before": round(float(m[m.y_yds_1 >= 100].y_yds_2.mean() - m[m.y_yds_1 >= 100].res_2.mean()), 1)}
print("rematch:", OUT["rematch"])
# short receivers vs man coverage: share deviation ~ opp man rate x aDOT, 2023-2025 (opponent man rate from prior weeks of the same season)
rows = []
for y in (2023, 2024, 2025):
    p = pd.read_parquet(C / f"play_by_play_{y}.parquet"); pp = pd.read_parquet(C / f"pbp_participation_{y}.parquet")
    j = p[(p.qb_dropback == 1) & (p.season_type == "REG")].merge(pp[["nflverse_game_id", "play_id", "defense_man_zone_type"]], left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "play_id"])
    j = j[j.defense_man_zone_type.isin(["MAN_COVERAGE", "ZONE_COVERAGE"])]
    wk = j.groupby(["defteam", "week"]).apply(lambda x: pd.Series({"man": (x.defense_man_zone_type == "MAN_COVERAGE").sum(), "n": len(x)}), include_groups=False).reset_index()
    for w in sorted(wk.week.unique()):
        pr = wk[wk.week < w].groupby("defteam")[["man", "n"]].sum()
        lg = pr.man.sum() / max(pr.n.sum(), 1)
        for t, r in pr.iterrows():
            rows.append({"season": y, "week": w, "opp": t, "opp_man": (r.man + 100 * lg) / (r.n + 100) - lg})
mr = pd.DataFrame(rows)
x = d[d.season.isin([2023, 2024, 2025]) & (d.pos == "WR")].merge(mr, on=["season", "week", "opp"])
x["dev"] = x.y_tgt / x.y_team_tgts - x.share; x["short"] = (x.adot < 8).astype(int)
f = smf.ols("dev ~ opp_man * short", data=x.dropna(subset=["dev"])).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.dropna(subset=["dev"]).game_id)[0]})
OUT["short_vs_man"] = {k: {"coef": round(float(f.params[k]), 4), "p": round(float(f.pvalues[k]), 4)} for k in f.params.index}
print("short WR vs man:", OUT["short_vs_man"])
# previous LA-ARI meeting(s)
g = pd.read_parquet(C / "games.parquet")
mm = g[((g.home_team == "ARI") & (g.away_team == "LA")) | ((g.home_team == "LA") & (g.away_team == "ARI"))].sort_values("gameday").tail(5)[["season", "week", "away_team", "away_score", "home_team", "home_score", "spread_line", "total_line"]]
print(mm.to_string()); OUT["la_ari_meetings"] = mm.astype(str).to_dict("records")
# this week's simulation for named players
want = {"2026_10_MIN_GB": ["Christian Watson", "Matthew Golden", "Justin Jefferson", "T.J. Hockenson", "Jordan Addison"], "2026_10_PIT_CIN": ["Ja'Marr Chase", "Tee Higgins"],
        "2026_10_BUF_NYJ": ["Khalil Shakir", "Dalton Kincaid", "Keon Coleman", "DJ Moore", "James Cook"], "2026_10_NE_DET": ["Hunter Henry", "DeMario Douglas", "Eli Raridon"],
        "2026_10_LA_ARI": ["Puka Nacua", "Trey McBride", "Michael Wilson", "Kyren Williams"]}
sim = {}
for gid, names in want.items():
    b = json.loads(Path(f"dashboard/data/{gid}.json").read_text())
    for sd in b["sides"].values():
        o = sd.get("opportunity") or {}
        for kind in ("receivers", "rushers"):
            for r in o.get(kind, []):
                if r["player"] in names and not r.get("status"):
                    sim[r["player"]] = {"game": gid, "kind": kind, "targets": r.get("targets_mean") or r.get("carries_mean"), "median": r.get("yards_median"),
                                        "p70": r["yards"].get("70"), "p100": r["yards"].get("100"), "p50": r["yards"].get("50")}
    tp = b.get("team_projection", {}).get("samplers", {}).get("matchup_pair")
    if gid == "2026_10_LA_ARI": OUT["la_ari_projection"] = tp; OUT["la_ari_market"] = b.get("market"); OUT["la_ari_inj"] = {s["offense"]: [(x["player"], x["position"], x.get("game_status") or x.get("espn")) for x in s.get("offense_injuries", []) if x.get("status_level", 0) >= 2][:8] for s in b["sides"].values()}
for k, v in sim.items(): print(k, v)
OUT["sim"] = sim; print("LA-ARI projection", OUT.get("la_ari_projection"), OUT.get("la_ari_market")); print("inj", OUT.get("la_ari_inj"))
(H / "extra.json").write_text(json.dumps(OUT, indent=1, default=str))

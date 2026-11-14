import numpy as np, pandas as pd, json
from pathlib import Path
C = Path("pregame/.cache"); H = Path(__file__).resolve().parent
p = pd.read_parquet(C / "play_by_play_2026.parquet"); p = p[(p.season_type == "REG") & (p.two_point_attempt != 1)]
r = pd.read_parquet(C / "roster_weekly_2026.parquet"); name = dict(zip(r.gsis_id, r.full_name)); pos = dict(zip(r.gsis_id, r.position))
pp = pd.read_parquet(C / "pbp_participation_2025.parquet"); p25 = pd.read_parquet(C / "play_by_play_2025.parquet")
OUT = {}
def tree(team, players=None, top=6):
    t = p[(p.posteam == team) & (p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()]
    tot = t.groupby("week").size()
    pg = t.groupby(["week", "defteam", "receiver_player_id"]).agg(tgt=("pass_attempt", "size"), rec=("complete_pass", "sum"), yds=("receiving_yards", lambda s: int(s.fillna(0).sum())), td=("pass_touchdown", "sum"), long=("receiving_yards", "max")).reset_index()
    pg["name"] = pg.receiver_player_id.map(name); pg["pos"] = pg.receiver_player_id.map(pos); pg["share"] = pg.tgt / pg.week.map(tot)
    ids = pg.groupby("receiver_player_id").tgt.sum().sort_values(ascending=False).head(top).index
    pg = pg[pg.receiver_player_id.isin(ids)]
    qb = p[(p.posteam == team) & (p.qb_dropback == 1)].groupby("week").passer_player_name.agg(lambda s: s.mode().iloc[0])
    return pg, qb
def show(team, title):
    pg, qb = tree(team)
    wk = sorted(pg.week.unique())
    opp = pg.groupby("week").defteam.first()
    lines = [f"\n== {title}: {team} target tree by game (catches-yards / targets, share)", "week opp QB | " + " | ".join(pg.groupby("name").tgt.sum().sort_values(ascending=False).index)]
    order = pg.groupby("name").tgt.sum().sort_values(ascending=False).index
    rows = []
    for w in wk:
        cells = []
        for n in order:
            x = pg[(pg.week == w) & (pg.name == n)]
            cells.append(f"{int(x.rec.iloc[0])}-{int(x.yds.iloc[0])}/{int(x.tgt.iloc[0])} ({x.share.iloc[0]:.0%})" if len(x) else "-")
        lines.append(f"{w} {opp.get(w)} {qb.get(w, '?')} | " + " | ".join(cells))
        rows.append({"week": int(w), "opp": opp.get(w), "qb": qb.get(w), **{n: c for n, c in zip(order, cells)}})
    print("\n".join(lines))
    return rows
OUT["BUF"] = show("BUF", "Bills")
# man/zone of BUF opponents (2025 rates) vs who got the ball
d25 = p25[(p25.qb_dropback == 1)].merge(pp[["nflverse_game_id", "play_id", "defense_man_zone_type", "defense_coverage_type"]], left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "play_id"])
d25 = d25[d25.defense_man_zone_type.isin(["MAN_COVERAGE", "ZONE_COVERAGE"])]
man = d25.groupby("defteam").apply(lambda x: (x.defense_man_zone_type == "MAN_COVERAGE").mean(), include_groups=False)
pg, qb = tree("BUF"); pg["opp_man25"] = pg.defteam.map(man)
cc = {n: round(float(x.share.corr(x.opp_man25)), 2) for n, x in pg.groupby("name") if len(x) >= 5}
print("BUF: corr of each player's game target share with the opponent's 2025 man rate:", cc)
OUT["BUF_man_corr"] = cc
OUT["NE"] = show("NE", "Patriots")
OUT["CIN"] = show("CIN", "Bengals")
OUT["GB"] = show("GB", "Packers")
OUT["MIN"] = show("MIN", "Vikings")
OUT["NYG"] = show("NYG", "Giants")
OUT["LA"] = show("LA", "Rams")
OUT["ARI"] = show("ARI", "Cardinals")
# DET vs TEs
t = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()].copy(); t["pos"] = t.receiver_player_id.map(pos)
g = t.groupby(["defteam"]).game_id.nunique()
te = t[t.pos == "TE"].groupby("defteam").agg(tgt=("pass_attempt", "size"), rec=("complete_pass", "sum"), yds=("receiving_yards", lambda s: s.fillna(0).sum()))
te = te.div(g, axis=0).round(1); te["rank_yds"] = te.yds.rank(ascending=True).astype(int)
print("\nDET allowed to TEs per game:", te.loc["DET"].to_dict(), "league avg", te.mean().round(1).to_dict())
OUT["DET_TE"] = {"det": te.loc["DET"].to_dict(), "league": te.mean().round(1).to_dict()}
# Team efficiency for LA and ARI
def eff(tm):
    o = p[(p.posteam == tm) & p.play_type.isin(["pass", "run"])]; dd = p[(p.defteam == tm) & p.play_type.isin(["pass", "run"])]
    gs = pd.read_parquet(C / "games.parquet"); gs = gs[(gs.season == 2026) & gs.home_score.notna() & ((gs.home_team == tm) | (gs.away_team == tm))]
    pf = np.where(gs.home_team == tm, gs.home_score, gs.away_score); pa = np.where(gs.home_team == tm, gs.away_score, gs.home_score)
    rec = f"{int((pf > pa).sum())}-{int((pf < pa).sum())}"
    sacks = dd.sack.sum(); db = dd.qb_dropback.sum()
    to_for = (dd.interception.sum() + dd.fumble_lost.sum()); to_ag = (o.interception.sum() + o.fumble_lost.sum())
    qbs = o[o.qb_dropback == 1].groupby("passer_player_name").agg(db=("qb_dropback", "size"), epa=("epa", "mean")).sort_values("db", ascending=False).head(3).round(3)
    return {"record": rec, "pf_pg": round(pf.mean(), 1), "pa_pg": round(pa.mean(), 1), "margin_pg": round((pf - pa).mean(), 1),
            "off_epa_play": round(o.epa.mean(), 3), "def_epa_play": round(dd.epa.mean(), 3), "off_success": round(o.success.mean(), 3), "def_success": round(dd.success.mean(), 3),
            "pass_epa": round(o[o.pass_attempt == 1].epa.mean(), 3), "rush_epa": round(o[o.rush_attempt == 1].epa.mean(), 3),
            "def_sack_rate": round(sacks / max(db, 1), 3), "turnover_diff": int(to_for - to_ag), "qbs": qbs.reset_index().to_dict("records")}
lg_rank = {}
allteams = sorted(p.posteam.dropna().unique())
E2 = {tm: eff(tm) for tm in allteams}
for k in ("off_epa_play", "def_epa_play", "margin_pg"):
    s = pd.Series({tm: E2[tm][k] for tm in allteams}); asc = k == "def_epa_play"
    for tm in ("LA", "ARI"): E2[tm][k + "_rank"] = int(s.rank(ascending=asc if k == "def_epa_play" else False)[tm])
print("\nLA:", json.dumps(E2["LA"], default=str)); print("ARI:", json.dumps(E2["ARI"], default=str))
OUT["LA_eff"], OUT["ARI_eff"] = E2["LA"], E2["ARI"]
# LA pass rush leaders
rush = p[(p.defteam == "LA") & (p.sack == 1)]
sk = pd.concat([rush.sack_player_name, rush.half_sack_1_player_name, rush.half_sack_2_player_name]).value_counts().head(5)
print("LA sacks by player:", sk.to_dict()); OUT["LA_sacks"] = sk.to_dict()
(H / "deepdives.json").write_text(json.dumps(OUT, indent=1, default=str))

#!/usr/bin/env python3
"""Blitz team database builder (Rico ask Nov 3 2026 00:03 ET). Data work only - lives in teams/ (not tools/, so the door code_hash is untouched).
Inputs (public): sources/nflverse/{pbp_2026.csv.gz, roster_weekly_2026.csv.gz, snap_counts_2026.csv.gz}, sources/sharp_2026-11-03/*.csv,
repo seeds: defenders/<T>_secondary.md, playlogs/archetype_vs_defense_2026.csv, runs/2026-11-02_CHI@SEA_r3/live/*_defender_log.csv.
Outputs: teams/defense/<T>.md, teams/offense/<T>.md, teams/defense/defense_db.csv, teams/offense/offense_db.csv, teams/<T>.json (door TEAM_FILES path teams/{team}.json).
ALL per-defender numbers are TACKLER/PBU TAGS, NOT TRUE COVERAGE (nflverse names tacklers and pass defenders, never the coverage defender)."""
import os, re, json, glob
from datetime import datetime
import pandas as pd, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = f"{ROOT}/sources/nflverse"; SH = f"{ROOT}/sources/sharp_2026-11-03"
LBL = "tackler/PBU tag, not true coverage"
MAP = {"LA": "LAR", "WAS": "WSH"}
def T(x): return MAP.get(x, x) if isinstance(x, str) else x
SHARP_NAMES = {"Arizona Cardinals":"ARI","Atlanta Falcons":"ATL","Baltimore Ravens":"BAL","Buffalo Bills":"BUF","Carolina Panthers":"CAR","Chicago Bears":"CHI","Cincinnati Bengals":"CIN","Cleveland Browns":"CLE","Dallas Cowboys":"DAL","Denver Broncos":"DEN","Detroit Lions":"DET","Green Bay Packers":"GB","Houston Texans":"HOU","Indianapolis Colts":"IND","Jacksonville Jaguars":"JAX","Kansas City Chiefs":"KC","Las Vegas Raiders":"LV","Los Angeles Chargers":"LAC","Los Angeles Rams":"LAR","Miami Dolphins":"MIA","Minnesota Vikings":"MIN","New England Patriots":"NE","New Orleans Saints":"NO","New York Giants":"NYG","New York Jets":"NYJ","Philadelphia Eagles":"PHI","Pittsburgh Steelers":"PIT","San Francisco 49ers":"SF","Seattle Seahawks":"SEA","Tampa Bay Buccaneers":"TB","Tennessee Titans":"TEN","Washington Commanders":"WSH"}

pbp = pd.read_csv(f"{S}/pbp_2026.csv.gz", low_memory=False)
pbp = pbp[pbp.season_type == "REG"].copy()
for c in ["posteam", "defteam", "home_team", "away_team", "solo_tackle_1_team", "tackle_with_assist_1_team", "assist_tackle_1_team", "penalty_team"]:
    pbp[c] = pbp[c].map(T)
pbp["game"] = pbp.away_team + "@" + pbp.home_team
ros = pd.read_csv(f"{S}/roster_weekly_2026.csv.gz", low_memory=False)
ros = ros.sort_values("week")
POS = dict(zip(ros.gsis_id, ros.position)); DPOS = dict(zip(ros.gsis_id, ros.depth_chart_position)); FULL = dict(zip(ros.gsis_id, ros.full_name))
PFR2G = {k: v for k, v in zip(ros.pfr_id, ros.gsis_id) if isinstance(k, str)}
snaps = pd.read_csv(f"{S}/snap_counts_2026.csv.gz"); snaps["team"] = snaps.team.map(T)
snaps["gsis"] = snaps.pfr_player_id.map(PFR2G)
def dpos(pid):
    p = DPOS.get(pid)
    if p in ("FS", "SS", "S"): return "S"
    if p in ("ILB", "MLB", "OLB", "LB"): return "LB" if p != "OLB" else "OLB"
    if p in ("DE", "DT", "NT"): return "DL"
    return p if isinstance(p, str) else (POS.get(pid) or "?")
def opos(pid):
    p = POS.get(pid); d = DPOS.get(pid)
    if d == "FB": return "RB"
    return p if isinstance(p, str) else "?"

# ---------------- pass targets ----------------
P = pbp[(pbp.play_type == "pass") & (pbp.sack != 1) & pbp.receiver_player_id.notna()].copy()
P["rpos"] = P.receiver_player_id.map(opos)
P["rec_yds"] = np.where(P.complete_pass == 1, P.yards_gained, 0)
P["td"] = (P.pass_touchdown == 1).astype(int)
P["exp20"] = ((P.complete_pass == 1) & (P.yards_gained >= 20)).astype(int)
P["dpi"] = (P.penalty_type == "Defensive Pass Interference").astype(int)
P["airb"] = pd.cut(P.air_yards, [-99, 0, 9, 19, 99], labels=["behind_los", "short_1-9", "inter_10-19", "deep_20+"])
P["dd"] = P.pass_length.fillna("?") + "_" + P.pass_location.fillna("?")
def charge(r):
    """-> (defender_id, defender_name, kind) for the play. kind: tackler|pbu|int|dpi|unattributed."""
    if r.interception == 1 and isinstance(r.interception_player_id, str): return r.interception_player_id, r.interception_player_name, "int"
    if r.dpi == 1 and isinstance(r.penalty_player_id, str) and r.penalty_team == r.defteam: return r.penalty_player_id, r.penalty_player_name, "dpi"
    if r.complete_pass == 1:
        for a, b, t in (("solo_tackle_1_player_id", "solo_tackle_1_player_name", "solo_tackle_1_team"), ("tackle_with_assist_1_player_id", "tackle_with_assist_1_player_name", "tackle_with_assist_1_team"), ("assist_tackle_1_player_id", "assist_tackle_1_player_name", "assist_tackle_1_team")):
            if isinstance(r[a], str) and r[t] == r.defteam: return r[a], r[b], "tackler"
        return None, None, "unattributed"
    if isinstance(r.pass_defense_1_player_id, str): return r.pass_defense_1_player_id, r.pass_defense_1_player_name, "pbu"
    return None, None, "unattributed"
ch = P.apply(charge, axis=1, result_type="expand"); P["dfr_id"], P["dfr"], P["dkind"] = ch[0], ch[1], ch[2]
P["dfr_pos"] = P.dfr_id.map(lambda x: dpos(x) if isinstance(x, str) else None)
# receiver rank within team (season targets) -> WR1/WR2/WR3+/TE1/TE2+/RB
tg = P.groupby(["posteam", "receiver_player_id", "rpos"]).size().reset_index(name="n").sort_values("n", ascending=False)
RANK = {}
for (tm, pos), g in tg.groupby(["posteam", "rpos"]):
    for i, pid in enumerate(g.receiver_player_id): RANK[(tm, pid)] = (pos, i + 1)
def rtype(r):
    pos, k = RANK.get((r.posteam, r.receiver_player_id), (r.rpos, 9))
    if pos == "WR": return "WR1" if k == 1 else "WR2" if k == 2 else "WR3+"
    if pos == "TE": return "TE1" if k == 1 else "TE2+"
    if pos in ("RB", "FB"): return "RB"
    return "other"
P["rtype"] = P.apply(rtype, axis=1)
# receiver aDOT archetype (season)
adot = P.groupby("receiver_player_id").air_yards.mean()
P["arch"] = P.receiver_player_id.map(lambda x: "deep (aDOT 13+)" if adot.get(x, 0) >= 13 else "intermediate (aDOT 8-13)" if adot.get(x, 0) >= 8 else "short/YAC (aDOT <8)")

R = pbp[(pbp.play_type == "run") & pbp.rusher_player_id.notna()].copy()
R["rpos"] = R.rusher_player_id.map(opos); R["exp15"] = (R.yards_gained >= 15).astype(int)
GAMES = pbp.groupby("game_id").agg(game=("game", "first"), week=("week", "first"), date=("game_date", "first"), home=("home_team", "first"), away=("away_team", "first"), hs=("total_home_score", "max"), as_=("total_away_score", "max")).reset_index()
TEAMS = sorted(set(GAMES.home) | set(GAMES.away))
LG = P.groupby("rtype").agg(t=("play_id", "size"), y=("rec_yds", "sum")); LG["ypt"] = LG.y / LG.t
LGA = P.groupby("airb", observed=True).agg(t=("play_id", "size"), y=("rec_yds", "sum")); LGA["ypt"] = LGA.y / LGA.t
LGD = P.groupby("dd").agg(t=("play_id", "size"), y=("rec_yds", "sum")); LGD["ypt"] = LGD.y / LGD.t
LGARCH = P.groupby("arch").agg(t=("play_id", "size"), y=("rec_yds", "sum")); LGARCH["ypt"] = LGARCH.y / LGARCH.t
sharp = {}
for f in ("nfl-coverage-schemes", "nfl-coverage-stats-by-position", "nfl-defensive-tendencies"):
    for r in pd.read_csv(f"{SH}/{f}.csv").to_dict("records"):
        t = SHARP_NAMES.get(r.pop("Team")); sharp.setdefault(t, {}).update(r)
arch_seed = pd.read_csv(f"{ROOT}/playlogs/archetype_vs_defense_2026.csv")

def grp(df, key):
    g = df.groupby(key, observed=True).agg(tgt=("play_id", "size"), rec=("complete_pass", "sum"), yds=("rec_yds", "sum"), td=("td", "sum"), exp20=("exp20", "sum"))
    g["ypt"] = (g.yds / g.tgt).round(2); return g
def md_table(df, cols=None):
    df = df if cols is None else df[cols]
    h = "| " + " | ".join(str(c) for c in df.columns) + " |\n|" + "---|" * len(df.columns) + "\n"
    return h + "".join("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else (str(int(v)) if isinstance(v, (float, np.floating)) and float(v).is_integer() else f"{v:.2f}" if isinstance(v, (float, np.floating)) else str(v)) for v in row) + " |\n" for row in df.itertuples(index=False))

def seed_notes(t):
    f = f"{ROOT}/defenders/{t}_secondary.md"
    if not os.path.exists(f): return []
    out = [l.rstrip() for l in open(f) if re.match(r"^- .*(←|rec \d+|rush \d+)", l)]
    return out[:40]

def live_log(path, defteam):
    """Parse a live ESPN-text defender log: pass target -> depth/dir, tacklers, PBU."""
    rows = []
    for r in pd.read_csv(path).to_dict("records"):
        tx = str(r["text"])
        m = re.search(r"pass (incomplete )?(short|deep) (left|middle|right) to ([A-Z][\w.\-']+)", tx)
        if not m: continue
        yd = re.search(r"for (-?\d+) yards?|for no gain", tx); y = int(yd[1]) if yd and yd[1] else 0
        tk = re.findall(r"\(([^()]*)\)\s*(?:\[|$|\.|PENALTY|Penalty)", tx.replace("\n", " "))
        tk = [x for x in tk if not re.search(r"Shotgun|Huddle|\d+:\d+", x)]
        pbu = re.findall(r"\[([^\]]+)\]", tx)
        rows.append(dict(target=m[4].rstrip("."), depth=m[2], dir=m[3], complete=0 if m[1] or "INTERCEPTED" in tx else 1, yds=0 if m[1] else y,
                         tackler=(tk[-1].split(";")[0].strip() if tk and not m[1] else ""), pbu="; ".join(pbu), td=int("TOUCHDOWN" in tx), text=tx[:160]))
    return pd.DataFrame(rows)

defense_rows, offense_rows = [], []
built = datetime.now().strftime("%Y-%m-%d %H:%M ET")
nweeks = int(pbp.week.max())

for t in TEAMS:
    D = P[P.defteam == t]; DR = R[R.defteam == t]
    gms = GAMES[(GAMES.home == t) | (GAMES.away == t)].sort_values("week"); ng = len(gms)
    # ---------- per-defender ----------
    Dd = D[D.dfr_id.notna()]
    per = Dd.groupby(["dfr_id", "week", "game"]).agg(tags=("play_id", "size"), rec=("complete_pass", "sum"), yds=("rec_yds", "sum"), td=("td", "sum"), exp20=("exp20", "sum"),
                                                     pbu=("dkind", lambda x: (x == "pbu").sum()), ints=("dkind", lambda x: (x == "int").sum()), dpi=("dkind", lambda x: (x == "dpi").sum()),
                                                     receivers=("receiver_player_name", lambda x: ", ".join(f"{k}x{v}" for k, v in x.value_counts().items()))).reset_index()
    per["dpi_yds"] = per.apply(lambda r: D[(D.dfr_id == r.dfr_id) & (D.week == r.week) & (D.dkind == "dpi")].penalty_yards.sum(), axis=1)
    ss = per.groupby("dfr_id").agg(games=("week", "nunique"), tags=("tags", "sum"), rec=("rec", "sum"), yds=("yds", "sum"), td=("td", "sum"), exp20=("exp20", "sum"), pbu=("pbu", "sum"), ints=("ints", "sum"), dpi=("dpi", "sum")).reset_index()
    ss["pos"] = ss.dfr_id.map(dpos); ss["name"] = ss.dfr_id.map(lambda x: FULL.get(x, x))
    ss["short"] = ss.dfr_id.map(lambda x: Dd[Dd.dfr_id == x].dfr.iloc[0])
    ss["ypt"] = (ss.yds / ss.tags).round(2); ss["yds_pg"] = (ss.yds / ss.games).round(1); ss["tags_pg"] = (ss.tags / ss.games).round(1)
    # receivers by type against each defender (season)
    vs = Dd.groupby(["dfr_id", "rtype"]).agg(n=("play_id", "size"), y=("rec_yds", "sum"))
    ss["vs_types"] = ss.dfr_id.map(lambda x: ", ".join(f"{k}:{int(r.n)}t/{int(r.y)}y" for k, r in vs.loc[x].sort_values("y", ascending=False).iterrows()) if x in vs.index.get_level_values(0) else "")
    exb = Dd[Dd.exp20 == 1].groupby("dfr_id").apply(lambda g: "; ".join(f"wk{r.week} {r.receiver_player_name}({r.rtype}) {int(r.yards_gained)} {r.dd}" for r in g.itertuples()), include_groups=False)
    ss["explosives"] = ss.dfr_id.map(exb).fillna("")
    cov = ss[ss.pos.isin(["CB", "S", "DB"]) | ((ss.pos.isin(["LB", "OLB"])) & (ss.tags >= 6))].sort_values(["pos", "yds"], ascending=[True, False])
    # snaps for defenders
    dsn = snaps[(snaps.team == t) & (snaps.defense_snaps > 0)].groupby("gsis").agg(dsnap=("defense_snaps", "sum"), dpct=("defense_pct", "mean"), gp=("week", "nunique"))
    cov = cov.join(dsn, on="dfr_id")
    for r in cov.itertuples():
        defense_rows.append(dict(team=t, defender=r.name, short=r.short, gsis_id=r.dfr_id, pos=r.pos, scope="season", week="", game="", games=r.games, tags=r.tags, rec=r.rec, yds=r.yds, ypt=r.ypt, td=r.td, exp20=r.exp20, pbu=r.pbu, ints=r.ints, dpi=r.dpi,
                                 tags_pg=r.tags_pg, yds_pg=r.yds_pg, def_snap_pct=round(r.dpct * 100, 1) if r.dpct == r.dpct else "", receivers=r.vs_types, explosives=r.explosives, method=LBL))
    for r in per[per.dfr_id.isin(cov.dfr_id)].sort_values(["week", "yds"], ascending=[True, False]).itertuples():
        defense_rows.append(dict(team=t, defender=FULL.get(r.dfr_id, r.dfr_id), short=Dd[Dd.dfr_id == r.dfr_id].dfr.iloc[0], gsis_id=r.dfr_id, pos=dpos(r.dfr_id), scope="game", week=r.week, game=r.game, games=1, tags=r.tags, rec=r.rec, yds=r.yds,
                                 ypt=round(r.yds / r.tags, 2), td=r.td, exp20=r.exp20, pbu=r.pbu, ints=r.ints, dpi=r.dpi, tags_pg=r.tags, yds_pg=r.yds, def_snap_pct="", receivers=r.receivers, explosives="", method=LBL))
    # ---------- team-level allowed ----------
    by_type = grp(D, "rtype"); by_type["tgt_pg"] = (by_type.tgt / ng).round(1); by_type["yds_pg"] = (by_type.yds / ng).round(1); by_type["lg_ypt"] = LG.ypt.reindex(by_type.index).round(2); by_type["ypt_vs_lg"] = (by_type.ypt - by_type.lg_ypt).round(2)
    l4d = list(gms.game_id)[-4:]; by_type4 = grp(D[D.game_id.isin(l4d)], "rtype"); by_type4["lg_ypt"] = LG.ypt.reindex(by_type4.index).round(2); by_type4["ypt_vs_lg"] = (by_type4.ypt - by_type4.lg_ypt).round(2)
    by_air = grp(D, "airb"); by_air["lg_ypt"] = LGA.ypt.reindex(by_air.index).round(2); by_air["ypt_vs_lg"] = (by_air.ypt - by_air.lg_ypt).round(2)
    by_dd = grp(D, "dd"); by_dd["lg_ypt"] = LGD.ypt.reindex(by_dd.index).round(2); by_dd["ypt_vs_lg"] = (by_dd.ypt - by_dd.lg_ypt).round(2)
    by_arch = grp(D, "arch"); by_arch["lg_ypt"] = LGARCH.ypt.reindex(by_arch.index).round(2); by_arch["ypt_vs_lg"] = (by_arch.ypt - by_arch.lg_ypt).round(2)
    ex = D[D.exp20 == 1]; exr = DR[DR.exp15 == 1]
    ex_pos = ex.groupby("rpos").size().to_dict(); ex_dd = ex.groupby("dd").size().to_dict(); exr_pos = exr.groupby("rpos").size().to_dict()
    beats = []
    for lab, tab in (("type", by_type), ("depth", by_air), ("depth/direction", by_dd), ("receiver archetype", by_arch)):
        for k, r in tab.iterrows():
            if r.tgt >= 12 and r.ypt_vs_lg >= 1.5: beats.append(f"{lab} {k}: {r.ypt} YPT on {int(r.tgt)} tgts (league {r.lg_ypt}, +{r.ypt_vs_lg}), {int(r.exp20)} catches of 20+")
    holds = [f"{k}: {r.ypt} YPT on {int(r.tgt)} tgts (league {r.lg_ypt}, {r.ypt_vs_lg})" for k, r in by_type.iterrows() if r.tgt >= 12 and r.ypt_vs_lg <= -1.5]
    rush_type = DR.groupby("rpos").agg(car=("play_id", "size"), yds=("yards_gained", "sum"), exp15=("exp15", "sum")); rush_type["ypc"] = (rush_type.yds / rush_type.car).round(2); rush_type["yds_pg"] = (rush_type.yds / ng).round(1)
    # weekly who-beat-them
    weekly = []
    for g in gms.itertuples():
        Dg = D[D.game_id == g.game_id]; opp = g.away if g.home == t else g.home
        top = Dg.groupby(["receiver_player_name", "rtype", "arch"]).agg(tgt=("play_id", "size"), rec=("complete_pass", "sum"), yds=("rec_yds", "sum"), td=("td", "sum")).reset_index().sort_values("yds", ascending=False).head(4)
        big = [f"{r.receiver_player_name}({r.rtype}) {int(r.yards_gained)}y {r.dd}{' TD' if r.td else ''} - {r.dfr if isinstance(r.dfr, str) else 'no tackler named'} [{r.dkind}]" for r in Dg[Dg.exp20 == 1].itertuples()]
        bigr = [f"{r.rusher_player_name}({r.rpos}) {int(r.yards_gained)}y rush {r.run_location or ''} {r.run_gap or ''}".replace("nan", "").strip() for r in DR[(DR.game_id == g.game_id) & (DR.exp15 == 1)].itertuples()]
        weekly.append(dict(week=int(g.week), game=g.game, opp=opp, top=[f"{r.receiver_player_name} ({r.rtype}, {r.arch}) {int(r.rec)}/{int(r.tgt)} {int(r.yds)}y{' ' + str(int(r.td)) + 'TD' if r.td else ''}" for r in top.itertuples()], big_pass=big, big_rush=bigr,
                           pass_yds_allowed=int(Dg.rec_yds.sum()), unattributed_share=round((Dg.dkind == "unattributed").mean(), 2) if len(Dg) else None))
    sh = sharp.get(t, {})
    dj = dict(games=ng, sharp_thru_wk7_2026_10_29=sh, by_receiver_type=by_type.reset_index().to_dict("records"), by_receiver_type_last4=by_type4.reset_index().to_dict("records"), by_air_depth=by_air.reset_index().astype({"airb": str}).to_dict("records"),
              by_depth_direction=by_dd.reset_index().to_dict("records"), by_receiver_archetype=by_arch.reset_index().to_dict("records"), explosives_pass20_by_pos=ex_pos, explosives_pass20_by_depth_dir=ex_dd,
              explosives_rush15_by_pos=exr_pos, rush_allowed_by_pos=rush_type.reset_index().to_dict("records"), beaten_by=beats, holds=holds, weekly=weekly,
              defenders=cov.drop(columns=["dfr_id"]).assign(gsis_id=cov.dfr_id).replace({np.nan: None}).to_dict("records"), defender_label=LBL)

    # ---------- OFFENSE ----------
    O = P[P.posteam == t]; OR = R[R.posteam == t]; OA = pbp[(pbp.posteam == t)]
    last_g = gms.iloc[-1].game_id
    qbs_last = OA[(OA.game_id == last_g) & OA.passer_player_id.notna()].groupby(["passer_player_id", "passer_player_name"]).size().sort_values(ascending=False)
    qb_id, qb_name = qbs_last.index[0]
    qb_games = OA[(OA.passer_player_id == qb_id)].game_id.unique()
    l4 = [x for x in gms.game_id if x in set(qb_games)][-4:]
    l4team = list(gms.game_id)[-4:]
    Q4 = O[(O.game_id.isin(l4)) & (O.passer_player_id == qb_id)]
    share = Q4.groupby(["receiver_player_id", "receiver_player_name", "rpos"]).agg(tgt=("play_id", "size"), rec=("complete_pass", "sum"), yds=("rec_yds", "sum"), air=("air_yards", "sum"), deep=("air_yards", lambda x: (x >= 20).sum())).reset_index()
    share["share"] = (share.tgt / share.tgt.sum()).round(3); share = share.sort_values("tgt", ascending=False)
    perg = Q4.groupby(["receiver_player_id", "week"]).size().unstack(fill_value=0)
    share["by_week"] = share.receiver_player_id.map(lambda x: " ".join(f"w{w}:{int(v)}" for w, v in perg.loc[x].items()) if x in perg.index else "")
    # snaps last 4 team games
    osn = snaps[(snaps.team == t) & (snaps.game_id.isin(l4team))].groupby("gsis").agg(osnap_pct=("offense_pct", "mean"), sn_g=("week", "nunique"))
    share = share.join(osn, on="receiver_player_id")
    # deep (season, all QBs)
    deep = O[O.air_yards >= 20].groupby(["receiver_player_id", "receiver_player_name"]).agg(dtgt=("play_id", "size"), drec=("complete_pass", "sum"), dyds=("rec_yds", "sum"), dtd=("td", "sum")).reset_index().sort_values("dyds", ascending=False)
    # never looked at: skill players with >=40% offense snaps (last 4) and <5% of targets
    skill = snaps[(snaps.team == t) & (snaps.game_id.isin(l4team)) & snaps.position.isin(["WR", "TE", "RB", "FB"])].groupby(["gsis", "player", "position"]).agg(pct=("offense_pct", "mean"), g=("week", "nunique")).reset_index()
    tl4 = O[O.game_id.isin(l4team)].groupby("receiver_player_id").size(); tot = tl4.sum()
    skill["tgt"] = skill.gsis.map(tl4).fillna(0).astype(int); skill["share"] = (skill.tgt / tot).round(3)
    ghosts = skill[(skill.pct >= 0.40) & (skill.share < 0.05)].sort_values("pct", ascending=False)
    # backfield
    RB4 = OR[OR.game_id.isin(l4team) & OR.rpos.isin(["RB", "FB", "QB", "WR"]) & (OR.qb_kneel != 1)]
    cs = RB4.groupby(["week", "rusher_player_name", "rpos"]).size().reset_index(name="car")
    tot_w = RB4[RB4.rpos.isin(["RB", "FB"])].groupby("week").size()
    cs["rb_share"] = cs.apply(lambda r: round(r.car / tot_w.get(r.week, np.nan), 3) if r.rpos in ("RB", "FB") else None, axis=1)
    bf = cs.pivot_table(index=["rusher_player_name", "rpos"], columns="week", values="car", fill_value=0)
    bfs = cs[cs.rpos.isin(["RB", "FB"])].pivot_table(index="rusher_player_name", columns="week", values="rb_share")
    yr = OR[OR.game_id.isin(l4team)].groupby("rusher_player_name").agg(car=("play_id", "size"), yds=("yards_gained", "sum"), exp15=("exp15", "sum"))
    # run/pass by score
    N = OA[(OA.play_type.isin(["pass", "run"])) & (OA.qb_kneel != 1) & (OA.qb_spike != 1) & OA.down.isin([1, 2, 3])].copy()
    N["bucket"] = pd.cut(N.score_differential, [-99, -8, -1, 0, 7, 99], labels=["trail 8+", "trail 1-7", "tied", "lead 1-7", "lead 8+"])
    def rp(df):
        g = df.groupby("bucket", observed=False).agg(plays=("play_id", "size"), pass_rate=("pass", "mean"), proe=("pass_oe", "mean")); g["pass_rate"] = (g.pass_rate * 100).round(1); g["proe"] = g.proe.round(1); return g
    rps = rp(N); rpl4 = rp(N[N.game_id.isin(l4team)])
    q4lead = N[(N.qtr == 4) & (N.score_differential >= 8)]; q4lead_pr = round(q4lead["pass"].mean() * 100, 1) if len(q4lead) else None
    neutral = N[(N.score_differential.abs() <= 7) & (N.qtr <= 3) & N.down.isin([1, 2])]
    oj = dict(current_qb=qb_name, current_qb_id=qb_id, qb_games_last4=[GAMES.set_index("game_id").loc[x, "game"] for x in l4], last4_team_games=[GAMES.set_index("game_id").loc[x, "game"] for x in l4team],
              qb_target_order_last4=share.drop(columns=["receiver_player_id"]).assign(pid=share.receiver_player_id).replace({np.nan: None}).to_dict("records"),
              deep_20plus_air_season=deep.replace({np.nan: None}).to_dict("records"), never_looked_at=ghosts.replace({np.nan: None}).to_dict("records"),
              backfield_last4={"carries": {f"{a}|{b}": {int(k): int(v) for k, v in row.items()} for (a, b), row in bf.iterrows()}, "rb_carry_share": {a: {int(k): (None if v != v else round(float(v), 3)) for k, v in row.items()} for a, row in bfs.iterrows()}},
              run_pass_by_score_season=rps.reset_index().astype({"bucket": str}).replace({np.nan: None}).to_dict("records"), run_pass_by_score_last4=rpl4.reset_index().astype({"bucket": str}).replace({np.nan: None}).to_dict("records"),
              neutral_early_down_pass_rate=round(neutral["pass"].mean() * 100, 1) if len(neutral) else None, q4_lead8_pass_rate=q4lead_pr)
    for r in share.itertuples():
        offense_rows.append(dict(team=t, section="qb_target_order_last4", qb=qb_name, player=r.receiver_player_name, gsis_id=r.receiver_player_id, pos=r.rpos, rank=list(share.receiver_player_id).index(r.receiver_player_id) + 1, games=len(l4),
                                 tgt=r.tgt, share=r.share, rec=r.rec, yds=r.yds, deep_tgt=r.deep, aDOT=round(r.air / r.tgt, 1), by_week=r.by_week, snap_pct=round(r.osnap_pct * 100, 1) if r.osnap_pct == r.osnap_pct else "", carries="", carry_share="", flag=""))
    for r in deep.itertuples():
        offense_rows.append(dict(team=t, section="deep_20plus_air_season", qb="all", player=r.receiver_player_name, gsis_id=r.receiver_player_id, pos=opos(r.receiver_player_id), rank="", games=ng, tgt=r.dtgt, share="", rec=r.drec, yds=r.dyds, deep_tgt=r.dtgt, aDOT="", by_week="", snap_pct="", carries="", carry_share="", flag="wins deep" if r.drec >= 3 or r.dyds >= 100 else ""))
    for r in ghosts.itertuples():
        offense_rows.append(dict(team=t, section="never_looked_at_last4", qb=qb_name, player=r.player, gsis_id=r.gsis, pos=r.position, rank="", games=r.g, tgt=r.tgt, share=r.share, rec="", yds="", deep_tgt="", aDOT="", by_week="", snap_pct=round(r.pct * 100, 1), carries="", carry_share="", flag="40%+ snaps, <5% targets"))
    for (a, b), row in bf.iterrows():
        tc = int(row.sum()); shs = bfs.loc[a] if a in bfs.index else None
        offense_rows.append(dict(team=t, section="backfield_last4", qb=qb_name, player=a, gsis_id="", pos=b, rank="", games=len(l4team), tgt="", share="", rec="", yds=int(yr.yds.get(a, 0)), deep_tgt="", aDOT="", by_week=" ".join(f"w{int(k)}:{int(v)}" for k, v in row.items()),
                                 snap_pct="", carries=tc, carry_share=" ".join(f"w{int(k)}:{v:.0%}" for k, v in shs.items() if v == v) if shs is not None else "", flag=("60%+ RB carries in >=3 of last 4" if shs is not None and (shs >= 0.6).sum() >= 3 else ("under 60% (N1 do-not-play for rush overs)" if b in ("RB", "FB") else ""))))
    for k, r in rps.iterrows():
        offense_rows.append(dict(team=t, section="run_pass_by_score_season", qb="all", player=str(k), gsis_id="", pos="", rank="", games=ng, tgt=r.plays, share=r.pass_rate, rec="", yds="", deep_tgt="", aDOT="", by_week="", snap_pct="", carries="", carry_share="", flag=f"PROE {r.proe}"))

    # ---------- write JSON ----------
    tj = dict(team=t, built_at=built, builder="teams/build_team_db.py", season=2026, weeks_covered=sorted(int(w) for w in gms.week), games=[dict(week=int(g.week), game=g.game, date=g.date) for g in gms.itertuples()],
              sources=["nflverse pbp_2026 (github.com/nflverse/nflverse-data releases, updated 2026-11-03 07:59 ET)", "nflverse roster_weekly_2026 / snap_counts_2026", "Sharp Football Analysis coverage-schemes / coverage-by-position / defensive-tendencies (dateModified 2026-10-29 15:53 ET, thru wk7)"],
              defense=dj, offense=oj)
    json.dump(tj, open(f"{ROOT}/teams/{t}.json", "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))

    # ---------- write DEFENSE md ----------
    L = [f"# {t} DEFENSE - team database (built {built} by Blitz)", "",
         f"Games covered: {ng} ({', '.join(f'wk{int(g.week)} {g.game}' for g in gms.itertuples())}). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).",
         f"**Per-defender numbers are {LBL.upper()}.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).", "",
         "## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)", ""]
    if sh: L.append(f"Man {sh.get('Man Rate')}% / Zone {sh.get('Zone Rate')}% | MOF closed {sh.get('Middle Closed Rate')}% / MOF open {sh.get('Middle Open Rate')}% | Blitz {sh.get('Blitz Rate')}% | Light box {sh.get('Light Box Rate')}% / Heavy box {sh.get('Heavy Box Rate')}% | Sub package {sh.get('Sub Package Rate')}% | Sharp YPT allowed WR {sh.get('YPT Allowed WR')}, TE {sh.get('YPT Allowed TE')}, RB {sh.get('YPT Allowed RB')}, Outside {sh.get('YPT Allowed Outside')}, Slot {sh.get('YPT Allowed Slot')}")
    else: L.append("No Sharp row.")
    L += ["", "## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)", ""] + ([f"- {b}" for b in beats] or ["- nothing flagged"]) + ["", "Holds (-1.5 YPT or better): " + ("; ".join(holds) or "none"), "",
          "## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)", "", md_table(by_type.reset_index()),
          "## Last 4 games, by receiver type", "", md_table(by_type4.reset_index()),
          "## By air depth", "", md_table(by_air.reset_index()), "## By depth x direction (nflverse pass_length/pass_location)", "", md_table(by_dd.reset_index()),
          "## By receiver archetype (receiver's season aDOT)", "", md_table(by_arch.reset_index()),
          f"## Explosives allowed (rec 20+ / rush 15+), season", "", f"- Pass 20+ by position: {ex_pos} ({sum(ex_pos.values())} total, {sum(ex_pos.values())/ng:.1f}/g)", f"- Pass 20+ by depth/direction: {ex_dd}", f"- Rush 15+ by position: {exr_pos} ({sum(exr_pos.values())} total)", "",
          "## Rush allowed by ball-carrier position", "", md_table(rush_type.reset_index()),
          f"## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - {LBL}", "",
          md_table(cov.assign(dpct=(cov.dpct * 100).round(1)), ["name", "pos", "games", "dpct", "tags", "tags_pg", "rec", "yds", "yds_pg", "ypt", "td", "exp20", "pbu", "ints", "dpi"]).replace("| dpct |", "| def snap% |"),
          "### Receiver types charged to each defender / explosives charged", ""]
    L += [f"- **{r.name}** ({r.pos}): {r.vs_types}" + (f" | 20+: {r.explosives}" if r.explosives else "") for r in cov.itertuples()]
    L += ["", f"### Per game ({LBL})", ""]
    pg = per[per.dfr_id.isin(cov.dfr_id)].copy(); pg["name"] = pg.dfr_id.map(lambda x: FULL.get(x, x)); pg["pos"] = pg.dfr_id.map(dpos)
    L.append(md_table(pg.sort_values(["week", "yds"], ascending=[True, False]), ["week", "game", "name", "pos", "tags", "rec", "yds", "td", "exp20", "pbu", "ints", "dpi", "receivers"]))
    L += ["## Who beat them each week", ""]
    for w in weekly:
        L.append(f"**Wk{w['week']} {w['game']}** (vs {w['opp']} offense, {w['pass_yds_allowed']} rec yds allowed; {int((w['unattributed_share'] or 0)*100)}% of targets unattributed)")
        L.append("- Top receivers: " + "; ".join(w["top"]))
        if w["big_pass"]: L.append("- 20+ catches: " + "; ".join(w["big_pass"]))
        if w["big_rush"]: L.append("- 15+ runs: " + "; ".join(w["big_rush"]))
        L.append("")
    sn = seed_notes(t)
    if sn: L += [f"## Seed notes from defenders/{t}_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)", ""] + sn + [""]
    a = arch_seed[arch_seed.defense == t]
    if len(a): L += ["## Seed: playlogs/archetype_vs_defense_2026.csv rows", ""] + [f"- wk{r.week} {r.game}: {r.offense_player} ({r.archetype}) {r.result_line} | shell {r.coverage_shell} | {r.edge_reason} [{r.attribution_confidence}]" for r in a.itertuples()] + [""]
    LIVE = {"SEA": "sea_defender_log.csv", "CHI": "chi_defender_log.csv"}
    if t in LIVE:
        lv = live_log(f"{ROOT}/runs/2026-11-02_CHI@SEA_r3/live/{LIVE[t]}", t)
        if len(lv):
            L += [f"## MNF CHI@SEA live log (runs/2026-11-02_CHI@SEA_r3/live/{LIVE[t]}, ESPN text, {LBL})", "", "By target, depth x direction (tgt / catches / yds / tacklers / PBU):", ""]
            for (tg_, dpt, dr), g in lv.groupby(["target", "depth", "dir"]):
                L.append(f"- {tg_} {dpt} {dr}: {len(g)} tgt, {int(g.complete.sum())} rec, {int(g.yds.sum())} yds; tacklers: {', '.join(x for x in g.tackler if x) or '-'}; PBU: {', '.join(x for x in g.pbu if x) or '-'}")
            tk = lv[lv.tackler != ""].groupby("tackler").agg(n=("yds", "size"), y=("yds", "sum"), who=("target", lambda x: ", ".join(sorted(set(x)))))
            L += ["", "Tackler-after-catch totals: " + "; ".join(f"{k} {int(r.n)} rec/{int(r.y)}y ({r.who})" for k, r in tk.sort_values("y", ascending=False).iterrows()), ""]
    open(f"{ROOT}/teams/defense/{t}.md", "w").write("\n".join(L) + "\n")

    # ---------- write OFFENSE md ----------
    L = [f"# {t} OFFENSE - team database (built {built} by Blitz)", "", f"Source: nflverse 2026 pbp + snap counts (public). Games: {ng}.", "",
         f"## Current QB: {qb_name} (led pass attempts in latest game {GAMES.set_index('game_id').loc[last_g, 'game']})", f"QB's last {len(l4)} games: {', '.join(oj['qb_games_last4'])}" + ("" if l4 == l4team else f" | NOTE team's last 4 were {', '.join(oj['last4_team_games'])} (QB change)"), "",
         f"## {qb_name} target order, last {len(l4)} games (his targets only; share of his targets; includes RBs/TEs)", "",
         md_table(share.assign(snap=(share.osnap_pct * 100).round(1), aDOT=(share.air / share.tgt).round(1)), ["receiver_player_name", "rpos", "tgt", "share", "rec", "yds", "deep", "aDOT", "snap", "by_week"]).replace("| deep |", "| 20+air tgt |").replace("| snap |", "| off snap% |"),
         "## Who wins deep (season, air yards 20+, all QBs)", "", md_table(deep.head(8), ["receiver_player_name", "dtgt", "drec", "dyds", "dtd"]) if len(deep) else "none\n",
         "## Never gets looked at (last 4 team games: 40%+ offense snaps, under 5% of team targets)", "",
         md_table(ghosts.assign(pct=(ghosts.pct * 100).round(1)), ["player", "position", "g", "pct", "tgt", "share"]) if len(ghosts) else "none\n",
         "## Backfield carry split, last 4 team games (carries; RB share of RB carries)", "", md_table(bf.reset_index()) if len(bf) else "none\n",
         "RB carry share by week: " + "; ".join(f"{a} " + " ".join(f"w{int(k)}:{v:.0%}" for k, v in row.items() if v == v) for a, row in bfs.iterrows()), "",
         "Rule N1 (Rico Nov 2): a back under 60% of his team's carries is do-not-play on cards (shares above are of RB carries).", "",
         "## Run/pass by score (downs 1-3, no kneels/spikes; pass = dropback incl sacks/scrambles; PROE = nflverse pass_oe)", "", "Season:", "", md_table(rps.reset_index().astype({"bucket": str})), "Last 4 team games:", "", md_table(rpl4.reset_index().astype({"bucket": str})),
         f"Neutral (score within 7, Q1-3, 1st/2nd down) pass rate: {oj['neutral_early_down_pass_rate']}% | Q4 leading by 8+: {q4lead_pr}% pass", ""]
    open(f"{ROOT}/teams/offense/{t}.md", "w").write("\n".join(L) + "\n")

pd.DataFrame(defense_rows).to_csv(f"{ROOT}/teams/defense/defense_db.csv", index=False)
pd.DataFrame(offense_rows).to_csv(f"{ROOT}/teams/offense/offense_db.csv", index=False)
print("teams", len(TEAMS), "defense rows", len(defense_rows), "offense rows", len(offense_rows), "weeks", nweeks)

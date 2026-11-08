import pandas as pd, numpy as np, math
mine = pd.read_csv("penalty_plays_2026.csv"); tg = pd.read_csv("penalties_2026.csv")
bg = pd.read_csv("../penalties/penalties_2026.csv"); dk = pd.read_csv("../penalties/drive_killers_2026.csv")
out = []
# BetGuru counts accepted+no-play per team-game vs box & mine
b = bg[bg.status.isin(["accepted","no-play"])].groupby(["game_id","team"]).size().rename("bg_acc")
x = tg.set_index(["game_id","team"]).join(b).fillna({"bg_acc":0})
x["bg_vs_box"] = x.bg_acc - x.box_pen; x["mine_vs_bg"] = x.pbp_accepted_pen - x.bg_acc
out.append(f"BetGuru accepted+no-play total {int(x.bg_acc.sum())}, box total {int(x.box_pen.sum())}, mine {int(x.pbp_accepted_pen.sum())}")
out.append(f"sum |BetGuru - box| over team-games = {int(x.bg_vs_box.abs().sum())}; team-games off = {(x.bg_vs_box!=0).sum()}")
dis = x[x.mine_vs_bg != 0].reset_index()[["week","game_id","team","box_pen","pbp_accepted_pen","bg_acc"]]
dis.to_csv("xcheck_vs_betguru_by_game.csv", index=False)
out.append(f"team-games where mine != BetGuru: {len(dis)}")
# drive killers: accepted offensive (incl no-play) on drives not scoring
nonscore = ~mine.drive_outcome.fillna("").str.contains("TD|Touchdown|FG|Field Goal", case=False) | mine.drive_outcome.fillna("").str.contains("Missed|Blocked", case=False)
mine["drive_killer"] = (mine.status == "accepted") & (mine.side == "offense") & nonscore & (mine.drive_team == mine.team_penalized)
mk = mine[mine.drive_killer].groupby(["game_id","team_penalized"]).size().rename("mine_dk")
bk = dk.groupby(["game_id","team"]).size().rename("bg_dk"); bk.index.names = ["game_id","team_penalized"]
k = pd.concat([mk, bk], axis=1).fillna(0); k["diff"] = k.mine_dk - k.bg_dk
out.append(f"drive killers: mine {int(k.mine_dk.sum())}, BetGuru {int(k.bg_dk.sum())}, team-games differing {(k['diff']!=0).sum()}")
k[k["diff"]!=0].reset_index().to_csv("xcheck_drive_killers.csv", index=False)
mine.to_csv("penalty_plays_2026.csv", index=False)
# correlation (pbp QB comps/pass yds vs proxy prior-median+0.5)
pbp = pd.read_parquet("../runs/2026-11-01_shared_src/play_by_play_2026.parquet")
pa = pbp[(pbp.pass_attempt==1)&(pbp.sack!=1)&pbp.passer_player_id.notna()&(pbp.two_point_attempt!=1)]
q = pa.groupby(["week","game_id","posteam","passer_player_id"]).agg(att=("pass_attempt","sum"),cmp=("complete_pass","sum"),yds=("passing_yards","sum"),spread=("spread_line","first"),home=("home_team","first"),res=("result","first")).reset_index()
q = q.sort_values("att").groupby(["game_id","posteam"]).tail(1); q = q[q.att >= 15]
q["fav"] = np.where(q.posteam==q.home, q.spread>0, q.spread<0); q["margin"] = np.where(q.posteam==q.home, q.res, -q.res)
def line(pid, wk, col):
    v = q[(q.passer_player_id==pid)&(q.week<wk)][col]; return math.floor(v.median())+0.5 if len(v)>=2 else np.nan
for c in ("cmp","yds"): q[f"{c}_line"] = [line(p,w,c) for p,w in zip(q.passer_player_id,q.week)]
ab = {"LA":"LAR","WAS":"WSH"}; q["team"] = q.posteam.replace(ab)
tg["off_all"] = tg.off_pen  # accepted incl. pre-snap no-play
tg["presnap"] = tg.false_start + tg.illegal_form_shift_motion
tg["off_per60"] = tg.off_pen/tg.off_plays*60
m = q.merge(tg[["week","team","off_all","presnap","off_per60"]], on=["week","team"]).dropna(subset=["cmp_line"])
def pc(a,b,ctrl):
    X = np.column_stack([np.ones(len(ctrl)), ctrl]); r1 = a - X@np.linalg.lstsq(X,a,rcond=None)[0]; r2 = b - X@np.linalg.lstsq(X,b,rcond=None)[0]; return np.corrcoef(r1,r2)[0,1]
res = []
for c in ("cmp","yds"):
    d = m[f"{c}_line"].notna(); mm = m[d]; miss = (mm[c]-mm[f"{c}_line"]).values.astype(float); over = (mm[c]>mm[f"{c}_line"]).astype(float).values
    for pen in ("off_all","presnap","off_per60"):
        p = mm[pen].values.astype(float)
        res.append(dict(stat=c, pen=pen, n=len(mm), r_margin=np.corrcoef(p,miss)[0,1], r_hit=np.corrcoef(p,over)[0,1],
            partial_r_ctrl_fav_margin=pc(p,miss,np.column_stack([mm.fav.astype(float),mm.margin.astype(float)])), partial_r_ctrl_fav=pc(p,miss,mm.fav.astype(float).values)))
r = pd.DataFrame(res); r.to_csv("penalty_qb_corr.csv", index=False)
print("\n".join(out)); print(r.round(3).to_string())

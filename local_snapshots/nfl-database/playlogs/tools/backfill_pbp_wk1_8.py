#!/usr/bin/env python3
"""Backfill playlogs/2026_wk<N>/<AWAY>_<HOME>.csv + defender_ledger.csv rows from public nflverse 2026 pbp (Blitz, Nov 3 2026).
Skips games that already have a saved play log; ledger rows only for games not already in the ledger.
Defender columns = tackler/PBU tag from pbp, NOT coverage."""
import os, glob, csv
import pandas as pd, numpy as np
B = "/workspace/nfl-database"; MAP = {"LA": "LAR", "WAS": "WSH"}
T = lambda x: MAP.get(x, x) if isinstance(x, str) else x
p = pd.read_csv(f"{B}/sources/nflverse/pbp_2026.csv.gz", low_memory=False); p = p[p.season_type == "REG"]
ros = pd.read_csv(f"{B}/sources/nflverse/roster_weekly_2026.csv.gz", low_memory=False).sort_values("week")
FULL = dict(zip(ros.gsis_id, ros.full_name)); POS = dict(zip(ros.gsis_id, ros.position)); DPOS = dict(zip(ros.gsis_id, ros.depth_chart_position))
for c in ["posteam", "defteam", "home_team", "away_team", "solo_tackle_1_team", "tackle_with_assist_1_team", "assist_tackle_1_team", "penalty_team"]: p[c] = p[c].map(T)
have = {os.path.basename(f)[:-4] for f in glob.glob(f"{B}/playlogs/2026_wk*/*.csv")}
led = {r["game"] for r in csv.DictReader(open(f"{B}/defender_ledger.csv"))}
COLS = "game,off,defn,when,kind,tgt,fullname,pos,yds,depth,loc,tk,dfr,conf,src,x,pen,text,week,play_id,air_yards,td,down,ydstogo,score_diff,pbu,int_by".split(",")
SRC = "nflverse pbp 2026 (public; tackler/PBU tag, not coverage)"
def tk(r):
    for a, t in (("solo_tackle_1_player_name", "solo_tackle_1_team"), ("tackle_with_assist_1_player_name", "tackle_with_assist_1_team"), ("assist_tackle_1_player_name", "assist_tackle_1_team")):
        if isinstance(r[a], str) and r[t] == r.defteam: return r[a], r[a.replace("_name", "_id")]
    return "", None
newlog, newled, ledrows = [], [], []
for gid, g in p.groupby("game_id"):
    a, h, w, date = T(g.away_team.iloc[0]), T(g.home_team.iloc[0]), int(g.week.iloc[0]), g.game_date.iloc[0]
    key = f"{a}_{h}"; game = f"{a}@{h}"
    rows = []
    for r in g[g.play_type.isin(["pass", "run"]) & ((g.rusher_player_id.notna()) | (g.receiver_player_id.notna()))].itertuples():
        r = pd.Series(r._asdict())
        if r.play_type == "run": kind, pid, nm = "rush", r.rusher_player_id, r.rusher_player_name
        else:
            pid, nm = r.receiver_player_id, r.receiver_player_name
            kind = "int" if r.interception == 1 else "rec" if r.complete_pass == 1 else "inc"
        t_, tid = tk(r); pbu = r.pass_defense_1_player_name if isinstance(r.pass_defense_1_player_name, str) else ""
        intb = r.interception_player_name if isinstance(r.interception_player_name, str) else ""
        dfr, conf = (intb, "confirmed (INT)") if kind == "int" else (pbu, "confirmed (PBU named)") if pbu and kind == "inc" else (t_, "tackler-of-record") if t_ else ("", "unknown")
        pen = f"['{r.penalty_player_name}', '{r.penalty_type}']" if r.penalty == 1 and isinstance(r.penalty_type, str) else ""
        yds = r.yards_gained if kind in ("rush", "rec") else 0
        x = bool((kind == "rush" and yds >= 15) or (kind == "rec" and yds >= 20))
        rows.append(dict(game=game, off=r.posteam, defn=r.defteam, when=f"Q{int(r.qtr)} {r.time}", kind=kind, tgt=nm, fullname=FULL.get(pid, nm), pos=POS.get(pid, ""), yds=int(yds) if yds == yds else 0,
                         depth=r.pass_length if isinstance(r.pass_length, str) else "", loc=(r.pass_location if isinstance(r.pass_location, str) else "") if kind != "rush" else (r.run_location if isinstance(r.run_location, str) else ""),
                         tk=t_, dfr=dfr, conf=conf, src=SRC, x=x, pen=pen, text=r.desc, week=w, play_id=int(r.play_id), air_yards=r.air_yards if r.air_yards == r.air_yards else "", td=int(r.touchdown == 1),
                         down=int(r.down) if r.down == r.down else "", ydstogo=int(r.ydstogo) if r.ydstogo == r.ydstogo else "", score_diff=int(r.score_differential) if r.score_differential == r.score_differential else "", pbu=pbu, int_by=intb))
        if kind != "rush" and game not in led:
            did = None
            if kind == "rec" and t_: ledrows.append(dict(date=date, game=game, defender=t_, team=r.defteam, pos=DPOS.get(tid, ""), receiver=nm, rec=1, yds=int(yds), method="nflverse pbp tackler after catch (not coverage)" + ("; EXPL20" if x else "")))
            elif kind == "inc" and pbu: ledrows.append(dict(date=date, game=game, defender=pbu, team=r.defteam, pos=DPOS.get(r.pass_defense_1_player_id, ""), receiver=nm, rec=0, yds=0, method="nflverse pbp PBU on incompletion (not coverage)"))
            elif kind == "int" and intb: ledrows.append(dict(date=date, game=game, defender=intb, team=r.defteam, pos=DPOS.get(r.interception_player_id, ""), receiver=nm, rec=0, yds=0, method="nflverse pbp INT"))
            if r.penalty == 1 and r.penalty_type == "Defensive Pass Interference" and isinstance(r.penalty_player_name, str):
                ledrows.append(dict(date=date, game=game, defender=r.penalty_player_name, team=r.defteam, pos=DPOS.get(r.penalty_player_id, ""), receiver=nm, rec=0, yds=int(r.penalty_yards or 0), method="penalty on pass play: Defensive Pass Interference (nflverse pbp)"))
    if game not in led: newled.append(game)
    if key in have: continue
    os.makedirs(f"{B}/playlogs/2026_wk{w}", exist_ok=True)
    pd.DataFrame(rows, columns=COLS).to_csv(f"{B}/playlogs/2026_wk{w}/{key}.csv", index=False); newlog.append(f"wk{w} {key}")
with open(f"{B}/defender_ledger.csv", "a", newline="") as f:
    wr = csv.DictWriter(f, fieldnames="date,game,defender,team,pos,receiver,rec,yds,method".split(",")); [wr.writerow(x) for x in ledrows]
print(f"play logs written: {len(newlog)}"); print(" ".join(newlog)); print(f"ledger: {len(ledrows)} rows appended for {len(newled)} games not previously in ledger: {' '.join(newled)}")

# DEPRECATED 2026-11-03: use /workspace/nfl-database/tools/pull_odds.py (canonical). Kept for run reproducibility only.
"""Odds pull via The Odds API (documented public API; key from env, never printed). Week 9+ copy (2026-11-01 22:47 ET, SRC-4).
Books: fanduel (price of record), draftkings, pinnacle (no-vig comparison), prizepicks, underdog (pick'em lines).
SA-3 patch applied: events that already kicked off are dropped (tools/odds_pregame.pregame_events) and every row carries an
`inplay` flag (tools/odds_pregame.flag_inplay); rows quoted at/after kickoff or with unknown kickoff are written to
odds_<tag>_inplay_dropped.csv, never to odds_<tag>.csv. SRC-5: writes season/data_week/pulled_et to feed_stamps.json.
Usage: python3 pull_odds.py <tag> --start 2026-11-06T00:00:00Z --end 2026-11-06T06:00:00Z [--week 9] [--season 2026]"""
import os,sys,json,csv,urllib.request,datetime
sys.path.insert(0,"/workspace/nfl-database/tools"); import odds_pregame
HERE=os.path.dirname(os.path.abspath(__file__))
COLS=["game","book","market","player","side","point","price","last_update_utc","inplay"]
def arg(k,d=None): return sys.argv[sys.argv.index(k)+1] if k in sys.argv else d
def split_inplay(rows,commence):
    """rows: [game,book,market,player,side,point,price,last_update_utc]. Keep only rows flagged pregame (False)."""
    fl=odds_pregame.flag_inplay([{"game":r[0],"last_update_utc":r[7]} for r in rows],commence)
    keep=[r+[False] for r,f in zip(rows,fl) if f is False]; drop=[r+[f] for r,f in zip(rows,fl) if f is not False]
    return keep,drop
def stamp(path,name,**kw):
    p=os.path.join(HERE,"feed_stamps.json"); S=json.load(open(p)) if os.path.exists(p) else {}
    S[name]=dict(file=path,**kw); json.dump(S,open(p,"w"),indent=1)
def main():
    tag=sys.argv[1]; START,END=arg("--start"),arg("--end")
    if not START or not END: sys.exit("need --start/--end UTC slate window (no hard-coded dates)")
    WEEK,SEASON=int(arg("--week",9)),int(arg("--season",2026))
    K=os.environ["ODDS_API_KEY"]
    MK="player_pass_yds,player_pass_completions,player_rush_yds,player_receptions,player_reception_yds,player_rush_reception_yds,player_pass_yds_alternate,player_rush_yds_alternate,player_receptions_alternate,player_reception_yds_alternate,player_rush_reception_yds_alternate,player_sacks"
    BK="fanduel,draftkings,pinnacle,prizepicks,underdog"
    ev=json.load(open(os.path.join(HERE,"oddsapi_events.json")))
    SL=odds_pregame.pregame_events([e for e in ev if START<=e["commence_time"]<END])   # drop games already kicked off
    commence={f"{e['away_team']} @ {e['home_team']}":e["commence_time"] for e in ev}
    rows=[];now=datetime.datetime.now();meta={"pulled_et":f"{now:%Y-%m-%dT%H:%M}","season":SEASON,"data_week":WEEK,"events":[],"remaining":None}
    for e in SL:
        u=f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{e['id']}/odds?apiKey={K}&markets={MK}&bookmakers={BK}&oddsFormat=american"
        try:
            r=urllib.request.urlopen(u,timeout=30); d=json.load(r); meta["remaining"]=r.headers.get("x-requests-remaining")
        except Exception as ex:
            meta["events"].append({"id":e["id"],"err":str(ex).replace(K,"***")}); continue
        g=f"{e['away_team']} @ {e['home_team']}"; meta["events"].append({"id":e["id"],"game":g,"books":[b["key"] for b in d.get("bookmakers",[])]})
        for b in d.get("bookmakers",[]):
            for m in b["markets"]:
                for o in m["outcomes"]:
                    rows.append([g,b["key"],m["key"],o.get("description"),o.get("name"),o.get("point"),o.get("price"),m.get("last_update")])
    keep,drop=split_inplay(rows,commence); meta["inplay_dropped"]=len(drop)
    for fn,rr in ((f"odds_{tag}.csv",keep),(f"odds_{tag}_inplay_dropped.csv",drop)):
        with open(os.path.join(HERE,fn),"w",newline="") as f: w=csv.writer(f); w.writerow(COLS); w.writerows(rr)
    json.dump(meta,open(os.path.join(HERE,f"odds_{tag}_meta.json"),"w"),indent=1)
    stamp(os.path.join(HERE,f"odds_{tag}.csv"),"odds_props",category="odds_props",season=SEASON,data_week=WEEK,week_kind="label",pulled_et=meta["pulled_et"])
    open(os.path.join(HERE,"pull_log.txt"),"a").write(f"{now:%Y-%m-%d %H:%M} The Odds API event odds ({len(SL)} pregame events {START}..{END}, books {BK}) -> odds_{tag}.csv {len(keep)} rows ({len(drop)} in-play/unknown dropped), remaining {meta['remaining']}\n")
    print(len(SL),len(keep),len(drop),meta["remaining"])
if __name__=="__main__" and "--lib" not in sys.argv: main()

# DEPRECATED 2026-11-03: use /workspace/nfl-database/tools/pull_odds.py (canonical). Kept for run reproducibility only.
"""Odds pull via The Odds API (documented public API; key from env, never printed).
Books: fanduel (price of record), draftkings, pinnacle (no-vig comparison), prizepicks, underdog (pick'em lines).
Usage: python3 pull_odds.py <tag>  -> odds_<tag>.csv + odds_<tag>_meta.json"""
import os,sys,json,csv,urllib.request,datetime
tag=sys.argv[1]
K=os.environ["ODDS_API_KEY"]
MK="player_pass_yds,player_pass_completions,player_rush_yds,player_receptions,player_reception_yds,player_rush_reception_yds,player_pass_yds_alternate,player_rush_yds_alternate,player_receptions_alternate,player_reception_yds_alternate,player_rush_reception_yds_alternate"
BK="fanduel,draftkings,pinnacle,prizepicks,underdog"
ev=json.load(open("oddsapi_events.json"))
SUN=[e for e in ev if e["commence_time"][:10] in ("2026-11-01","2026-11-02") and not e["commence_time"].startswith("2026-11-02T0") or e["commence_time"]=="2026-11-02T01:20:00Z"]
SUN=[e for e in SUN if e["home_team"]!="Seattle Seahawks"]
rows=[];meta={"pulled_et":f"{datetime.datetime.now():%Y-%m-%dT%H:%M}","events":[],"remaining":None}
for e in SUN:
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
with open(f"odds_{tag}.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["game","book","market","player","side","point","price","last_update_utc"]); w.writerows(rows)
json.dump(meta,open(f"odds_{tag}_meta.json","w"),indent=1)
open("pull_log.txt","a").write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} The Odds API event odds ({len(SUN)} Sunday events, books {BK}) -> odds_{tag}.csv {len(rows)} rows, remaining {meta['remaining']}\n")
print(len(SUN),len(rows),meta["remaining"]); print([ (x.get('game'),x.get('books'),x.get('err')) for x in meta["events"]])

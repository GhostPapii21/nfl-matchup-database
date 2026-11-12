"""Game spreads/totals via The Odds API (key from env, never printed). Usage: python3 pull_lines.py <tag> -> lines_<tag>.json"""
import os,sys,json,urllib.request,datetime
tag=sys.argv[1]; K=os.environ["ODDS_API_KEY"]
u=f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds?apiKey={K}&regions=us,eu&markets=spreads,totals&bookmakers=fanduel,draftkings,pinnacle&oddsFormat=american"
try:
    r=urllib.request.urlopen(u,timeout=30); d=json.load(r); rem=r.headers.get("x-requests-remaining")
except Exception as ex: print("ERR",str(ex).replace(K,"***")); sys.exit(1)
out={"pulled_et":f"{datetime.datetime.now():%Y-%m-%dT%H:%M}","games":{}}
for e in d:
    g=f"{e['away_team']} @ {e['home_team']}"; out["games"][g]={b["key"]:{m["key"]:m["outcomes"] for m in b["markets"]} for b in e["bookmakers"]}; out["games"][g]["commence_time"]=e["commence_time"]
json.dump(out,open(f"lines_{tag}.json","w"),indent=1)
open("pull_log.txt","a").write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} The Odds API spreads/totals (fanduel,draftkings,pinnacle) -> lines_{tag}.json {len(out['games'])} games, remaining {rem}\n")
print(len(out["games"]),rem)

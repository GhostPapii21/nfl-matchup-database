import json,urllib.request,os
B="https://site.api.espn.com/apis/site/v2/sports/football/nfl/"
def g(u): return json.load(urllib.request.urlopen(u,timeout=30))
games=[]
for w in range(1,9):
    for e in g(B+f"scoreboard?seasontype=2&week={w}&dates=2026")['events']:
        if e['status']['type']['name']!='STATUS_FINAL': continue
        p=f"raw/{e['id']}.json"
        if not os.path.exists(p): json.dump(g(B+f"summary?event={e['id']}"),open(p,'w'))
        games.append((w,e['id']))
json.dump(games,open('raw/games.json','w')); print(len(games))

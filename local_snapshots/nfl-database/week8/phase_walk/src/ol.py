import json,urllib.request,glob,sys
def g(u): return json.load(urllib.request.urlopen(u,timeout=20))
teams=g('https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams')['sports'][0]['leagues'][0]['teams']
out={}
for t in teams:
    t=t['team'];ab=t['abbreviation']
    try:
        d=g(f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2026/teams/{t['id']}/depthcharts")
        five={}
        for it in d['items']:
            for k,pos in it['positions'].items():
                if k in('lt','lg','c','rg','rt'):
                    a=pos['athletes'][0]['athlete']['$ref']
                    five[k]=g(a.replace('http:','https:'))['displayName']
        out[ab]=five
    except Exception as e: out[ab]={'err':str(e)[:80]}
json.dump(out,open('espn_ol_depth.json','w'),indent=1);print(out)

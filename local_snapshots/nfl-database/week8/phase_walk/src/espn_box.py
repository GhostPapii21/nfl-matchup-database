import json,urllib.request,os
def g(u): return json.load(urllib.request.urlopen(u,timeout=20))
os.makedirs('espn_summary',exist_ok=True);out={}
for wk in range(1,9):
    sb=g(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week={wk}&dates=2026')
    for ev in sb['events']:
        if ev['status']['type']['state']!='post': continue
        p=f"espn_summary/{ev['id']}.json"
        s=json.load(open(p)) if os.path.exists(p) else g(f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={ev['id']}")
        json.dump(s,open(p,'w'))
        for t in s['boxscore'].get('players',[]):
            ab=t['team']['abbreviation']
            for cat in t['statistics']:
                if cat['name'] not in('receiving','rushing'):continue
                for a in cat['athletes']:
                    st=dict(zip(cat['keys'],a['stats']))
                    k=f"{a['athlete']['displayName']}|{wk}"
                    r=out.setdefault(k,{'team':ab,'event':ev['id']})
                    if cat['name']=='receiving': r.update(tg=int(st.get('receivingTargets',0)),rec=int(st.get('receptions',0)),ryd=int(st.get('receivingYards',0)))
                    else: r.update(car=int(st.get('rushingAttempts',0)),rush=int(st.get('rushingYards',0)))
json.dump(out,open('espn_box.json','w'));print(len(out))

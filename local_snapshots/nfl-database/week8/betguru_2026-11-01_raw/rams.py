import json,urllib.request,re
def g(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))
s=g("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/14/schedule?season=2026")
evs=[(e['id'],e['date'],e['name']) for e in s['events'] if e['competitions'][0]['status']['type']['completed']]
out=[]
for eid,d,n in evs[-4:]:
  sm=g(f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}")
  box={}
  for t in sm['boxscore']['players']:
    if t['team']['abbreviation']!='LAR':continue
    for cat in t['statistics']:
      if cat['name'] in('rushing','receiving'):
        for a in cat['athletes']:
          nm=a['athlete']['displayName']
          if nm in('Blake Corum','Kyren Williams'): box.setdefault(nm,{})[cat['name']]=dict(zip(cat['labels'],a['stats']))
  # first offensive series RB touches
  first=[];cnt={'Corum':0,'Williams':0};rz={'Corum':0,'Williams':0}
  drives=sm.get('drives',{}).get('previous',[])
  lar=[dr for dr in drives if dr.get('team',{}).get('abbreviation')=='LAR']
  for i,dr in enumerate(lar):
    for p in dr.get('plays',[]):
      t=p.get('text','')
      for k in cnt:
        if re.search(r'\b[BK]\.\s?'+k,t) and ('left' in t or 'right' in t or 'middle' in t or 'pass' in t):
          if i==0: first.append(t[:90])
  fd=[p['text'][:100] for p in (lar[0]['plays'] if lar else [])][:6]
  out.append((n,d,box,fd))
for o in out:
  print('\n==',o[0],o[1]);print(json.dumps(o[2]));print(' first LAR drive:');[print('  ',x) for x in o[3]]

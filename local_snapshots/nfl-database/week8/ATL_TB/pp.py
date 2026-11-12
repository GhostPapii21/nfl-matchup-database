import json,glob,collections
d=[x for x in json.load(open('raw/dropbacks.json')) if x['off']=='ATL' and x['qb']=='M.Penix' and not x['nul']]
P=['D.London','Bi.Robinson','K.Pitts']
def dist(dd):
  try: return int(dd.split('&')[1])
  except: return 0
rows=collections.defaultdict(lambda: collections.Counter())
for x in d:
  pr = bool(x['hit']) or 'pressure' in x['t'].lower()
  tl = x['down']==3 and dist(x['dd'])>=7
  k=(x['wk'],x['g'])
  rows[k]['db']+=1; rows[k]['prdb']+=pr or x['kind']!='target'
  if x['kind']!='target': continue
  for tag,flag in (('PR',pr),('CL',not pr),('3D',x['down']==3),('3L',tl),('AL',True)):
    if not flag: continue
    rows[k][tag+'tgt']+=1
    for p in P:
      if x['rcv']==p:
        rows[k][tag+p+'t']+=1
        if x['res'] in('rec','TD'): rows[k][tag+p+'r']+=1; rows[k][tag+p+'y']+=x['yds']
tot=collections.Counter()
for k in sorted(rows):
  r=rows[k]; tot+=r
  print(k,'db',r['db'],'pressDB(sack/scr/hit)',r['prdb'],'PRtgt',r['PRtgt'],'CLtgt',r['CLtgt'],'3Dtgt',r['3Dtgt'],'3Ltgt',r['3Ltgt'])
  for tag in('AL','PR','CL','3D','3L'): print('  ',tag,' | '.join(f"{p} {r[tag+p+'t']}-{r[tag+p+'r']}-{r[tag+p+'y']}" for p in P))
print('TOT',dict((a,tot[a]) for a in['db','prdb','PRtgt','CLtgt','3Dtgt','3Ltgt']))
for tag in('AL','PR','CL','3D','3L'): print('  ',tag,' | '.join(f"{p} {tot[tag+p+'t']}-{tot[tag+p+'r']}-{tot[tag+p+'y']} ({100*tot[tag+p+'t']/max(1,tot[tag+'tgt']):.0f}%)" for p in P))
# receivers seen
print(collections.Counter(x['rcv'] for x in d if x['kind']=='target').most_common(8))
for f in glob.glob('raw/summary_*.json'):
  s=json.load(open(f));c=s['header']['competitions'][0]
  if 'ATL' not in [t['team']['abbreviation'] for t in c['competitors']] or not s.get('boxscore'): continue
  sc=' '.join(f"{t['team']['abbreviation']} {t.get('score')}" for t in c['competitors'])
  for tm in s['boxscore'].get('players',[]):
    if tm['team']['abbreviation']!='ATL':continue
    for st in tm['statistics']:
      if st['name']=='passing':
        for a in st['athletes']: print(s['header']['week'],c['date'][:10],sc,a['athlete']['displayName'],a['stats'])

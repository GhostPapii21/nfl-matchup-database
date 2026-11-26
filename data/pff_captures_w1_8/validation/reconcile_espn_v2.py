import json,glob,re,os,pandas as pd
src=open('reconcile_v2.py').read().split('res=[];quar=[]')[0]
src=src.replace("pbp=pd.read_csv","pbp=None and pd.read_csv").replace("src_meta={","src_meta=None and {").replace("G=pbp.groupby","G=None and pbp.groupby").replace("key={(r.week","key=None and {(r.week").replace("reg=pbp[","reg=None and pbp[")
src=src.replace('(side,nk(name))','(side,fk(name))').replace("('away',nk(qa))","('away',fk(qa))").replace("('home',nk(qh))","('home',fk(qh))")
exec(src)
E2N={'LAR':'LA','WSH':'WAS'}
ret=open('espn_raw/retrieved_at.txt').read().strip()
esp={}
for f in glob.glob('espn_raw/sum_*.json'):
  j=json.load(open(f));c=j['header']['competitions'][0];eid=os.path.basename(f)[4:-5]
  t={x['homeAway']:E2N.get(x['team']['abbreviation'],x['team']['abbreviation']) for x in c['competitors']}
  sc={x['homeAway']:x.get('score') for x in c['competitors']}
  wk=j['header'].get('week');P={}
  for tp in j['boxscore'].get('players',[]):
    tm=E2N.get(tp['team']['abbreviation'],tp['team']['abbreviation'])
    for s in tp['statistics']:
      if s['name'] not in('passing','rushing','receiving'):continue
      for a in s['athletes']:
        nm=a['athlete']['displayName'];d=dict(zip(s['labels'],a['stats']));r=P.setdefault((tm,fk(nm)),{'name':nm,'espn_athlete_id':a['athlete'].get('id')})
        def n(x):
          try: return float(x)
          except: return None
        if s['name']=='passing':
          ca=d['C/ATT'].split('/');r.update(pass_cmp=n(ca[0]),pass_att=n(ca[1]),pass_yds=n(d['YDS']),pass_td=n(d['TD']),pass_int=n(d['INT']))
        if s['name']=='rushing': r.update(rush_att=n(d['CAR']),rush_yds=n(d['YDS']),rush_td=n(d['TD']))
        if s['name']=='receiving': r.update(rec=n(d['REC']),rec_yds=n(d['YDS']),rec_td=n(d['TD']),tgt=n(d.get('TGTS')))
  esp[(wk,t['away'],t['home'])]=dict(eid=eid,date=c['date'],away_score=sc['away'],home_score=sc['home'],P=P,
     url=f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}',
     team_stats={E2N.get(tb['team']['abbreviation'],tb['team']['abbreviation']):{x['name']:x['displayValue'] for x in tb['statistics']} for tb in j['boxscore']['teams']})
nv=pd.read_csv('field_reconciliation_v2_nflverse.csv')
games=[];rows=[]
for f in sorted(glob.glob(f'{B}/week0*/games/*_accessible-recap-text.txt')):
  w=int(f.split('week0')[1][0]);gid=os.path.basename(f)[:5];t=open(f,errors='replace').read();Pp=parse(t)
  a,h=NICK[Pp['away_nick']],NICK[Pp['home_nick']];e=esp.get((w,a,h))
  g=dict(pff_game_id=gid,week=w,away=a,home=h,pff_final=f"{Pp['away_pts']}-{Pp['home_pts']}")
  if not e: g['espn']='unmatched';games.append(g);continue
  g.update(espn_event_id=e['eid'],espn_url=e['url'],espn_retrieved_at=ret,espn_date_utc=e['date'],espn_final=f"{e['away_score']}-{e['home_score']}");g['final_match']=g['espn_final']==g['pff_final']
  games.append(g);side={'away':a,'home':h}
  # also PFF dup-name check: full name keys
  for (sd,k),pv in Pp['players'].items():
    tm=side[sd];full=fk(pv['pff_name'])
    er=e['P'].get((tm,full))
    if er is None: # try nk
      c=[v for (tt,kk),v in e['P'].items() if tt==tm and nk(v['name'])==k];er=c[0] if len(c)==1 else None
    for fld,v in pv.items():
      if fld in('pff_name','collision'):continue
      r=dict(pff_game_id=gid,espn_event_id=e['eid'],team=tm,player_pff=pv['pff_name'],field=fld,pff=v,parser_collision=pv.get('collision'))
      if er is None:
        r.update(espn=None,espn_status='match' if v==0 else 'unverifiable',espn_note='no ESPN row' )
      else:
        ev=er.get(fld)
        if ev is None: ev=0.0 if fld in('rec','rec_yds','rec_td','tgt','rush_att','rush_yds','rush_td') else None
        r.update(player_espn=er['name'],espn_athlete_id=er['espn_athlete_id'],espn=ev)
        r['espn_status']='unverifiable' if ev is None else ('match' if abs(ev-v)<.01 else 'mismatch')
      rows.append(r)
E=pd.DataFrame(rows)
m=E.merge(nv.drop_duplicates(['pff_game_id','team','player_pff','field'])[['pff_game_id','team','player_pff','field','nflverse','status']].rename(columns={'status':'nflverse_status'}).astype({'pff_game_id':str}),on=['pff_game_id','team','player_pff','field'],how='left')
m.to_csv('field_reconciliation_v2_espn.csv',index=False)
json.dump(games,open('games_reconciliation_v2_espn.json','w'),indent=1)
# team totals exact-definition comparison: PFF overview "Total net yards","Total first downs","Total offensive plays"
print(len(games),sum(1 for g in games if g.get('final_match')),[ (g['pff_game_id'],g['pff_final'],g.get('espn_final')) for g in games if not g.get('final_match')])
print(m.groupby(['field','espn_status']).size().unstack(fill_value=0))
print(pd.crosstab(m.nflverse_status,m.espn_status))

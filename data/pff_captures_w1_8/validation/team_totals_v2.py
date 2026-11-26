import json,glob,os,re,pandas as pd
E2N={'LAR':'LA','WSH':'WAS'}
G={g['pff_game_id']:g for g in json.load(open('games_reconciliation_v2_espn.json'))}
snp=pd.read_csv('/workspace/nfl-database/sources/nflverse/snap_counts_2026.csv.gz')
nvg={g['pff_game_id']:g for g in json.load(open('games_reconciliation.json'))['games']}
fmap={'Total offensive plays':'totalOffensivePlays','Total net yards':'totalYards','Total first downs':'firstDowns','Rushing first downs':'firstDownsRushing','Passing first downs':'firstDownsPassing','Penalty first downs':'firstDownsPenalty','Total rushing plays':'rushingAttempts','Net yards rushing':'rushingYards'}
rows=[]
for f in sorted(glob.glob('../week0*/games/*_accessible-recap-text.txt')):
  gid=os.path.basename(f)[:5];g=G[gid];L=[l.strip() for l in open(f,errors='replace') if l.strip()]
  j=json.load(open(f"espn_raw/sum_{g['espn_event_id']}.json"));ts={E2N.get(t['team']['abbreviation'],t['team']['abbreviation']):{x['name']:x['displayValue'] for x in t['statistics']} for t in j['boxscore']['teams']}
  for lab,ek in fmap.items():
    if lab not in L: continue
    i=L.index(lab);va,vh=L[i+2],L[i+4]
    for side,v in(('away',va),('home',vh)):
      tm=g[side];e=ts.get(tm,{}).get(ek)
      try: pv=float(v);ev=float(e)
      except: rows.append(dict(pff_game_id=gid,team=tm,field=ek,pff=v,espn=e,status='unverifiable'));continue
      rows.append(dict(pff_game_id=gid,team=tm,field=ek,pff=pv,espn=ev,status='match' if pv==ev else 'mismatch'))
  # snap ceiling vs ESPN plays (diagnostic)
  nid=nvg[gid].get('nflverse_game_id')
  for side in('away','home'):
    tm=g[side];pfr=snp[(snp.game_id==nid)&(snp.team==tm)].offense_snaps.max()
    rows.append(dict(pff_game_id=gid,team=tm,field='diag_pfr_max_offense_snaps_vs_espn_plays',pff=None,espn=float(ts[tm]['totalOffensivePlays']),nflverse=pfr,status='diagnostic'))
d=pd.DataFrame(rows);d.to_csv('team_totals_v2_espn.csv',index=False)
print(d[d.status!='diagnostic'].groupby(['field','status']).size().unstack(fill_value=0))

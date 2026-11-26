import re,glob,json,csv,os,hashlib,datetime,unicodedata
import pandas as pd
B='/workspace/research/nfl_backfill_2026-11-06/pff';S='/workspace/nfl-database/sources/nflverse'
NICK={'CARDINALS':'ARI','FALCONS':'ATL','RAVENS':'BAL','BILLS':'BUF','PANTHERS':'CAR','BEARS':'CHI','BENGALS':'CIN','BROWNS':'CLE','COWBOYS':'DAL','BRONCOS':'DEN','LIONS':'DET','PACKERS':'GB','TEXANS':'HOU','COLTS':'IND','JAGUARS':'JAX','CHIEFS':'KC','RAIDERS':'LV','CHARGERS':'LAC','RAMS':'LA','DOLPHINS':'MIA','VIKINGS':'MIN','PATRIOTS':'NE','SAINTS':'NO','GIANTS':'NYG','JETS':'NYJ','EAGLES':'PHI','STEELERS':'PIT','49ERS':'SF','SEAHAWKS':'SEA','BUCCANEERS':'TB','TITANS':'TEN','COMMANDERS':'WAS'}
def nk(n):
  n=unicodedata.normalize('NFKD',n).encode('ascii','ignore').decode().lower().replace('.',' ').replace("'",'')
  t=[x for x in re.split(r'[\s\-]+',n) if x and x not in('jr','sr','ii','iii','iv','v')]
  return (t[0][0]+'_'+t[-1]) if len(t)>1 else n
pbp=pd.read_csv(f'{S}/pbp_2026.csv.gz',low_memory=False);snaps=pd.read_csv(f'{S}/snap_counts_2026.csv.gz')
src_meta={f:dict(sha256=hashlib.sha256(open(f'{S}/{f}','rb').read()).hexdigest(),mtime_et=datetime.datetime.fromtimestamp(os.path.getmtime(f'{S}/{f}')).isoformat()) for f in['pbp_2026.csv.gz','snap_counts_2026.csv.gz']}
G=pbp.groupby('game_id').agg(week=('week','max'),date=('game_date','first'),home=('home_team','first'),away=('away_team','first'),hs=('total_home_score','max'),as_=('total_away_score','max')).reset_index()
key={(r.week,r.away,r.home):r for r in G.itertuples()}
reg=pbp[(pbp.two_point_attempt!=1)&(pbp.play_type!='no_play')]
def agg_players(gid):
  d=reg[reg.game_id==gid];P={}
  def add(team,name,f,v):
    if not isinstance(name,str): return
    P.setdefault((team,nk(name)),{'src_name':name}).setdefault(f,0);P[(team,nk(name))][f]+=v
  for r in d[(d.pass_attempt==1)&(d.sack!=1)].itertuples():
    add(r.posteam,r.passer_player_name,'pass_att',1);add(r.posteam,r.passer_player_name,'pass_cmp',int(r.complete_pass==1))
    add(r.posteam,r.passer_player_name,'pass_yds',r.passing_yards if r.passing_yards==r.passing_yards else 0)
    add(r.posteam,r.passer_player_name,'pass_td',int(r.pass_touchdown==1));add(r.posteam,r.passer_player_name,'pass_int',int(r.interception==1))
    if isinstance(r.receiver_player_name,str):
      add(r.posteam,r.receiver_player_name,'tgt',1);add(r.posteam,r.receiver_player_name,'rec',int(r.complete_pass==1))
      add(r.posteam,r.receiver_player_name,'rec_yds',r.receiving_yards if r.receiving_yards==r.receiving_yards else 0);add(r.posteam,r.receiver_player_name,'rec_td',int(r.pass_touchdown==1))
  for r in d[d.rush_attempt==1].itertuples():
    add(r.posteam,r.rusher_player_name,'rush_att',1);add(r.posteam,r.rusher_player_name,'rush_yds',r.rushing_yards if r.rushing_yards==r.rushing_yards else 0);add(r.posteam,r.rusher_player_name,'rush_td',int(r.rush_touchdown==1))
  ints=[dict(defteam=r.defteam,player=r.interception_player_name,return_yards=r.return_yards) for r in d[d.interception==1].itertuples()]
  return P,ints
def fk(n):
  n=unicodedata.normalize('NFKD',n).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'')
  return ' '.join(x for x in re.split(r'[\s\-]+',n) if x and x not in('jr','sr','ii','iii','iv','v'))
def val(x):
  try: return float(x.replace('%',''))
  except: return None
def parse(t):
  L=[l.strip() for l in t.splitlines() if l.strip()];out={'players':{},'snaps':{}}
  out['away_nick'],out['away_pts'],out['home_pts'],out['home_nick']=L[1],L[2],L[4],L[5]
  # QB box
  i=L.index('DROPBACKS') if 'DROPBACKS' in L else None
  if i:
    q=max(k for k in range(i) if L[k]=='Quarterback Comparison');qa,qh=L[q+1],L[q+3];seq=L[i-1:i+20];lab={'ATTEMPTS':'pass_att','COMPLETIONS':'pass_cmp','PASSING YARDS':'pass_yds','TOUCHDOWNS':'pass_td','INTERCEPTIONS':'pass_int'}
    for j,l in enumerate(seq):
      if l in lab: out['players'].setdefault(('away',nk(qa)),{'pff_name':qa})[lab[l]]=val(seq[j-1]);out['players'].setdefault(('home',nk(qh)),{'pff_name':qh})[lab[l]]=val(seq[j+1])
  # box score rushing/receiving (v2: split by card markers)
  bs=t[t.find('Box Score Breakdown'):]
  cards=re.split(r'\n\d+ / 12\n',bs)
  for cd in cards:
    LL=[x.strip() for x in cd.split('\n') if x.strip()]
    hi=next((i for i,x in enumerate(LL[:4]) if re.fullmatch(r'.+ - (Rushing|Receiving)',x)),None)
    if hi is None: continue
    team,kind=LL[hi].rsplit(' - ',1);side='away' if team.upper()==out['away_nick'] else 'home' if team.upper()==out['home_nick'] else '?'
    body=LL[hi+2:];starts=[j for j in range(len(body)-4) if re.fullmatch(r'[A-Z]{1,4}',body[j+1]) and re.fullmatch(r'[A-Z]{1,3}',body[j+2]) and re.fullmatch(r'-?\d+',body[j+3]) and body[j+4] in('RUSH YDS','REC YDS')]
    for si,j in enumerate(starts):
      end=starts[si+1] if si+1<len(starts) else len(body);seg=body[j:end];name=seg[0]
      rec=out['players'].setdefault((side,nk(name)),{'pff_name':name})
      if rec['pff_name']!=name: rec['collision']=rec.get('collision','')+name
      rec['rush_yds' if kind=='Rushing' else 'rec_yds']=val(seg[3])
      mp={'Rushing':{'ATT':'rush_att','RUN TD':'rush_td'},'Receiving':{'REC':'rec','TGT':'tgt','REC TD':'rec_td'}}[kind]
      for k in range(5,len(seg)-1):
        if seg[k] in mp and mp[seg[k]] not in rec: rec[mp[seg[k]]]=val(seg[k+1])
  # snaps
  sp=t[t.find('Player Participation'):t.find('Initial PFF Grades')]
  for m in re.finditer(r'(\S[^\n]*) - (Offense|Defense)\n(\d+) PLAYERS\n(.*?)(?=\n\S[^\n]* \S (?:Offense|Defense) participation)',sp,re.S):
    team,unit=m.group(1),m.group(2);side='away' if team.upper()==out['away_nick'] else 'home' if team.upper()==out['home_nick'] else '?'
    LL=[x.strip() for x in re.split(r'\n[^\n]* participation\n|\nInitial PFF',m.group(4))[0].split('\n') if x.strip()];rows=[(LL[j-1],LL[j],LL[j+1]) for j in range(1,len(LL)-1) if re.fullmatch(r'[A-Z]{1,4}',LL[j]) and re.fullmatch(r'\d+',LL[j+1])]
    out['snaps'][(side,unit)]=dict(declared=int(m.group(3)),rows={fk(n):int(s) for n,p,s in rows},nrows=len(rows))
  return out
res=[];quar=[];games=[]
for f in sorted(glob.glob(f'{B}/week0*/games/*_accessible-recap-text.txt')):
  w=int(f.split('week0')[1][0]);gid=os.path.basename(f)[:5];t=open(f,errors='replace').read()
  meta=json.load(open(glob.glob(f'{B}/week0{w}/games/{gid}_*metadata.json')[0]))
  P=parse(t);a,h=NICK.get(P['away_nick']),NICK.get(P['home_nick']);g=key.get((w,a,h))
  rec=dict(pff_game_id=gid,week=w,pff_url=meta.get('source_url'),pff_retrieved_at_et=meta.get('retrieved_at_et'),pff_title=meta.get('page_title'),away=a,home=h,pff_final=f"{P['away_pts']}-{P['home_pts']}")
  if not g: rec['join']='unmatched';quar.append(dict(pff_game_id=gid,reason='no nflverse game for week/teams'));games.append(rec);continue
  title_date=re.search(r'\((\w+ \d+, \d{4})\)',meta.get('page_title',''));td=datetime.datetime.strptime(title_date.group(1),'%b %d, %Y').date().isoformat() if title_date else None
  rec.update(nflverse_game_id=g.game_id,nflverse_date=g.date,pff_title_date=td,date_match=(td==g.date),nflverse_final=f'{int(g.as_)}-{int(g.hs)}',join='week+team_abbrev(high)')
  rec['final_match']=rec['nflverse_final']==rec['pff_final']
  if not rec['final_match']: quar.append(dict(pff_game_id=gid,reason=f"final pff {rec['pff_final']} vs nflverse {rec['nflverse_final']}"))
  NP,ints=agg_players(g.game_id);rec['nflverse_interceptions']=ints
  side={'away':a,'home':h}
  for (sd,k),pv in P['players'].items():
    team=side.get(sd);nv=NP.get((team,k))
    for fld,v in pv.items():
      if fld in('pff_name','collision'): continue
      r=dict(pff_game_id=gid,nflverse_game_id=g.game_id,team=team,player_pff=pv['pff_name'],field=fld,pff=v)
      if 'collision' in pv: r.update(status='unverifiable',reason='ambiguous name key '+pv['collision'])
      elif team is not None and nv is None and v==0: r.update(nflverse=0,status='match',reason='pff zero; no nflverse event row')
      elif team is None or nv is None: r.update(status='unverifiable',reason='no nflverse player match (name key/team)')
      else:
        r.update(player_nflverse=nv['src_name'],nflverse=nv.get(fld,0));dd=abs((r['nflverse'] or 0)-(v or 0));r['abs_diff']=dd;r['status']='match' if dd<0.01 else ('within_1' if dd<=1.01 else 'mismatch')
      res.append(r)
  sn=snaps[snaps.game_id==g.game_id];sk={(r.team,fk(r.player)):(r.offense_snaps,r.defense_snaps) for r in sn.itertuples()}
  for (sd,unit),d in P['snaps'].items():
    team=side.get(sd);rec.setdefault('snap_units',{})[f'{team}_{unit}']=dict(declared=d['declared'],parsed=d['nrows'])
    if d['declared']!=d['nrows']: quar.append(dict(pff_game_id=gid,reason=f'snap rows parsed {d["nrows"]} vs declared {d["declared"]} {team} {unit}'))
    for k,v in d['rows'].items():
      x=sk.get((team,k));r=dict(pff_game_id=gid,nflverse_game_id=g.game_id,team=team,player_pff=k,field=f'{unit.lower()}_snaps',pff=v)
      if x is None: r.update(status='unverifiable',reason='no PFR snap row match')
      else: nvv=x[0] if unit=='Offense' else x[1];r.update(nflverse=nvv,abs_diff=abs(nvv-v),status='match' if nvv==v else ('within_1' if abs(nvv-v)<=1 else 'mismatch'))
      res.append(r)
  games.append(rec)
json.dump(dict(sources=src_meta,games=games),open('games_reconciliation_v2_nflverse.json','w'),indent=1,default=str)
pd.DataFrame(res).to_csv('field_reconciliation_v2_nflverse.csv',index=False);json.dump(quar,open('quarantine_auto_v2.json','w'),indent=1)
df=pd.DataFrame(res);print(len(games),sum(1 for x in games if x.get('final_match')),sum(1 for x in games if x.get('date_match')))
print(df.groupby(['field','status']).size().unstack(fill_value=0))

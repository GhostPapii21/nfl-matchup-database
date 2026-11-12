"""BetGuru Week 8 three-groups builder. Seeds fixed; rebuild: python3 build_legs.py"""
import sqlite3,json,csv,re,os,math,urllib.request
import numpy as np
from collections import defaultdict
W8='/workspace/nfl-database/week8'
c=sqlite3.connect('/workspace/nfl-database/fixes/fixes.sqlite')
FD=list(csv.DictReader(open(W8+'/three_groups/fd_now.csv')))
FDTS=open(W8+'/three_groups/fd_pulled_at.txt').read()
# game meta: (opp, spread for team (neg=fav), total, outdoor, defense file, kickoff, venue latlon)
G={'BAL':('BUF',3,54.5,1,'BAL_at_BUF','18:00',(42.774,-78.787)),'BUF':('BAL',-3,54.5,1,'BAL_at_BUF','18:00',(42.774,-78.787)),
'TEN':('CIN',12.5,46.5,1,'TEN_at_CIN','18:00',(39.095,-84.516)),'CIN':('TEN',-12.5,46.5,1,'TEN_at_CIN','18:00',(39.095,-84.516)),
'ARI':('DAL',7,54.5,0,'ARI_at_DAL','18:00',None),'DAL':('ARI',-7,54.5,0,'ARI_at_DAL','18:00',None),
'MIN':('DET',3,46.5,0,'MIN_at_DET','18:00',None),'DET':('MIN',-3,46.5,0,'MIN_at_DET','18:00',None),
'LV':('NYJ',1.5,45.5,1,'LV_at_NYJ','18:00',(40.813,-74.074)),'NYJ':('LV',-1.5,45.5,1,'LV_at_NYJ','18:00',(40.813,-74.074)),
'CLE':('PIT',3.5,39.5,1,'CLE_at_PIT','18:00',(40.447,-80.016)),'PIT':('CLE',-3.5,39.5,1,'CLE_at_PIT','18:00',(40.447,-80.016)),
'ATL':('TB',2.5,44.5,1,'ATL_at_TB','18:00',(27.976,-82.503)),'TB':('ATL',-2.5,44.5,1,'ATL_at_TB','18:00',(27.976,-82.503)),
'IND':('JAX',10,46.5,1,'IND_at_JAX','18:00',(30.324,-81.637)),'JAX':('IND',-10,46.5,1,'IND_at_JAX','18:00',(30.324,-81.637)),
'LAC':('LA',6.5,45.5,0,'LAC_at_LAR','21:05',None),'LA':('LAC',-6.5,45.5,0,'LAC_at_LAR','21:05',None),
'KC':('DEN',-1.5,40.5,1,'KC_at_DEN','21:25',(39.744,-105.020)),'DEN':('KC',1.5,40.5,1,'KC_at_DEN','21:25',(39.744,-105.020)),
'NE':('MIA',-7,43.5,1,'NE_at_MIA','21:25',(25.958,-80.239)),'MIA':('NE',7,43.5,1,'NE_at_MIA','21:25',(25.958,-80.239)),
'PHI':('WAS',6,40.5,1,'PHI_at_WSH','01:20',(38.908,-76.865)),'WAS':('PHI',-6,40.5,1,'PHI_at_WSH','01:20',(38.908,-76.865))}
DEFABBR={'LA':'LA','WAS':'WSH'}
# Questionable/out (injury_sweep_2026-11-01.md + Sat practice_watch)
Q={'George Pickens','Jaylen Waddle','Calvin Ridley','Breece Hall','Jakobi Meyers','Khalil Shakir'} 
OUT={'A.J. Brown','DeVonta Smith','Emeka Egbuka','Carnell Tate','Tyjae Spears','RJ Harvey','Brian Robinson Jr.','KaVontae Turpin','TreVeyon Henderson'}
INJ=json.load(open(W8+'/injuries.json')) if os.path.exists(W8+'/injuries.json') else {}
# candidates: (player, team, pos, market)
CANDS=[('Puka Nacua','LA','WR','rec'),('Puka Nacua','LA','WR','recyds'),('Amon-Ra St. Brown','DET','WR','rec'),('Amon-Ra St. Brown','DET','WR','recyds'),
('CeeDee Lamb','DAL','WR','recyds'),('CeeDee Lamb','DAL','WR','rec'),('Trey McBride','ARI','TE','rec'),('Trey McBride','ARI','TE','recyds'),
('Zay Flowers','BAL','WR','recyds'),('Zay Flowers','BAL','WR','rec'),('Drake London','ATL','WR','rec'),('Drake London','ATL','WR','recyds'),
('Brock Bowers','LV','TE','rec'),('Brock Bowers','LV','TE','recyds'),('Tee Higgins','CIN','WR','recyds'),('DK Metcalf','PIT','WR','recyds'),
('Garrett Wilson','NYJ','WR','recyds'),('Tyler Warren','IND','TE','recyds'),('Chris Godwin Jr.','TB','WR','rec'),('Justin Jefferson','MIN','WR','recyds'),
('Jahmyr Gibbs','DET','RB','rushrec'),('Jahmyr Gibbs','DET','RB','rushyds'),('James Cook','BUF','RB','rushrec'),('James Cook','BUF','RB','rushyds'),('Braelon Allen','NYJ','RB','rushrec'),
('Bijan Robinson','ATL','RB','rushrec'),('Bijan Robinson','ATL','RB','rushyds'),('Jonathan Taylor','IND','RB','rushyds'),('Jonathan Taylor','IND','RB','rushrec'),
('Kenneth Walker III','KC','RB','rushyds'),('Javonte Williams','DAL','RB','rushyds'),('Ashton Jeanty','LV','RB','rushrec'),('Jaylen Warren','PIT','RB','rushrec'),
('Kyren Williams','LA','RB','rushrec'),('Chase Brown','CIN','RB','rushrec'),('Tony Pollard','TEN','RB','rushrec'),('Aaron Jones','MIN','RB','rushyds'),
('Bucky Irving','TB','RB','rushrec'),('Braelon Allen','NYJ','RB','rushyds'),('Dallas Goedert','PHI','TE','rec'),('Parker Washington','JAX','WR','recyds')]
MK={'rec':('Receptions','Alt Receptions'),'recyds':('Receiving Yds','Alt Receiving Yds'),'rushyds':('Rushing Yds','Alt Rushing Yds'),'rushrec':('Rushing + Receiving Yds','Alt Rushing + Receiving Yds')}
FDN={'Chris Godwin Jr.':'Chris Godwin'}

# FULL SLATE: every FD player with a rec / rec yds / rush yds / rush+rec market, all 12 Sunday games
_ROLE={}
for p_,t_,pos_ in c.execute("select player,team,position from fix_player_role"): _ROLE.setdefault(p_,(t_,pos_))
_FDREV={'Chris Godwin':'Chris Godwin Jr.'}
_suf={'Alt Receptions':'rec','Total Receptions':'rec','Alt Receiving Yds':'recyds','Receiving Yds':'recyds','Alt Rushing Yds':'rushyds','Rushing Yds':'rushyds','Rushing + Receiving Yds':'rushrec','Alt Rushing + Receiving Yds':'rushrec'}
_seen=set();CANDS=[];NOROLE=[]
for r_ in FD:
  if ' - ' not in r_['market']: continue
  nm,suf=r_['market'].rsplit(' - ',1)
  if suf not in _suf: continue
  nm=_FDREV.get(nm,nm); k=(nm,_suf[suf])
  if k in _seen: continue
  _seen.add(k)
  cand=[n for n in _ROLE if n==nm or n.startswith(nm+' ') or n.replace(' Jr.','').replace(' Sr.','').replace(' III','').replace(' II','')==nm]
  if not cand: NOROLE.append(k); continue
  t_,pos_=_ROLE[cand[0]]
  if pos_ not in ('WR','TE','RB') or t_ not in G: continue
  if cand[0]!=nm: FDN[cand[0]]=nm
  CANDS.append((cand[0],t_,pos_,k[1]))
json.dump(NOROLE,open('full_norole.json','w'))
def ladder(p,m):
  p=FDN.get(p,p);main,alt=MK[m];out={};mainline=None
  for r in FD:
    mn=r['market']
    if mn==f'{p} - {alt}':
      x=re.search(r'(\d+)\+',r['runner'])
      if x and r['odds']: out[int(x.group(1))]=int(r['odds'])
    if mn in (f'{p} - {main}',f'{p} - Total {main}') and r['runner'].endswith('Over'): mainline=(float(r['hcp']),int(r['odds']))
  if not out and mainline: out={int(math.ceil(mainline[0])):mainline[1]}
  return out,mainline
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
# game logs from ESPN box (player_stats) joined to games date; plus nflverse usage
gdate={g:d for g,d in c.execute('select game_id,date from games')}
ESPNID={'James Cook':'4379399','Aaron Jones':'3042519','Braelon Allen':'4685247','Chris Godwin Jr.':'3116165'}
def logs(p):
  rows=defaultdict(dict)
  q=("select game_id,category,data from player_stats where player_id=? and category in('receiving','rushing')",(ESPNID[p],)) if p in ESPNID else ("select game_id,category,data from player_stats where player=? and category in('receiving','rushing')",(p,))
  for gid,cat,d in c.execute(*q):
    d=json.loads(d);rows[gid]['date']=gdate.get(gid,'')
    if cat=='receiving': rows[gid].update(tg=int(d.get('receivingTargets',0) or 0),rec=int(d['receptions']),ryd=int(d['receivingYards']))
    else: rows[gid].update(car=int(d['rushingAttempts']),rush=int(d['rushingYards']))
  L=sorted(rows.values(),key=lambda r:r['date'])
  for r in L:
    for k in('tg','rec','ryd','car','rush'): r.setdefault(k,0)
  return L
def usage(p,t):
  return [dict(zip(['week','snap','tg','car','team_tg','team_car'],r)) for r in c.execute("select week,offense_pct,targets,carries,team_targets,team_carries from fix_player_game_usage where full_name=? order by week",(p,))]
def role(p): 
  r=c.execute("select position,season_target_share,season_carry_share,current_target_share_l3,current_carry_share_l3,current_snap_pct_l3,targets_per_game,carries_per_game from fix_player_role where player=?",(p,)).fetchone()
  return dict(zip(['pos','tgt_share','car_share','tgt_share_l3','car_share_l3','snap_l3','tpg','cpg'],r)) if r else None
def defmd(team):
  opp=G[team][0];f=f"{W8}/defense/{G[team][4]}.md";txt=open(f).read()
  ab=DEFABBR.get(opp,opp)
  sec=re.split(r'\n## ',txt);s=[x for x in sec if x.startswith(f'{ab} DEFENSE') or x.startswith(f'{opp} DEFENSE') or (opp=='LA' and x.startswith('LA DEFENSE'))]
  s=s[0] if s else '';d={}
  for line in s.splitlines():
    m=re.match(r'\| (.+?) \| (.+?) \| (.*?) \|',line)
    if m: d[m.group(1)]=m.group(2)+(' (rank '+m.group(3)+')' if m.group(3).strip() else '')
  soft=re.findall(r'- \*\*(.+?)\*\*',s); hard=re.findall(r'### Hard spots\n((?:- .*\n?)*)',s)
  return d,soft,(hard[0].strip() if hard else ''),f
# PBP coverage proxy: defenders named as tackler/defender on completions/incompletions vs position group
abbr={}
for p,t,pos in c.execute('select player,team,position from fix_player_role'):
  parts=p.split(); 
  if len(parts)>=2: abbr[(t,parts[0][0]+'.'+parts[-1].replace('Jr.','').strip())]=pos
TEAMID={}
def defenders(team,pos):
  opp=G[team][0];stats=defaultdict(lambda:[0,0,0])
  for gid,off,data in c.execute("select game_id,offense_id,data from plays where play_type like 'Pass%'"):
    pass
  return None
def cov_proxy(opp,pos):
  # opponents of 'opp': plays where offense!=opp team and game involved opp
  gids=[g for g,d in c.execute("select game_id,data from games") if f'"abbreviation": "{ {"LA":"LAR","WAS":"WSH"}.get(opp,opp) }"' in d]
  st=defaultdict(lambda:[0,0,0])
  for gid in gids:
    for (data,) in c.execute("select data from plays where game_id=? and play_type in('Pass Reception','Pass Incompletion','Passing Touchdown')",(gid,)):
      t=json.loads(data).get('text','')
      m=re.search(r'pass \w+ \w+ to ([A-Z][a-z]?\.[A-Za-z\'\-]+)',t) or re.search(r'intended for ([A-Z][a-z]?\.[A-Za-z\'\-]+)',t)
      if not m: continue
      rp=None
      for (tm,ab),ps in abbr.items():
        if ab==m.group(1) and tm!=opp: rp=ps;break
      if rp!=pos: continue
      dm=re.search(r'\(([^)]+)\)',t.split(' to ',1)[-1])
      if not dm: continue
      dn=dm.group(1).split(';')[0].strip()
      y=re.search(r'for (-?\d+) yard',t); comp='incomplete' not in t
      st[dn][0]+=1; st[dn][1]+=comp; st[dn][2]+=int(y.group(1)) if (y and comp) else 0
  top=sorted(st.items(),key=lambda x:-x[1][0])[:3]
  return [dict(defender=k,plays=v[0],rec_allowed=v[1],yds_allowed=v[2]) for k,v in top]
def weather(team):
  g=G[team]
  if not g[3] or not g[6]: return 'indoor/roof (no weather factor)'
  lat,lon=g[6]
  try:
    u=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability&wind_speed_unit=mph&temperature_unit=fahrenheit&timezone=UTC&start_date=2026-11-01&end_date=2026-11-02"
    d=json.load(urllib.request.urlopen(u,timeout=20))['hourly']
    key=('2026-11-02T' if g[5]=='01:20' else '2026-11-01T')+g[5][:2]+':00'
    i=d['time'].index(key)
    return f"{d['temperature_2m'][i]:.0f}F, wind {d['wind_speed_10m'][i]:.0f} mph (gust {d['wind_gusts_10m'][i]:.0f}), precip {d['precipitation_probability'][i]}% @kick (Open-Meteo, pulled now)"
  except Exception as e: return f'MISSING (weather fetch failed: {e})'
# ---- three models, 100k each, fixed seeds ----
N=100000
def stat_of(r,m): return {'rec':r['rec'],'recyds':r['ryd'],'rushyds':r['rush'],'rushrec':r['rush']+r['ryd']}[m]
def vol_of(r,m): return r['tg'] if m in('rec','recyds') else (r['car'] if m=='rushyds' else r['car']+r['tg'])
def sims(L,m,line,spread,mf):
  last=L[-5:]; vols=np.array([vol_of(r,m) for r in last],float); vals=np.array([stat_of(r,m) for r in last],float)
  allv=np.array([vol_of(r,m) for r in L],float); allx=np.array([stat_of(r,m) for r in L],float)
  per=allx.sum()/max(allv.sum(),1); per_l5=vals.sum()/max(vols.sum(),1)
  # Model 1 Monte Carlo: NB volume (L5 mean, season var) x bootstrap per-opp efficiency
  r1=np.random.default_rng(101); mu=vols.mean()*mf; var=max(allv.var(),mu*1.1); pnb=mu/var; n=mu*pnb/(1-pnb)
  v=r1.negative_binomial(max(n,0.5),min(max(pnb,0.05),0.95),N)
  if m=='rec': cr=allx.sum()/max(allv.sum(),1); y=r1.binomial(v,min(cr,0.95))
  else:
    eff=r1.normal(per_l5*0.5+per*0.5, max(np.std(allx/np.maximum(allv,1)),0.8)/np.sqrt(np.maximum(v,1)),N); y=v*eff
  p1=(y>=line).mean(); med1=np.median(y)
  # Model 2 bias (Bayesian shrink): posterior mean = (season*k + L5*n)/(k+n), lognormal-ish with season CV; matchup factor mf
  r2=np.random.default_rng(202); prior=allx.mean(); k=4; post=(prior*k+vals.sum())/(k+len(vals))*mf
  cv=max(allx.std()/max(allx.mean(),1),0.25); sig=math.sqrt(math.log(1+cv**2))
  y2=r2.lognormal(math.log(max(post,0.5))-sig**2/2,sig,N)
  if m=='rec': y2=r2.poisson(post,N)
  p2=(y2>=line).mean(); med2=np.median(y2)
  # Model 3 game randomness: script states from spread (lead/trail/neutral) shift volume; 4% early exit (injury/ejection); blowout Q4 pull
  r3=np.random.default_rng(303); pl=1/(1+math.exp(spread/6.5))  # prob team leads
  st=r3.random(N); lead=st<pl
  rb = m in('rushyds','rushrec')
  shift=np.where(lead, 1.08 if rb else 0.94, 0.92 if rb else 1.08)
  blow=r3.random(N)< (0.10 if abs(spread)>=7 else 0.04); shift=shift*np.where(blow&lead,0.85,1.0)
  exitf=np.where(r3.random(N)<0.04, r3.uniform(0.1,0.7,N),1.0)
  base=r3.choice(allx[-6:],N)*0.5+r3.normal(post,max(allx.std(),1),N)*0.5
  y3=np.maximum(base*shift*exitf,0)
  if m=='rec': y3=np.round(y3)
  p3=(y3>=line).mean(); med3=np.median(y3)
  return dict(mc=dict(p=round(float(p1),4),median=round(float(med1),1),seed=101),bias=dict(p=round(float(p2),4),median=round(float(med2),1),seed=202),
              gr=dict(p=round(float(p3),4),median=round(float(med3),1),seed=303,p_team_leads=round(pl,3)),n=N)
def matchup_factor(d,pos,m):
  try:
    if m in('rushyds',): ypc=float(d['RB rush car / yds per g, YPC'].split(',')[1].split()[0]); return round(min(max(ypc/4.3,0.85),1.12),3)
    key={'WR':'WR tgt / rec / yds per g (pbp)','TE':'TE tgt / rec / yds per g','RB':'RB rush+rec yds per g'}[pos]
    v=d[key]; 
    if pos=='RB': return round(min(max(float(v.split()[0])/125,0.85),1.12),3)
    yds=float(v.split('/')[2].split()[0]); base={'WR':140,'TE':50}[pos]; return round(min(max(yds/base,0.85),1.12),3)
  except Exception: return 1.0
out=[];wx={}
for p,t,pos,m in CANDS:
  rec={'player':p,'team':t,'opp':G[t][0],'pos':pos,'market':m,'spread':G[t][1],'total':G[t][2]}
  rec['status']='OUT' if p in OUT else ('Q' if p in Q else 'active (not on report)')
  L=logs(p); U=usage(p,t); R=role(p); rec['logs_espn']=L[-5:]; rec['usage_nflverse']=U[-5:]; rec['role']=R
  lad,main=ladder(p,m); rec['fd_main']=main; rec['fd_ladder']=lad; rec['fd_pulled_at']=FDTS
  d,soft,hard,dfile=defmd(t); rec['opp_def']=d; rec['opp_soft']=soft; rec['opp_hard']=hard; rec['opp_def_src']=dfile
  if t not in wx: wx[t]=weather(t)
  rec['weather']=wx[t]
  rec['cov_proxy']=cov_proxy(G[t][0],pos if pos!='RB' else 'RB')
  mf=matchup_factor(d,pos,m); rec['matchup_factor']=mf
  if len(L)<4 or not lad: rec['cut']='no logs or no FD ladder'; out.append(rec); continue
  # choose mid rung: evaluate each rung, pick the one whose consensus p in [0.65,0.80] with best price & edge>=3pts over devig(4.5% vig)
  best=None;allr={}
  for ln,od in sorted(lad.items()):
    s=sims(L,m,ln,G[t][1],mf); cons=(s['mc']['p']+s['bias']['p']+s['gr']['p'])/3; fair=imp(od)/1.045
    allr[ln]=dict(odds=od,cons=round(cons,4),fair=round(fair,4),**{k:s[k]['p'] for k in('mc','bias','gr')})
    l4=sum(stat_of(r,m)>=ln for r in L[-4:])
    if 0.65<=cons<=0.82 and 0.03<=cons-fair<=0.15 and -300<=od<=-120 and l4>=3 and min(s['mc']['p'],s['bias']['p'],s['gr']['p'])>=0.60 and min(s['mc']['median'],s['bias']['median'],s['gr']['median'])>=ln:
      if best is None or od>best[1]: best=(ln,od,s,cons,fair)
  rec['rungs_eval']=allr
  if best:
    ln,od,s,cons,fair=best; rec.update(rung=ln,price=od,sims=s,cons=round(cons,4),fair_devig=round(fair,4))
    l5=[stat_of(r,m) for r in L[-4:]]; rec['l4_vals']=l5; rec['l4_hits']=sum(x>=ln for x in l5)
  else: rec['cut']='no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD'
  out.append(rec)
json.dump(out,open('legs_full.json','w'),indent=1,default=str)
for r in out:
  if r.get('rung'): json.dump(r,open(f"full_leg_{r['player'].replace(' ','_').replace('.','')}_{r['market']}.json",'w'),indent=1,default=str)
  print(r['player'],r['market'],r['status'],r.get('rung'),r.get('price'),r.get('cons'),r.get('fair_devig'),r.get('l4_hits'),r.get('cut',''))

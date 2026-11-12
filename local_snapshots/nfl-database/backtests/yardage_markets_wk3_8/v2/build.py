"""Offline inventory, pre-week features, training-only rule selection. No network imports."""
from pathlib import Path
import json,re,unicodedata,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
MARKETS={'player_rush_yds':'rushyds','player_reception_yds':'recyds','player_rush_reception_yds':'rushrecyds'}
def norm(s): return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())
def profit(price): return 10*price/100 if price>0 else 1000/-price
def summary(d,keys):
 if d.empty:return pd.DataFrame(columns=keys+['n','wins','losses','pushes','ungraded','hit_pct','pl','stake','roi'])
 x=d.groupby(keys,dropna=False).agg(n=('price','size'),wins=('result',lambda x:(x=='win').sum()),losses=('result',lambda x:(x=='loss').sum()),pushes=('result',lambda x:(x=='push').sum()),ungraded=('result',lambda x:(x=='ungraded').sum()),pl=('pl','sum'),stake=('stake','sum')).reset_index();x['hit_pct']=100*x.wins/(x.wins+x.losses);x['roi']=100*x.pl/x.stake;return x

def main():
 p=pd.read_parquet(ROOT/'runs/2026-11-02_shared_src/play_by_play_2026.parquet');p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)]
 gi=p.drop_duplicates('game_id'); ab=json.loads((ROOT/'backtests/rulebook_replay_wk6_8/abbr.json').read_text());ab.update({'LAR':'LA','WSH':'WAS'})
 players=pd.read_parquet(ROOT/'runs/2026-11-02_shared_src/players.parquet'); names={norm(r.display_name):r.gsis_id for r in players.itertuples()}
 # Saved metadata identity aliases only; no outcomes used.
 aliases={'Brian Robinson Jr.':'Brian Robinson','Chris Godwin':'Chris Godwin Jr.','Deebo Samuel':'Deebo Samuel Sr.','Lew Nichols':'Lew Nichols III','Michael Pittman Jr.':'Michael Pittman','Travis Etienne Jr.':'Travis Etienne','Drew Ogletree':'Andrew Ogletree','Joshua Palmer':'Josh Palmer','Pierre Strong Jr.':'Pierre Strong'}
 for alias,canonical in aliases.items():names[norm(alias)]=names[norm(canonical)]
 games={(str(r.game_date)[:10],r.away_team,r.home_team):r for r in gi.itertuples()}
 files=[]
 for root in ['backtests/rulebook_replay_wk6_8/raw','backtests/current_rules_wk6_8/raw','runs','week8','week9','backtests/yardage_markets_wk3_8/raw']:
  files+=sorted((ROOT/root).rglob('*.json'))
 quotes=[]; lines=[]; inventory=[]
 for f in files:
  try:j=json.loads(f.read_text())
  except (ValueError,UnicodeError):continue
  if not isinstance(j,dict):continue
  data=j.get('data',j); es=data if isinstance(data,list) else [data]
  for e in es:
   if not isinstance(e,dict) or 'commence_time' not in e:continue
   ko=e['commence_time'];a=ab.get(e.get('away_team'),e.get('away_team'));h=ab.get(e.get('home_team'),e.get('home_team'));g=games.get((ko[:10],a,h))
   # UTC after midnight corresponds to previous US game date.
   if g is None:
    date=str((pd.Timestamp(ko)-pd.Timedelta(hours=6)).date());g=games.get((date,a,h))
   if g is None or not 3<=g.week<=8:continue
   snap=j.get('timestamp') or j.get('snapshot_time')
   for b in e.get('bookmakers',[]):
    for m in b.get('markets',[]):
     ts=snap or m.get('last_update') or b.get('last_update'); valid=bool(ts and pd.Timestamp(ts)<=pd.Timestamp(ko))
     for o in m.get('outcomes',[]):
      if m['key'] in ('spreads','totals') and valid:lines.append(dict(game_id=g.game_id,snap=ts,book=b['key'],market=m['key'],name=ab.get(o['name'],o['name']),point=o.get('point')))
      mk=m['key']
      if mk not in MARKETS:continue
      inventory.append(dict(source=str(f.relative_to(ROOT)),week=g.week,key=m['key'],valid_prekick=valid))
      if not valid or o.get('point') is None or o.get('price') is None or o.get('price')==0 or o.get('name','').lower() not in ('over','under'):continue
      quotes.append(dict(week=g.week,game_id=g.game_id,game=f'{a}@{h}',player=o.get('description'),market=MARKETS[mk],side=o['name'].lower(),tier='alt' if m['key'].endswith('_alternate') else 'main',line=float(o['point']),price=float(o['price']),book=b['key'],snap=ts,kickoff=ko,source=str(f.relative_to(ROOT))))

 pd.DataFrame(inventory).to_csv(OUT/'source_inventory.csv',index=False)
 d=pd.DataFrame(quotes)
 d['player']=d.player.map(lambda name: norm(aliases.get(name,name)))
 key=['game_id','player','market','side','book']
 d=d.sort_values(['snap','source']).drop_duplicates(key,keep='last').reset_index(drop=True)
 coverage=[]
 for w in range(3,9):
  for mk in MARKETS.values():
   z=d[(d.week==w)&(d.market==mk)]
   coverage.append(dict(week=w,market=mk,events=z.game_id.nunique(),quotes=len(z),books=z.book.nunique(),book_names=';'.join(sorted(z.book.unique()))))
 pd.DataFrame(coverage).to_csv(OUT/'coverage.csv',index=False)
 pa=p[(p.pass_attempt==1)&(p.sack!=1)&p.receiver_player_id.notna()];ru=p[(p.rush_attempt==1)&p.rusher_player_id.notna()]
 statr=ru.groupby(['game_id','rusher_player_id']).rushing_yards.sum();statt=pa.groupby(['game_id','receiver_player_id']).receiving_yards.sum()
 gameindex=gi.set_index('game_id');ldf=pd.DataFrame(lines).drop_duplicates()
 sharp={}
 import io
 try:
  sh=pd.read_html(io.StringIO((OUT/'HINDSIGHT_sharp_oct27.html').read_text()))[0]
  sharp={ab.get(r['Team'],r['Team']):{'man':r['Man Rate'],'zone':r['Zone Rate']} for r in sh.to_dict('records')}
 except (FileNotFoundError,ValueError):pass
 histories={(w,t):z.game_id.unique() for w in range(3,9) for t,z in p[p.week<w].groupby('posteam')}
 defenses={(w,t):z.game_id.nunique() for w in range(3,9) for t,z in p[p.week<w].groupby('defteam')}
 carries={(w,t):z for w in range(3,9) for t,z in ru[ru.week<w].groupby('posteam')}
 targets={(w,t):z for w in range(3,9) for t,z in pa[pa.week<w].groupby('posteam')}
 allowedrush={(w,t):z for w in range(3,9) for t,z in ru[ru.week<w].groupby('defteam')}
 allowedrec={(w,t):z for w in range(3,9) for t,z in pa[pa.week<w].groupby('defteam')}
 rows=[];feature_cache={}
 for r in d.itertuples():
  feature_key=(r.week,r.game_id,r.player,r.market,r.snap)
  if feature_key in feature_cache:
   rows.append(feature_cache[feature_key]);continue
  pid=names.get(norm(r.player));g=gameindex.loc[r.game_id]
  participation=pd.concat([ru[(ru.week<r.week)&(ru.rusher_player_id==pid)][['week','posteam']],pa[(pa.week<r.week)&(pa.receiver_player_id==pid)][['week','posteam']]])
  participation=participation[participation.posteam.isin([g.home_team,g.away_team])].sort_values('week')
  team=participation.iloc[-1].posteam if len(participation) else None
  opp=g.home_team if team==g.away_team else g.away_team if team else None
  gids=histories.get((r.week,team),[]);n=len(gids)
  pr=carries.get((r.week,team),ru.iloc[:0]);pt=targets.get((r.week,team),pa.iloc[:0])
  dr=allowedrush.get((r.week,opp),ru.iloc[:0]);dt=allowedrec.get((r.week,opp),pa.iloc[:0]);dn=defenses.get((r.week,opp),0)
  def yards(gid):return float(statr.get((gid,pid),0))*(r.market!='recyds')+float(statt.get((gid,pid),0))*(r.market!='rushyds')
  ll=ldf[(ldf.game_id==r.game_id)&(ldf.snap<=r.snap)].sort_values('snap') if len(ldf) else ldf
  sp=ll[(ll.market=='spreads')&(ll.name==team)].drop_duplicates('book',keep='last').point.median() if len(ll) else np.nan
  tot=ll[(ll.market=='totals')&(ll.name=='Over')].drop_duplicates('book',keep='last').point.median() if len(ll) else np.nan
  rows.append(dict(gsis=pid,team=team,opp=opp,spread=sp,total=tot,implied_team_total=(tot-sp)/2,prior_games=n,prior_carry_share=(pr.rusher_player_id==pid).sum()/len(pr) if len(pr) else np.nan,prior_target_share=(pt.receiver_player_id==pid).sum()/len(pt) if len(pt) else np.nan,prior_yds_avg=np.mean([yards(x) for x in gids]) if n else np.nan,opp_prior_allowance=(dr.rushing_yards.sum()*(r.market!='recyds')+dt.receiving_yards.sum()*(r.market!='rushyds'))/dn if dn else np.nan,HINDSIGHT_sharp_man=sharp.get(opp,{}).get('man'),HINDSIGHT_sharp_zone=sharp.get(opp,{}).get('zone'),feature_cutoff=f'weeks<{r.week}'))
  feature_cache[feature_key]=rows[-1]
 d=pd.concat([d,pd.DataFrame(rows)],axis=1)
 d['model_edge']=np.where(d.side=='over',d.prior_yds_avg-d.line,d.line-d.prior_yds_avg)
 d.to_csv(OUT/'candidates.csv',index=False)
 legs=[]
 for keys,z in d.groupby(['week','player','market','side'],sort=True):
  line=z.line.median();at=z[z.line==line]
  # An even-count midpoint can be unquoted: retain it with no fabricated price.
  r=z.sort_values(['snap','source']).iloc[0].to_dict()
  r.update(line=line,price=at.price.median(),books_at_line=at.book.nunique(),quote_count=len(z),book='consensus',source=';'.join(sorted(z.source.unique())),snap=z.snap.min())
  r['model_edge']=(r['prior_yds_avg']-line)*(1 if r['side']=='over' else -1)
  r['candidate_id']=hashlib.sha256('|'.join(map(str,keys)).encode()).hexdigest()[:16]
  r['result_stat']=np.nan;r['result']='withheld';r['pl']=np.nan;r['stake']=np.nan
  if r['week']<=6:
   actual=(float(statr.get((r['game_id'],r['gsis']),0))*(r['market']!='recyds')+float(statt.get((r['game_id'],r['gsis']),0))*(r['market']!='rushyds')) if r['gsis'] and r['team'] else np.nan
   r['result_stat']=actual
   r['result']='ungraded' if pd.isna(actual) or pd.isna(r['price']) else 'push' if actual==line else 'win' if ((actual>line)==(r['side']=='over')) else 'loss'
   r['pl']=profit(r['price']) if r['result']=='win' else -10 if r['result']=='loss' else 0
   r['stake']=0 if r['result']=='ungraded' else 10
  legs.append(r)
 x=pd.DataFrame(legs);x.to_csv(OUT/'legs.csv',index=False)
 train=x[x.week<=6].copy();summary(train,['market','side']).to_csv(OUT/'grading_train.csv',index=False)
 traits=[]
 bins={'model_edge':[-np.inf,-15,0,5,10,15,20,np.inf],'line':[-np.inf,25,50,75,100,np.inf],'price':[-np.inf,-150,-110,0,150,np.inf],'prior_carry_share':[-np.inf,.1,.25,.5,.75,np.inf],'prior_target_share':[-np.inf,.1,.2,.3,np.inf],'spread':[-np.inf,-7,0,7,np.inf],'implied_team_total':[-np.inf,20,25,30,np.inf],'opp_prior_allowance':[-np.inf,100,150,200,250,np.inf]}
 for feature,b in bins.items():
  z=train.copy();z['bucket']=pd.cut(z[feature],b).astype(str);a=summary(z,['market','side','bucket']);a['feature']=feature;traits.append(a)
 t=pd.concat(traits);t.to_csv(OUT/'traits.csv',index=False)
 (OUT/'traits.md').write_text('# Weeks 3–6 traits only\n\nExploratory univariate splits; missing features are separate nan buckets. Hit% excludes pushes and ungraded; ROI uses settled $10 stakes. No holdout outcomes used.\n\n'+t.to_string(index=False)+'\n')
 locked=[]
 for (mk,side),z in train.groupby(['market','side']):
  opts=[]
  for threshold in [0,5,10,15,20]:
   q=z[(z.model_edge>=threshold)&(z.result.isin(['win','loss','push']))];a=summary(q,['market','side'])
   if len(q)>=30 and a.roi.iloc[0]>0:opts.append((float(a.roi.iloc[0]),len(q),threshold))
  if opts:
   roi,n,threshold=sorted(opts,key=lambda v:(-v[0],-v[1],v[2]))[0];locked.append(dict(market=mk,side=side,min_model_edge=threshold,train_n=n,train_roi=roi))
 config=dict(train_weeks=[3,4,5,6],rules=locked,variants={'baseline':{},'edgecap':{'max_model_edge':15}},sharp_hindsight={'over_man_min':30,'under_man_lt':30})
 (OUT/'locked_rules.json').write_text(json.dumps(config,indent=2)+'\n')
 (OUT/'RULES.md').write_text('# Train-only locked rules\n\nEach market-side searches model_edge >= 0,5,10,15,20. Keep highest ROI with >=30 graded legs and positive ROI; ties larger n then lower threshold. At most three conditions: market, side, minimum edge. Missing edge/price abstains. Edgecap is identical with model_edge <=15, pre-registered without refitting. Sharp is never used for fitting; ON is Oct27 HINDSIGHT only: over man>=30, under man<30; missing abstains.\n\n'+json.dumps(config,indent=2)+'\n')
 print('Stage A:',len(d),'main quotes;',len(x),'consensus legs;',len(locked),'kept train cells')
 print(summary(train,['market','side']).to_string(index=False))
 print('Weeks 7–8 outcomes withheld; grade.py not run.')
if __name__=='__main__':main()

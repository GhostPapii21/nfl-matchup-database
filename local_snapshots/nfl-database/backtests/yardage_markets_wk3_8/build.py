"""Offline inventory, pre-week features, training-only rule selection. No network imports."""
from pathlib import Path
import json,re,unicodedata,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
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
 games={(str(r.game_date)[:10],r.away_team,r.home_team):r for r in gi.itertuples()}
 files=[]
 for root in ['backtests/rulebook_replay_wk6_8/raw','backtests/current_rules_wk6_8/raw','runs','week8','week9']:
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
      mk=m['key'].removesuffix('_alternate')
      if mk not in MARKETS:continue
      inventory.append(dict(source=str(f.relative_to(ROOT)),week=g.week,key=m['key'],valid_prekick=valid))
      if not valid or o.get('point') is None or o.get('name','').lower() not in ('over','under'):continue
      quotes.append(dict(week=g.week,game_id=g.game_id,game=f'{a}@{h}',player=o.get('description'),market=MARKETS[mk],side=o['name'].lower(),tier='alt' if m['key'].endswith('_alternate') else 'main',line=float(o['point']),price=float(o['price']),book=b['key'],snap=ts,kickoff=ko,source=str(f.relative_to(ROOT))))
 pd.DataFrame(inventory).to_csv(OUT/'source_inventory.csv',index=False)
 d=pd.DataFrame(quotes); key=['game_id','player','market','side','tier','line','book'];d=d.sort_values(['snap','source']).drop_duplicates(key,keep='last').reset_index(drop=True)
 d['candidate_id']=[hashlib.sha256('|'.join(map(str,[r[k] for k in key])).encode()).hexdigest()[:16] for r in d.to_dict('records')]
 pa=p[(p.pass_attempt==1)&(p.sack!=1)&p.receiver_player_id.notna()];ru=p[(p.rush_attempt==1)&p.rusher_player_id.notna()]
 statr=ru.groupby(['game_id','rusher_player_id']).rushing_yards.sum();statt=pa.groupby(['game_id','receiver_player_id']).receiving_yards.sum()
 teammap={};
 for q,col in [(pa,'receiver_player_id'),(ru,'rusher_player_id')]:
  for r in q[['game_id',col,'posteam']].drop_duplicates().itertuples(index=False):teammap[(r[0],r[1])]=r[2]
 sharp={}
 try:
  import io
  sh=pd.read_html(io.StringIO(Path('/tmp/sharp.html').read_text()))[0]
  sharp={ab.get(r['Team'],r['Team']):{'man':r['Man Rate'],'zone':r['Zone Rate']} for r in sh.to_dict('records')}
 except (FileNotFoundError,ValueError):pass
 features=[]; ldf=pd.DataFrame(lines).drop_duplicates()
 linegroups={g:z for g,z in ldf.groupby("game_id")}
 gameindex=gi.set_index("game_id")
 from functools import lru_cache
 @lru_cache(None)
 def prior(w,t,o):
  hist=p[(p.week<w)&(p.posteam==t)]; pr=ru[(ru.week<w)&(ru.posteam==t)];pt=pa[(pa.week<w)&(pa.posteam==t)];dr=ru[(ru.week<w)&(ru.defteam==o)];dt=pa[(pa.week<w)&(pa.defteam==o)];dn=p[(p.week<w)&(p.defteam==o)].game_id.nunique()
  return hist.game_id.unique(),pr,pt,dr,dt,dn
 for ix,r in enumerate(d.itertuples()):
  if ix%5000==0:print("features",ix,"/",len(d),flush=True)
  pid=names.get(norm(r.player));g=gameindex.loc[r.game_id];team=teammap.get((r.game_id,pid)); opp=g.home_team if team==g.away_team else g.away_team if team else None
  # Player team from observed game is identity metadata, never used as predictive input.
  gids,pr,pt,dr,dt,dn=prior(r.week,team,opp);n=len(gids)
  yards=lambda gid: float(statr.get((gid,pid),0))*(r.market!='recyds')+float(statt.get((gid,pid),0))*(r.market!='rushyds')
  actual=yards(r.game_id) if pid and team else np.nan
  ll=linegroups.get(r.game_id,ldf.iloc[:0]);ll=ll[ll.snap<=r.snap].sort_values('snap')
  sp=ll[(ll.market=='spreads')&(ll.name==team)].drop_duplicates('book',keep='last').point.median() if len(ll) else np.nan
  tot=ll[(ll.market=='totals')&(ll.name=='Over')].drop_duplicates('book',keep='last').point.median() if len(ll) else np.nan
  
  allowance=(dr.rushing_yards.sum()*(r.market!='recyds')+dt.receiving_yards.sum()*(r.market!='rushyds'))/dn if dn else np.nan
  result='ungraded' if pd.isna(actual) else 'push' if actual==r.line else 'win' if ((actual>r.line)==(r.side=='over')) else 'loss'
  features.append(dict(gsis=pid,team=team,opp=opp,result_stat=actual,result=result,pl=profit(r.price) if result=='win' else -10 if result=='loss' else 0,stake=0 if result=='ungraded' else 10,spread=sp,total=tot,implied_team_total=(tot-sp)/2,prior_games=n,prior_carry_share=(pr.rusher_player_id==pid).sum()/len(pr) if len(pr) else np.nan,prior_target_share=(pt.receiver_player_id==pid).sum()/len(pt) if len(pt) else np.nan,prior_yds_avg=np.mean([yards(x) for x in gids]) if n else np.nan,opp_prior_allowance=allowance,man=np.nan,zone=np.nan,HINDSIGHT_sharp_man=sharp.get(opp,{}).get('man'),HINDSIGHT_sharp_zone=sharp.get(opp,{}).get('zone'),feature_cutoff=f'weeks<{r.week}',identity_flag='team inferred from game participation; not a rule input',line_size=r.line,price_bucket='plus' if r.price>0 else 'minus_100_149' if r.price>=-149 else 'minus_150_249' if r.price>=-249 else 'minus_250_plus'))
 d=pd.concat([d,pd.DataFrame(features)],axis=1);d['form_edge']=np.where(d.side=='over',d.prior_yds_avg-d.line,d.line-d.prior_yds_avg);d.to_csv(OUT/'candidates.csv',index=False)
 coverage=[]
 for w in range(3,9):
  for mk in MARKETS.values():
   z=d[(d.week==w)&(d.market==mk)];coverage.append(dict(week=w,market=mk,priced_main=(z.tier=='main').sum(),priced_alt=(z.tier=='alt').sum(),books=';'.join(sorted(z.book.unique())),events=z.game_id.nunique(),scheduled_events=int((gi.week==w).sum()),fields_available='price,line,book,snap; prior-week pbp features' if len(z) else 'none',ungraded=int((z.result=='ungraded').sum())))
 c=pd.DataFrame(coverage);c.to_csv(OUT/'coverage.csv',index=False)
 gaps=['# Saved-data gaps','Counts are distinct book/player/side/tier/line quotes, latest verified pre-kickoff snapshot per quote. Not a full historical slate. No prices fabricated.','Raw JSON inventory covers both replay folders, runs, week8 and week9. Outlier CSVs are curated screen transcriptions, lack verified quote timestamps/tier and are not admitted. Existing replay/simulation outputs are filtered and not used as the universe.','Weeks use saved NFL play-by-play game IDs (2026 season). Games missing from that schedule cannot be assigned or graded safely. No week-9 games admitted.','Missing-event minimum retrieval budget (one region, one main market; 10 credits/event/market). Alternate endpoint retrieval would add an equivalent budget where needed; actual charges not verified:']
 for r in c.itertuples():gaps.append(f'- W{r.week} {r.market}: {r.scheduled_events-r.events} events without prices; ~{10*(r.scheduled_events-r.events)} credits main only.')
 gaps+=['Sum minimum main-market budget: ~%d credits.'%(10*(c.scheduled_events-c.events).sum()),'No point-in-time man/zone table found. Sharp Oct27 is separately HINDSIGHT for every week here, never a legal baseline feature. No current aggregated matchup/defender table used.','PBP features: all earlier team games, including zero player yards when no recorded target/carry; absence is a proxy, not a verified active-game log. Carry share uses all team carries; target share uses named receivers on non-sack pass attempts. Opp allowance is team yards/game, not position-adjusted. PBP final corrections are not reconstructable as-of kickoff.','Book quotes form correlated rows; summary and minimum sample counts are quote counts, not independent bets. Slips collapse to one player. No SGP correlation-adjusted executable parlay quotes exist; product-of-decimal payouts are illustrative.','No network calls made.']
 (OUT/'GAPS.md').write_text('\n\n'.join(gaps)+'\n')
 train=d[d.week<=6];summary(train,['market','side','tier']).to_csv(OUT/'grading_train.csv',index=False)
 # Holdout aggregate grading required by step 3; never consumed by selection.
 summary(d[d.week>=7],['market','side','tier']).to_csv(OUT/'grading_holdout.csv',index=False)
 traits=[];rules=[]
 for (mk,side),z in train.groupby(['market','side']):
  for feature in ['tier','price_bucket']:
   a=summary(z,[feature]);a.insert(0,'side',side);a.insert(0,'market',mk);a.insert(2,'feature',feature);traits.append(a.rename(columns={feature:'value'}))
  for threshold in [0,10,20]:
   a=summary(z.assign(value=np.where(z.form_edge>=threshold,'above','below')),['value']);a.insert(0,'side',side);a.insert(0,'market',mk);a.insert(2,'feature',f'form_edge>={threshold}');traits.append(a)
  opts=[]
  for tier in ['main','alt']:
   for threshold in [0,10,20]:
    q=z[(z.tier==tier)&(z.form_edge>=threshold)&(z.result!='ungraded')];s=summary(q,['market','side'])
    if len(q)>=15 and len(s) and s.roi.iloc[0]>0:opts.append((float(s.roi.iloc[0]),len(q),tier,threshold))
  if opts:
   roi,n,tier,threshold=sorted(opts,key=lambda x:(-x[0],-x[1],x[2],x[3]))[0];rules.append(dict(market=mk,side=side,tier=tier,min_form_edge=threshold,train_n=n,train_roi=roi))
 pd.concat(traits,ignore_index=True).to_csv(OUT/'traits.csv',index=False)
 (OUT/'traits.md').write_text('# Train-only univariate traits\n\nSee traits.csv: each split reports n, wins, losses, pushes, hit%, $10 P/L and ROI. Above/below comparisons include losing rows; below includes missing form. Quote-level exploratory splits are correlated and multiple-tested, not causal evidence. No holdout values used.\n\n'+pd.concat(traits,ignore_index=True).to_string(index=False)+'\n')
 (OUT/'locked_rules.json').write_text(json.dumps(rules,indent=2)+'\n')
 (OUT/'RULES.md').write_text('# Rules locked from weeks 3–6 only\n\nFor each market/side search exactly 6 cells: tier main/alt × directional prior-yard-average edge >= 0/10/20 yards. Require >=15 graded priced quotes and positive training ROI. Choose highest ROI, then larger n, alphabetical tier, lower threshold. Three conditions: market-side identity, tier, edge threshold. Unrepresented or nonpositive cells abstain. No Sharp feature used.\n\n'+json.dumps(rules,indent=2)+'\n\nSelection is exploratory and book-correlated; sparse weeks are unavailable rather than treated as losing observations.\n')
 print('Built',len(d),'quotes; rules',len(rules),'weeks',sorted(d.week.unique()))
if __name__=='__main__':main()

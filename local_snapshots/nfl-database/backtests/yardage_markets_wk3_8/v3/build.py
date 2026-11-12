"""Offline Stage A; never aggregate week 7–8 outcomes."""
from pathlib import Path
import json, hashlib, re
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
def profit(p): return p/10 if p>0 else 1000/-p
def summary(d,keys):
 cols=keys+['n','wins','losses','pushes','ungraded','hit_pct','pl','stake','roi']
 if d.empty:return pd.DataFrame(columns=cols)
 a=d.groupby(keys,dropna=False).agg(n=('result','size'),wins=('result',lambda s:(s=='win').sum()),losses=('result',lambda s:(s=='loss').sum()),pushes=('result',lambda s:(s=='push').sum()),ungraded=('result',lambda s:(s=='ungraded').sum()),pl=('pl','sum'),stake=('stake','sum')).reset_index()
 a['hit_pct']=100*a.wins/(a.wins+a.losses);a['roi']=100*a.pl/a.stake;return a[cols]
def settle(x,p):
 ru=p[(p.rush_attempt==1)&p.rusher_player_id.notna()].groupby(['game_id','rusher_player_id']).rushing_yards.sum()
 rec=p[(p.pass_attempt==1)&(p.sack!=1)&p.receiver_player_id.notna()].groupby(['game_id','receiver_player_id']).receiving_yards.sum()
 x=x.copy();vals=[]
 for r in x.itertuples():
  actual=(ru.get((r.game_id,r.gsis),0)*(r.market!='recyds')+rec.get((r.game_id,r.gsis),0)*(r.market!='rushyds')) if pd.notna(r.gsis) and pd.notna(r.team) else np.nan
  result='ungraded' if pd.isna(actual) or pd.isna(r.price) or r.price==0 else 'push' if actual==r.line else 'win' if (actual>r.line)==(r.side=='over') else 'loss'
  vals.append((actual,result,profit(r.price) if result=='win' else -10 if result=='loss' else 0,0 if result=='ungraded' else 10))
 x[['result_stat','result','pl','stake']]=pd.DataFrame(vals,index=x.index);return x

def main():
 from rules import one_player, mask
 cols=['week','game_id','game','player','market','side','tier','line','price','snap','kickoff','source','gsis','team','opp','candidate_id']
 x=pd.read_csv(OUT.parent/'v2/legs.csv',usecols=cols)
 assert (x.tier=='main').all() and not x.duplicated(['week','player','market','side']).any()
 p=pd.read_parquet(ROOT/'runs/2026-11-02_shared_src/play_by_play_2026.parquet');p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)]
 p=p[['week','game_id','posteam','defteam','rush_attempt','rusher_player_id','pass_attempt','sack','receiver_player_id','rushing_yards','receiving_yards']]
 players=pd.read_parquet(ROOT/'runs/2026-11-02_shared_src/players.parquet');pos=players.drop_duplicates('gsis_id').set_index('gsis_id').position.to_dict();pfr=players.drop_duplicates('gsis_id').set_index('gsis_id').pfr_id.to_dict()
 snaps=pd.read_parquet('/tmp/snap_counts_2026.parquet');snaps=snaps[(snaps.season==2026)&(snaps.game_type=='REG')]
 # Enumerate only allowed offline source roots.
 roots=[ROOT/'runs',ROOT/'backtests/yardage_markets_wk3_8/raw',ROOT/'backtests/rulebook_replay_wk6_8/raw',ROOT/'backtests/current_rules_wk6_8/raw']+list(ROOT.glob('week*'))
 files=sorted({f for root in roots if root.is_dir() for f in root.rglob('*.json')})
 ab={'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL', 'Buffalo Bills': 'BUF', 'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE', 'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB', 'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KC', 'Las Vegas Raiders': 'LV', 'Los Angeles Chargers': 'LAC', 'Los Angeles Rams': 'LA', 'Miami Dolphins': 'MIA', 'Minnesota Vikings': 'MIN', 'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG', 'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 'San Francisco 49ers': 'SF', 'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB', 'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS', 'LAR': 'LA', 'WSH': 'WAS'}
 events=[];weather=[];coverage=[]
 for f in files:
  if 'weather' in f.name.lower():weather.append(str(f.relative_to(ROOT)))
  try:j=json.loads(f.read_text())
  except (ValueError,UnicodeError,OSError):continue
  if not isinstance(j,dict):continue
  data=j.get('data',j)
  for e in data if isinstance(data,list) else [data]:
   if not isinstance(e,dict) or 'commence_time' not in e:continue
   for b in e.get('bookmakers',[]):
    for m in b.get('markets',[]):
     if m.get('key') not in ['h2h','spreads','totals']:continue
     ts=j.get('timestamp') or j.get('snapshot_time') or m.get('last_update') or b.get('last_update')
     try: valid=bool(ts and pd.Timestamp(ts)<=pd.Timestamp(e['commence_time']) and (not m.get('last_update') or pd.Timestamp(m['last_update'])<=pd.Timestamp(e['commence_time'])))
     except (ValueError,TypeError):valid=False
     if valid:
      for o in m.get('outcomes',[]):events.append(dict(kickoff=e['commence_time'],home=ab.get(e.get('home_team'),e.get('home_team')),away=ab.get(e.get('away_team'),e.get('away_team')),market=m['key'],book=b['key'],ts=ts,name=ab.get(o['name'],o['name']),point=o.get('point',np.nan),source=str(f.relative_to(ROOT))))
 odds=pd.DataFrame(events,columns=['kickoff','home','away','market','book','ts','name','point','source']).drop_duplicates()
 odds.to_csv(OUT/'saved_game_odds_inventory.csv',index=False)
 weather_rows=[]
 for name in weather:
  j=json.loads((ROOT/name).read_text());issued=j.get('pulled_et',j.get('_pulled_et'))
  if not issued:continue
  issued=pd.Timestamp(issued).tz_localize('America/New_York').tz_convert('UTC')
  for home,v in j.items():
   if not isinstance(v,dict) or v.get('roof')!='open':continue
   for forecast in v.get('om',[]):
    t=pd.Timestamp(forecast['t']);t=t.tz_localize('UTC') if t.tzinfo is None else t.tz_convert('UTC')
    weather_rows.append(dict(home=ab.get(home,home),issued=issued,time=t,temp=forecast.get('temp'),wind=forecast.get('wind'),source=name))
 rows=[];cache={}
 for r in x.itertuples():
  key=(r.week,r.game_id,r.player,r.market)
  if key in cache:
   rows.append(cache[key]);continue
  h=p[p.week<r.week];ru=h[(h.rush_attempt==1)&h.rusher_player_id.notna()];pa=h[(h.pass_attempt==1)&(h.sack!=1)&h.receiver_player_id.notna()]
  tr=ru[ru.posteam==r.team];ta=pa[pa.posteam==r.team];dr=ru[ru.defteam==r.opp];da=pa[pa.defteam==r.opp]
  ng=h[h.posteam==r.team].game_id.nunique();dn=h[h.defteam==r.opp].game_id.nunique();position=pos.get(r.gsis)
  shares=tr.groupby('rusher_player_id').size();rb=shares[shares.index.map(lambda v:pos.get(v)=='RB')].sort_values(ascending=False)
  # Second largest RB's share of ALL team carries.
  second=rb.iloc[1]/len(tr) if len(rb)>1 and len(tr) else (0 if len(tr) else np.nan)
  s=snaps[(snaps.week<r.week)&(snaps.team==r.team)];ss=s[s.pfr_player_id==pfr.get(r.gsis)]
  # Sum team offensive snaps once per game, including zero for player absences.
  denom=s.groupby('game_id').offense_snaps.max().sum()
  gids=h[h.posteam==r.team].game_id.unique();ys=[]
  for gid in gids:
   ys.append(tr[(tr.game_id==gid)&(tr.rusher_player_id==r.gsis)].rushing_yards.sum()*(r.market!='recyds')+ta[(ta.game_id==gid)&(ta.receiver_player_id==r.gsis)].receiving_yards.sum()*(r.market!='rushyds'))
  oo=odds[(odds.kickoff==r.kickoff)&(odds.ts<=r.kickoff)&(((odds.home==r.team)&(odds.away==r.opp))|((odds.away==r.team)&(odds.home==r.opp)))].sort_values(['ts','source']).drop_duplicates(['book','market','name'],keep='last')
  sp=oo[(oo.market=='spreads')&(oo.name==r.team)].point.median();tot=oo[(oo.market=='totals')&(oo.name=='Over')].point.median()
  home=r.game_id.split('_')[-1];ko=pd.Timestamp(r.kickoff)
  ww=[v for v in weather_rows if v['home']==home and v['issued']<=ko and abs((v['time']-ko).total_seconds())<=3600]
  ww=sorted(ww,key=lambda v:(-v['issued'].timestamp(),abs((v['time']-ko).total_seconds()),v['source']))
  wx=ww[0] if ww else {}
  rows.append(dict(position=position,prior_games=ng,prior_carry_share=(tr.rusher_player_id==r.gsis).sum()/len(tr) if len(tr) else np.nan,prior_snap_share=ss.offense_snaps.sum()/denom if denom and len(ss) else np.nan,second_back_share=second,prior_target_share=(ta.receiver_player_id==r.gsis).sum()/len(ta) if len(ta) else np.nan,opp_rush_yds_game=dr.rushing_yards.sum()/dn if dn else np.nan,opp_rush_yds_carry=dr.rushing_yards.sum()/len(dr) if len(dr) else np.nan,opp_rec_yds_position_game=da[da.receiver_player_id.map(pos)==position].receiving_yards.sum()/dn if dn and position in ['WR','TE','RB'] else np.nan,prior_yds_avg=np.mean(ys) if ys else np.nan,spread=sp,total=tot,implied_team_total=(tot-sp)/2,favored=float(sp<0) if pd.notna(sp) else np.nan,injury_status=np.nan,weather_temp=wx.get('temp',np.nan),weather_wind=wx.get('wind',np.nan),weather_source=wx.get('source',''),weather_issued=str(wx.get('issued','')),feature_cutoff=f'weeks<{r.week}',game_odds_sources=';'.join(sorted(oo.source.unique())),game_odds_markets=';'.join(sorted(oo.market.unique()))))
  cache[key]=rows[-1]
 x=pd.concat([x,pd.DataFrame(rows)],axis=1);x['model_edge']=(x.prior_yds_avg-x.line)*np.where(x.side=='over',1,-1)
 x['result']='withheld';x['result_stat']=np.nan;x['pl']=np.nan;x['stake']=np.nan
 train=settle(x[x.week.between(3,6)],p[p.week.between(3,6)])
 x.loc[train.index,['result','result_stat','pl','stake']]=train[['result','result_stat','pl','stake']]
 x.to_csv(OUT/'features.csv',index=False)
 base=train[(train.market=='rushyds')&(train.side=='under')]
 pd.concat([summary(base.assign(baseline='all'),['baseline','week']),summary(one_player(base).assign(baseline='one_player'),['baseline','week'])]).to_csv(OUT/'baseline_train.csv',index=False)
 traits=[]
 for feature,bins in {'model_edge':[-np.inf,0,5,10,15,20,np.inf],'prior_carry_share':[-np.inf,.25,.5,.6,.75,np.inf],'prior_snap_share':[-np.inf,.4,.6,.8,np.inf],'second_back_share':[-np.inf,.1,.25,.4,np.inf],'prior_target_share':[-np.inf,.1,.2,.3,np.inf],'opp_rush_yds_game':[-np.inf,100,125,150,np.inf],'opp_rush_yds_carry':[-np.inf,4,4.5,5,np.inf],'opp_rec_yds_position_game':[-np.inf,40,80,120,160,np.inf],'spread':[-np.inf,-7,0,7,np.inf],'implied_team_total':[-np.inf,20,25,30,np.inf]}.items():
  z=train.copy();z['bucket']=pd.cut(z[feature],bins).astype(str);a=summary(z,['market','side','bucket']);a['feature']=feature;traits.append(a)
 t=pd.concat(traits);t.to_csv(OUT/'traits.csv',index=False)
 (OUT/'traits.md').write_text('# Train-only traits: weeks 3–6\n\nExploratory, not causal. Hit excludes pushes/ungraded; ROI uses $10 settled stakes. No holdout grading.\n\n'+t.to_string(index=False)+'\n')
 from rules import fit
 locked=fit(train)['rules']
 gaps=['# Gaps and leakage risks','No network or environment keys used. v2 outcomes, features and Sharp hindsight excluded; only identity/consensus quote columns reused. Prior-week features use weeks strictly <w; week 7 statistics may inform week 8 features, but no week 7–8 market outcomes are computed. Training settlement aggregates only weeks 3–6.','Snap share: saved /tmp/snap_counts_2026.parquet, linked by players.parquet pfr_id; player offensive snaps / sum of team per-game maximum offensive snaps, including missed games. Missing identity/participation remains missing. RB carry share uses all team carries including QB; second-back share is second largest RB share of all team carries. Targets exclude sacks and require identified receiver. Position allowance uses static players.parquet position and all opponent prior games. Static position/identity metadata and retrospective corrections to historical pbp/snaps can introduce revision bias. v2 team identity retained; v2 derived it from prior participation.','Injuries: /tmp/inj26.parquet inspected; no report dates or publication timestamps. All injury features missing; week alone is insufficient proof of availability as of kickoff.','Weather: saved weather JSON files inventoried in weather_inventory.txt. Use shared_src weather hourly Open-Meteo entries only where saved _pulled_et/pulled_et (America/New_York) <= kickoff, home-team linkage matches, roof is open, and forecast valid hour is within one hour of kickoff. Latest issuance then nearest hour wins. Missing weeks/games remain missing; no indoor weather used. Snapshot issuance is a locally recorded collection timestamp, not independently audited. Array-only matchup forecasts are unused because valid hours are absent.','Odds: saved h2h/spreads/totals scanned in allowed raw/run/week roots; require snapshot and market update <=kickoff, latest per book/market/outcome, median across books. Kickoff exact match and teams required. Odds use pre-kick data but may be later than prop consensus snapshot, so strategy assumes decision at kickoff. Consensus prices are estimates, potentially unquoted median; missing prices abstain. No closing-only odds invented.','Overfit risk: a 1–3 condition matchup/script/role tercile grid per market-side, univariate traits exploratory, no validation beyond train. Product slip odds ignore correlation and SGP repricing. Source coverage and unknown players limit interpretation.']
 for w in range(3,9):
  z=x[x.week==w];msgs=[]
  for mk in ['h2h','spreads','totals']:
   has=z[z.game_odds_markets.str.contains(mk,na=False)].game_id.nunique();msgs.append(f'{mk} {has}/{z.game_id.nunique()} games')
  gaps.append(f'Week {w} saved pre-kick coverage: '+', '.join(msgs)+'. Zero means week lacks that market; partial coverage leaves remaining games missing.')
 gaps.append('Feature missing counts by week:\n\n'+x.groupby('week')[[c for c in rows[0] if c not in ['feature_cutoff','game_odds_sources','game_odds_markets','weather_source','weather_issued']]].agg(lambda s:s.isna().sum()).to_string())
 (OUT/'GAPS.md').write_text('\n\n'.join(gaps)+'\n');(OUT/'weather_inventory.txt').write_text('\n'.join(weather)+'\n')
 assert (x.loc[x.week>=7,'result']=='withheld').all() and x.loc[x.week>=7,['result_stat','pl','stake']].isna().all().all()
 frozen=['TASK3.md','build.py','features.csv','baseline_train.csv','traits.csv','traits.md','GAPS.md','saved_game_odds_inventory.csv','weather_inventory.txt','rules.py','locked_rules.json','RULES.md','slip_method.md','grade.py','validate.py']
 (OUT/'frozen_sha256.json').write_text(json.dumps({f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in frozen},indent=2)+'\n')
 print(f'Stage A complete: {len(x)} consensus legs, {len(locked)} locked rules. Holdout outcomes withheld.')
if __name__=='__main__':main()

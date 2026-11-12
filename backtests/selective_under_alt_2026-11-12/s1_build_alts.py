"""Step 1: real alt-rung prices (player alts + game alts) from the saved inventory. No outcomes used.
Latest verified pre-kick quote per book/rung; best price across books kept. Pass yards excluded."""
import os, pandas as pd, numpy as np
INV=os.environ.get('INV','/workspace/research/historical_nfl_odds_inventory_2026-11-07/sportsbook_observations.csv')
PROPS=os.environ.get('PROPS','/workspace/nfl-database/backtests/confidence_check_2026-11-03/legs_with_probs.csv')
OUT=os.environ.get('OUT','/workspace/research/selective_under_alt_2026-11-12')
MK={'player_rush_yds_alternate':'rushyds','player_reception_yds_alternate':'recyds','player_receptions_alternate':'rec',
    'player_rush_reception_yds_alternate':'rushrec'}
GM=['spreads','totals','alternate_totals','alternate_spreads','alternate_team_totals']
d=pd.read_csv(INV,low_memory=False)
d=d[(d.pregame_status=='verified_capture_before_start')&d.week.between(4,9)&(d.period.fillna('FT')=='FT')]
d['snap']=pd.to_datetime(d.snapshot_timestamp,utc=True,errors='coerce'); d['ko']=pd.to_datetime(d.event_start_timestamp,utc=True,errors='coerce')
d=d[d.snap<d.ko]
def dec(a): a=float(a); return 1+a/100 if a>0 else 1+100/-a
# player alts
p=d[d.market.isin(MK)].copy(); p['m']=p.market.map(MK)
p=p.sort_values('snap').groupby(['game_id','player','m','selection','line','bookmaker']).tail(1)
p['dec']=p.price.map(dec)
best=p.sort_values('dec').groupby(['game_id','player','m','selection','line']).tail(1)
L=pd.read_csv(PROPS); L=L[L.week.between(4,9)&(L.market!='passyds')]
key=L[['week','game_id','player','gsis','market','line']].rename(columns={'line':'main_line','market':'m'})
alt=best.merge(key,on=['game_id','player','m'],how='inner')
alt=alt[alt.line!=alt.main_line]
alt=alt[['week_x','game_id','player','gsis','m','selection','line','main_line','price','dec','bookmaker','snapshot_timestamp','event_start_timestamp']].rename(columns={'week_x':'week','m':'market','line':'rung'})
alt.to_csv(OUT+'/alt_rungs_props.csv',index=False)
# game lines (main + alt)
g=d[d.market.isin(GM)].copy()
g=g.sort_values('snap').groupby(['game_id','market','selection','line','bookmaker']).tail(1)
g['dec']=g.price.map(dec)
g[['week','game_id','home_team','away_team','market','selection','line','price','dec','bookmaker','snapshot_timestamp','event_start_timestamp']].to_csv(OUT+'/game_quotes.csv',index=False)
print('prop alt rungs',len(alt),alt.groupby(['week','market']).size().unstack().to_string())
print('legs with alts',alt.groupby(['game_id','player','market']).ngroups)
print('game quotes',g.groupby(['week','market']).size().unstack().to_string())

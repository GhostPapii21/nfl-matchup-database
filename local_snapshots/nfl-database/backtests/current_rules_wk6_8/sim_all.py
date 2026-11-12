"""Leak-free sims (Engine cutoff = first game date of week W, raw/no calibration, oppadj full strength per current sim_v6) at real lines."""
import os,sys,re,json,numpy as np,pandas as pd
os.environ['SIMV6_SRC']='/workspace/nfl-database/runs/2026-11-02_shared_src'
sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as S
N=int(sys.argv[1]) if len(sys.argv)>1 else 100_000
P=S._P; PL=S._PL
AB={'Arizona Cardinals':'ARI','Atlanta Falcons':'ATL','Baltimore Ravens':'BAL','Buffalo Bills':'BUF','Carolina Panthers':'CAR','Chicago Bears':'CHI','Cincinnati Bengals':'CIN','Cleveland Browns':'CLE','Dallas Cowboys':'DAL','Denver Broncos':'DEN','Detroit Lions':'DET','Green Bay Packers':'GB','Houston Texans':'HOU','Indianapolis Colts':'IND','Jacksonville Jaguars':'JAX','Kansas City Chiefs':'KC','Las Vegas Raiders':'LV','Los Angeles Chargers':'LAC','Los Angeles Rams':'LA','Miami Dolphins':'MIA','Minnesota Vikings':'MIN','New England Patriots':'NE','New Orleans Saints':'NO','New York Giants':'NYG','New York Jets':'NYJ','Philadelphia Eagles':'PHI','Pittsburgh Steelers':'PIT','San Francisco 49ers':'SF','Seattle Seahawks':'SEA','Tampa Bay Buccaneers':'TB','Tennessee Titans':'TEN','Washington Commanders':'WAS'}
nm=lambda s:re.sub(r'\b(jr|sr|ii|iii|iv|v)\b','',re.sub(r'[^a-z ]','',str(s).lower())).split()
key=lambda s:' '.join(nm(s))
L=pd.read_csv('real_lines_wk6_8.csv'); L['h']=L.home.map(AB); L['a']=L.away.map(AB)
G=P.drop_duplicates('game_id')[['game_id','week','home_team','away_team','spread_line','total_line']]
L=L.merge(G,left_on=['h','a'],right_on=['home_team','away_team']); L=L[L.week.isin([6,7,8])]
# who played in each game, keyed by name
ids=pd.concat([P[[c+'_player_id',c+'_player_name','posteam','game_id']].rename(columns={c+'_player_id':'gsis',c+'_player_name':'abbr'}) for c in ('passer','receiver','rusher')]).dropna().drop_duplicates(['gsis','game_id'])
full=PL.set_index('gsis_id').display_name.to_dict(); ids['k']=ids.gsis.map(full).map(key)
ids=ids.dropna(subset=['k'])
L['k']=L.player.map(key)
L=L.merge(ids[['k','game_id','gsis','posteam']],on=['k','game_id'],how='left')
print('unmatched',L.gsis.isna().sum(),'of',len(L)); L=L.dropna(subset=['gsis'])
rows=[]
for W in (6,7,8):
    cut=P[P.week==W].game_date.min(); E=S.Engine(cutoff=cut,calib=None,n=N)
    for _,r in L[L.week==W].iterrows():
        t=r.posteam; opp=r.home_team if r.away_team==t else r.away_team
        tsp=-r.spread_line if r.home_team==t else r.spread_line
        thr=r.line+0.5 if r.market=='rec' else r.line
        try: o,info=E.sim(dict(player=r.gsis,gsis=r.gsis,team=t,opp=opp,market=r.market,spread=tsp,rungs=[thr]),raw=True)
        except Exception as e: continue
        d=r.to_dict(); d.update(team=t,opp=opp,team_spread=tsp,**{f'p_{m}':o[m]['rungs'][str(thr)] for m in S.MODES},**{f'med_{m}':o[m]['cmedian'] for m in S.MODES},pos=info['pos'],n_games=info['n_games'])
        rows.append(d)
    print('week',W,'done',len(rows),flush=True)
pd.DataFrame(rows).to_csv('sims_wk6_8.csv',index=False)

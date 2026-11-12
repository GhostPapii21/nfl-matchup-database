"""Rico Nov 3 6:37 AM: 4-5 leg slips, one leg per game, except a 2nd leg from the same game allowed when BOTH legs are strong edges (raw_edge >= T). Max 2 per game. Cap 5 slips/day by build order. $25. Combined pool (no passyds + game legs). M1 greedy otherwise unchanged. No network."""
import pandas as pd, numpy as np, json, sys
ab=json.load(open('abbr.json'))
inv=pd.read_csv('test_d_nopass_gamelines/gameline_inventory.csv')
inv['g']=inv.game.map(lambda f:'@'.join(ab[t] for t in f.split('@'))); inv['day']=pd.to_datetime(inv.commence_utc).dt.tz_convert('America/New_York').dt.date
g2d=dict(zip(inv.g,inv.day)); dec=lambda a:1+(a/100 if a>0 else 100/-a)
L=pd.read_csv('graded_legs.csv',keep_default_na=False,na_values=[''])
L=L[(L['pool'].astype(str)=='True')&(L.market!='passyds')]; L['depth']=L.depth.astype(str)=='True'
GL=pd.read_csv('test_d_nopass_gamelines/game_legs.csv'); GL=GL[GL.passed.astype(bool)]; GL['depth']=False
P=pd.concat([L,GL],ignore_index=True)
print('edge quantiles',P.raw_edge.quantile([.25,.5,.75,.9]).round(3).to_dict())
STAKE=25; allrows=[]
for T in (0.08,0.10,0.12):
  rows=[]
  for W in (6,7,8,9):
    pool=P[P.week==W].sort_values(['raw_edge','price'],ascending=[False,True]).drop_duplicates('gsis')
    for k in (4,5):
        S=[];openS=[]
        for x in pool.to_dict('records'):
            for s in openS:
                same=[y for y in s if y['game']==x['game']]
                if same and (len(same)>=2 or x['raw_edge']<T or same[0]['raw_edge']<T): continue
                if x['depth'] and any(y['depth'] for y in s): continue
                s.append(x); break
            else: openS.append([x])
            S+=[s for s in openS if len(s)==k]; openS=[s for s in openS if len(s)<k]
        for i,s in enumerate(S):
            res=[x['result'] for x in s]; live=[x for x in s if x['result'] in('win','loss')]
            if 'loss' in res: out,pr='loss',-STAKE
            elif not live: out,pr='refund',0
            else: out,pr='win',STAKE*(np.prod([dec(x['price']) for x in live])-1)
            g=pd.Series([x['game'] for x in s])
            rows.append(dict(T=T,week=W,k=k,order=i,day=max(g2d[x['game']] for x in s),sgp=int(g.duplicated().any()),legs=' | '.join(x['leg'] for x in s),results=' '.join(res),nloss=res.count('loss'),outcome=out,profit=round(pr,2),dec_price=round(np.prod([dec(x['price']) for x in s]),2)))
  S=pd.DataFrame(rows); allrows.append(S)
  for k in (4,5,'4+5'):
    sub=S if k=='4+5' else S[S.k==k]
    cap=sub.sort_values(['order','k']).groupby('day').head(5)
    t=cap.groupby('week').agg(slips=('outcome','size'),won=('outcome',lambda x:(x=='win').sum()),sgp=('sgp','sum'),one_off=('nloss',lambda x:(x==1).sum()),pl=('profit','sum'))
    print(f'\n== T={T} k={k} uncapped {len(sub)} won {(sub.outcome=="win").sum()} pl {sub.profit.sum():.0f} | CAPPED {len(cap)} won {(cap.outcome=="win").sum()} pl {cap.profit.sum():.2f} sgp-slips {cap.sgp.sum()}')
    print(t.to_string())
    w=cap[cap.outcome=='win']; 
    if len(w): print(w[['week','k','sgp','dec_price','profit']].to_string())
pd.concat(allrows).to_csv('test_d_nopass_gamelines/m3_two_edge_sgp_all.csv',index=False)

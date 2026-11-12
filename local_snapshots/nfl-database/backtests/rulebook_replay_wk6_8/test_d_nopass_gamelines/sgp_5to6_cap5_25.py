"""Rico Nov 3 6:36 AM: 5-6 leg slips, same-game allowed (M2 method, unchanged), combined pool (no passyds + game legs), cap 5 slips/day by build order, $25/slip. No network."""
import pandas as pd, numpy as np, json
ab=json.load(open('abbr.json'))
inv=pd.read_csv('test_d_nopass_gamelines/gameline_inventory.csv')
code=lambda f:'@'.join(ab[t] for t in f.split('@'))
inv['g']=inv.game.map(code); inv['day']=pd.to_datetime(inv.commence_utc).dt.tz_convert('America/New_York').dt.date
g2d=dict(zip(inv.g,inv.day))
dec=lambda a:1+(a/100 if a>0 else 100/-a)
L=pd.read_csv('graded_legs.csv',keep_default_na=False,na_values=[''])
L=L[(L['pool'].astype(str)=='True')&(L.market!='passyds')]
GL=pd.read_csv('test_d_nopass_gamelines/game_legs.csv'); GL=GL[GL.passed.astype(bool)]
P=pd.concat([L,GL],ignore_index=True)
STAKE=25; rows=[]
for W in (6,7,8,9):
    pool=P[P.week==W].sort_values(['raw_edge','price'],ascending=[False,True]).drop_duplicates('gsis')
    v=pool.to_dict('records')
    for k in (5,6):
        for i in range(0,len(v)-k+1,k):
            s=v[i:i+k]; res=[x['result'] for x in s]; live=[x for x in s if x['result'] in('win','loss')]
            if 'loss' in res: out,pr='loss',-STAKE
            elif not live: out,pr='refund',0
            else: out,pr='win',STAKE*(np.prod([dec(x['price']) for x in live])-1)
            day=max(g2d[x['game']] for x in s)
            rows.append(dict(week=W,k=k,order=i//k,day=day,legs=' | '.join(x['leg'] for x in s),results=' '.join(res),outcome=out,profit=round(pr,2),dec_price=round(np.prod([dec(x['price']) for x in s]),2)))
S=pd.DataFrame(rows); S.to_csv('test_d_nopass_gamelines/sgp_5to6_all.csv',index=False)
for k in (5,6,'5+6'):
    sub=S if k=='5+6' else S[S.k==k]
    cap=sub.sort_values(['order','k']).groupby('day').head(5)
    print(f'\n== k={k}  uncapped {len(sub)} slips, won {(sub.outcome=="win").sum()}, pl {sub.profit.sum():.2f}')
    t=cap.groupby('week').agg(days=('day','nunique'),slips=('outcome','size'),won=('outcome',lambda x:(x=='win').sum()),pl=('profit','sum'))
    print(t.to_string()); print('TOTAL',len(cap),(cap.outcome=='win').sum(),round(cap.profit.sum(),2), 'staked',len(cap)*STAKE)
    print(cap[cap.outcome=='win'][['week','k','dec_price','profit']].to_string())
    cap.assign(kset=str(k)).to_csv(f'test_d_nopass_gamelines/sgp_cap5_k{k}.csv',index=False)

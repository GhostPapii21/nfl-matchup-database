"""Rico Nov 3 6:45 AM: remove receiving-yards UNDERS (plus passyds already gone), rerun Test A M2 (3-4 legs, same-game allowed), cap 5 slips/day in build order, $25. Same ordering as cap5_per_day.py. No network."""
import pandas as pd, numpy as np, json
ab=json.load(open('abbr.json'))
inv=pd.read_csv('test_d_nopass_gamelines/gameline_inventory.csv')
inv['g']=inv.game.map(lambda f:'@'.join(ab[t] for t in f.split('@'))); inv['day']=pd.to_datetime(inv.commence_utc).dt.tz_convert('America/New_York').dt.date
g2d=dict(zip(inv.g,inv.day)); dec=lambda a:1+(a/100 if a>0 else 100/-a)
L=pd.read_csv('graded_legs.csv',keep_default_na=False,na_values=[''])
L=L[(L['pool'].astype(str)=='True')&(L.market!='passyds')]
GL=pd.read_csv('test_d_nopass_gamelines/game_legs.csv'); GL=GL[GL.passed.astype(bool)]
BASE=pd.concat([L,GL],ignore_index=True)
def run(P,STAKE,tag):
    rows=[]
    for W in (6,7,8,9):
        v=P[P.week==W].sort_values(['raw_edge','price'],ascending=[False,True]).drop_duplicates('gsis').to_dict('records')
        for k in (3,4):
            for i in range(0,len(v)-k+1,k):
                s=v[i:i+k]; res=[x['result'] for x in s]; live=[x for x in s if x['result'] in('win','loss')]
                if 'loss' in res: out,pr='loss',-STAKE
                elif not live: out,pr='refund',0
                else: out,pr='win',STAKE*(np.prod([dec(x['price']) for x in live])-1)
                rows.append(dict(week=W,k=k,day=max(g2d[x['game']] for x in s),legs=' | '.join(x['leg'] for x in s),results=' '.join(res),outcome=out,profit=round(pr,2),killers=' | '.join(f"{x['market']} {x['side']}" for x in s if x['result']=='loss')))
    S=pd.DataFrame(rows); cap=S.groupby('day').head(5)
    t=cap.groupby('week').agg(slips=('outcome','size'),won=('outcome',lambda x:(x=='win').sum()),pl=('profit','sum'))
    print(f'\n== {tag}: capped {len(cap)} slips, won {(cap.outcome=="win").sum()}, P/L {cap.profit.sum():.2f}, staked {len(cap)*STAKE}'); print(t.round(2).to_string())
    print(cap[cap.outcome=='win'][['week','k','legs','profit']].to_string())
    print(cap.killers.str.split(' \| ').explode().value_counts().head(6).to_string())
    return cap
c0=run(BASE,25,'BEFORE (with recyds unders) $25')
P=BASE[~((BASE.market=='recyds')&(BASE.side=='under'))]
print('removed recyds unders:',len(BASE)-len(P))
c1=run(P,25,'AFTER (no recyds unders) $25'); c1.to_csv('test_d_nopass_gamelines/no_recyds_under_A_M2_25.csv',index=False)

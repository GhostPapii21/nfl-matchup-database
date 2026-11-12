import pandas as pd
k=pd.read_csv('graded_legs.csv')
dec=lambda a: 1+a/100 if a>0 else 1+100/abs(a)
k=k[k.result!='VOID'].copy(); k['score']=k.edge*k.h/k.n
sun=k[~k.game.isin(['CAR@GB','CHI@SEA'])].sort_values('score',ascending=False)
best=sun.drop_duplicates('game').head(8); rest=sun.drop(best.index)
S={'S1':best,'S2':rest.head(8),'S3':rest.iloc[8:16],'TNF':k[k.game=='CAR@GB'],'MNF':k[k.game=='CHI@SEA']}
for n in ['S1','S2','S3']: S[n+'_7']=S[n].sort_values('score',ascending=False).head(7)
rows=[]
for n,s in S.items():
    s=s[s.result!='PUSH']; won=(s.result=='HIT').all(); price=s.price.map(dec).prod()
    killers=list(s[s.result=='MISS'].market)
    rows.append(dict(slip=n,legs=len(s),hits=(s.result=='HIT').sum(),dec=round(price,2),won=won,pl=round(10*(price-1) if won else -10,2),legs_list='; '.join(f"{r.player} {r.market} {r.side[0]}{r.line} {r.result}" for _,r in s.iterrows()),killed_by=','.join(killers)))
sl=pd.DataFrame(rows); sl.to_csv('slips_graded.csv',index=False); print(sl.to_string())
m=k.groupby(['market','side']).agg(n=('result','size'),hit=('result',lambda x:(x=='HIT').mean()),pl=('pl10','sum')).round(3); print(m); print('singles',len(k),(k.result=='HIT').mean(),k.pl10.sum())
for s in ['RECONSTRUCTED','RECONSTRUCTED(repl)']: x=k[k.src==s]; print(s,len(x),(x.result=='HIT').mean(),x.pl10.sum())

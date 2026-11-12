import pandas as pd, json, numpy as np
f=pd.read_csv('../src/fd_snapshot_20261031_1937.csv'); R=json.load(open('bg_sims.json'))
imp=lambda o:(-o/(-o+100)) if o<0 else 100/(o+100)
ALT={'rec':('Alt Receptions','{n} Receptions'),'recyds':('Alt Receiving Yds','{n} Yards'),'rushyds':('Alt Rushing Yds','{n} Yards')}
MAIN={'rec':'Total Receptions','recyds':'Receiving Yds','rushyds':'Rushing Yds','rushrec':'Rushing + Receiving Yds'}
rows=[]
for k,v in R.items():
    if k=='_meta': continue
    L=v['leg']; nm=L['player']; mk=L['market']
    m=f[f.market==f"{nm} - {MAIN[mk]}"]
    ov=m[m.runner.str.endswith('Over')]; un=m[m.runner.str.endswith('Under')]
    if len(ov): o_,u_=int(ov.odds.iloc[0]),int(un.odds.iloc[0]); line=float(ov.hcp.iloc[0]); k_=imp(o_)+imp(u_)
    else: o_=u_=line=None; k_=None
    for r in L['rungs']:
        price=None
        if mk in ALT:
            a=f[(f.market==f"{nm} - {ALT[mk][0]}")&(f.runner==f"{nm} {int(r)}+ {ALT[mk][1].split()[-1]}")]
            if len(a): price=int(a.odds.iloc[0])
        if mk=='rushrec' and line is not None and abs(r-line)<1e-9: price=o_
        s=v['sims']; ps=[s[x]['rungs'][str(r)] for x in ('mc','bias','gr')]; avg=float(np.mean(ps))
        nv=imp(price)/k_ if (price is not None and k_) else None
        rows.append(dict(leg=k,rung=r,price=price,implied=None if price is None else round(imp(price),3),overround=None if k_ is None else round(k_,3),
          main=f"{line} {o_}/{u_}" if line is not None else None,nv=None if nv is None else round(nv,3),mc=round(ps[0],3),bias=round(ps[1],3),gr=round(ps[2],3),avg=round(avg,3),
          edge=None if nv is None else round(100*(avg-nv),1),med_mc=s['mc']['median'],med_bias=s['bias']['median'],med_gr=s['gr']['median'],
          med_ok=all(s[x]['median']>=r for x in ('mc','bias','gr'))))
df=pd.DataFrame(rows); df.to_csv('bg_price_table.csv',index=False); pd.set_option('display.width',250); print(df.to_string())

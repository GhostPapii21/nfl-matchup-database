"""Shared grader: v5 PRIMARY and v5.1 graded identically from nflverse player-game outcomes (written after v5.1 lock)."""
import pandas as pd, numpy as np
B='../../'
pg=pd.read_csv('../data/player_games_2026.csv')
def dec(a): return np.where(a>0,1+a/100,1+100/np.abs(a))
def grade(d):
    d=d.copy(); m=d.merge(pg[['week','gsis','rushyds','recyds','rushrecyds']],on=['week','gsis'],how='left')
    d['actual']=[r[r.market] if pd.notna(r.get(r.market)) else np.nan for _,r in m.iterrows()]
    d['result']=np.select([d.actual.isna(),d.actual==d.line,(d.side=='over')==(d.actual>d.line)],['UNRESOLVED','PUSH','WIN'],'LOSS')
    d.loc[d.price.abs()<100,'price']=np.nan  # invalid American odds (e.g. Sadiq -6) = unpriced, as v5 grade.py
    pr=d.price.notna()&d.result.isin(['WIN','LOSS'])
    d['pl']=np.where(pr,np.where(d.result=='WIN',10*(dec(d.price.fillna(-110))-1),-10),np.nan)
    d['split']=np.where(d.week<=6,'train(3-6)','holdout(7-8)'); return d
def summ(d,keys):
    f=lambda x: pd.Series({'W':(x.result=='WIN').sum(),'L':(x.result=='LOSS').sum(),'hit':(x.result=='WIN').sum()/max(1,x.result.isin(['WIN','LOSS']).sum()),'priced':x.pl.notna().sum(),'pl':x.pl.sum(),'roi':x.pl.sum()/max(1,10*x.pl.notna().sum())})
    return d.groupby(keys).apply(f,include_groups=False).round(3)
g5=pd.read_csv(B+'yardage_markets_wk3_8/v5/graded_picks.csv')
v5=grade(g5[g5.tag.isin(['SAVED_READ','RECONSTRUCTED'])][['week','game_id','gsis','player','market','side','line','price','confidence','verdict']])
v51=grade(pd.read_csv('out/v5_1_picks.csv'))
# ablation (not pre-registered, diagnostic): gate only at original v5 prices
r=pd.read_csv('data/v5_reads.csv'); k=r[r.tag.isin(['SAVED_READ','RECONSTRUCTED'])&(r.confidence=='strong')&(r.verdict=='agree')]
abl=grade(k[['week','game_id','gsis','player','market','side','line','price']])
v6=pd.read_csv(B+'v6_brainstorm_proedge/graded_picks.csv'); v6=v6[v6.bucket.str.startswith('a_wk3-8')]
v6['split']=np.where(v6.week<=6,'train(3-6)','holdout(7-8)')
bl=pd.read_csv(B+'yardage_markets_wk3_8/v5/graded_baseline.csv'); bl['split']=np.where(bl.week<=6,'train(3-6)','holdout(7-8)')
rows=[]
for name,d in [('v5 PRIMARY',v5),('v5.1 (locked)',v51),('ablation: strong+agree @v5 price',abl),('v6 READS',v6[v6.origin=='READ']),('v6 GATED',v6[v6.gate=='PASS']),('rush-under baseline',bl)]:
    for sp in ['train(3-6)','holdout(7-8)']:
        x=d[d.split==sp]; s=summ(x.assign(k=1),['k']).iloc[0]; rows.append([name,sp,int(s.W),int(s.L),s.hit,int(s.priced),round(s.pl,2),s.roi])
T=pd.DataFrame(rows,columns=['set','split','W','L','hit','priced','pl','roi'])
# slips
sl=pd.read_csv('out/v5_1_slips.csv'); sl=grade(sl)
def slipres(x):
    if (x.result=='LOSS').any(): return -10.0
    live=x[x.result=='WIN']; return 10*(np.prod(dec(live.price))-1) if len(live) else 0.0
S=sl.groupby(['slip_id','week']).apply(slipres,include_groups=False).rename('pl').reset_index()
S5=pd.read_csv(B+'yardage_markets_wk3_8/v5/graded_slips_PRIMARY.csv')
sw=pd.DataFrame({'v5.1_slips_won':S.groupby('week').pl.apply(lambda p:f"{(p>0).sum()}/{len(p)}"),'v5.1_pl':S.groupby('week').pl.sum().round(2),
 'v5_slips_won':S5.groupby('week').won.apply(lambda p:f"{p.sum()}/{len(p)}"),'v5_pl':S5.groupby('week').pl.sum().round(2)})
out=["# v5 vs v5.1 (shared harness)\n","## Side by side\n",T.to_markdown(index=False),
"\n## v5.1 by week\n",summ(v51,['week']).to_markdown(),"\n## v5 PRIMARY by week (harness regrade)\n",summ(v5,['week']).to_markdown(),
"\n## v5.1 by split x market x side\n",summ(v51,['split','market','side']).to_markdown(),
"\n## v5.1 by split x side\n",summ(v51,['split','side']).to_markdown(),
"\n## Slips by week ($10, 3-4 legs; v5.1 FanDuel-style product of saved prices)\n",sw.to_markdown()]
open('out/results.md','w').write("\n".join(out)); v51.to_csv('out/v5_1_graded.csv',index=False); print("\n".join(out))

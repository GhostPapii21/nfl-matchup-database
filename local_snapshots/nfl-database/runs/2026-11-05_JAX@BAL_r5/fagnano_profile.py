# Fagnano vs BUF (2026_08_BAL_BUF), all dropbacks; nflverse pbp + FTN charting (r2/src)
import pandas as pd
g=pd.read_pickle('/tmp/fag.pkl')
g['blitz']=g.n_blitzers.gt(0).map({True:'blitzed',False:'not blitzed'})
g['press']=((g.sack==1)|(g.qb_hit==1)|(g.qb_scramble==1)).map({True:'pressure PROXY',False:'clean PROXY'})
def band(a):
    if pd.isna(a): return 'no target'
    return 'short <10' if a<10 else ('intermediate 10-19' if a<20 else 'deep 20+')
g['air']=g.air_yards.map(band)
def res(r):
    if r.sack==1: return 'SACK'
    if r.qb_scramble==1: return f'SCRAMBLE {r.rushing_yards:.0f}'
    if r.interception==1: return 'INT'
    if r.complete_pass==1: return f'C {r.passing_yards:.0f}'
    return 'INC'
g['result']=g.apply(res,axis=1)
log=g[['qtr','time','down','ydstogo','n_blitzers','n_pass_rushers','press','receiver_player_name','air_yards','result','desc']]
log.to_csv('fagnano_throw_log.csv',index=False)
def sp(d):
    a=d[(d.pass_attempt==1)&(d.sack!=1)]
    return pd.Series(dict(db=len(d),att=len(a),cmp=int(a.complete_pass.sum()),cmp_pct=round(100*a.complete_pass.mean(),1) if len(a) else None,
      sacks=int(d.sack.sum()),sack_rate=round(100*d.sack.mean(),1),ypa=round(a.passing_yards.fillna(0).sum()/len(a),1) if len(a) else None,INT=int(a.interception.sum())))
rows=[]
for k in ['blitz','press','air']:
    for v,d in g.groupby(k): rows.append(dict(split=k,value=v,**sp(d)))
rows.append(dict(split='all',value='all',**sp(g)))
S=pd.DataFrame(rows); S.to_csv('fagnano_splits.csv',index=False)
t=g[g.receiver_player_name.notna()&(g.sack!=1)]
T=t.groupby('receiver_player_name').apply(lambda d:pd.Series(dict(tgt=len(d),rec=int(d.complete_pass.sum()),yds=int(d.passing_yards.fillna(0).sum()),
  tgt_blitzed=int((d.blitz=='blitzed').sum()),tgt_pressure=int((d.press=='pressure PROXY').sum()),
  short=int((d.air=='short <10').sum()),inter=int((d.air=='intermediate 10-19').sum()),deep=int((d.air=='deep 20+').sum()),aDOT=round(d.air_yards.mean(),1)))).sort_values('tgt',ascending=False)
T.to_csv('fagnano_profile.csv')
with open('/tmp/fp.txt','w') as o:
    o.write(S.to_markdown(index=False)+'\n\n'+T.to_markdown()+'\n\n'+log.to_markdown(index=False))
print(open('/tmp/fp.txt').read())

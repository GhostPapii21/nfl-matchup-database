"""v6 Stage B: run ONLY after lock commit. Reuses v4 grade()/summary() unchanged (imported)."""
import sys,math,pandas as pd,numpy as np
from common import *
sys.path.insert(0,str(DB/'backtests/yardage_markets_wk3_8/v4'));import grade as g4
pb=clean(pd.read_parquet(PB26))
P=pd.read_csv(ROOT/'locked_picks.csv')
G=g4.grade(P,pb);G['ou']=G.side
G.to_csv(ROOT/'graded_picks.csv',index=False)
READS=G[G.origin=='READ'];GATED=G[G.gate.isin(['PASS','FLAG'])]
# baselines (all main rush-yds unders): wk3-8 saved, wk1-2 stand-in
q=pd.concat([pd.read_csv(V4/f'w{w}/props_main.csv') for w in range(3,9)]);q=q.sort_values(['snap','book','candidate_id']).drop_duplicates(['week','game','player','market','side'],keep='last')
B=g4.grade(q[(q.market=='rushyds')&(q.side=='under')&(q.tier=='main')],pb)
s=pd.concat([pd.read_csv(ROOT/f'packs/w{w}/props_standin.csv') for w in (1,2)]);B12=g4.grade(s[(s.market=='rushyds')&(s.side=='under')],pb)
B.to_csv(ROOT/'graded_baseline_wk3-8.csv',index=False);B12.to_csv(ROOT/'graded_baseline_wk1-2_standin.csv',index=False)
def hr(d):
    st=d[d.result.isin(['WIN','LOSS'])];return f"{(st.result=='WIN').sum()}-{(st.result=='LOSS').sum()} ({(st.result=='WIN').mean()*100:.1f}%)" if len(st) else 'n=0'
def roi(d):
    st=d[d.result.isin(['WIN','LOSS'])&d.pl.notna()];return f"{st.pl.sum():+.2f} on {len(st)} ({st.pl.sum()/len(st)/10*100:+.1f}%)" if len(st) else 'n/a'
def tab(d,keys):
    rows=[]
    for k,x in d.groupby(keys):rows.append(dict(zip(keys,k if isinstance(k,tuple) else (k,)))|dict(W_L=hr(x),pl_roi=roi(x),unres=int((x.result=='UNRESOLVED').sum())))
    return pd.DataFrame(rows).to_string(index=False) if rows else 'none'
def slips(df,lo,hi,per=5,priced=True):
    out=[]
    for w,g in df.groupby('week'):
        pool=g[g.result.isin(['WIN','LOSS','PUSH'])&(g.decimal.notna() if priced else True)].sort_values(['game','player']).drop_duplicates('player').to_dict('records');n=0
        while len(pool)>=lo and n<per:
            sel=[];c=set()
            for r in pool:
                if r['game'] not in c:sel.append(r);c.add(r['game'])
                if len(sel)==hi:break
            if len(sel)<lo:break
            nmz={r['player'] for r in sel};pool=[r for r in pool if r['player'] not in nmz]
            lost=any(r['result']=='LOSS' for r in sel);od=math.prod(r['decimal'] for r in sel if r['result']!='PUSH') if priced else float('nan')
            out.append(dict(week=w,legs=len(sel),players=';'.join(f"{r['player']} {r['market']} {r['side']} {r['line']}" for r in sel),product_decimal=round(od,2) if priced else None,won=int(not lost),pl=(-10 if lost else round(10*(od-1),2)) if priced else None));n+=1
    return pd.DataFrame(out)
sec=['# v6 graded results (separate buckets; never blended)']
for name,S in [('READS (every Grok edge leg, pre-gate)',READS),('GATED (PASS+FLAG after data check, incl. mirror overs)',GATED)]:
    a=S[(S.week>=3)];b=S[S.week<=2]
    sec+=[f'## {name}',
      '### (a) 2026 wk3-8 priced (ROI on priced legs only; hit rate on all settled)','```\nall: '+hr(a)+' | ROI '+roi(a)+'\n'+tab(a,['week'])+'\n\n'+tab(a,['market'])+'\n\n'+tab(a,['ou'])+'\n\n'+tab(a,['gate'])+'\n```',
      '### (b) 2026 wk1-2 STAND-IN lines (hit rate only)','```\nall: '+hr(b)+'\n'+tab(b,['week'])+'\n\n'+tab(b,['market'])+'\n\n'+tab(b,['ou'])+'\n```']
    for lo,hi in[(3,4),(6,7)]:
        sa=slips(a,lo,hi);sb=slips(b,lo,hi,priced=False);sa.to_csv(ROOT/f"graded_slips_{name.split()[0]}_{lo}-{hi}_wk3-8.csv",index=False);sb.to_csv(ROOT/f"graded_slips_{name.split()[0]}_{lo}-{hi}_wk1-2.csv",index=False)
        sec+=[f'### slips {lo}-{hi} legs ({name.split()[0]})','```\nwk3-8 priced: '+(sa.groupby('week').agg(slips=('won','size'),won=('won','sum'),pl=('pl','sum')).to_string()+f"\ntotal {int(sa.won.sum())}/{len(sa)} won, P&L {sa.pl.sum():+.2f}" if len(sa) else 'none')+
          '\nwk1-2 stand-in (hit only): '+(sb.groupby('week').agg(slips=('won','size'),won=('won','sum')).to_string() if len(sb) else 'none')+'\n```']
sec+=['## Baselines: every main rush-yds under','```\nwk3-8 saved: '+hr(B)+' ROI '+roi(B)+'\n'+tab(B,['week'])+'\nwk1-2 stand-in: '+hr(B12)+'\n```']
# (d) saved pre-kick reads vs reconstructed on same games
sv=pd.read_csv(DB/'backtests/yardage_markets_wk3_8/v5/graded_picks.csv');sv=sv[sv.tag=='SAVED_READ']
sg=set(zip(sv.week,sv.game))
on=READS[[ (w,gm) in sg for w,gm in zip(READS.week,READS.game)]];off=READS[[ (w,gm) not in sg for w,gm in zip(READS.week,READS.game)]]
sec+=['## (d) saved pre-kick reads vs reconstructed','```\nSAVED_READ (Ghost6 13d41b9 + w8 checklists, graded in v5): '+hr(sv)+' ROI '+roi(sv)+'\nv6 Grok on the same saved-read games: '+hr(on)+' ROI '+roi(on)+'\nv6 Grok RECONSTRUCTED, all other wk3-8 games: '+hr(off[off.week>=3])+' ROI '+roi(off[off.week>=3])+'\n```']
(ROOT/'results.md').write_text('\n\n'.join(sec)+'\n');print('\n\n'.join(sec))

"""v6 2025 Stage B (bucket c: hit rate only, HINDSIGHT RISK). Run ONLY after 2025 lock commit."""
import sys,pandas as pd
from common import *
sys.path.insert(0,str(DB/'backtests/yardage_markets_wk3_8/v4'));import grade as g4
pb=clean(pd.read_parquet(PB25))
P=pd.read_csv(ROOT/'locked_picks_2025.csv');G=g4.grade(P,pb);G['ou']=G.side;G.to_csv(ROOT/'graded_picks_2025.csv',index=False)
s=pd.concat([pd.read_csv(ROOT/f'packs25/w{w}/props_standin.csv') for w in range(2,19)]);B=g4.grade(s[(s.market=='rushyds')&(s.side=='under')],pb);B.to_csv(ROOT/'graded_baseline_2025_standin.csv',index=False)
import importlib.util
def hr(d):
    st=d[d.result.isin(['WIN','LOSS'])];return f"{(st.result=='WIN').sum()}-{(st.result=='LOSS').sum()} ({(st.result=='WIN').mean()*100:.1f}%)" if len(st) else 'n=0'
def tab(d,k):
    return pd.DataFrame([dict(zip(k,x if isinstance(x,tuple) else (x,)))|dict(W_L=hr(y)) for x,y in d.groupby(k)]).to_string(index=False) if len(d) else 'none'
def slips(df,lo,hi,per=5):
    out=[]
    for w,g in df.groupby('week'):
        pool=g[g.result.isin(['WIN','LOSS','PUSH'])].sort_values(['game','player']).drop_duplicates('player').to_dict('records');n=0
        while len(pool)>=lo and n<per:
            sel=[];c=set()
            for r in pool:
                if r['game'] not in c:sel.append(r);c.add(r['game'])
                if len(sel)==hi:break
            if len(sel)<lo:break
            pool=[r for r in pool if r['player'] not in {x['player'] for x in sel}]
            out.append(dict(week=w,legs=len(sel),won=int(not any(r['result']=='LOSS' for r in sel))));n+=1
    return pd.DataFrame(out)
sec=['# v6 2025 bucket (c) — HINDSIGHT RISK, STAND-IN median lines, hit rate only (no ROI)']
for name,S in [('READS',G[G.origin=='READ']),('GATED',G[G.gate.isin(['PASS','FLAG'])])]:
    sec+=[f'## {name}','```\nall: '+hr(S)+'\n'+tab(S,['week'])+'\n\n'+tab(S,['market'])+'\n\n'+tab(S,['ou'])+'\n```']
    for lo,hi in[(3,4),(6,7)]:
        sl=slips(S,lo,hi);sl.to_csv(ROOT/f'graded_slips_2025_{name}_{lo}-{hi}.csv',index=False)
        sec+=[f'### slips {lo}-{hi} ({name}, hit only)','```\n'+(sl.groupby('week').agg(slips=('won','size'),won=('won','sum')).to_string()+f"\ntotal {int(sl.won.sum())}/{len(sl)}" if len(sl) else 'none')+'\n```']
sec+=['## Baseline every rush-yds under (stand-in)','```\n'+hr(B)+'\n```']
(ROOT/'results_2025.md').write_text('\n\n'.join(sec)+'\n');print('\n\n'.join(sec))

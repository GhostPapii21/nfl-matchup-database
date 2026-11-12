"""Overlay: re-score build.py legs under the Nov 3 parent rules (anchored p from FD no-vig, avg3 weights a/b copied
from nfl-db-review config/market_anchor_weights.json; sims flag only; bar +5 / +7 backup-QB/injury-role/depth;
§7 3-of-4 kept; N1; no TD/pass yds). CLV fields recorded for every candidate."""
import json, math, csv, pandas as pd
A,B=-0.014863178010206913,0.022983299151190368
lg=lambda p:math.log(max(min(p,1-1e-6),1e-6)/(1-max(min(p,1-1e-6),1e-6)))
cal=lambda s,n:1/(1+math.exp(-(lg(n)+A+B*(lg(s)-lg(n)))))
d=json.load(open('legs.json')); out=[]
INJ={'Justice Hill','Bhayshul Tuten','Travis Etienne Jr.'}
for L in d['legs']:
    ps=[v for v in (L['p'].values() if isinstance(L['p'],dict) else [L['p']]) if isinstance(v,(int,float))]
    s=sum(ps)/len(ps) if ps else None; nv=L['no_vig']
    if s is None or nv is None: continue
    pa=cal(s,nv); e=pa-nv
    bar=7 if (L['team']=='BAL' or L['player'] in INJ or L.get('wr_rank',0) and L.get('wr_rank',0)>=2) else 5
    why=[]
    if e*100<bar: why.append(f'anchored edge {e*100:+.2f} < +{bar}')
    if any('§7' in w for w in L['why']): why+= [w for w in L['why'] if '§7' in w]
    if any(w.startswith('#3/#4') or 'DEPTH' in w for w in L['why']): why+= [w for w in L['why'] if w.startswith('#3/#4') or 'DEPTH' in w]
    flags=[w for w in L['why'] if 'sim' in w or 'min model' in w]
    out.append(dict(player=L['player'],team=L['team'],market=L['market'],side=L['side'],line=L['line'],rung=L['rung'],price=L['price'],
        fd_no_vig=round(nv,4),sim_avg3=round(s,4),raw_edge=round((s-nv)*100,1),anchored_p=round(pa,4),anchored_edge=round(e*100,2),bar=bar,
        status='PASS' if not why else 'CUT',cut=why,sim_flags=flags,clv_open_price=L['price'],clv_close_price=None))
pd.DataFrame(out).to_csv('policy_legs.csv',index=False); json.dump(out,open('policy_legs.json','w'),indent=1)
df=pd.DataFrame(out); print(df.status.value_counts()); print('max anchored edge',df.anchored_edge.max())
print(df.sort_values('raw_edge',ascending=False).head(12)[['player','market','side','line','price','fd_no_vig','sim_avg3','raw_edge','anchored_edge','bar','status']].to_string())

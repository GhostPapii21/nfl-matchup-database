"""Test C: same pool + same slip method as grade_slips.py (code copied verbatim), only sizes changed to k=4,5. No network."""
"""Step 4: door leg_rules, grading, slips (method fixed in SLIP_METHOD below BEFORE results were looked at), door stamps, tables."""
import os,sys,json,re,glob,itertools,numpy as np,pandas as pd
from datetime import datetime,timedelta
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ROOT='/workspace/nfl-database'
os.environ['DOOR_OUT']=f'{HERE}/door_out/wk6'; sys.path.insert(0,f'{ROOT}/tools'); sys.path.insert(0,ROOT)
import door
SLIP_METHOD="""Pool = legs that PASS the in-process gate at leg level (no leg-named miss) AND have no door.leg_rules BLOCK.
One leg per player (highest raw edge avg(p)-no_vig; ties -> shorter price). No TD markets exist in the pool. Sort pool by raw edge desc.
M1 cross-game greedy: walk the sorted pool, put each leg in the first open slip that has no leg from the same game; close a slip at size k.
M2 sequential chunks: consecutive chunks of k from the sorted pool (same-game allowed; real SGP pricing would be lower than product of prices).
Sizes: Test A k=3,4; Test B k=6,7. Each leg used at most once per (method,k). Incomplete last slip dropped.
Depth receivers (WR3/4, TE2+ overs) only if rung=low (door DEPTH_RECEIVER enforces this); max 1 per slip enforced in M1 (skip to next slip).
Price = product of decimal prices of the leg's own book; push/void legs drop out (slip reprices on remaining legs; all void = refund). $10 stake per slip."""
os.chdir(HERE)
G=pd.read_csv('gate_results.csv'); base=G[G.variant=='base']
MAN={}
def man(run):
    if run not in MAN: MAN[run]=json.load(open(f'{run}/run_manifest.json'))
    return MAN[run]
dec=lambda a:1+(a/100 if a>0 else 100/-a)
L=pd.read_csv('graded_legs.csv',keep_default_na=False,na_values=['']); L['door_block']=L['door_block'].fillna('')
L['pool']=L['pool'].astype(str)=='True'; L['depth']=L['depth'].astype(str)=='True'
print('pool',L.pool.sum())
# gate results for door.run_gate patch
GR={}
for run,x in base.groupby('run'):
    out=open(f'{run}/gate_output.txt').read(); se=out.split('SCHEME_EDGE ALERT:',1)[1] if 'SCHEME_EDGE ALERT:' in out else ''
    GR[run]=dict(strict=dict(ok=bool(x.strict_ok.all()),live=list(x[x.leg_pass].leg),out=out,scheme_alert=se),
                 leglevel=dict(ok=True,live=list(x[x.leg_pass].leg),out=out+'\n[harness] ok=True at LEG LEVEL: run-level film miss reported separately\n',scheme_alert=se))
MODE=['strict']; door.run_gate=lambda rd,now:GR[rd][MODE[0]]
LEDGER={}; _led=door.ledger
def led():
    if 'r' not in LEDGER: LEDGER['r']=_led()
    return LEDGER['r']
door.ledger=led   # harness: run the real ledger check once and reuse the result (same code, same files)
def build_slips(pool,k,meth):
    pool=pool.sort_values(['raw_edge','price'],ascending=[False,True]).drop_duplicates('gsis')
    S=[]
    if meth=='M2':
        v=pool.to_dict('records'); S=[v[i:i+k] for i in range(0,len(v)-k+1,k)]
    else:
        openS=[]
        for x in pool.to_dict('records'):
            for s in openS:
                if x['game'] in {y['game'] for y in s}: continue
                if x['depth'] and any(y['depth'] for y in s): continue
                s.append(x); break
            else: openS.append([x])
            done=[s for s in openS if len(s)==k]; S+=done; openS=[s for s in openS if len(s)<k]
    return S
SL=[]
for W in (6,7,8,9):
    pool=L[(L.week==W)&L.pool]; door.OUT=f'{HERE}/door_out/wk{W}'
    for test,ks in (('C',(4,5)),):
        for k in ks:
            for meth in ('M1','M2'):
                for i,s in enumerate(build_slips(pool,k,meth)):
                    res=[x['result'] for x in s]; live=[x for x in s if x['result'] in('win','loss')]
                    if any(r=='loss' for r in res): out='loss'; pr=-10
                    elif not live: out='refund'; pr=0
                    else: out='win'; pr=10*(np.prod([dec(x['price']) for x in live])-1)
                    sid=f'wk{W}_{test}_{meth}_k{k}_{i:02d}'; slip=dict(slip_id=sid,date=str(W),sport='NFL',legs=[dict(run=x['run'],leg=x['leg']) for x in s])
                    now=datetime.fromisoformat(man(s[0]['run'])['kickoff_et'])-timedelta(minutes=30)
                    st={}
                    for mode in ('strict','leglevel'):
                        MODE[0]=mode; b=door.build(slip,now,write=False); st[mode]=(b['status'],sorted({f['rule'] for f in b['blocking']}),sorted({f['rule'] for f in b['fails'] if f['sev']!='BLOCK'}))
                    SL.append(dict(week=W,test=test,method=meth,k=k,slip_id=sid,legs=' | '.join(x['leg'] for x in s),results=' '.join(res),outcome=out,stake=10,profit=round(pr,2),
                        dec_price=round(np.prod([dec(x['price']) for x in s]),3),killers=' | '.join(f"{x['market']} {x['side']}" for x in s if x['result']=='loss'),
                        door_strict=st['strict'][0],door_strict_block=';'.join(st['strict'][1]),door_leglevel=st['leglevel'][0],door_leglevel_block=';'.join(st['leglevel'][1]),door_warn=';'.join(st['leglevel'][2])))
S=pd.DataFrame(SL); S.to_csv('test_c_4to5/slips.csv',index=False)
print(S.groupby(['method','k']).agg(n=('profit','size'),won=('outcome',lambda x:(x=='win').sum()),pl=('profit','sum')))
print(S.groupby(['door_strict','door_strict_block']).size()); print(S.groupby(['door_leglevel','door_leglevel_block']).size())

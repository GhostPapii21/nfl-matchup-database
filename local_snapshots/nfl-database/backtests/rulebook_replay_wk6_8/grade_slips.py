"""Step 4: door leg_rules, grading, slips (method fixed in SLIP_METHOD below BEFORE results were looked at), door stamps, tables."""
import os,sys,json,re,glob,itertools,numpy as np,pandas as pd
from datetime import datetime,timedelta
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT='/workspace/nfl-database'
os.environ['DOOR_OUT']=f'{HERE}/door_out/wk6'; sys.path.insert(0,f'{ROOT}/tools'); sys.path.insert(0,ROOT)
import door
SLIP_METHOD="""Pool = legs that PASS the in-process gate at leg level (no leg-named miss) AND have no door.leg_rules BLOCK.
One leg per player (highest raw edge avg(p)-no_vig; ties -> shorter price). No TD markets exist in the pool. Sort pool by raw edge desc.
M1 cross-game greedy: walk the sorted pool, put each leg in the first open slip that has no leg from the same game; close a slip at size k.
M2 sequential chunks: consecutive chunks of k from the sorted pool (same-game allowed; real SGP pricing would be lower than product of prices).
Sizes: Test A k=3,4; Test B k=6,7. Each leg used at most once per (method,k). Incomplete last slip dropped.
Depth receivers (WR3/4, TE2+ overs) only if rung=low (door DEPTH_RECEIVER enforces this); max 1 per slip enforced in M1 (skip to next slip).
Price = product of decimal prices of the leg's own book; push/void legs drop out (slip reprices on remaining legs; all void = refund). $10 stake per slip."""
G=pd.read_csv('gate_results.csv'); base=G[G.variant=='base']
MAN={}; 
def man(run):
    if run not in MAN: MAN[run]=json.load(open(f'{run}/run_manifest.json'))
    return MAN[run]
P=pd.read_parquet(f'{ROOT}/runs/2026-11-02_shared_src/play_by_play_2026.parquet'); P=P[(P.season_type=='REG')&(P.two_point_attempt!=1)]
pa=P[(P.pass_attempt==1)&(P.sack!=1)]; ru=P[P.rush_attempt==1]
ACT={}
for g,x in pa.groupby(['passer_player_id','game_id']): ACT[(g[0],g[1],'passyds')]=x.passing_yards.fillna(0).sum()
for g,x in pa.groupby(['receiver_player_id','game_id']): ACT[(g[0],g[1],'rec')]=x.complete_pass.sum(); ACT[(g[0],g[1],'recyds')]=x.receiving_yards.fillna(0).sum()
for g,x in ru.groupby(['rusher_player_id','game_id']): ACT[(g[0],g[1],'rushyds')]=x.rushing_yards.fillna(0).sum()
APP={(a,b) for a,b,_ in ACT}
PL=pd.read_parquet(f'{ROOT}/runs/2026-11-02_shared_src/players.parquet'); G2E=PL.dropna(subset=['espn_id']).set_index('gsis_id').espn_id.map(lambda x:str(x).replace('.0','')).to_dict()
E=json.load(open('espn/401873036.json')); MB={}
for t in E['boxscore']['players']:
    for s in t['statistics']:
        for a in s['athletes']:
            st=dict(zip(s['keys'],a['stats'])); i=str(a['athlete']['id'])
            if s['name']=='passing': MB[(i,'passyds')]=float(st['passingYards'])
            if s['name']=='rushing': MB[(i,'rushyds')]=float(st['rushingYards'])
            if s['name']=='receiving': MB[(i,'rec')]=float(st['receptions']); MB[(i,'recyds')]=float(st['receivingYards'])
MBP={i for i,_ in MB}
def actual(l,W,gid):
    if W==9:
        e=G2E.get(l['gsis']); 
        if e not in MBP: return None
        return MB.get((e,l['market']),0.0)
    if (l['gsis'],gid) not in APP: return None
    return float(ACT.get((l['gsis'],gid,l['market']),0.0))
dec=lambda a:1+(a/100 if a>0 else 100/-a)
rows=[]
for r in base.itertuples():
    m=man(r.run); l=next(x for x in m['legs'] if x['name']==r.leg); a=actual(l,r.week,m['game_id'])
    res='void' if a is None else ('push' if a==l['line'] else ('win' if (a>l['line'])==(l['side']=='over') else 'loss'))
    door.OUT=f'{HERE}/door_out/wk{r.week}'; fr=door.leg_rules(r.leg,l,m); blk=[f['rule'] for f in fr if f['sev']=='BLOCK']; flg=[f['rule'] for f in fr if f['sev']!='BLOCK']
    sims={s['model']:s['legs'][r.leg] for s in m['sims']}; ps=[v['p'] for v in sims.values()]
    rows.append(dict(week=r.week,game=r.game,run=r.run,leg=r.leg,player=l['player'],gsis=l['gsis'],team=l['team'],type=l['type'],market=l['market'],side=l['side'],line=l['line'],rung=l['rung'],
        price=l['price'],no_vig=l['no_vig'],no_vig_note=l['no_vig_note'],p_avg=np.mean(ps),raw_edge=np.mean(ps)-l['no_vig'],gate_leg_pass=r.leg_pass,gate_misses=r.leg_misses,
        scheme_edge_flag=bool(r.scheme_note),depth=door.depth_rule.is_depth(l) and l['side']=='over',door_block=';'.join(blk),door_flag=';'.join(flg),
        injury_status=l['injury_status'],actual=a,result=res,profit_single=(10*(dec(l['price'])-1) if res=='win' else -10 if res=='loss' else 0.0)))
L=pd.DataFrame(rows); L['pool']=L.gate_leg_pass&(L.door_block=='')
L.to_csv('graded_legs.csv',index=False); print('legs',len(L),'gate pass',L.gate_leg_pass.sum(),'pool',L.pool.sum())
# rule matrix
def keys(s): return sorted({re.sub(r'[\d\.\-+%]+','#',re.sub(r'^leg .*?: ','',x)).split(' (')[0][:70] for x in str(s).split(' || ') if x and x!='nan'})
RM=[]
for r in L.itertuples():
    d=dict(week=r.week,leg=r.leg,gate_leg_pass=r.gate_leg_pass,door_block=r.door_block,pool=r.pool,result=r.result)
    for k in keys(r.gate_misses): d['GATE: '+k]=1
    for k in r.door_block.split(';'):
        if k: d['DOOR: '+k]=1
    RM.append(d)
pd.DataFrame(RM).fillna(0).to_csv('rule_matrix.csv',index=False)
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
    for test,ks in (('A',(3,4)),('B',(6,7))):
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
S=pd.DataFrame(SL); S.to_csv('slips.csv',index=False)
open('slip_method.txt','w').write(SLIP_METHOD)
print(S.groupby(['test','method','k']).agg(n=('profit','size'),won=('outcome',lambda x:(x=='win').sum()),pl=('profit','sum')))
print(S.groupby(['door_strict','door_strict_block']).size()); print(S.groupby(['door_leglevel','door_leglevel_block']).size())

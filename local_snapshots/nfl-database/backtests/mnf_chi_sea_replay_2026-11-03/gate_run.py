"""Run the real Gate on run/ (rules forced active via gate_replay harness import), then depth_rule.evaluate per depth leg, then grade vs ESPN box."""
import os,sys,json,re,importlib.util
from datetime import datetime,timedelta
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT='/workspace/nfl-database'
os.chdir(f'{ROOT}/backtests/rulebook_replay_wk6_8')
spec=importlib.util.spec_from_file_location('gr',f'{ROOT}/backtests/rulebook_replay_wk6_8/gate_replay.py'); GR=importlib.util.module_from_spec(spec); spec.loader.exec_module(GR)
os.chdir(HERE); sys.path.insert(0,f'{ROOT}/tools'); import depth_rule
RUN=f'{HERE}/run'; m=json.load(open(f'{RUN}/run_manifest.json'))
# keep the target-share pool pointing at current leg names
nm={(l['player'],l['market'],l['side'],l['rung']):l['name'] for l in m['legs']}
for p in m.get('target_share_pool',{}).get('players',[]):
    old=p.get('leg'); mk=old.split()[-3]; p['leg']=nm.get((p['name'],mk,'over','main'),old)
json.dump(m,open(f'{RUN}/run_manifest.json','w'),indent=1,default=str)
now=datetime.fromisoformat(m['kickoff_et'])-timedelta(minutes=30)
g=GR.gate(RUN,now); names=[l['name'] for l in m['legs']]; by,run=GR.classify(g,names)
ACT={('Colston Loveland','rec'):7,('Colston Loveland','recyds'):65,('Luther Burden III','rec'):7,('Luther Burden III','recyds'):56,('Rome Odunze','rec'):4,('Rome Odunze','recyds'):87,
 ('Kalif Raymond','rec'):2,('Kalif Raymond','recyds'):14,('Jaxon Smith-Njigba','rec'):6,('Jaxon Smith-Njigba','recyds'):118,('Cooper Kupp','rec'):1,('Cooper Kupp','recyds'):7,
 ('AJ Barner','rec'):2,('AJ Barner','recyds'):23,("D'Andre Swift",'rec'):2,("D'Andre Swift",'recyds'):10,("D'Andre Swift",'rushyds'):69,('Roschon Johnson','rushyds'):17,
 ('Roschon Johnson','rec'):1,('Roschon Johnson','recyds'):11,('Caleb Williams','passyds'):247,('Sam Darnold','passyds'):188,('Tory Horton','rec'):3,('Tory Horton','recyds'):26,
 ('Jadarian Price','rec'):2,('Jadarian Price','recyds'):8,('Jadarian Price','rushyds'):29,('Sam Darnold','rushyds'):20,('Luther Burden III','rushyds'):0}
rows=[];se_names={bd[0].split(' [')[0] for bd in getattr(g,'se_breakdowns',[])}
for l in m['legs']:
    n=l['name']; a=ACT.get((l['player'],l['market'])); hit=None if a is None else (a>l['line'] if l['side']=='over' else a<l['line'])
    pr=l['price']; win=(pr/100 if pr>0 else 100/-pr)
    dr=depth_rule.evaluate(l) if depth_rule.is_depth(l) and l['side']=='over' else None
    p=[g2['legs'][n]['p'] for g2 in m['sims']]; 
    rows.append(dict(leg=n,player=l['player'],market=l['market'],side=l['side'],line=l['line'],rung=l['rung'],price=pr,no_vig=l['no_vig'],p_avg=round(sum(p)/3,3),edge=round(sum(p)/3-l['no_vig'],3),
        gate=('PASS' if not by[n] else 'BLOCK'),scheme_edge_all4=bool(l.get('scheme_edge',{}).get('explanation')),scheme_alert=n in se_names,
        depth=None if dr is None else ('OK' if dr[0] else 'BLOCK: '+'; '.join(dr[1])) if isinstance(dr,tuple) else str(dr),
        actual=a,hit=hit,pnl10=None if hit is None else round(10*win if hit else -10,2),why=' || '.join(re.sub(r'^leg .*?: ','',x) for x in by[n])))
import pandas as pd
D=pd.DataFrame(rows); D.to_csv(f'{HERE}/replay_legs.csv',index=False)
with open(f'{HERE}/gate_output_replay.txt','w') as f:
    f.write(f"in-process Gate now={now:%Y-%m-%d %H:%M} ET, rules forced active\nGATE strict: {'PASS' if not g.miss else 'FAIL'}\nRUN-LEVEL: {run}\n")
    for r in rows: f.write(f"{r['gate']:5s} {r['leg']}: {r['why']}\n")
    f.write('Notes:\n'+'\n'.join('  - '+x for x in g.notes)+'\n')
    for bd in getattr(g,'se_breakdowns',[]): f.write('SCHEME_EDGE ALERT:\n'+'\n'.join(bd)+'\n')
print('run-level',run)
print(D.groupby('gate').agg(n=('leg','size'),hits=('hit','sum'),pnl=('pnl10','sum')))
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',120)
print(D[D.gate=='PASS'][['leg','price','no_vig','p_avg','edge','actual','hit','pnl10']].to_string())
print(D[D.player.isin(['Colston Loveland','Luther Burden III','Rome Odunze','Kalif Raymond'])&(D.side=='over')][['leg','price','no_vig','p_avg','edge','actual','hit','gate','depth','why']].to_string())

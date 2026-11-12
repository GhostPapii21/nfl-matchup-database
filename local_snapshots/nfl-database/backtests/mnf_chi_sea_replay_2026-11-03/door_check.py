"""Read-only door check of replay slips: tools/door.py evaluate() in-process with DOOR_OUT=/tmp/mnf/door_out
(teams/ symlinked read-only to the repo teams/). door.run_gate is replaced by the harness gate result (rules forced active,
now = kickoff-30m, run-level 'film' miss waived) because the CLI uses the real clock. Nothing is written to approved/blocked/."""
import os,sys,json,re,importlib.util
from datetime import datetime,timedelta
os.makedirs('/tmp/mnf/door_out',exist_ok=True)
if not os.path.exists('/tmp/mnf/door_out/teams'): os.symlink('/workspace/nfl-database/teams','/tmp/mnf/door_out/teams')
os.environ['DOOR_OUT']='/tmp/mnf/door_out'
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,'/workspace/nfl-database/tools')
import door, pandas as pd
D=pd.read_csv(f'{HERE}/replay_legs.csv'); live=list(D[D.gate=='PASS'].leg)
door.run_gate=lambda rd,now: dict(ok=True,live=live,out='harness gate (see gate_output_replay.txt)',scheme_alert='')
RUN=f'{HERE}/run'
SLIPS={
 'R1_top_edge_per_player_4leg':["Jaxon Smith-Njigba recyds over 124.5 [high]","Tory Horton recyds under 23.5","Cooper Kupp rec under 2.5","AJ Barner rec under 3.5"],
 'R2_top_edge_per_player_3leg':["Jaxon Smith-Njigba recyds over 124.5 [high]","Tory Horton recyds under 23.5","Cooper Kupp rec under 2.5"],
 'RICO_15_cashed_out_as_built':["AJ Barner rec over 3.5","Jaxon Smith-Njigba recyds over 109.5 [high]","Cooper Kupp recyds over 14.5 [low]","D'Andre Swift rec over 2.5 [low]","Colston Loveland rec over 3.5 [low]","Luther Burden III recyds over 29.5 [low]","Rome Odunze rec over 1.5 [low]"],
}
out={}
for sid,legs in SLIPS.items():
    r=door.evaluate(dict(slip_id=sid,date='2026-11-02',sport='NFL',legs=[dict(run=RUN,leg=x) for x in legs]),datetime(2026,11,2,19,50))
    out[sid]=[dict(rule=f.get('rule') if isinstance(f,dict) else f[0],leg=f.get('leg') if isinstance(f,dict) else f[1],why=f.get('why',f.get('text')) if isinstance(f,dict) else f[-1]) for f in r['fails']]
    print('==',sid,'FAILS:',len(out[sid]))
    for f in out[sid]: print('  ',f)
json.dump(out,open(f'{HERE}/door_check.json','w'),indent=1,default=str)

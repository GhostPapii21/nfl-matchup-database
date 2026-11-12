"""Build locked pick sets (no outcomes). Primary = SAVED_READ where a saved read names an edge leg, else Grok RECONSTRUCTED.
ZONE_MOF: for rec/rushrec legs vs zone-heavy opp (teams/<OPP>.json Sharp Zone Rate>=75; NOTE thru-wk7 snapshot = hindsight on scheme label),
keep over only if opp as-of middle-of-field YPA allowed >= league as-of middle YPA; keep under only if <=. Other legs pass through."""
import json,pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PK=ROOT.parent/'v4'/'packs';TEAMS=ROOT.parents[2]/'teams'
g=pd.read_csv(ROOT/'grok_picks.csv');s=pd.read_csv(ROOT/'saved_picks.csv')
sg=set(zip(s.week,s.game))
g['tag']=['GROK_ON_SAVED_GAME' if (w,gm) in sg else 'RECONSTRUCTED' for w,gm in zip(g.week,g.game)]
s['tag']='SAVED_READ'
allp=pd.concat([g,s],ignore_index=True)
def zr(t):
    try:return json.load(open(TEAMS/f'{t}.json'))['defense']['sharp_thru_wk7_2026_10_29']['Zone Rate']
    except Exception:return None
mid={}
for w in range(3,9):
    pb=pd.read_parquet(PK/f'w{w}/pbp_prior.parquet');pa=pb[(pb.pass_attempt==1)&(pb.pass_location=='middle')]
    lg=pa.yards_gained.mean();
    for t,x in pa.groupby('defteam'):mid[(w,t)]=(x.yards_gained.mean(),lg)
keep=[]
for r in allp.itertuples():
    z=zr(r.opp);k=1;why='not rec/zone'
    if r.market in('recyds','rushrecyds') and z is not None and z>=75 and (r.week,r.opp) in mid:
        m,lg=mid[(r.week,r.opp)];k=int(m>=lg) if r.side=='over' else int(m<=lg);why=f'zone {z}, mid YPA {m:.2f} vs lg {lg:.2f}'
    keep.append((k,z,why))
allp['zone_mof_keep']=[k[0] for k in keep];allp['opp_zone_rate']=[k[1] for k in keep];allp['zone_note']=[k[2] for k in keep]
import proedge
pe=proedge.run(allp);allp=allp.join(pe)
allp['steps']=allp.apply(lambda r:'PRO_EDGE(post-read gate,'+('pass' if r.pe_pass else 'fail')+')>'+('BRAINSTORM(grok-4.7)' if r.tag!='SAVED_READ' else 'SAVED_READ(human)')+'>PHASE_SCRIPT(main line from saved prices; approx)',axis=1)
allp.to_csv(ROOT/'locked_picks.csv',index=False);print(allp.groupby('tag').size(),allp.zone_mof_keep.value_counts())

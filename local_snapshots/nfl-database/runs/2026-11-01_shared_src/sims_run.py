"""Run sim_v5 (3 models x 100k, seed 20261101) for every leg in legs_<tag>.json. Usage: python3 sims_run.py <tag>"""
import json,sys,os,math
import sim_v5 as S
tag=sys.argv[1]; D=json.load(open(f'legs_{tag}.json'))
SLIPR={('Tee Higgins','recyds'):[68.5,49.5,59.5],('CeeDee Lamb','rec'):[4.5,6.5,3.5],('Brock Bowers','recyds'):[49.5],('Amon-Ra St. Brown','rec'):[5.5,6.5,7.5],
 ('Amon-Ra St. Brown','recyds'):[49.5,59.5],('Matthew Stafford','comp'):[22.5],('Kenneth Walker III','rushyds'):[97.5,69.5,79.5],('Puka Nacua','recyds'):[69.5],
 ('Drake London','rec'):[5.5,4.5],('Zay Flowers','recyds'):[49.5,59.5],('Zay Flowers','rec'):[5.5,6.5,4.5],('Denzel Boston','recyds'):[29.5],('Bijan Robinson','rec'):[3.5],
 ('Jaylen Warren','rushrec'):[69.5],('Patrick Mahomes','passyds'):[0.5,223.5],('Jahmyr Gibbs','rec'):[4.5],('Chris Godwin Jr.','rec'):[3.5,2.5],('George Pickens','rec'):[3.5,4.5],
 ('James Cook','rushrec'):[69.5],('CeeDee Lamb','recyds'):[49.5,59.5],('Parker Washington','recyds'):[39.5],('Tee Higgins','rec'):[3.5],('Puka Nacua','rec'):[7.5]}
cache_f='sims_cache.json'; C=json.load(open(cache_f)) if os.path.exists(cache_f) else {}
out={}
for L in D['legs']:
    r=set([L['fd']['point']]+list(map(float,L['alts'])))
    for x in L['pp']+L['ud']+SLIPR.get((L['player'],L['market']),[]):
        x=float(x)
        if x==int(x): r|={x-0.5,x+0.5}
        else: r.add(x)
    if L.get('explicit'): r.add(L['explicit']['line'])
    for b in ('pin','dk'):
        if L.get(b): r.add(L[b]['point'])
    rungs=sorted(r); key=f"{L['player']}|{L['market']}|{L['spread']}|{','.join(map(str,rungs))}"
    if key not in C:
        try: o,i=S.sim(dict(player=L['player'],team=L['team'],opp=L['opp'],market=L['market'],spread=L['spread'],rungs=rungs)); C[key]=dict(sims=o,info=i)
        except Exception as ex: C[key]=dict(error=repr(ex))
        json.dump(C,open(cache_f,'w'),default=float)
    out[f"{L['player']}|{L['market']}"]=dict(key=key,**C[key])
    print(L['player'],L['market'],'ok' if 'sims' in C[key] else C[key]['error'],flush=True)
import hashlib
meta=dict(N=S.N,seed=S.SEED,sd_margin=S.SD_MARGIN,pbp_sha=hashlib.sha256(open(S.SRC+'play_by_play_2026.parquet','rb').read()).hexdigest()[:16],code_sha=hashlib.sha256(open(S.__file__,'rb').read()).hexdigest()[:16])
json.dump(dict(meta=meta,sims=out),open(f'sims_{tag}.json','w'),default=float)

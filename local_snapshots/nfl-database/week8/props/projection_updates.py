"""Data-driven projection updates (never toward the line). Writes proj_overrides.json.
A) Missing-participation denominator (GAME_SCRIPT issue #3): weeks with no offensive snaps in fixes/src/snap_counts_2026.parquet are absent rows,
   volume rescaled by (0.6*L3 + 0.4*season on games played) / (same on all weeks). Only for players whose last game is active (played Wk7 or L3 played>=2).
B) Small-sample efficiency: season targets < 20 -> yds/target regressed to position league YPT (WR 8.1 / TE 6.9 / RB 5.4) with 20-target prior.
Applied only where |model median - FD line| / line > 25% on some market (recheck list); every change is logged."""
import json,re
W='/workspace/nfl-database/week8/'
F=json.load(open(W+'breakdown/full/full.json')); C=json.load(open(W+'props/compare.json')) if False else None
P=json.load(open(W+'props/props.json'))
LG={'WR':8.1,'TE':6.9,'RB':5.4}
GID={'LAC@LAR':'LAC@LA','PHI@WSH':'PHI@WAS'}
lines={}
for r in P['rows']:
    if r['market'] in('rec_yds','receptions','rush_yds','rush_rec_yds') and r['line']!='': lines.setdefault((GID.get(r['game'],r['game']),r['player']),{})[r['market']]=float(r['line'])
MK={'rec_yds':'recyds','receptions':'rec','rush_yds':'rushyds','rush_rec_yds':'tot'}
def parse(log):
    out=[]
    for m in re.finditer(r'W(\d+) (\d+)-(\d+)-(-?\d+)(?:/(\d+)c(-?\d+))?',log):
        w,t,rc,y,c,ry=m.groups(); out.append(dict(w=int(w),t=int(t),r=int(rc),y=int(y),c=int(c or 0),ry=int(ry or 0)))
    return out
import pandas as pd
SN=pd.read_parquet('/workspace/nfl-database/fixes/src/snap_counts_2026.parquet')
nrm=lambda n:re.sub(r'[^a-z]','',re.sub(r'\b(jr|sr|ii|iii|iv)\b\.?','',n.lower()))
SN['k']=SN.player.map(nrm)
SNAP={}
for k,w,o in zip(SN.k,SN.week,SN.offense_snaps): SNAP.setdefault(k,{})[int(w)]=o or 0
ov={}; log=[]
for g in F['games']:
    for t in g['teams']:
        for p in t['players']:
            L=lines.get((g['id'],p['name']))
            if not L: continue
            pr=p['proj']
            if not any(abs(pr[MK[m]]-l)/l>0.25 for m,l in L.items() if l): continue
            gl=parse(p['log']);
            if not gl: continue
            new=dict(pr); why=[]
            sn=SNAP.get(nrm(p['name']))
            played=[x for x in gl if (sn.get(x['w'],0)>0 if sn else (x['t'] or x['c']))]
            l3=gl[-3:]; l3p=[x for x in l3 if x in played]
            vol=lambda xs:(sum(x['c'] for x in xs)/len(xs)) if p['pos']=='RB' and pr['car']>=pr['tgt'] else (sum(x['t'] for x in xs)/len(xs))
            absent=len(gl)-len(played)
            ret=bool(p['q']) and gl[-1] not in played
            if absent and played and (gl[-1] in played or ret) and vol(l3) and vol(gl):
                f=(0.6*vol(l3p or played)+0.4*vol(played))/(0.6*vol(l3)+0.4*vol(gl))
                if abs(f-1)>=0.08:
                    f=min(f,4.0)
                    for k in('tgt','rec','recyds','car','rushyds'): new[k]=round(pr[k]*f,1 if k in('tgt','rec','car') else 0)
                    why.append(f"A: {absent} absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x{f:.2f}"+(" (Questionable, returning from absence: projection assumes he plays; confirm active)" if ret else ""))
            st=sum(x['t'] for x in gl); sy=sum(x['y'] for x in gl)
            if p['pos'] in LG and 0<st<20 and new['tgt']>0 and sy>0:
                raw=sy/st; dm=(pr['recyds']/pr['tgt'])/raw if pr['tgt'] else 1
                reg=(sy+LG[p['pos']]*20)/(st+20)
                if abs(reg/raw-1)>=0.08:
                    new['recyds']=round(new['tgt']*reg*dm); why.append(f"B: {st} season targets, YPT {raw:.1f} regressed to {reg:.1f} (prior {LG[p['pos']]}, 20 tgt)")
            if why:
                new['tot']=round(new['recyds']+new['rushyds']); s=new['tot']/pr['tot'] if pr['tot'] else 1
                new['lo']=round(pr['lo']*s); new['hi']=round(pr['hi']*s)
                ov[f"{g['id']}|{p['name']}"]=dict(old=pr,proj=new,why=why,q=p['q'])
json.dump(ov,open(W+'props/proj_overrides.json','w'),indent=1)
print(len(ov),'updated')
for k,v in ov.items(): print(k,v['old']['tgt'],v['old']['car'],v['old']['recyds'],v['old']['rushyds'],'->',v['proj']['tgt'],v['proj']['car'],v['proj']['recyds'],v['proj']['rushyds'],'|',' ; '.join(v['why']))

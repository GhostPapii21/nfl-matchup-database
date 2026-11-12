"""Step 3: run the real Gate in-process (now = kickoff-30m) with every rule forced active (harness monkeypatch only; no tool file edited)."""
import os,sys,re,json,glob,copy,shutil,io,contextlib
from datetime import datetime,timedelta
ROOT='/workspace/nfl-database'; sys.path.insert(0,f'{ROOT}/tools'); sys.path.insert(0,ROOT)
from rules import rulebook as _rb
import run_gate as RG, srclist_rules, rico4_rules, snf_rules, rico_nov2_rules
FORCE='2000-01-01'
_rb.active=lambda *a,**k: True; RG._rb.active=_rb.active
for mod in (RG,srclist_rules,rico4_rules,snf_rules,rico_nov2_rules):
    if hasattr(mod,'_rb'): mod._rb.active=_rb.active
for k in ('SIMV6_FROM','FORECAST_FROM','COVPROF_FROM'): setattr(RG,k,FORCE)
rico_nov2_rules.NOV2_FROM=FORCE; snf_rules.SNF_FROM=FORCE; rico4_rules.RICO4_FROM=FORCE; srclist_rules.FEEDWEEK_FROM=FORCE
def gate(d,now):
    g=RG.Gate(d,now); g.live=g.cut=[]; g.applied=[]; g.wx_alerts=[]
    try: g.run()
    except Exception as e: g.miss.append(f'GATE EXCEPTION: {type(e).__name__}: {e}')
    return g
def classify(g,names):
    by={n:[] for n in names}; run=[]
    for m in g.miss:
        hit=[n for n in names if re.search(re.escape(n)+r"(?=[: ]|$)",m)]
        if hit: [by[n].append(m) for n in hit]
        else: run.append(m)
    return by,run
REALMISS=re.compile(r'source category film')
def rulekey(m):
    m=re.sub(r'leg .*?: ','',m); return re.sub(r'[\d\.\-+]+','#',m)[:90]
def run_all(variant='base',mutate=None,weeks=None):
    out=[]
    for d in sorted(glob.glob('runs/wk*_*')):
        if '__' in d: continue
        m=json.load(open(f'{d}/run_manifest.json')); W=m['week']
        if weeks and W not in weeks: continue
        dd=d
        if mutate:
            dd=f'variants/{variant}/{os.path.basename(d)}'; os.makedirs(dd,exist_ok=True)
            for f in ('checklist.md','report.md'): shutil.copy(f'{d}/{f}',dd)
            m2=copy.deepcopy(m); mutate(m2); json.dump(m2,open(f'{dd}/run_manifest.json','w'),indent=1,default=str); m=m2
        now=datetime.fromisoformat(m['kickoff_et'])-timedelta(minutes=30)
        g=gate(os.path.abspath(dd),now); names=[l['name'] for l in m['legs']]; by,run=classify(g,names)
        real=[x for x in run if REALMISS.search(x)]; other=[x for x in run if not REALMISS.search(x)]
        with open(f'{dd}/gate_output.txt','w') as f:
            f.write(f"VARIANT {variant} | in-process Gate, now={now:%Y-%m-%d %H:%M} ET | rules forced active (harness)\nGATE strict: {'PASS' if not g.miss else 'FAIL'}\nLive legs (gate): {g.live}\n")
            f.write(f"RUN-LEVEL real missing data: {real}\nRUN-LEVEL other: {other}\n")
            for n in names: f.write(f"LEG {n}: {'PASS' if not by[n] else 'BLOCK'} {by[n]}\n")
            f.write('Notes:\n'+'\n'.join('  - '+x for x in g.notes)+'\n')
            for bd in getattr(g,'se_breakdowns',[]): f.write('SCHEME_EDGE ALERT:\n'+'\n'.join(bd)+'\n')
        se_names={bd[0].split(' [')[0] for bd in getattr(g,'se_breakdowns',[])}
        for n in names:
            out.append(dict(variant=variant,week=W,run=os.path.abspath(dd),game=m['game'],leg=n,gate_live=n in g.live,leg_pass=not by[n],
                            leg_misses=' || '.join(by[n]),run_real_miss=' || '.join(real),run_other_miss=' || '.join(other),strict_ok=not g.miss,scheme_alert=n in se_names,
                            scheme_note=any(x.startswith(n+': SCHEME_EDGE flag') for x in g.notes)))
    return out
if __name__=='__main__':
    import pandas as pd
    R=run_all('base')
    def sf_off(m):
        for l in m['legs']:
            se=l.get('scheme_edge'); 
            if se: se['scheme_fit']['ok']=False; se['scheme_fit']['detail']+=' [FORCED NOT OK: Sharp hindsight removed]'; se.pop('explanation',None)
    R+=run_all('wk67_schemefit_off',sf_off,weeks={6,7})
    def truedate(m):
        st='2026-10-27T12:00'
        for l in m['legs']:
            cv=l.get('coverage',{})
            for k in ('man_zone','mof'):
                if k in cv: cv[k]['pulled_et']=st; cv[k]['label']='TRUE DATE'
    R+=run_all('wk8_truedate_coverage',truedate,weeks={8})
    pd.DataFrame(R).to_csv('gate_results.csv',index=False)
    D=pd.DataFrame(R); print(D.groupby('variant').agg(legs=('leg','size'),gate_live=('gate_live','sum'),leg_pass=('leg_pass','sum'),strict_ok=('strict_ok','sum')))
    print(D[D.variant=='base'].run_other_miss.str.split(r' \|\| ').explode().map(lambda x:rulekey(str(x))).value_counts().head(20))
    print(D[D.variant=='base'].leg_misses.str.split(r' \|\| ').explode().map(lambda x:rulekey(str(x))).value_counts().head(30))

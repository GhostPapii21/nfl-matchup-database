#!/usr/bin/env python3
"""Merge r6 CODEX/GROK artifacts and evaluate all three user-defined slips.
No stat or model disagreement changes leg status. Missing evidence stays MISSING.
Run from any directory: python3 runs/2026-11-05_JAX@BAL_r6/assemble.py [--now ET_ISO]
Exit 1 means one or more gates failed; outputs are still complete and reviewable.
"""
import argparse, ast, copy, datetime as dt, json, subprocess, sys
from pathlib import Path
from zoneinfo import ZoneInfo
RUN=Path(__file__).resolve().parent; ROOT=RUN.parents[1]
CATEGORIES=['core_stats_pbp','coverage_matchups','ngs','film','injuries_news','weather','odds_props']
PH={1:'Data pull',2:'Opportunity',3:'Defense profile',4:'Defender coverage',5:'Pressure/blitz/checkdown',6:'QB card',7:'Recent form',8:'Injuries',9:'NGS',10:'Film',11:'Environment',12:'Source audit',13:'Game script',14:'Models/price/edge',15:'Inactives'}
PBP=ROOT/'runs/2026-11-05_JAX@BAL_r2/src/play_by_play_2026.parquet'
def stamp(p): return dt.datetime.fromtimestamp(p.stat().st_mtime,ZoneInfo('America/New_York')).strftime('%Y-%m-%dT%H:%M')
def load(path,default,missing):
 if not path.exists(): missing.append(str(path.relative_to(RUN))); return copy.deepcopy(default)
 return json.loads(path.read_text())
def definitions():
 # Read adapter constants without executing its legacy folder-writing side effects.
 tree=ast.parse((RUN/'gate_adapter.py').read_text()); out={}
 for node in tree.body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('L','SL') for t in node.targets):
   node=copy.deepcopy(node)
   for call in ast.walk(node):
    if isinstance(call,ast.Call): call.keywords=[k for k in call.keywords if k.arg!='carry_share']
   out[node.targets[0].id]=eval(compile(ast.Expression(node.value),str(RUN/'gate_adapter.py'),'eval'),{'dict':dict})
 return out['L'],out['SL']
def clean(x): return str(x).replace('|','/').replace('\n',' ')
def evidence_gaps(leg, pressure, sims, missing):
 # run_gate.stamped checks provenance only, so explicit MISSING must also block
 # the leg even if an independently edited checklist claims PASS.
 gaps=list(leg.get('gaps') or [])
 gaps += ['Missing artifact: '+p for p in missing]
 if len((leg.get('recent_form') or {}).get('values') or [])<3:
  gaps.append('MISSING recent_form: fewer than three games with current QB')
 if leg.get('receiving'):
  cv=leg.get('coverage') or {}
  for key, fields in [('man_zone',('man','zone')),('mof',('open','closed'))]:
   b=cv.get(key) or {}
   if b.get('status') in ('MISSING','UNVERIFIED','STALE') or not all(isinstance(b.get(k),(int,float)) for k in fields):
    gaps.append('MISSING coverage.'+key+' numeric rates')
  for key in ('blitz_rate','pressure_rate','checkdown_share','time_to_throw','targets_under_pressure'):
   b=pressure.get(key) or {}
   if b.get('status') in ('MISSING','UNVERIFIED','STALE') or b.get('value') is None:
    gaps.append('MISSING pressure_inputs.'+key)
 for sim in sims:
  v=sim.get('legs',{}).get(leg['name'],{})
  if v.get('status') in ('MISSING','UNVERIFIED') or 'UNVERIFIED' in str(v.get('pricing_engine','')):
   gaps.append('UNVERIFIED '+str(sim.get('model'))+' pricing for '+leg['name'])
 return list(dict.fromkeys(gaps))

def main():
 parser=argparse.ArgumentParser(); parser.add_argument('--now',help='Optional run_gate evaluation timestamp (ET naive ISO)'); args=parser.parse_args()
 missing=[]; L,SL=definitions()
 sims=load(RUN/'codex/sims.json',[],missing); coverage=load(RUN/'codex/coverage.json',{},missing); pressure=load(RUN/'codex/pressure_inputs.json',{},missing); extra=load(RUN/'codex/legs_extra.json',{},missing)
 rows=load(RUN/'grok/checklist_rows.json',{},missing); gsources=load(RUN/'grok/sources.json',[],missing); csources=load(RUN/'codex/sources.json',[],missing)
 forecast=load(RUN/'grok/weather_forecast.json',{'status':'MISSING','games':{}},missing)
 pool=load(RUN/'grok/target_share_pool.json',{'status':'MISSING','threshold':.22,'players':[]},missing)
 script=load(RUN/'grok/n3_1h_script.json',{'status':'MISSING'},missing)
 # Confirmed game week is ESPN week 9; week10 folder is a workspace label.
 odds=RUN/'odds/odds_r6.csv'
 sources=[dict(category='core_stats_pbp',name='nflverse pbp 2026 through week 8',url_or_file=str(PBP),pulled_et=stamp(PBP),tool='existing nflverse parquet',season=2026,data_week=8)]
 if odds.exists(): sources.append(dict(category='odds_props',name='Saved r6 FD/DK/Pinnacle odds; no API calls',url_or_file=str(odds),pulled_et='2026-11-04T14:59',tool='existing odds snapshot',season=2026,data_week=9))
 else: missing.append('odds/odds_r6.csv')
 auxiliary=[]
 for s in csources+gsources:
  # Preserve supplied provenance and week labels; never silently upgrade stale feeds.
  if s.get('category') not in CATEGORIES or s.get('status') in ('MISSING','UNVERIFIED','STALE'): auxiliary.append(s)
  elif s not in sources: sources.append(s)
 gaps=[dict(category=c,reason='No verified r6 source; see missing_artifacts and auxiliary_sources') for c in CATEGORIES if not any(s.get('category')==c for s in sources)]
 if pool.get('status')=='MISSING': gaps.append(dict(category='core_stats_pbp',reason='target_share_pool MISSING; no GROK artifact'))
 summary={}
 for folder,names in SL.items():
  dest=RUN/folder; dest.mkdir(exist_ok=True); legs=[]; checklist=['| Leg | Phase | Status | Number | Source | Pulled (ET) |','|---|---|---|---|---|---|']; flags=[]
  for name in names:
   x=L[name]; leg={k:copy.deepcopy(v) for k,v in x.items() if k not in ('rf','games','qb')}
   leg.update(name=name,status='PASS',team='BAL' if name.startswith('Henry') else 'JAX',opp='JAX' if name.startswith('Henry') else 'BAL',player={'Strange':'Brenton Strange','Washington':'Parker Washington','Henry':'Derrick Henry','JAX':'JAX'}[name.split()[0]],game='JAX@BAL',gaps=[],recent_form=dict(values=x['rf'],games=x['games'],qb=x['qb'],source=str(PBP),pulled_et=stamp(PBP)))
   leg.update(copy.deepcopy(extra.get(name,{})))
   if name in coverage: leg['coverage']=copy.deepcopy(coverage[name])
   if name=='JAX 1H -6.5':
    # Accept only an explicitly supplied sourced read, not an inferred expected winner.
    sr=script.get('script_read')
    if sr: leg['script_read']=copy.deepcopy(sr)
    else: flags.append('N3 script_read expected_winner/source MISSING; GROK narrative retained in n3_1h_script.')
   leg['gaps']=evidence_gaps(leg,pressure,sims,missing)
   legs.append(leg)
   for ph in range(1,16):
    if ph==7:
     rf=leg['recent_form']; hits=sum(v>leg['line'] if leg['side']=='over' else v<leg['line'] for v in rf['values'])
     row=dict(status='PASS' if hits>=3 and len(rf['values'])>=3 else 'FAIL',number=f"{hits}/{len(rf['values'])} {rf['values']}; current QB {rf['qb']}; flag only, no auto-cut",source=rf['source'],pulled_et=rf['pulled_et'])
    else: row=copy.deepcopy(rows.get(name,{}).get(str(ph),{}))
    if not row: row=dict(status='MISSING',number='No supplied checklist evidence',source='MISSING',pulled_et='MISSING')
    # Missing values are never assigned a fresh timestamp just to satisfy the gate.
    checklist.append(f"| {clean(name)} | {ph} {PH[ph]} | {clean(row.get('status','MISSING'))} | {clean(row.get('number','MISSING'))} | {clean(row.get('source','MISSING'))} | {clean(row.get('pulled_et','MISSING')).replace('T',' ')} |")
    if row.get('status') in ('FAIL','MISSING','STALE','UNVERIFIED'): flags.append(f"{name} phase {ph}: {row.get('status')} — {row.get('number')}")
  local_sims=copy.deepcopy(sims)
  for sim in local_sims: sim['legs']={n:v for n,v in sim.get('legs',{}).items() if n in names}
  M=dict(game='JAX@BAL',game_date='2026-11-05',kickoff_et='2026-11-05T20:15',season=2026,week=9,week_source=str(ROOT/'runs/2026-11-05_JAX@BAL_r2/src/espn_scoreboard.json'),week_note='ESPN event week 9; week10 input directory name is not a feed week.',venue='M&T Bank Stadium',roof='open',slip=names,legs=legs,sources=sources,auxiliary_sources=auxiliary,flagged_gaps=gaps,missing_artifacts=missing,pressure_inputs=pressure,sims=local_sims,weather_forecast=forecast,target_share_pool=pool,n3_1h_script=script,stat_gate_policy='Flags only; never automatically cut a read-selected leg. PASS is an evaluation status, not gate approval.',seed=20261104,trials=100000,sim_script='tools/sim_v6.py')
  if forecast.get('games',{}).get('JAX@BAL'):
   e=forecast['games']['JAX@BAL']; M['weather']={'JAX@BAL':{k:e[k] for k in ('roof','precip_pct','gust_mph','wind_mph') if k in e}}
   M['weather']['JAX@BAL'].update(source=forecast.get('source'),pulled_et=forecast.get('pulled_et'),label='Forecast only; Phase 11 pre-kick observation/inactives still required')
  (dest/'run_manifest.json').write_text(json.dumps(M,indent=2,allow_nan=False)+'\n'); (dest/'checklist.md').write_text('\n'.join(checklist)+'\n')
  report=[f'# JAX@BAL r6 {folder}', '', 'All requested legs remain live for evaluation. Stat/model disagreement is flagged, never an automatic read cut. A failed gate does not authorize a slip.', '', '## Simulations', '', '100,000 per model, fixed seed 20261104. Native player-market engine: tools/sim_v6.py; wrapper: codex/run_sims.py. Fagnano base estimates are the manifest case; rico/flip sensitivities and assumptions are in codex/sims_audit.json.', '', '**JAX 1H is an UNVERIFIED wrapper extension, not a native or calibrated sim_v6 spread model.** No native spread_h1 market exists; its numeric sensitivity must not be treated as approved pricing.', '', '| Leg | Monte Carlo p / median | Bias p / median | Game randomness p / median |','|---|---|---|---|']
  for n in names:
   vals=[]
   for s in local_sims:
    v=s.get('legs',{}).get(n,{}); vals.append(f"{v['p']:.5f} / {v['median']:.2f}" if v.get('p') is not None and v.get('median') is not None else 'MISSING')
   report.append('| '+n+' | '+' | '.join(vals or ['MISSING']*3)+' |')
  report+=['', '## Risks', '', 'Hamilton and CB assignments are hypotheses. No verified primary defender; Hamilton suppression is NOT COUNTED per r5 addendum 3. PFR performance does not verify future matchups. Man/zone, MOF and time-to-throw remain MISSING. Pressure/checkdown measures are labelled proxies.', '', 'Per-source timestamps and season/data_week are preserved; missing, stale, or incorrectly labelled GROK feeds remain visible to SRC-5. No staleness exceptions applied. Missing opposite-side prices leave Strange yards and Henry no_vig missing. Exact Pinnacle two-way no-vig fractions are used without rounding. No Odds API calls.', '', 'Forecast values do not replace the Phase 11 pre-kick weather/inactives recheck. Placed legs are unknown unless supplied. Phase 7 uses gate_adapter recent_form values and is independent of GROK rows.', '', 'Missing artifacts: '+(', '.join(missing) or 'none'), '', '## Checklist flags', '']+['- '+f for f in flags]
  body='\n'.join(report)+'\n'; (dest/'report.md').write_text(body)
  cmd=[sys.executable,str(ROOT/'tools/run_gate.py'),str(dest)]
  if args.now: cmd+=['--now',args.now]
  proc=subprocess.run(cmd,capture_output=True,text=True); output=proc.stdout+proc.stderr
  (dest/'gate_output.txt').write_text(output); (dest/'report.md').write_text('```text\n'+output.rstrip()+'\n```\n\n'+body)
  summary[folder]=dict(exit_code=proc.returncode,result=output.splitlines()[0] if output else 'NO GATE OUTPUT')
 (RUN/'codex/assembly_results.json').write_text(json.dumps(summary,indent=2)+'\n')
 for k,v in summary.items(): print(k,v['result'],f"(exit {v['exit_code']})")
 return 1 if any(v['exit_code'] for v in summary.values()) else 0
if __name__=='__main__': sys.exit(main())

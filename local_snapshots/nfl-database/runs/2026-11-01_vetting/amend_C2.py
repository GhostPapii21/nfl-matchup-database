import json,glob,subprocess,re,datetime
now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
REJ={'Boston':"Denzel Boston Receptions Under 3.5","Cooper":"Omar Cooper Jr. Receptions Under 3.5","JW":"Jameson Williams Rec Yds Under 51.5","DotR":"Jahan Dotson Receptions Under 2.5"}
WHY={REJ['Boston']:'P14 FAIL: conflicts with placed UD Boston o29.5 rec yds (Ghost6 vet)',
REJ['Cooper']:'P14 FAIL: edge exists only with bias model; MC+GR edge +1.4 < +3, shrunk -0.9 (Ghost6 vet)',
REJ['JW']:'P14 FAIL: rejected by Ghost6 vet (primary WR under; MC+GR edge thin +4.1/+2.9)',
REJ['DotR']:'P14 FAIL: same-player duplicate of Dotson Rec Yds Under 25.5 (Ghost6: pick one; kept the -113 yds leg)'}
RISK='- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).'
res=[]
for d in sorted(glob.glob('2026-11-01_*@*/')):
  m=json.load(open(d+'run_manifest.json')); S={x['model']:x['legs'] for x in m['sims']}
  b=sum(l['status']=='PASS' for l in m['legs']); cut=[]
  m['edge_decision']='avg(monte_carlo, game_randomness); bias recorded, excluded from edge pending BUGLOG fix'
  for l in m['legs']:
    n=l['name']; a=(S['monte_carlo'][n]['p']+S['game_randomness'][n]['p'])/2
    l['avg_p_mc_gr']=round(a,4); l['edge_mc_gr']=round(a-l['no_vig'],4); l['shrunk_mc_gr']=round(0.5+0.7*(a-0.5)-l['no_vig'],4)
    if l['status']=='PASS':
      r=WHY.get(n)
      if not r and (a-l['no_vig']<.03 or 0.5+0.7*(a-0.5)-l['no_vig']<=0): r='P14 FAIL: MC+GR edge below rule after bias exclusion'
      if r: l['status']='CUT'; l['cut_reasons'].append(r+f' ({now} ET)'); cut.append((n,r))
  json.dump(m,open(d+'run_manifest.json','w'),indent=1,default=str)
  ck=open(d+'checklist.md').read().split('\n')
  for i,row in enumerate(ck):
    for n,r in cut:
      if row.startswith(f'| {n} | 14 '):
        c=row.split(' | '); c[2]='FAIL'; c[3]+='; CUT: '+r; ck[i]=' | '.join(c)
  ck.append(f'\n**Vetting amendment 2 {now} ET:** edge decision on MC+GR average (bias model excluded pending fix). Cut: {[n for n,_ in cut] or "none"}.')
  open(d+'checklist.md','w').write('\n'.join(ck))
  rp=open(d+'report.md').read(); body=rp[rp.index('\n# ')+1:]
  live=[l for l in m['legs'] if l['status']=='PASS']
  am=f"\n## Vetting amendment 2 ({now} ET)\n- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: {', '.join(n+' - '+r for n,r in cut) or 'none'}.\n- Live legs now: "+('; '.join(f"{l['name']} (MC+GR avg p {l['avg_p_mc_gr']:.3f}, no-vig {l['no_vig']:.3f}, edge {100*l['edge_mc_gr']:+.1f}, shrunk {100*l['shrunk_mc_gr']:+.1f})" for l in live) or 'none')+"\n"
  body=body.replace('\n## 1. Header',am+'\n## 1. Header',1)
  h=re.search(r'^#+ .*Risks.*\n',body,re.M); body=body[:h.end()]+RISK+'\n'+body[h.end():]
  for _ in range(2):
    g=subprocess.run(['python3','/workspace/nfl-database/tools/run_gate.py',d],capture_output=True,text=True); open(d+'report.md','w').write(g.stdout+'\n'+body)
  res.append((d[11:-1],b,len(live),[l['name'] for l in live],g.stdout.split('\n')[0][:10]))
for r in res: print(r)

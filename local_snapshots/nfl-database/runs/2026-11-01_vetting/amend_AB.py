import json,re,subprocess,glob,datetime
R='/workspace/nfl-database/runs/'
STAR={'Michael Penix Jr. Pass Yds Under 229.5':'ATL starting QB',
'Drake London Rec Yds Under 79.5':'ATL target leader (57 tgt)',
'Bucky Irving Rush Yds Under 70.5':'TB RB1 (120 car)',
'Derrick Henry Rush Yds Under 78.5':'BAL RB1 (148 car)',
'Deshaun Watson Pass Yds Under 210.5':'CLE starting QB',
'KC Concepcion Rec Yds Under 46.5':'CLE target leader (45 tgt)',
'Garrett Wilson Rec Yds Under 63.5':'NYJ target leader (52 tgt)',
'Garrett Wilson Receptions Under 5.5':'NYJ target leader (52 tgt)',
'Ollie Gordon II Rush Yds Under 64.5':'MIA RB1 (72 car)'}
NGSNAME='BACKUP nflverse nextgen_stats release (published copy, data through 2026 Wk8 / 2026-10-29; nextgenstats.nfl.com on hold) - accepted by Ghost6 for 2026-11-01 only'
NGSRISK='- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.'
now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
out=[]
for d in sorted(glob.glob(R+'2026-11-01_*@*/')):
  mf=d+'run_manifest.json'; m=json.load(open(mf))
  before=sum(l['status']=='PASS' for l in m['legs'])
  for s in m['sources']:
    if s['category']=='ngs': s['name']=NGSNAME
  cut=[]
  for l in m['legs']:
    if l['name'] in STAR and l['status']=='PASS':
      l['status']='CUT'; l['cut_reasons'].append(f"P14 FAIL: under on primary star (Ghost6 rule) - {STAR[l['name']]}; cut {now} ET"); cut.append(l['name'])
  json.dump(m,open(mf,'w'),indent=1,default=str)
  ck=open(d+'checklist.md').read().split('\n')
  for i,row in enumerate(ck):
    for n in cut:
      if row.startswith(f'| {n} | 14 '):
        c=row.split(' | '); c[2]='FAIL'; c[3]=c[3]+f'; CUT: under on primary star (Ghost6 rule) ({STAR[n]})'; ck[i]=' | '.join(c)
  ck.append(f'\n**Vetting amendment {now} ET:** cut for under on primary star (Ghost6 rule): {cut or "none"}. NGS source relabelled BACKUP (data through 2026-10-29).')
  open(d+'checklist.md','w').write('\n'.join(ck))
  rp=open(d+'report.md').read()
  body=rp[rp.index('\n# ')+1:]
  am=f"\n## Vetting amendments ({now} ET)\n- Cut, under on primary star (Ghost6 rule): {', '.join(cut) if cut else 'none'}. Pass count {before} -> {before-len(cut)}.\n- NGS source relabelled BACKUP with data date (see Risks).\n"
  body=body.replace('\n## 1. Header',am+'\n## 1. Header',1)
  body=body.replace('## 6. Risks and checks still to come\n','## 6. Risks and checks still to come\n'+NGSRISK+'\n',1)
  open(d+'report.md','w').write('GATE: PENDING\n\n'+body)
  g=subprocess.run(['python3','/workspace/nfl-database/tools/run_gate.py',d],capture_output=True,text=True)
  open(d+'report.md','w').write(g.stdout+'\n'+body)
  g2=subprocess.run(['python3','/workspace/nfl-database/tools/run_gate.py',d],capture_output=True,text=True)
  open(d+'report.md','w').write(g2.stdout+'\n'+body)
  out.append((d.split('/')[-2],before,before-len(cut),cut,g2.stdout.split('\n')[0]))
for o in out: print(o)

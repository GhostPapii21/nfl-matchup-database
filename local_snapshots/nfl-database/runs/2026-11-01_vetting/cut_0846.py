import json,re,shutil,os
C={'Xavier Worthy Rec Yds Over 29.5':'WITHDRAWN by Ghost6; fails §7/§14 (BUG-2026-11-01-FORM)',
   'Stefon Diggs Rec Yds Over 42.5':'WITHDRAWN by Ghost6; fails §14',
   'Jahan Dotson Rec Yds Under 25.5':'WITHDRAWN by Ghost6; fails §7',
   'Jordan Addison Receptions Under 3.5':'fails §7 (under hit 1 of 3 with current QB); pending Ghost6 confirmation'}
for f in ['FD7_REPLACEMENTS','KC@DEN','PHI@WSH','ATL@TB','MIN@DET']:
    d=f'2026-11-01_{f}/'; mp=d+'run_manifest.json'
    for x in ['run_manifest.json','checklist.md','report.md','gate_output.txt']:
        a,b=x.rsplit('.',1)
        if os.path.exists(d+x) and not os.path.exists(d+f'{a}.pre_cut0846.{b}'): shutil.copy(d+x,d+f'{a}.pre_cut0846.{b}')
    m=json.load(open(mp)); done=[]
    for L in m['legs']:
        if L['name'] in C and L['status']!='CUT':
            L['status']='CUT'; L.setdefault('cut_reasons',[]).append(C[L['name']]); L['cut_et']='2026-11-01T08:46'; done.append(L['name'])
    json.dump(m,open(mp,'w'),indent=2)
    live=[L['name'] for L in m['legs'] if L['status']!='CUT']
    sec='\n## CUT 08:46 ET (BUG-2026-11-01-FORM, standing rule: gate fail = cut)\n'+''.join(f'- {n}: CUT — {C[n]}\n' for n in done)+f'- Remaining live legs: {live}\n'
    for x in ['checklist.md','report.md']:
        t=open(d+x).read()
        if x=='report.md': t=re.sub(r'^(Live legs: .*)$',lambda mm:f'Live legs (after 08:46 cuts): {live}\n(superseded) '+mm.group(1),t,count=1,flags=re.M)
        t=sec+'\n'+t if x=='report.md' else t+sec
        open(d+x,'w').write(t)
    print(f,done,'LIVE:',live)

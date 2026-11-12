"""Phase 15 (inactives + reprice) for SNF PHI@WSH 8:20 PM ET, run 2026-11-01 18:50-19:05 ET. Append-only."""
import json,re
R='/workspace/nfl-database/runs'; S=R+'/2026-11-01_shared_src'; T='2026-11-01 19:02'
INJ='/workspace/nfl-database/week8/inactives/espn_inj_20261101_1852.json'
WX='/workspace/nfl-database/week8/weather/om_PHIWSH_20261101_1855.json'
PHI_OUT="PHI official inactives (@Eagles 18:52 graphic): DeVonta Smith, Jihaad Campbell, Dontayvion Wicks, CB Jonathan Jones, OL Jake Majors, Britain Covey (CB J. Bennett, RB Pierce IR)"
WSH_OUT="WSH (@Commanders post 18:52 had no readable media via x connector; ESPN summary 19:00 + injuries 18:52): Payne, Kinlaw Out; Newton, McLaurin, Tunsil, Lane IR; Burks, Bates Q (not confirmed); Diggs, Okonkwo, White, D. Brown, Daniels Active"
GEN="Saquon, Lemon, Cooper, Goedert, DeJean, M. Carter II active; no line moved >0.5/20c vs 14:35 (spread WSH -5.5 -122->-115, total 40.5). Weather Open-Meteo 18:55: 0% precip, gusts 7-10 mph, 50-52F -> no Phase 11 flag. Leg stays CUT (no live price edge re-opened)."
SRC="@Eagles/@Commanders inactives posts via x connector + ESPN injuries API 18:52 + ESPN summary 19:00 + The Odds API 18:51 (i1850) + Open-Meteo 18:55"
def diggs_note():
    return ("ACTIVE (ESPN 18:52 Active; not on WSH outs). Phase 4 defender Cooper DeJean ACTIVE. HELPED mildly: PHI CB Jonathan Jones INACTIVE + Bennett IR (thin CB depth); PHI WR Smith/Wicks out may raise WSH possession time. "
            "Lines: FD alt 3.5 -166 -> -168 (2c, not material); FD main 4.5 O+132/U-178; PP rec 4.0; Pinnacle 4.5 +132/-160; DK 4.5 O+121. No-vig alt vs main two-way ~0.585 (was 0.583); sim_v6 08:36 p 0.665/0.665/0.677 unchanged inputs -> edge ~+8.4, shrunk ~+3.3, still PASS. Not on any placed ticket (FD7 replacement / bonus fallback only). "
            "Weather clear (0% precip, gusts <=10 mph).")
done={}
for g in ['PHI@WSH','FD7_REPLACEMENTS']:
    d=f'{R}/2026-11-01_{g}'; mp=d+'/run_manifest.json'; m=json.load(open(mp)); rows=[]
    for l in m['legs']:
        if g=='FD7_REPLACEMENTS' and 'Diggs' not in l['name']: continue
        st=l.get('status','PASS').upper()
        note = diggs_note() if (l['name']=='Stefon Diggs Receptions Over 3.5') else GEN
        rows.append(f"| {l['name']} | 15 Inactives | {st} | 19:02 ET: {note} | {SRC} | {T} |")
    hdr=(f"\n\n## Phase 15 re-check — inactives & reprice, SNF PHI@WSH 8:20 PM ET (run 2026-11-01 18:50–19:05 ET)\nSupersedes earlier Phase 15 rows for the legs below. Read only; no bets placed. {PHI_OUT}. {WSH_OUT}. "
         "No user-placed ticket has a PHI or WSH leg; no placed RB legs in this game (backfield-split check N/A).\n\n| Leg | Phase | Status | Number | Source | Pulled (ET) |\n|-----|-------|------|--------|--------|-------------|\n")
    open(d+'/checklist.md','a').write(hdr+'\n'.join(rows)+'\n')
    for s in m['sources']:
        if s['category']=='odds_props':
            s['pulled_et']='2026-11-01T18:51'; s['url_or_file']=S+('/lines_i1850.json' if 'spread' in s['name'] else '/odds_i1850.csv'); s['name']=re.sub(r'\(re-pull \d\d:\d\d\)','',s['name']).strip()+' (re-pull 18:51)'
        if s['category']=='injuries_news' and s['name'].startswith('ESPN injuries API'):
            s['pulled_et']='2026-11-01T18:52'; s['url_or_file']=INJ
        if s['name'].startswith('X reporters'): s['pulled_et']='2026-11-01T19:00'
        if s['category']=='weather' and g=='PHI@WSH':
            s['pulled_et']='2026-11-01T18:55'
    if not any(s['name'].startswith('X reporters') for s in m['sources']):
        m['sources'].append(dict(category='injuries_news',name='X reporters/team inactives posts via x connector',url_or_file='https://x.com/Eagles/status/2117042050919288953',pulled_et='2026-11-01T19:00',tool='x connector'))
    if g=='PHI@WSH' and not any(s['category']=='weather' and 'Open-Meteo 18:55' in s['name'] for s in m['sources']):
        m['sources'].append(dict(category='weather',name='Open-Meteo hourly Northwest Stadium 18:55',url_or_file=WX,pulled_et='2026-11-01T18:55',tool='curl'))
    json.dump(m,open(mp,'w'),indent=1); print(g,len(rows),'rows')

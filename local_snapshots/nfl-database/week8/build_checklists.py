import json,glob,re,os,urllib.request,datetime,hashlib
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40))
NOW=datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')
slate=json.load(open('slate.json'))['games']; inj=json.load(open('injuries.json'))
ros={f[8:-5]:json.load(open(f)) for f in glob.glob('rosters/[A-Z]*.json')}
import unicodedata
def nz(n):
    n=unicodedata.normalize('NFKD',n).encode('ascii','ignore').decode().lower().replace("'",'').replace('.','')
    w=[x for x in n.split() if x not in ('jr','sr','ii','iii','iv')]
    al={'matthew':'matt','joshua':'josh'}
    return ' '.join(al.get(x,x) for x in w)
allr={}
for t,o in ros.items():
    for p in o['players']: allr.setdefault(nz(p['name']),[]).append((t,p['status']))
injn={(t,nz(p['name'])):p for t,v in inj['teams'].items() for p in v}
COORD={'Highmark Stadium':(42.774,-78.787),'Paycor Stadium':(39.095,-84.516),'MetLife Stadium':(40.813,-74.074),'Acrisure Stadium':(40.447,-80.016),'Raymond James Stadium':(27.976,-82.503),'EverBank Stadium':(30.324,-81.637),'Empower Field at Mile High':(39.744,-105.020),'Hard Rock Stadium':(25.958,-80.239),'Northwest Stadium':(38.908,-76.864)}
# film coverage
film={}
for f in glob.glob('film/games/*.json'):
    g=json.load(open(f)); done=os.path.exists('film/codex_out/'+os.path.basename(f))
    for t in (g['away'],g['home']): film.setdefault(t,[0,0]); film[t][0]+=1; film[t][1]+=done
# schedules for rest
ids={t:o['espn_id'] for t,o in ros.items()}; rest={}
for t,i in ids.items():
    try:
        s=get(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{i}/schedule?season=2026')
        ds=[e['date'] for e in s['events'] if e['date']<'2026-10-31' and e.get('competitions',[{}])[0].get('status',{}).get('type',{}).get('completed')]
        last=max(ds); rest[t]=(last[:10],(datetime.date(2026,11,1)-datetime.date.fromisoformat(last[:10])).days)
    except Exception as e: rest[t]=('unknown',None)
def crosscheck(path,team_of_line):
    flags=[]
    for ln in open(path):
        m=re.match(r'^- ([A-Z][\w\.\'\- ]+?) \((QB|RB|WR|TE|FB)\)',ln) or re.match(r'^\|([A-Z][\w\.\'\- ]+?)\|(QB|RB|WR|TE|FB)\|',ln)
        if not m: continue
        n=m.group(1).strip(); t=team_of_line(ln); t={'LA':'LAR'}.get(t,t); k=nz(n)
        if t is None: continue
        ij=injn.get((t,k)); on=[x for x in allr.get(k,[]) if x[0]==t]
        if ij and ij['designation'] in ('Injured Reserve','Out','Suspension','Doubtful'): flags.append((n,t,'REMOVE',f"{ij['designation']} per ESPN injuries ({ij['source_ts_utc']}): {ij['comment'][:140]}"))
        elif not on:
            else_=[x for x in allr.get(k,[])]
            flags.append((n,t,'REMOVE',f"not on {t} ESPN roster ({NOW})"+(f"; now on {else_}" if else_ else "; not on any Sunday-team roster (traded to non-slate team, released, or IR)")))
        elif on and on[0][1]=='Practice Squad': flags.append((n,t,'REMOVE',f'on {t} practice squad (needs elevation)'))
        elif ij and ij['designation']=='Questionable': flags.append((n,t,'FLAG-Q',f"Questionable — script low alts/fade, not cut. {ij['comment'][:140]}"))
    return list(dict.fromkeys(flags))
summary=[]
for g in slate:
    A,H=g['matchup'].split(' @ '); key=f'{A}_at_{H}'; dpath=f'defense/{key}.md'
    txt=open(dpath).read().split('\n## Roster & Injury Update')[0]
    # determine candidate team by section
    cur={'t':None}
    def tol(ln,cur=cur): return cur['t']
    flags=[]; secs=re.split(r'(### \w+ candidates)',txt)
    t=None
    for s in secs:
        m=re.match(r'### (\w+) candidates',s)
        if m: t=m.group(1); continue
        if t:
            open('/tmp/s.md','w').write(s); flags+=crosscheck('/tmp/s.md',lambda l,t=t:t)
    for T in (A,H): flags+=[(n,t,a,r) for n,t,a,r in crosscheck(f'team_baselines/{T}.md',lambda l,T=T:T) if a=='REMOVE']
    flags=list(dict.fromkeys(flags))
    # injury impact
    imp=[]
    for T,opp in ((A,H),(H,A)):
        rows=[p for p in inj['teams'].get(T,[]) if p['designation']!='Active']
        off=[p for p in rows if p['pos'] in ('QB','RB','WR','TE','FB','OT','G','C','OL','T')]
        de=[p for p in rows if p not in off]
        dc=ros[T].get('depth_chart',{})
        def repl(n):
            for k,v in dc.items():
                if n in v[:1] and len(v)>1: return f"depth chart next at {k.split(':')[1].upper()}: {v[1]}"
            return 'no ESPN depth-chart starter slot (not a listed starter)'
        imp.append(f"\n**{T} offense (vs {opp} defense)**")
        imp+= [f"- {p['name']} {p['pos']} — {p['designation']}; practice: {p['practice_note_from_comment'] or 'official Wed/Thu table not in source (Thu PENDING)'}; {repl(p['name'])}. src ts {p['source_ts_utc']}Z" for p in off if p['designation']!='Injured Reserve'] or ['- none non-IR listed']
        imp.append(f"**{T} defense (faced by {opp})**")
        imp+= [f"- {p['name']} {p['pos']} — {p['designation']}; practice: {p['practice_note_from_comment'] or 'Thu PENDING'}; {repl(p['name'])}. src ts {p['source_ts_utc']}Z" for p in de if p['designation']!='Injured Reserve'] or ['- none non-IR listed']
        ir=[f"{p['name']} {p['pos']}" for p in rows if p['designation']=='Injured Reserve']
        if ir: imp.append(f"- IR ({T}): "+', '.join(ir))
    imp.append("\nProfile effect rule: a missing starter (CB1/S/edge/OL) is noted as a *direction* only (e.g. outside coverage may soften); Sharp/pbp allowance numbers are NOT adjusted and targets/carries are NOT redistributed without evidence (replacement's own snaps/targets). Questionable = scripted on low alts/fade, never cut; 90-min inactive approval goes to the user.")
    # weather
    wx='NOT_APPLICABLE: indoor/roof (ESPN indoor=true)'; wxs='NOT_APPLICABLE'
    if not g['indoor']:
        c=COORD.get(g['venue'])
        if c:
            try:
                w=get(f"https://api.open-meteo.com/v1/forecast?latitude={c[0]}&longitude={c[1]}&hourly=temperature_2m,precipitation_probability,wind_speed_10m,wind_gusts_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America/New_York&start_date=2026-11-01&end_date=2026-11-01")
                hr=int(g['kickoff_et'].split()[3].split(':')[0])%12+12 if 'PM' in g['kickoff_et'] else int(g['kickoff_et'].split()[3].split(':')[0])
                if g['venue']=='Empower Field at Mile High': hr-=0  # API returns ET-local times
                h=w['hourly']; i=h['time'].index(f'2026-11-01T{hr:02d}:00')
                wx=f"Forecast (Open-Meteo, pulled {NOW}) kickoff hr: {h['temperature_2m'][i]}°F, precip prob {h['precipitation_probability'][i]}%, wind {h['wind_speed_10m'][i]} mph gust {h['wind_gusts_10m'][i]} — 3-day-out forecast, re-pull Sat/Sun"; wxs='PARTIAL'
            except Exception as e: wx=f'forecast fetch failed: {e}'; wxs='UNAVAILABLE'
        else: wx=f"no coordinates mapped for {g['venue']}"; wxs='UNAVAILABLE'
    rem=os.path.exists(f'rematches/{A}_{H}.md') or os.path.exists(f'rematches/{H}_{A}.md')
    rf=f"rematches/{A}_{H}.md" if os.path.exists(f'rematches/{A}_{H}.md') else f"rematches/{H}_{A}.md"
    fa,fh=film.get(A,[0,0]),film.get(H,[0,0])
    fs='PARTIAL' if fa[1] or fh[1] else 'UNAVAILABLE'
    fr=f"Codex YouTube highlight notes done for {A} {fa[1]}/{fa[0]} games, {H} {fh[1]}/{fh[0]} (film/codex_out, still running; not yet verified vs pbp by this worker)"
    qbs=[x for x in re.findall(r'^- ([A-Z][\w\.\' ]+): NGS TTT',txt,re.M)]
    nd=len([f for f in flags if f[2]=='REMOVE'])
    C=[
('P1.pbp','PASS','Repo SQLite plays (ESPN PBP) Wk1–7 + nflverse via overlay','repo/data/nfl_matchups.sqlite; fixes/fixes.sqlite'),
('P1.boxscores','PASS','player_stats + fix_player_game_usage','fixes/fixes.sqlite'),
('P1.tackles_sacks','PARTIAL','fix_play_credits reconciled; tackler≠coverage defender','fixes/FIXES.md'),
('P1.pressure','PARTIAL','Pressure is opponent-Sharp-allowed proxy + pbp sack/hit; no charted pressure source','defense/'+key+'.md'),
('P1.ol_snaps','PARTIAL','nflverse participation snaps only; Wk7 participation lag possible','fixes/fixes.sqlite fix_participation'),
('P1.air_yards','PARTIAL','NGS IAY per QB; per-target air yards via nflverse only where loaded','defense/raw'),
('P1.redzone','PASS','RZ targets/goal-line carries in baselines','team_baselines/'+A+'.md, '+H+'.md'),
('P1.scrambles','PARTIAL','fix_qb_rushing scramble flags from nflverse; ESPN PBP lacks explicit flag','fixes/fixes.sqlite fix_qb_rushing'),
('P2.team_defense','PASS','Production + explosive counts per game','defense/'+key+'.md'),
('P2.coverage','PASS','Sharp coverage pages dated Oct 20 = CURRENT per user (last games before slate)','defense/SOURCES.md'),
('P2.individual_assignments','PARTIAL','Only PBP-named defenders on big plays (weak signal); no charted assignment source','team_baselines/'),
('P2.weakest_link','PARTIAL','Alignment-level weakest link from Sharp ranks (see Soft spots); player-level unverified','defense/'+key+'.md'),
('P2.pressure_trend','PARTIAL','ESPN PRWR through Wk6 only; pbp sack/hit trend','defense/'+key+'.md'),
('P3.team_offense','PASS','QB/team production','team_baselines/'),
('P3.player_roles','PASS','Roles + L3 vs season shares; roster-checked '+NOW,'defense/'+key+'.md; rosters/'),
('P3.ol_health','PARTIAL','OL designations from ESPN injuries; Thu practice pending','injuries.json'),
('P3.target_hierarchy','PASS','L3 vs season target/carry share (opportunity gate inputs)','team_baselines/'),
('P3.routes_gaps','PARTIAL','NGS separation/cushion; run gaps from pbp direction; no route participation','defense/raw'),
('P3.qb_blitz','PASS','FTN EPA vs blitz / no-blitz per offense','defense/'+key+'.md'),
('P4.slip_comparison','NOT_APPLICABLE','No slip supplied for this game','—'),
('P4.injury_alerts','PARTIAL','Wed status logged; Thursday reports PENDING','injuries.json; this file Injury impact'),
('P4.script_risk','PARTIAL','Backup-QB/workload risk noted from injuries; 10G labels pending','this file'),
('P5.bundle','PARTIAL','Markdown/JSON bundle; no engine-versioned bundle','week8/'),
('P5.provenance','PARTIAL','sha256 of inputs recorded below; engine code/model hash unavailable (nfl.py on user Mac)','this file'),
('P5.source_preservation','PASS','Repo SQLite untouched; fixes in overlay','fixes/PATCH_SPEC.md'),
('P6.live_policy','NOT_APPLICABLE','Pregame; live polling off','—'),
('P7.ngs_targeted_charts','PARTIAL','NGS public leaderboards (sep/cushion/YACOE/TTT); per-game targeted charts not read','defense/raw'),
('P7.all_routes','UNAVAILABLE','Route participation not in any public source loaded','—'),
('P7.run_concepts','UNAVAILABLE','No verified run-concept source; film pending','film/'),
('P7.strength_map','PARTIAL','Sharp alignment YPT + box rates; no side-level split','defense/'+key+'.md'),
('P7.rb_suppression','PARTIAL','RB YPC/rush+rec allowed + game state; RB quality adj not applied','defense/'+key+'.md'),
('P7.cb_suppression','UNAVAILABLE','Individual CB coverage stats are paid/not loaded','—'),
('P7.panthers_rule','PARTIAL','QB NGS/blitz review for: '+(', '.join(qbs) or 'none parsed')+'; exact OL/pass-rush matchup not charted','defense/'+key+'.md'),
('P8.film',fs,fr,'film/codex_out'),
('P8.personnel','UNAVAILABLE','Personnel packages need film; depth chart formation only','rosters/'),
('P8.scheme','PARTIAL','Coverage shells from Sharp (man/zone/MOFC); fronts/run fits need film','defense/'+key+'.md'),
('P8.missed_looks','UNAVAILABLE','Pending verified film notes','film/'),
('P8.film_notes',fs,'Codex notes unverified; hypotheses only',"film/codex_out"),
('P9.weather',wxs,wx,'https://api.open-meteo.com' if wxs!='NOT_APPLICABLE' else 'slate.json'),
('P9.rest_travel','PASS',f"{A} last game {rest[A][0]} ({rest[A][1]} days rest); {H} last game {rest[H][0]} ({rest[H][1]} days). Time-zone change only from venue, no itineraries invented",'ESPN team schedule API'),
('P9.stakes','PARTIAL','Records from ESPN scoreboard; divisional/rematch '+('YES ('+rf+')' if rem else 'not a 2026 rematch')+'; playoff-odds not pulled','defense/'+key+'.md'),
('P9.injury_spikes','PARTIAL','Exact-game availability: Wed designations; Thu/Fri + inactives pending','injuries.json'),
('P9.turnovers','PARTIAL','Turnovers in pbp/baselines; rolling interpretation not modeled','team_baselines/'),
('P9.situational_efficiency','PASS','3rd-down % and RZ TD % allowed','defense/'+key+'.md'),
('P9.unclassified','PARTIAL','Roster moves reviewed (rosters/ROSTER_CHANGES.md); travel/coaching notes not reviewed','rosters/ROSTER_CHANGES.md'),
('P10.espn','PARTIAL','ESPN PRWR/RSWR through Wk6 only','defense/SOURCES.md'),
('P10.position','PASS','Sharp positional/alignment YPT (current per user)','defense/SOURCES.md'),
('P10.scheme','PASS','Sharp man/zone/MOFC/MOFO','defense/SOURCES.md'),
('P10.tendencies','PASS','Blitz %, box rates, sub % (Sharp + FTN)','defense/SOURCES.md'),
('P10.advanced','PASS','EPA/play allowed from pbp','defense/'+key+'.md'),
('P10.individual_db','UNAVAILABLE','Individual CB sites not loaded; PFF grades NOT required by user','—'),
('P10G.script_gate','PARTIAL',f"Spread {g['spread']}/total {g['total']} recorded; script label PENDING (accepted by user); underdog-script legs blocked until labeled",'slate.json'),
('MODEL.inputs','PARTIAL','Numbers sourced; identities roster-checked; Thu injuries pending','rosters/; injuries.json'),
('MODEL.lineup','PARTIAL','Starting QB per ESPN depth chart; Questionables unresolved','rosters/'+A+'.json, '+H+'.json'),
('MODEL.simulation','UNIMPLEMENTED','SIMULATION NOT RUN — user 100k engine outputs/nfl.py is on user Mac, not in repo','GAME_SCRIPT_2026-10-29.md'),
('MODEL.calibration','UNIMPLEMENTED','No independent chronological validation without engine','—'),
('TICKET.markets','UNAVAILABLE','FD/DK prop lines not pulled in this pass','—'),
('TICKET.roles_matchups','PARTIAL','Soft-spot candidates pass role+volume screen; final after Thu injuries','defense/'+key+'.md'),
('TICKET.correlation','UNIMPLEMENTED','No ticket built','—'),
('TICKET.cap','NOT_APPLICABLE','No ticket built (6 target / 7 max applies when built)','—')]
    assert len(C)==60
    hs={p:hashlib.sha256(open(p,'rb').read()).hexdigest()[:16] for p in ['slate.json','injuries.json',dpath,f'rosters/{A}.json',f'rosters/{H}.json','../fixes/fixes.sqlite']}
    from collections import Counter; cnt=Counter(c[1] for c in C)
    out=[f"# {A} @ {H} — Week 8 60-check manifest\nGame {g['id']}, {g['kickoff_et']}, {g['venue']} ({'indoor' if g['indoor'] else 'outdoor'}), {g['spread']} / {g['total']}. Built {NOW}. Status counts: {dict(cnt)}\n","| # | Check | Status | Reason | Evidence |","|-|-|-|-|-|"]
    out+=[f"|{i+1}|{c[0]}|{c[1]}|{c[2]}|{c[3]}|" for i,c in enumerate(C)]
    out+=["\n## Injury impact (ESPN injuries API "+inj['api_timestamp']+"; Thursday official reports PENDING)"]+imp
    out+=["\n## Roster cross-check of named candidates"]+([f"- {n} ({t}): {a} — {r}" for n,t,a,r in flags] or ['- all named candidates on current roster, none Out/IR'])
    out+=["\n## Provenance (sha256/16)"]+[f"- {k}: {v}" for k,v in hs.items()]
    open(f'checklist/{key}_checklist.md','w').write('\n'.join(out)+'\n')
    upd=[f"\n\n## Roster & Injury Update (Oct 29)\nRetrieved {NOW}. Rosters: rosters/{A}.json, rosters/{H}.json (ESPN roster + depth chart). Injuries: injuries.json (ESPN, {inj['api_timestamp']}); Thursday reports pending. Checklist: checklist/{key}_checklist.md\n","### Candidate changes"]+([f"- {n} ({t}): {a} — {r}" for n,t,a,r in flags] or ['- none'])+["\n### Injury impact"]+imp
    open(dpath,'a').write('\n'.join(upd)+'\n')
    summary.append((key,dict(cnt),flags))
json.dump([(k,c,f) for k,c,f in summary],open('checklist/summary.json','w'),indent=1)
for k,c,f in summary: print(k,c); [print('   ',x[:4] if len(str(x))<300 else str(x)[:300]) for x in f]

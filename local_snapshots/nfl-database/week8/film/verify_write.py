import json,glob,re,os,collections
slate=json.load(open('../slate.json'))
teams=sorted({t for g in slate['games'] for t in g['matchup'].split(' @ ')})
G={json.load(open(f))['gid']:json.load(open(f)) for f in glob.glob('games/*.json')}
stats=collections.Counter(); per=collections.defaultdict(list); notes=collections.defaultdict(list)
def dbline(g,ref):
    m=re.match(r'\s*Q(\d)\s+(\d+:\d\d)',ref or '')
    if not m: return None
    for l in g['key_plays']:
        if l.startswith(f"Q{m.group(1)} {m.group(2)} "): return l
    return 'BADREF'
for gid,g in G.items():
    f=f'codex_out/{gid}.json'
    if not os.path.exists(f): continue
    o=json.load(open(f))
    for p in o['plays']:
        l=dbline(g,p['db_match'])
        status='unverified (no DB match; caption-only)'
        if l=='BADREF': status='CONFLICT (cited DB play not found)'
        elif l:
            yd=p['yards']; okyd = yd is None or re.search(rf'\b{abs(yd)}\s*(yard|yd|Yd)',l) or f"| {float(yd)} yds" in l
            status='verified vs DB' if okyd else f'CONFLICT (yardage {yd} vs DB)'
        stats[status.split(' (')[0]]+=1
        p['status']=status; p['dbline']=l if l and l!='BADREF' else ''
        for t in (g['away'],g['home']):
            if t in teams: per[t].append((g,p))
    for tn in o['team_notes']:
        notes[tn['team']].append((g,tn))
    for t in (g['away'],g['home']):
        if t in teams: notes.setdefault(t+'_lim',[]).append((g,o['limitations']))
print(stats)
os.makedirs('teams',exist_ok=True)
summary={}
for t in teams:
    gs=sorted([g for g in G.values() if t in (g['away'],g['home'])],key=lambda g:g['week'])
    L=[f"# {t} — Phase 8 film notes (Weeks 1–6, 2026)\n",
       "Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.\n"]
    for g in gs:
        y=g.get('yt',{})
        L.append(f"\n## Week {g['week']}: {g['score']} (game {g['gid']})\nVideo: {y.get('title','NONE')} — {y.get('url','no NFL-channel video found')}  | captions: {'yes' if y.get('captions') else 'NO'}\n")
        ps=[p for gg,p in per[t] if gg['gid']==g['gid']]
        if not ps: L.append("_No Codex film notes (no captions or run not completed)._\n"); continue
        L.append("|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|\n|-|-|-|-|-|-|-|-|-|-|")
        for p in ps:
            L.append("|"+"|".join(str(x).replace('|','/').replace('\n',' ') for x in [p['caption_ts'],p['team'],p['player'],p['description'],p['yards'],p['concept'],p['personnel_formation'],p['coverage_scheme'],p['defender_beaten'],p['status']])+"|")
        for gg,tn in notes.get(t,[]):
            if gg['gid']==g['gid']:
                L.append("\nOffense (Codex synthesis from this game's plays): "+' / '.join(tn['offense_strengths']))
                L.append("\nDefense weaknesses: "+' / '.join(tn['defense_weaknesses']))
        for gg,lim in notes.get(t+'_lim',[]):
            if gg['gid']==g['gid']: L.append(f"\nLimitations: {lim}\n")
    open(f'{t}_film.md','w').write('\n'.join(L))
    # summary for baseline
    off=[p for g,p in per[t] if p['team']==t and p['status'].startswith('verified')]
    dfn=[p for g,p in per[t] if p['team']!=t and p['status'].startswith('verified')]
    conc=collections.Counter(p['concept'].split(';')[0].strip().lower() for p in off if p['concept']!='unknown')
    conc_d=collections.Counter(p['concept'].split(';')[0].strip().lower() for p in dfn if p['concept']!='unknown')
    beaten=collections.Counter(d.strip() for p in dfn for d in re.split(r'[;,]| and ',p['defender_beaten']) if d.strip() and d.strip().lower()!='unknown')
    big_off=[f"W{g['week']} {p['player']} {p['yards']}y ({p['concept']})" for g,p in per[t] if p['team']==t and p['status'].startswith('verified') and (p['yards'] or 0)>=20 and p['concept']!='field goal']
    big_def=[f"W{g['week']} {p['team']} {p['player']} {p['yards']}y" for g,p in per[t] if p['team']!=t and p['status'].startswith('verified') and (p['yards'] or 0)>=20 and 'field goal' not in p['concept']]
    allp=[p for g,p in per[t]]
    summary[t]=dict(games=len(gs),with_notes=len({g['gid'] for g,p in per[t]}),plays=len(allp),verified=sum(p['status'].startswith('verified') for p in allp),conflicts=sum(p['status'].startswith('CONFLICT') for p in allp))
    S=f"\n\n## FILM NOTES (Phase 8) — appended {__import__('datetime').datetime.now():%Y-%m-%d %H:%M} ET\n"
    S+=f"Source: NFL YouTube highlight **captions only** (no frames viewed), Codex extraction, DB cross-check. Full notes + URLs: week8/film/{t}_film.md\n"
    S+=f"Coverage: {summary[t]['with_notes']}/{len(gs)} Wk1–6 games; {summary[t]['plays']} plays logged, {summary[t]['verified']} verified vs DB, {summary[t]['conflicts']} conflicts (flagged, not used).\n"
    S+="Videos: "+"; ".join(f"W{g['week']} {g.get('yt',{}).get('url','none')}" for g in gs)+"\n"
    S+=f"- Offense, verified explosive plays (20+ yds): {'; '.join(big_off[:12]) or 'none verified'}\n"
    S+=f"- Offense concepts, verified plays (commentary-stated): {', '.join(f'{k} x{v}' for k,v in conc.most_common(8)) or 'unknown'}\n"
    S+=f"- Defense, verified explosives allowed: {'; '.join(big_def[:12]) or 'none verified'}\n"
    S+=f"- Defense concepts allowed: {', '.join(f'{k} x{v}' for k,v in conc_d.most_common(6)) or 'unknown'}\n"
    S+=f"- Defenders named on verified plays allowed (DB tackler or commentary; being named ≠ proof of a coverage loss): {', '.join(f'{k} x{v}' for k,v in beaten.most_common(8)) or 'unknown'}\n"
    S+="- Personnel/coverage shells: mostly unknown (captions rarely state them). Treat as a gap.\n"
    open(f'teams/{t}_appendix.md','w').write(S)
json.dump(summary,open('summary.json','w'),indent=1)
print(json.dumps(summary))

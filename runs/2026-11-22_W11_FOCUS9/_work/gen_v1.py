import json, statistics, os
from manual import *
OUT='/workspace/runs/2026-11-22_W11_FOCUS9'
GAMES=['ARI_KC','BAL_CAR','MIA_BUF','NO_CHI','TB_DET','JAX_NYG','LV_DEN','MIN_SF','CIN_WAS']
AST={'Sun Nov 22, 1:00 PM ET':'2:00 PM AST','Sun Nov 22, 4:25 PM ET':'5:25 PM AST','Sun Nov 22, 8:20 PM ET (SNF)':'9:20 PM AST','Mon Nov 23, 8:15 PM ET (MNF)':'9:15 PM AST'}
BK={'fanduel':'FD','draftkings':'DK','betmgm':'MGM','caesars':'CZR'}
BKORD=['FD','DK','MGM','CZR']
def fmt(o): return 'n/a' if o is None else (f'+{o}' if o>0 else str(o))
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
def be(o): return imp(o)
def pct(x): return 'n/a' if x is None else f'{x*100:.1f}%'
def wx_cut(g): return WX[g][2]

def cushion(log, rung, price):
    l4=log[-4:]; med=statistics.median(l4); need=0.20 if price<=-150 else 0.25
    c=(med-rung)/rung; clear10=sum(1 for v in l4 if v>=rung*1.10)
    ok = c>=need and (price<=-150 or clear10>=3)
    return ('PASS' if ok else 'FAIL', f'last-4 median {med:g} vs {rung:g}: {c*100:.0f}% cushion (needs {need*100:.0f}%); cleared by 10%+ in {clear10} of {len(l4)}')

def hits(log, line, over=True): return sum(1 for v in log if (v>line if over else v<line))

def game_market(f, g):
    gl=f['game_lines']; a,h=f['away'],f['home']; rico=RICO[g]
    L=['| Book (Nov 20, 6:33 AM AST) | Spread | Total (O/U) | ML away / home | No-vig home win |','|---|---|---|---|---|']
    for k,v in gl.items():
        sp=v.get('spread') or []; tt=v.get('total') or []; ml=v.get('moneyline') or []
        hsp=[s for s in sp if s[0]!=sp[0][0]] if sp else []
        def tm(rows,name_idx): return rows
        spd=' / '.join(f"{s[0].split()[-1]} {s[1]:+g} ({fmt(s[2])})" for s in sp)
        tot=f"{tt[0][1]:g} ({fmt(tt[0][2])}/{fmt(tt[1][2])})" if len(tt)==2 else 'n/a'
        mls=' / '.join(f"{m[0].split()[-1]} {fmt(m[2])}" for m in ml)
        nv='n/a'
        if len(ml)==2:
            p=[imp(m[2]) for m in ml]; s=sum(p)
            hi=[i for i,m in enumerate(ml) if h in m[0] or m[0].split()[-1].upper()[:3]==h]  # best effort
            nv=' / '.join(f"{m[0].split()[-1]} {p[i]/s*100:.1f}%" for i,m in enumerate(ml))
        L.append(f'| {BK.get(k,k)} | {spd} | {tot} | {mls} | {nv} |')
    L.append(f"| **Rico consensus (screenshot, Sat 3:47 PM AST)** | {rico['fav']} -{rico['spread']:g} | {rico['total']:g} | dog {fmt(rico['dog_ml'])} | dog no-vig n/a (one side only) |")
    return '\n'.join(L)

def crosscheck(f):
    out=[];tot=0
    for t,x in f['sides'].items():
        o=x['off_prod']['points_pg']; d=x['def_allowed']['points_pg']; e=(o+d)/2; tot+=e
        out.append((t,o,x.get('off_rank',{}).get('points_pg'),d,x['def_rank'].get('points_pg'),e))
    return out,tot

def implied(g,f):
    r=RICO[g]; fav=r['fav']; other=[t for t in (f['away'],f['home']) if t!=fav][0]
    return {fav:(r['total']+r['spread'])/2, other:(r['total']-r['spread'])/2}

def matchup_table(m):
    L=['| Offense | Receiver (target share) | Likely defenders, ESTIMATE (PFR 2026: targets, YPT, TD/INT) | Status |','|---|---|---|---|']
    for t,v in m.items():
        for r in v['rows']:
            defs='<br>'.join(d.replace(' tgt,',' tgt,') for d in r['defs'][:3]) or 'not mapped'
            L.append(f"| {t} vs {v['opp']} | {r['player']} {r['pos']} ({r['tshare']*100:.1f}%) | {defs} | ESTIMATE, not a verified main defender |")
    return '\n'.join(L)

def rec_floor_rows(c,g):
    L=['| Player | Rung | Best price (book) | FD | Hit rate (last 8 / last 4) | Board sim P | Cushion | Gate result |','|---|---|---|---|---|---|---|---|']
    legs=[]
    for r in c['receiving']:
        fl=r.get('floor')
        if not fl: continue
        cu=cushion(r['ylog'],fl['rung'],fl['best'])
        gates=['no verified main defender (Phase 4)']
        if r['pos']=='WR' and r['rank']>=3: gates.append('#3 WR over ban')
        if wx_cut(g): gates.append('weather flag cuts receiving overs')
        if r.get('status'): gates.append(f"status {r['status']}")
        if cu[0]=='FAIL': gates.append('cushion FAIL')
        res='WATCH: '+'; '.join(gates)
        L.append(f"| {r['player']} ({r['team']} {r['pos']}#{r['rank']}) | {fl['rung']:g} | {fmt(fl['best'])} ({fl['best_book']}) | {fmt(fl.get('fd'))} | {round(fl['hit_all']*fl['n'])}/{fl['n']} / {fl['hit_l4']*4:.0f}/4 | {fl['board_sim'] if fl['board_sim'] is not None else 'n/a'} | {cu[0]}: {cu[1]} | {res} |")
        legs.append(dict(kind='rec',player=r['player'],team=r['team'],desc=f"{r['player']} receiving yards {fl['rung']:g}+ (alt) {fmt(fl['best'])} {fl['best_book']}",gates=gates,cush=cu,log=r['ylog'],pos=r['pos'],rank=r['rank']))
    return '\n'.join(L) if len(L)>2 else '_No receiving floor met the ladder rule (7 of 8 hit, last 4 all clear, break-even 55-80%)._', legs

def rush_floor_rows(c,g):
    L=['| Player | Carry share last 4 | 60% gate | Rung | Best price (book) | Hit rate | Cushion | Result |','|---|---|---|---|---|---|---|---|']
    legs=[]
    for r in c['rushing']:
        if r['gate60']!='PASS': continue
        fl=r.get('floor'); sh=', '.join(f'{s:.2f}' for s in r['shares'][-4:])
        if r.get('status') and 'OUT' in r['status'].upper():
            L.append(f"| {r['player']} ({r['team']}) | {sh} | PASS | - | - | - | - | OUT, not playing |"); continue
        if not fl:
            lad=[x for x in (r.get('ladder') or []) if x.get('n') and x['hit_all']>=(x['n']-1)/x['n'] and x['hit_l4']==1.0 and x.get('best') is not None]
            if lad:
                x=max(lad,key=lambda z:z['rung']); cu=cushion(r['ylog'],x['rung'],x['best'])
                L.append(f"| {r['player']} ({r['team']}) | {sh} | PASS ({r['n60_l4']} of 4) | {x['rung']:g} (deep) | {fmt(x['best'])} ({x['best_book']}) | {round(x['hit_all']*x['n'])}/{x['n']} | {cu[0]}: {cu[1]} | WATCH: only a deep rung qualifies (break-even {x['be_best']*100:.0f}%, outside the 55-80% band; little value) |")
            else:
                L.append(f"| {r['player']} ({r['team']}) | {sh} | PASS ({r['n60_l4']} of 4) | none | - | - | - | No rung cleared 7 of 8 with the last 4 all clear |")
            continue
        cu=cushion(r['ylog'],fl['rung'],fl['best'])
        dog = RICO[g]['fav']!=r['team']
        rec=next((x for x in c['receiving'] if x['player']==r['player']),None)
        tpg = statistics.mean(rec['tlog'][-4:]) if rec else None
        if dog and (tpg is None or tpg<4):
            L.append(f"| {r['player']} ({r['team']}) | {sh} | PASS ({r['n60_l4']} of 4) | {fl['rung']:g} | {fmt(fl['best'])} ({fl['best_book']}) | {round(fl['hit_all']*fl['n'])}/{fl['n']} | {cu[0]} | BLOCKED: rushing over on a team that could trail needs 4+ targets a game (last 4: {'unknown' if tpg is None else format(tpg,'.1f')}) |"); continue
        L.append(f"| {r['player']} ({r['team']}) | {sh} | PASS ({r['n60_l4']} of 4) | {fl['rung']:g} | {fmt(fl['best'])} ({fl['best_book']}) | {round(fl['hit_all']*fl['n'])}/{fl['n']} | {cu[0]}: {cu[1]} | WATCH (sims not run) |")
        legs.append(dict(kind='rush',player=r['player'],team=r['team'],desc=f"{r['player']} rushing yards {fl['rung']:g}+ (alt) {fmt(fl['best'])} {fl['best_book']}",gates=['sims not run'],cush=cu,log=r['ylog']))
    return '\n'.join(L) if len(L)>2 else '_No back passes the 60% carry gate with a priced ladder._', legs

def rush_under_rows(c):
    L=['| Player | Lines (Nov 20) | Best under | Log (most recent last) | Under hits all / last 4 | Source of log |','|---|---|---|---|---|---|']
    for r in c['rush_unders']:
        bu=r.get('best_under'); 
        if not bu: continue
        line=bu[1]; log=r['log']
        if r['pos']!='QB':
            rr=next((x for x in c['rushing'] if x['player']==r['player']),None)
            if rr and rr['gate60']!='PASS': continue
        mains='; '.join(f"{k} {v['line']:g} ({fmt(v['over'])}/{fmt(v['under'])})" for k,v in r['mains'].items())
        h=hits(log,line,False); h4=hits(log[-4:],line,False)
        L.append(f"| {r['player']} ({r['team']} {r['pos']}) | {mains} | {bu[0]} U{line:g} {fmt(bu[2])} (no-vig {bu[3]*100:.1f}%) | {', '.join(f'{v:g}' for v in log)} | {h}/{len(log)} / {h4}/{min(4,len(log))} | {'nflverse pbp incl. scrambles (pulled Sat 3:54 PM AST)' if r['pos']=='QB' else 'packet game log'} |")
    return '\n'.join(L)

def watch80(c):
    rows=[w for w in c['watch80'] if w.get('edge_vs_best') is not None]
    rows.sort(key=lambda w:-w['edge_vs_best'])
    keep=[w for w in rows if w['edge_vs_best']>=0.02][:4]
    if not keep: keep=rows[:2]
    L=['| Player | Model P(80+) | Book prices (79.5+ alt) | Best | Break-even at best | Blend | Edge vs best | Note |','|---|---|---|---|---|---|---|---|']
    gate={}
    for r in c['rushing']: gate[r['player']]=r['gate60']
    for w in keep:
        bk=', '.join(f"{k} {fmt(v)}" for k,v in sorted(w['books'].items(), key=lambda kv: BKORD.index(kv[0]) if kv[0] in BKORD else 9))
        fd=w['books'].get('FD')
        note=[]
        if w['edge_vs_best']>=0.03: note.append('clears +3 vs best price')
        else: note.append('under the +3 bar')
        if w.get('outliers'): note.append('outlier: '+str(w['outliers']))
        if gate.get(w['player'])=='FAIL': note.append('BLOCKED: back under 60% of carries')
        if w.get('status'): note.append(w['status'])
        if fd is None: note.append('no FD price')
        L.append(f"| {w['player']} ({w['team']}) | {w['p80_model']*100:.1f}% | {bk} | {w['best'][0]} {fmt(w['best'][1])} | {w['be_best']*100:.1f}% | {w['blend']*100:.1f}% | {w['edge_vs_best']*100:+.1f} pts | {'; '.join(note)} |")
    return '\n'.join(L), keep

def opp_table(c):
    L=['| Player | Role | Last-4 targets or carries | Last-4 yards | Opportunity label |','|---|---|---|---|---|']
    for r in c['receiving']:
        if r['pos'] in ('WR','TE') and r['rank']<=3:
            t4=r['tlog'][-4:]; y4=r['ylog'][-4:]
            lab='VOLUME-SUPPORTED' if statistics.mean(t4)>=6 else ('EFFICIENCY-DRIVEN' if statistics.mean(y4)>=50 else 'LOW VOLUME')
            L.append(f"| {r['player']} ({r['team']}) | {r['pos']}#{r['rank']}, {r['tshare']*100:.1f}% share | {', '.join(map(str,t4))} tgt | {', '.join(map(str,y4))} | {lab} |")
    for r in c['rushing']:
        if r['gate60']=='PASS' or max(r['shares'][-2:] or [0])>=0.5:
            L.append(f"| {r['player']} ({r['team']}) | RB, carry share {', '.join(f'{s:.2f}' for s in r['shares'][-4:])} | {', '.join(map(str,r['clog'][-4:]))} car | {', '.join(map(str,r['ylog'][-4:]))} | {'VOLUME-SUPPORTED' if r['gate60']=='PASS' else 'COMMITTEE (60% gate FAIL)'} |")
    return '\n'.join(L)

def shadow_sgp(g, leans, rlegs, flegs):
    legs=[]
    lt=' '.join(l[0] for l in leans)
    rlegs=[x for x in rlegs if x['player'] not in lt]; flegs=[x for x in flegs if x['player'] not in lt]
    for l in leans:
        if 'NO PLAY' in l[3]: continue
        legs.append((l[0], l[3]))
    for x in flegs: legs.append((x['desc'], 'WATCH; '+'; '.join(x['gates'])))
    for x in rlegs: legs.append((x['desc'], 'WATCH; sims not run; cushion '+x['cush'][0]))
    return legs

PH=['1 Data pull and reconcile','2 Opportunity gate','3 Defensive profile','4 Defender coverage check','5 Pressure, blitz, checkdown','6 QB grade card','7 Role and RB market rules','8 Injuries','9 Next Gen Stats','10 Film','11 Environment','12 Source audit','13 Game-script gate','14 Models, price, edge','15 Inactives check']
def phase_rows(leg, g):
    rec = leg['kind']=='rec'; under=leg['kind']=='under'; tot=leg['kind']=='total'
    wx=WX[g]
    rows=[]
    rows.append(('PASS','nflverse pbp through Week 11 TNF (release pulled Sat 3:54 PM AST) plus repo packet game logs','packet 2026-11-19 11:39 PM AST; pbp Sat 3:54 PM AST'))
    if tot: rows.append(('N/A','game-level market; volume is the scoring cross-check','-'))
    elif rec: rows.append(('FAIL' if (leg.get('pos')=='WR' and leg.get('rank',1)>=3) else 'PASS', f"{leg['pos']} rank #{leg.get('rank')}" + (' (#3 WR over ban)' if (leg.get('pos')=='WR' and leg.get('rank',1)>=3) else ''),'packet usage shares'))
    else: rows.append(('PASS','carry share gate / QB rush logs, see report','packet + pbp'))
    rows.append(('PASS','team defense allowed by position, through Week 10','packet 2026-11-19 11:39 PM AST'))
    rows.append(('UNVERIFIED' if rec else 'N/A','defender mapped by depth chart only (ESTIMATE); no per-route alignment source' if rec else 'not a receiving leg','PFR 2026 table in the board'))
    rows.append(('STALE' if rec else 'PASS','pressure rate 2026 from the packet; man/zone and MOF are 2025 only (STALE)' if rec else 'pressure rate 2026 from the packet (label PROXY where not real pressure)','packet / board'))
    rows.append(('MISSING','QB grade card (§15) not run this pass','-'))
    if leg['kind']=='rush': rows.append(('PASS','60%+ carry share in 3 of the last 4','packet team carries'))
    else: rows.append(('N/A' if not under else 'PASS','QB rush market' if under else 'not an RB leg','-'))
    rows.append(('PASS','Friday official designations plus Saturday public-web updates; final inactives pending','DIGEST Fri; web Sat ~3:50 PM AST'))
    rows.append(('MISSING','Next Gen Stats not pulled','-'))
    rows.append(('MISSING','no film review','-'))
    if rec and wx[2]: rows.append(('FAIL',f'{wx[0]}: receiving overs cut','conditions file Fri ~7:50 PM ET; MNF pulled Sat 3:57 PM AST'))
    else: rows.append(('PASS' if not wx[2] else 'PASS (flag noted)', wx[0],'conditions file / Sat pull'))
    rows.append(('STALE','prop prices from The Odds API Fri Nov 20 6:33 AM AST, over 48 h old by kickoff; packet over 24 h old','repo pregame/grok_lines'))
    rows.append(('PASS','script read written (base plus two flips); see report','this report'))
    rows.append(('MISSING','SIMULATION NOT RUN (projection_ready=false; NFL-49 and NFL-56 gates unmet)','-'))
    rows.append(('MISSING','inactives about 90 min before kickoff: not yet','-'))
    return rows

def checklist(g, legs):
    L=[f'VETTED: ______ (Ghost6 to sign, or REJECTED: reasons)','',f"# Checklist {g.replace('_','@')}, Week 11 (MANUAL RUN, requested Sat Nov 21 3:48 PM AST)",'','Every leg below is CUT for now: Phase 14 (SIMULATION NOT RUN) and Phase 15 (inactives) are MISSING, and Phase 12 is STALE. They are research leans and WATCH items, not picks.','']
    for leg in legs:
        L.append(f"## {leg['desc']}")
        L.append('| Leg | Phase | Status | Number | Source | Pulled |'); L.append('|---|---|---|---|---|---|')
        for ph,(st,num,src) in zip(PH,phase_rows(leg,g)):
            L.append(f"| {leg['desc'][:60]} | {ph} | {st} | {num} | {src} | {'-' if src=='-' else 'see source'} |")
        L.append('')
    L.append('## Summary block'); L.append('- Legs passed: 0 (gates unmet; sims not run).')
    L.append('- Legs cut and why: every leg MISSING Phase 6, 9, 10, 14 and 15 and STALE Phase 12. Receiving legs are also UNVERIFIED at Phase 4' + (' and FAIL at Phase 11 (weather flag).' if WX[g][2] else '.'))
    L.append('- Seeds: none (no simulation). Script paths: /workspace/runs/2026-11-22_W11_FOCUS9/_work/{extract,analyze,matchups,qbrush,gen}.py')
    L.append('- Data gaps: NGS, film, FTN model, Pinnacle, alt totals, half/quarter markets, 2026 man/zone, verified CB alignment.')
    return '\n'.join(L)

def report(g):
    f=json.load(open(f'facts_{g}.json')); c=json.load(open(f'cand_{g}.json')); m=json.load(open(f'match_{g}.json'))
    a,h=f['away'],f['home']; r=RICO[g]; wx=WX[g]; imp_=implied(g,f); cc,ctot=crosscheck(f)
    rec_tbl, flegs = rec_floor_rows(c,g); rush_tbl, rlegs = rush_floor_rows(c,g)
    w80_tbl, w80 = watch80(c)
    leans=LEANS[g]
    widealt=r['total']+7
    S=[]
    S.append(f"# {a} @ {h}, Week 11: research projection report")
    S.append('')
    S.append('**SIMULATION NOT RUN. RESEARCH ONLY, NOT VETTED, NOT PICKS.** Gate blocker: NFL-49 and NFL-56 are unmet and projection_ready=false. Nothing here goes to Rico as a pick until Ghost6 writes VETTED on the checklist.')
    S.append('')
    S.append(f"- MANUAL RUN (on demand, not the scheduled routine). Requested by Rico Sat Nov 21, 3:48 PM AST; written Sat Nov 21 about 4:05 PM AST.")
    S.append(f"- Kickoff: {r['kick']} ({AST[r['kick']]}). Venue: {r['venue']}.")
    S.append(f"- Data pulled: repo packet and board built Thu Nov 19, 11:39 PM AST (over 24 h old and before the final injury report, so every label is capped at Lean). Props from The Odds API Fri Nov 20, 6:33 AM AST (FD, DK, BetMGM, Caesars), STALE. Rico's consensus screenshot Sat 3:47 PM AST. nflverse pbp pulled Sat 3:54 PM AST. Injuries: Friday official reports plus Saturday public-web updates (sources below).")
    S.append(f"- Checklist: {OUT}/{a}@{h}/checklist.md")
    S.append('')
    S.append('## Five-line summary')
    top=[l for l in leans if 'LEAN' in l[3]]
    S.append(f"1. Market (Rico 3:47 PM AST): {r['fav']} -{r['spread']:g}, total {r['total']:g}; implied {', '.join(f'{t} {v:.2f}' for t,v in imp_.items())}.")
    S.append(f"2. Strongest research lean: {top[0][0] if top else 'none at Lean; WATCH only'}.")
    S.append(f"3. Weather/environment: {wx[0]}.")
    S.append(f"4. Season-average scoring cross-check: about {ctot:.1f} vs the {r['total']:g} total.")
    S.append(f"5. Receiving legs are all ESTIMATE/WATCH (no verified main defender){'; the weather flag also cuts receiving overs' if wx[2] else ''}. No passing-yards legs.")
    S.append('')
    S.append('## 1. Defender-by-receiver matchups (lead)')
    S.append('Per-defender alignment isn\'t publicly charted, so these maps come from the depth chart (WR to LCB/RCB/nickel) and the board\'s most-targeted LB/S (TE). They\'re ESTIMATES, and no receiving leg can go on a slip until a main defender is verified.')
    S.append('')
    S.append(matchup_table(m))
    S.append('')
    S.append('## 2. Game script')
    S.append(f"**Base:** {SCRIPT[g][0]}")
    S.append('')
    for i,fl in enumerate(SCRIPT[g][1],1): S.append(f"**Flip {i}:** {fl}")
    S.append('')
    S.append('Half and quarter spreads and totals: NOLINE in the Nov 20 files, so there are no period legs. If Rico prices them, they must match the base script above (the favorite\'s 1H/Q1 side follows its scoring script; under-lean games favor 1H unders).')
    S.append('')
    S.append('## 3. Slip-style core (research leans and WATCH, not picks)')
    S.append('### 3a. Game leans and rush-under spots')
    S.append('| Market | Line / price (book, time) | Evidence | Label | Kill-switch |'); S.append('|---|---|---|---|---|')
    for l in leans: S.append(f"| {l[0]} | {l[1]} | {l[2]} | {l[3]} | {l[4]} |")
    S.append('')
    S.append('### 3b. Wide alt total under')
    S.append(f"Suggested anchor rung: about {widealt:g} (main {r['total']:g} + 7). Alt-total prices are NOLINE in our files, so I have no price or no-vig. Verify it at the book before use. The scoring cross-check (about {ctot:.1f}) sits {'below' if ctot<widealt else 'ABOVE'} that rung{' by '+format(widealt-ctot,'.1f')+' points' if ctot<widealt else ', so the wide under is thin here'}.")
    S.append('')
    S.append('| Team | Offense points/game (rank) | Opponent defense allows (rank) | Average |'); S.append('|---|---|---|---|')
    for t,o,orr,d,dr,e in cc: S.append(f"| {t} | {o:.1f} ({orr}) | {d:.2f} ({dr}) | {e:.1f} |")
    S.append(f"| **Game** | | | **{ctot:.1f}** vs market {r['total']:g} |")
    S.append('')
    S.append('### 3c. Alt floors: rushing (60% carry gate applied)')
    S.append(rush_tbl); S.append('')
    S.append('### 3d. Alt floors: receiving (all WATCH)')
    S.append(rec_tbl); S.append('')
    S.append('### 3e. Rush-under board (QB logs include scrambles; backs only if they pass the 60% gate)')
    S.append(rush_under_rows(c)); S.append('')
    S.append('### 3f. Candidate SGP (Rico style: 6-8 legs, alt floors plus a wide alt total under)')
    sh=shadow_sgp(g,leans,rlegs,flegs)
    S.append('**None qualifies.** Gates are unmet, sims weren\'t run, and the receiving legs fail the verified-defender rule' + (' and the weather gate.' if wx[2] else '.') + ' Below is a WATCH-only shadow build that names the blocking gate on each leg; it isn\'t a slip.')
    S.append('')
    for i,(d,why) in enumerate(sh[:8],1): S.append(f"{i}. {d}: {why}")
    S.append(f"{min(len(sh),8)+1}. Wide alt total under about {widealt:g}: NOLINE, verify the price.")
    S.append('')
    S.append('Minimum-cushion check: every floor above shows its cushion. Any FAIL drops a rung or drops the leg.')
    S.append('')
    S.append('### 3g. Do not play')
    for d in c['dnp']: S.append(f"- {d}")
    S.append('- Any passing-yards leg (house rule).')
    S.append('')
    S.append('## 4. Opportunity table')
    S.append(opp_table(c)); S.append('')
    S.append('## 5. Brainstorm and critical review')
    S.append('| Angle | Verdict | Why |'); S.append('|---|---|---|')
    for a1,v,why in REVIEW[g]: S.append(f"| {a1} | {v} | {why} |")
    S.append('')
    S.append(f"**Case against the main read:** {CASE_AGAINST[g]}")
    S.append('')
    S.append('## 6. Market table and movement')
    S.append(game_market(f,g)); S.append('')
    S.append('Line movement: the Nov 20 book lines compared with Rico\'s Sat 3:47 PM AST consensus are the only two snapshots. True openers and Pinnacle are MISSING (no new Odds API pulls; the balance of 681 is below the 800 floor).')
    S.append('')
    S.append('## 7. Side list: 80+ yard long shots (WATCH only, outside the normal strategy)')
    S.append('This list holds players whose matchup gives them a better shot at 80+ yards than the price implies. It uses the dashboard watch model (watch.py: an even blend on the logit scale of the model P(80+) and the book break-even), judged against the best price at the 79.5 rung. The board model was built Thu night, before Saturday\'s news, so it\'s stale where injuries changed roles.')
    S.append(''); S.append(w80_tbl); S.append('')
    S.append('## 8. Injuries (source and time)')
    for i in INJ[g]: S.append(f"- {i}")
    S.append('')
    S.append('## 9. Weather and environment')
    S.append(f"- {wx[0]}: {wx[1]}")
    S.append('')
    S.append('## 10. Phases run')
    S.append('| Phase | Status for this game |'); S.append('|---|---|')
    st={1:'PASS',2:'PASS (shares, 60% gate)',3:'PASS',4:'UNVERIFIED (ESTIMATE maps only)',5:'PARTIAL (2026 pressure; blitz and man/zone 2025, STALE)',6:'MISSING (QB card not run)',7:'PASS',8:'PASS (final inactives pending)',9:'MISSING',10:'MISSING',11:('PASS, '+wx[0]),12:'STALE (props Nov 20; packet over 24 h old)',13:'PASS (script written)',14:'MISSING (SIMULATION NOT RUN)',15:'MISSING (pending inactives)'}
    for i,p in enumerate(PH,1): S.append(f"| {p} | {st[i]} |")
    S.append(''); S.append('Counts: PASS 8 (incl. partial), UNVERIFIED 1, STALE 1, MISSING 5. Gaps: phases 4, 5, 6, 9, 10, 12, 14 and 15.')
    S.append('')
    S.append('## 11. Sources by category')
    S.append('- Core stats and play-by-play: nflverse pbp 2026 (release pulled Sat 3:54 PM AST, through Week 11 TNF) for QB rushing including scrambles; repo packet game logs and team allowed/offense tables (built Thu 11:39 PM AST); PFR 2026 defender coverage lines in the board.')
    S.append('- Coverage schemes and matchups: board coverage_profile (2025 FTN-derived man/zone and shells, STALE); depth-chart CB/S/LB from the packet. Sharp, StatRankings and FTN 2026 not pulled (MISSING).')
    S.append('- Next Gen Stats: MISSING. Film: MISSING.')
    S.append('- Injuries and news: Friday DIGEST of official reports (/workspace/runs/2026-11-20_FRI_PRACTICE/DIGEST.md) and Saturday team sites, NFL.com, NBC/Rotoworld, CBS, SI, as cited in section 8.')
    S.append('- Weather: NWS and Open-Meteo via conditions_2026-11-22.md (Fri ~7:50 PM ET); MNF pulled Sat 3:57 PM AST.')
    S.append('- Odds and props: repo pregame/grok_lines (The Odds API, Fri Nov 20 6:33 AM AST); Rico\'s screenshot Sat 3:47 PM AST. Pinnacle, alt totals, period markets: MISSING/NOLINE.')
    S.append('- Simulation models: SIMULATION NOT RUN.')
    S.append('')
    S.append('## 12. Open items before kickoff')
    S.append('- Re-check every prop price at kickoff (Nov 20 prices). Any move over 0.5 or 20 cents means a reprice.')
    S.append('- Inactives about 90 minutes before kickoff; re-run the matchups for any replaced defender.')
    S.append('- Weather recheck about 4 hours before kickoff.' + (' Reinstate receiving overs only if the flag clears.' if wx[2] else ''))
    S.append('- Verify the main defender on any receiving leg before it can go on a slip.')
    S.append('- Run the three 100k models once the NFL-49 and NFL-56 gates clear; Ghost6 vets.')
    S.append('')
    S.append('Research only. Not validated. Not betting advice.')
    # checklist legs
    legs=[]
    for l in leans:
        t=l[0].lower()
        k='total' if 'total' in t else ('under' if (' under' in t and 'mirror' not in t) else ('rush' if 'rush' in t else 'rec'))
        if k=='rec': continue
        legs.append(dict(kind=k,desc=f"{l[0]} [{l[1][:50]}]"))
    lt=' '.join(l[0] for l in leans)
    legs+=[x for x in flegs+rlegs if x['player'] not in lt]
    return '\n'.join(S), checklist(g,legs), dict(leans=leans,w80=w80,dnp=c['dnp'],sh=sh,flegs=flegs,rlegs=rlegs,ctot=ctot,wx=wx)

summ={}
for g in GAMES:
    rep,chk,info=report(g)
    d=f"{OUT}/{g.replace('_','@')}"; os.makedirs(d,exist_ok=True)
    open(f'{d}/report.md','w').write(rep); open(f'{d}/checklist.md','w').write(chk)
    summ[g]=info
json.dump({g:{k:v for k,v in i.items() if k in('leans','ctot')} for g,i in summ.items()},open('summ.json','w'),default=str)
import pickle; pickle.dump(summ,open('summ.pkl','wb'))
print('done')

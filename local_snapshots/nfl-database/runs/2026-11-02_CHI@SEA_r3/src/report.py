import json
R='/workspace/nfl-database/runs/2026-11-02_CHI@SEA_r3'
B=json.load(open(R+'/src/build_legs.json')); M=json.load(open(R+'/run_manifest.json'))
f=lambda x:f"{x:.3f}"
L=[]
L+=['# Projection report: MNF Chicago Bears @ Seattle Seahawks (r3, game-day 4:30 PM ET routine)','',
'**Header.** Mon Nov 2 2026, Lumen Field (open air). Kickoff is 8:15 PM ET per ESPN (The Odds API lists 8:20 PM ET). ESPN calls this **Week 8**; the task called it Week 9. Week 8 is recorded. Price-sensitive data (FanDuel/DK/Pinnacle odds, ESPN injuries and news, NWS/Open-Meteo weather, nflverse pbp) was pulled at **4:38 PM ET**. Coverage was reused from 5:09 AM ET, PFR defenders from 5:10 and 6:40 AM ET, and NGS/FTN/snaps from 5:03 AM ET (all under 48h). Checklist: `checklist.md`. Manifest: `run_manifest.json`. Gate: `gate_output.txt`.','',
'**Bottom line: no card. All 23 legs evaluated are CUT, and 0 are live. No MANUAL_REVIEW leg is open: JSN O89.5 met the press/manual-review numbers but is barred as a nested rung of the open JSN 70+ ticket.**','']
L+=['## 1. Phases run (counts over 23 legs)']
for line in open(R+'/checklist.md'):
    if line.startswith('- Phase'): L.append(line.rstrip())
L+=['Gaps: Phase 4 has 4 UNVERIFIED (ISS-05 has no TE defender data for Loveland/Barner; Kupp\'s slot CB Gordon has no PFR row). Phase 10 has 6 UNVERIFIED (Kupp, Barner, R. Johnson and Wilson have no caption cue matched to pbp). All of these are on CUT legs.','']
L+=['## 2. Sources used, by category',
'- **Core stats / pbp:** nflverse play_by_play_2026 (release 2:29 PM ET, through Nov 1 incl. Week 8 SNF; pulled 4:38 PM ET with curl). Gives §7 last-4 with current QB, targets and carries. Snap counts and depth charts are nflverse (5:03 AM ET).',
'- **Coverage / matchups:** Sharp Football coverage schemes plus StatRankings CoverageIQ as the agreeing second source (5:09 AM ET). SEA plays 90.0% zone / 5.4% man (SR 82.3/17.7) with MOF open 60.6%. CHI plays 29.9% man (SR 39.4%) with MOF closed 53.6%. PFR per-defender advanced defense: CHI 5:10 AM ET; SEA via Firecrawl 6:40 AM ET. FTN charting supplies blitz rates. ESPN WR/CB matchups name defenders (JSN vs Malik Muhammad, Kupp vs Kyler Gordon, Odunze vs Devon Witherspoon, Burden vs Nick Emmanwori).',
'- **NGS:** nflverse NGS receiving/passing/rushing (5:03 AM ET): separation, aDOT and time to throw (Williams 3.22 s, Darnold 3.00 s).',
'- **Film:** official NFL YouTube Week 6-7 highlights for CHI and SEA. Auto-captions came through yt-dlp at 4:42 PM ET; the earlier 429 has cleared. 11 plays were matched to pbp rows (see `src/film_matches.md`).',
'- **Injuries / news:** ESPN injuries API plus league/CHI/SEA news (4:38 PM ET). Official-source checks of the Loeb claims are below.',
'- **Weather:** tools/weather_forecast.py (NWS + Open-Meteo only), 4:38 PM ET: precip 2%, wind 2.7 mph, gust 3.4 mph, NWS "Cloudy". No flag.',
'- **Odds / props:** The Odds API via pull_odds.py, FanDuel/DK/Pinnacle pregame only (0 in-play rows dropped), 4:38 PM ET. FD: SEA -3.5 (-102), total 46.5, ML CHI +152 / SEA -180. No PFF was used for weather, script or projections. Outlier was not used.','']
L+=['## Loeb claims (official sources only)']+[f"- **{k}:** {v}" for k,v in M['loeb_claims'].items()]
L+=['- Impact: CHI pass rush gets stronger (Sweat back, plus Simmons in his first CHI game). Neither is in CHI\'s 22.3% PROXY pressure rate. SEA still has LT Charles Cross OUT; Nelson upgrades the interior, not LT. Pressure is a flag only, because the pressure/pass-rush cuts were not adopted (Rico, 5:01 AM ET).','']
L+=['## Reprice (FD 4:38 PM ET vs r2/Ghost6 morning)',
'| Market | Earlier | Now | Moved enough to re-run P14? |','|---|---|---|---|',
'| Williams pass yds | 227.5 | 224.5 | yes (re-run: edge +2.6, cut) |','| Burden rec yds | 51.5 | 52.5 | yes (re-run: §7 1/4, cut) |',
'| Swift receptions O3.5 | +140 | +112 (alt +108) | yes, 28 cents (re-run: edge +2.5, cut) |','| Swift rush+rec | 81.5 | 86.5 | yes (cut, 10G and §7 1/4) |',
'| JSN rec yds 99.5 | -113/-113 (alt -114) | -113/-113 | no |','| Roschon rush yds | 12.5 | 10.5 | yes (cut) |','']
L+=['## Zone check: Odunze and Moore',
'- **Rome Odunze:** SEA is the most zone-heavy defense (90% Sharp / 82.3% SR). Odunze averages 44.8 yds/g against zone-heavy defenses and 67.3 against man-heavier ones (small n). Separation 2.48, aDOT 13.6. In Caleb games he is CHI\'s WR3 (targets: Burden 24, Raymond 18, Odunze 16), so the WR3 over ban applies. SEA has no CBs out, so the depleted-secondary exception is N/A. Unders: rec yds U38.5 has edge +1.9 and §7 0/4; rec U3.5 has negative edge. Both are cut.',
'- **D.J. Moore:** he plays for BUF in 2026 (27 targets in nflverse pbp). No Moore is on CHI or SEA and no Moore prop exists for this game, so the check is N/A.','']
L+=['## 3. Simulations','tools/sim_v6.py (LIVE version). Monte Carlo, Bias and Game Randomness each ran **100,000 sims, seed 20261101**. The unit tests passed first (108 OK). Fit was rerun at 4:42 PM ET on new pbp; the calib multipliers are unchanged (the fit window is weeks 4-7). **BUG-2026-11-02-BIASDUP is still present: Bias = MC. The fix is STAGED in tools/sim_v6_fix/ for the 11:45 PM ET swap and was NOT swapped in by this run.** Only MC and GR are independent votes.','',
'| Leg | FD price | no-vig | p MC / Bias / GR | median MC / Bias / GR | edge | shrunk |','|---|---|---|---|---|---|---|']
for x in B['legs']:
    p=x['p'];m=x['median']
    L.append(f"| {x['name']} | {x['price_fd']:+d} | {f(x['no_vig'])} | {f(p['mc'])} / {f(p['bias'])} / {f(p['gr'])} | {m['mc']:.1f} / {m['bias']:.1f} / {m['gr']:.1f} | {x['edge_3']:+.3f} | {x['shrunk']:+.3f} |")
L+=['','## 4. Projections and picks','**No leg passed, so there are no picks.**','','Cut legs and the phase that cut them:']
for x in B['legs']: L.append(f"- **{x['name']}** ({x['price_fd']:+d}): {'; '.join(x['cut_reasons'])}. §7: {x['recent_form']['values']} with {x['recent_form']['qb']}." + (f" Note: {x['note']}" if x['note'] else ''))
L+=['- No SEA RB leg: Charbonnet has 0 games in 2026 (sim can\'t price him; P1 MISSING), and J. Price was activated at 4:05 PM ET with no 2026 sample. Committee.','']
L+=['## Open-ticket bar (the task\'s rule: bar same player+stat or nested rung)',
'- Live SGP (Ghost6 bankroll_slips.md, 4:11 PM ET): JSN 70+ rec yds, JSN TD, Swift 50+ rush+rec, Swift TD, E. Wilson 15+ rush, Under 58.5. **All JSN rec-yds rungs are barred (99.5, 89.5, 109.5).** JSN receptions, Swift and Wilson legs get the §11 one-slip-per-player flag.',
'- **Ambiguous:** r2/odunze/results.md (~1:20 PM ET) says "Swift 3+ and Burden 4+ placed", and the 7-leg ticket containing Swift 3+ was cashed out (Ghost6, 4:10 PM ET). I could not confirm whether a separate Swift 3+ or Burden 4+ ticket is still open. Swift receptions rungs are treated as barred (fail closed); they fail Phase 14 anyway.','']
L+=['## 5. Risks and checks still to come','- **6:50 PM ET inactives:** '+' | '.join(M['inactives_watch_650pm']),
'- **LOW-SAMPLE / PROXY:** pressure rate is a PROXY. Roschon Johnson has only 2 carry games. Charbonnet and Price have no 2026 sample. SEA LB coverage on RBs is a first-tackler proxy.',
'- **UNVERIFIED film:** Kupp, Barner, R. Johnson and Wilson (all cut).',
'- **Week label:** ESPN says Week 8 and the task says Week 9.',
'- **Odds staleness:** odds were pulled at 4:38 PM ET and the gate allows 1h. Any later use needs a fresh pull and a re-gate.',
'- **Applied exceptions:** none. BIASDUP is still staged (see section 3).','']
g=open(R+'/gate_output.txt').read() if __import__('os').path.exists(R+'/gate_output.txt') else 'GATE NOT YET RUN'
open(R+'/report.md','w').write('## Gate output\n```\n'+g.strip()+'\n```\n\n'+'\n'.join(L)+'\n')

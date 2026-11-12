import json,csv
L=[r for r in json.load(open('legs_all.json'))]
def dec(o): return 1+(o/100 if o>0 else 100/-o)
def amer(d): return f"+{round((d-1)*100)}" if d>=2 else f"{round(-100/(d-1))}"
CUT_EXTRA={('Drake London','recyds'):'HARD area cut: TB defense flagged "Hard vs WRs overall" (Sharp WR YPT 7.2, rank 25/32) - over into a strength (skill sec.8)'}
FLAG={('CeeDee Lamb','recyds'):'Lamb 60+ yds is already on placed FD SGP Ticket 2 - skill sec.11 bars a player on two slips; Rico/Ghost6 decide',
      ('Jahmyr Gibbs','rushyds'):'Gibbs (5+ rec) is already on placed FD SGP Ticket 2 - same-player conflict; Rico/Ghost6 decide'}
INJ={'LA':'LAC: S Derwin James OUT, CB Deane Leonard OUT, G Awosika OUT (helps LAR passing); LAR: TE Parkinson Q, LS Cardona D',
 'DAL':'ARI: DT Walter Nolen OUT, G Gaines OUT; DAL: Turpin OUT (more Lamb targets), Pickens Q (if he sits, Lamb gains)','ARI':'DAL: LB Dee Winters OUT (coverage LB - helps TE); ARI: G Gaines OUT, TE Reiman OUT (McBride share up)',
 'LV':'NYJ: DT Sweat OUT, DE Ossai OUT, LB Bailey D, OT Max Mitchell OUT (NYJ side); LV: DE P.Johnson OUT','PIT':'CLE: none listed; PIT: CB Slaughter, CB Echols OUT (defense - longer CLE drives); WR Skowronek Q',
 'DET':'MIN: none listed; DET: S Kerby Joseph OUT (defense)'}
legs=[];cut=[]
for r in L:
  k=(r['player'],r['market'])
  if r.get('rung') and k not in CUT_EXTRA: legs.append(r)
  else: cut.append((k,CUT_EXTRA.get(k,r.get('cut'))))
mk={'rec':'Receptions','recyds':'Receiving Yds','rushyds':'Rushing Yds','rushrec':'Rush+Rec Yds'}
o=["# BetGuru: three groups for Sun Nov 1, 2026 (Week 8) - RESEARCH ONLY, Rico places bets",
f"Built Sat Oct 31 ~7:10 PM ET. FanDuel prices pulled {L[0]['fd_pulled_at'][:16]} ET (public sbapi, fd_pull_all.py). Rebuild: /workspace/nfl-database/week8/betguru_2026-11-01_raw/ (build_legs.py seeds 101/202/303, legs_all.json, leg_*.json, sims_summary.csv).",
"","## Headline",f"- Only {len(legs)} of {len(L)} candidate props passed every computable gate. That fills ONE group of six, not three. Groups 2 and 3 were NOT padded.",
"- **Strict-rule warning:** two required inputs are MISSING for every leg: (a) the individual CB/S coverage numbers (per-defender catches/yards allowed are paid-only - PFF/FantasyPoints; checklist P7.cb_suppression = UNAVAILABLE), used here only as a PBP proxy (defender named on completions); (b) NGS route-tendency percentages (public NGS route charts are images of targeted routes; route participation is UNAVAILABLE). Under the 'any missing input cuts the leg' rule, ALL legs fail. Ghost6/Rico must decide whether the proxy is acceptable.",
"- Outlier / PropsMadness: MISSING (browser-only; not reached). Two volume sources used instead: ESPN box scores (fixes.sqlite player_stats) + nflverse usage/snaps (fix_player_game_usage / fix_player_role).",
"- Two legs (Lamb, Gibbs) conflict with Rico's placed FD SGP Ticket 2 (same player) - flagged.",""]
tot=1;rows=[]
o.append("## Group A (the only group that passed)")
o.append("| # | Player | Mkt | Rung | FD | MC | Bias | GameRand | Avg | Flag |");o.append("|-|-|-|-|-|-|-|-|-|-|")
for i,r in enumerate(legs,1):
  s=r['sims'];avg=(s['mc']['p']+s['bias']['p']+s['gr']['p'])/3;tot*=dec(r['price'])
  o.append(f"|{i}|{r['player']} ({r['team']} vs {r['opp']})|{mk[r['market']]}|{r['rung']}+|{r['price']}|{s['mc']['p']:.3f}|{s['bias']['p']:.3f}|{s['gr']['p']:.3f}|{avg:.3f}|{FLAG.get((r['player'],r['market']),'')}|")
  rows.append([r['player'],r['team'],r['opp'],r['market'],r['rung'],r['price'],s['mc']['p'],s['bias']['p'],s['gr']['p'],round(avg,4),r['fair_devig'],r['status'],FLAG.get((r['player'],r['market']),'')])
import numpy as np
ph=np.prod([x[9] for x in rows])
o.append(f"\nCombined FD price (independent legs, SGP will reprice for same-game Lamb+McBride): {amer(tot)} ({tot:.2f}x). Product of avg sim probs = {ph:.3f} (~1 in {1/ph:.1f}).")
o.append("Without the two placed-ticket conflicts (4 legs): see per-leg prices; alternates = none passed.\n")
o.append("## Group B / Group C: NOT BUILT - not enough legs passed (see Cuts).\n")
o.append("## Rams backfield verdict (Corum vs Kyren)")
o.append("Sources: nflverse snaps (fix_player_game_usage) + ESPN box & play-by-play (summary API).\n- Wk4 @PHI: Kyren 83% snaps, 16 car/13 tgt, first-drive RB touches = Kyren; Corum 15%, 5 car.\n- Wk5 vs BUF: Kyren 73%, 16 car/8 tgt, first RB carry = Kyren; Corum 27%, 5 car.\n- Wk6 vs ARI: Kyren 72%, 10 car (first play of game was a Kyren run); Corum 28%, 9 car.\n- Wk7 @LV: Kyren 51%, 16 car 99 yds; Corum 44%, 17 car 93 yds (first drive was 3 passes, no RB touch).\n**Verdict: Kyren Williams is still the starter** (took the first RB touch in every game where one came on drive 1, and led snaps every week). Corum's role is growing fast: snaps 15→27→28→44% and he out-carried Kyren 17-16 last week. Treat it as a near-split committee going forward; no Rams RB leg passed the gates (Kyren rush+rec failed L4 hit gate).\n")
o.append("## Leg cards")
for i,r in enumerate(legs,1):
  s=r['sims'];R=r['role'];d=r['opp_def'];lg=r['logs_espn'][-4:];us=r['usage_nflverse'][-4:]
  def g(k): return d.get(k,'MISSING')
  o.append(f"### A{i}. {r['player']} - {mk[r['market']]} {r['rung']}+ @ {r['price']} (FD main: {r['fd_main']})")
  o.append(f"- Game: {r['team']} vs {r['opp']}, spread {r['team']} {r['spread']:+}, total {r['total']}. Status: {r['status']}. Raw: leg_{r['player'].replace(' ','_').replace('.','')}_{r['market']}.json")
  o.append(f"- Opportunity (src1 ESPN box L4): " + "; ".join(f"{x['date'][5:]} {x['tg']}tg/{x['rec']}rec/{x['ryd']}yd/{x['car']}car/{x['rush']}ru" for x in lg))
  o.append(f"- Opportunity (src2 nflverse): season tgt share {R['tgt_share']:.0%}, L3 {R['tgt_share_l3']:.0%}; carry share {R['car_share']:.0%} (L3 {R['car_share_l3']:.0%}); {R['tpg']:.1f} tgt/g, {R['cpg']:.1f} car/g; snaps L3 {R['snap_l3']:.0%} (60% gate PASS); last-4 snap%: {[u['snap'] for u in us]}")
  o.append(f"- L4 values vs rung: {r['l4_vals']} -> {r['l4_hits']}/4 cleared.")
  o.append(f"- Coverage/scheme ({r['opp']}, Sharp via {r['opp_def_src'].split('/')[-1]}): Man/Zone/MOFC/MOFO % = {g('Man / Zone / MOFC / MOFO %')}; YPT WR/TE/RB {g('Sharp YPT WR / TE / RB')}; Outside/Slot {g('Sharp YPT Outside / Slot')}; blitz {g('Blitz % (Sharp) / FTN blitz % (n=254)') if 'Blitz % (Sharp) / FTN blitz % (n=254)' in d else [v for k,v in d.items() if k.startswith('Blitz')][:1]}.")
  o.append(f"- Defender matchup: individual CB/S allowed = **MISSING (paid)**. PBP proxy (defender named on completions to his position, Wk1-7): " + "; ".join(f"{x['defender']} {x['rec_allowed']} rec/{x['yds_allowed']} yds" for x in r['cov_proxy']))
  o.append(f"- Explosives allowed/g (WR20+, TE20+, RB10+run, RB20+rec, stuffs): {g('Explosives/g: WR 20+ rec, TE 20+, RB 10+ run, RB 20+ rec, stuffs')}")
  o.append(f"- Team allowed/g: WR {g('WR tgt / rec / yds per g (pbp)')}; TE {g('TE tgt / rec / yds per g')}; RB rec {g('RB rec tgt / rec / yds per g')}; RB rush {g('RB rush car / yds per g, YPC')}. Soft: {r['opp_soft'] or 'none'}; Hard: {r['opp_hard']}")
  o.append(f"- 3rd-down / RZ TD% allowed: {g('3rd-down % allowed / RZ TD % allowed (trips)')}. EPA/play allowed: {g('EPA/play allowed (pbp)')}")
  o.append(f"- Injuries: {INJ.get(r['team'],'see injury_sweep_2026-11-01.md')}")
  o.append(f"- Routes: NGS route-tendency % MISSING (public charts are targeted-route images only). Area read uses Sharp outside/slot YPT above.")
  o.append(f"- Weather: {r['weather']}")
  o.append(f"- Sims (100k each): MC {s['mc']['p']:.3f} (median {s['mc']['median']}), Bias {s['bias']['p']:.3f} (median {s['bias']['median']}), GameRand {s['gr']['p']:.3f} (median {s['gr']['median']}, P(team leads) {s['gr']['p_team_leads']}). De-vigged FD {r['fair_devig']:.3f}. Matchup factor {r['matchup_factor']}.")
  o.append(f"- Phase checklist (PHASE_SCRIPT + skill): P0 injury PASS ({r['status']}) | P1 role lock PASS | P2 coverage profile PASS (team) / defender-level MISSING | P3 environment PASS (spread/total above) | P4 opportunity gate PASS (snaps {R['snap_l3']:.0%}, share above) | P5 role grade PASS (no Hard spot in his area) | P6 triggers checked | P7 recent env PASS ({r['l4_hits']}/4) | P8 projection = model medians > rung PASS | P9 three-model PASS (all >=0.60) | P10-11 FD line + edge PASS (+{(sum(s[k]['p'] for k in ('mc','bias','gr'))/3-r['fair_devig'])*100:.1f} pts vs de-vig) | Skill s.14 cushion/catch rules checked by rung choice | NGS routes MISSING | Outlier/PropsMadness MISSING | 11:30 AM inactives recheck REQUIRED.")
  if FLAG.get((r['player'],r['market'])): o.append(f"- FLAG: {FLAG[(r['player'],r['market'])]}")
  o.append("")
o.append("## Anytime TDs\nNone built (separate section reserved; not requested in the gate pass).\n")
o.append(f"## Cuts ({len(cut)} of {len(L)} candidate props)")
for k,why in cut: o.append(f"- {k[0]} {mk[k[1]]}: {why}")
o.append("""
## Follow-up (Sat ~7:05 PM ET): name-match fix via ESPN athlete IDs (Cook 4379399 'James Cook III', A. Jones 3042519 'Aaron Jones Sr.', B. Allen 4685247, Godwin 3116165; FD lists Godwin as 'Chris Godwin')
All re-graded through the same gates/three 100k sims (rungs_eval in leg_*.json, sims_summary.csv). Phase checklist: P0 injury PASS (none on report), P1 role PASS, P4 opportunity PASS (snaps L3: Cook 62%, Jones 62%, Allen 84%, Godwin 84%), then failures at P9-P11:
- James Cook rush yds (main 82.5 -113). L4 rushing 135/154/75/111, 71% L3 carry share. 80+ @ -130: MC .730 / Bias .661 / GR .760 (avg .717) vs de-vig .541 -> edge 17.6 pts > 15-pt model-overconfidence cap -> CUT. 70+ @ -210: avg .834 (above 82% mid-rung band) -> CUT. ALSO on placed Ticket 2 (Cook 70+ rush+rec) = same-player conflict.
- James Cook rush+rec 96.5 @ -113 (main only, no FD alt ladder): MC .647 / Bias .577 / GR .713 (avg .646) -> bias <60% and avg <65% -> CUT. Ticket 2 conflict.
- Aaron Jones rush yds: FD main is only 29.5 (-113) vs his 17-25 carry games; last game 8 car/26 yds. Models 94-98% at 30+, de-vig .51 -> edge far beyond cap: the market is pricing a role/health change our data doesn't show -> CUT pending news check (do not bet a model-vs-market gap this size).
- Braelon Allen rush yds: logs now matched (L4 14/24/17/17 car), but FanDuel has NO Braelon Allen rushing market posted -> line MISSING -> CUT.
- Chris Godwin receptions (main 4.5 +100). 4+ @ -225: MC .696 / Bias .641 / GR .735 (avg .691) vs de-vig .663 -> edge 2.8 pts < 3 -> CUT (L4 catches 6/3/4/4). 5+ @ -102: avg .412 -> CUT. ALSO on placed Ticket 2 (Godwin 4+ rec) = conflict.
Result: no new passing legs; Group B still not formed.""")
open('/workspace/nfl-database/week8/betguru_three_groups_2026-11-01.md','w').write("\n".join(o))
w=csv.writer(open('/workspace/nfl-database/week8/betguru_three_groups_2026-11-01.csv','w'));w.writerow(['player','team','opp','market','rung','fd_price','p_mc','p_bias','p_gamerand','p_avg','fd_devig','status','flag']);w.writerows(rows)
w=csv.writer(open('sims_summary.csv','w'));w.writerow(['player','market','rung','odds','mc','bias','gr','cons','fair'])
for r in L:
  for ln,v in (r.get('rungs_eval') or {}).items(): w.writerow([r['player'],r['market'],ln,v['odds'],v['mc'],v['bias'],v['gr'],v['cons'],v['fair']])
print(amer(tot),ph,len(legs),len(cut))

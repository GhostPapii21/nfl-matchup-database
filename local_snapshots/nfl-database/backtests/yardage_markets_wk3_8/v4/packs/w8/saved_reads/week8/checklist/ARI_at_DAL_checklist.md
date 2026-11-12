# ARI @ DAL — Week 8 60-check manifest
Game 401873024, Sun Nov 01 01:00 PM ET, AT&T Stadium (indoor), DAL -7 / 54.5. Built 2026-10-29 05:25 EDT. Status counts: {'PASS': 16, 'PARTIAL': 30, 'NOT_APPLICABLE': 4, 'UNAVAILABLE': 7, 'UNIMPLEMENTED': 3}

| # | Check | Status | Reason | Evidence |
|-|-|-|-|-|
|1|P1.pbp|PASS|Repo SQLite plays (ESPN PBP) Wk1–7 + nflverse via overlay|repo/data/nfl_matchups.sqlite; fixes/fixes.sqlite|
|2|P1.boxscores|PASS|player_stats + fix_player_game_usage|fixes/fixes.sqlite|
|3|P1.tackles_sacks|PARTIAL|fix_play_credits reconciled; tackler≠coverage defender|fixes/FIXES.md|
|4|P1.pressure|PARTIAL|Pressure is opponent-Sharp-allowed proxy + pbp sack/hit; no charted pressure source|defense/ARI_at_DAL.md|
|5|P1.ol_snaps|PARTIAL|nflverse participation snaps only; Wk7 participation lag possible|fixes/fixes.sqlite fix_participation|
|6|P1.air_yards|PARTIAL|NGS IAY per QB; per-target air yards via nflverse only where loaded|defense/raw|
|7|P1.redzone|PASS|RZ targets/goal-line carries in baselines|team_baselines/ARI.md, DAL.md|
|8|P1.scrambles|PARTIAL|fix_qb_rushing scramble flags from nflverse; ESPN PBP lacks explicit flag|fixes/fixes.sqlite fix_qb_rushing|
|9|P2.team_defense|PASS|Production + explosive counts per game|defense/ARI_at_DAL.md|
|10|P2.coverage|PASS|Sharp coverage pages dated Oct 20 = CURRENT per user (last games before slate)|defense/SOURCES.md|
|11|P2.individual_assignments|PARTIAL|Only PBP-named defenders on big plays (weak signal); no charted assignment source|team_baselines/|
|12|P2.weakest_link|PARTIAL|Alignment-level weakest link from Sharp ranks (see Soft spots); player-level unverified|defense/ARI_at_DAL.md|
|13|P2.pressure_trend|PARTIAL|ESPN PRWR through Wk6 only; pbp sack/hit trend|defense/ARI_at_DAL.md|
|14|P3.team_offense|PASS|QB/team production|team_baselines/|
|15|P3.player_roles|PASS|Roles + L3 vs season shares; roster-checked 2026-10-29 05:25 EDT|defense/ARI_at_DAL.md; rosters/|
|16|P3.ol_health|PARTIAL|OL designations from ESPN injuries; Thu practice pending|injuries.json|
|17|P3.target_hierarchy|PASS|L3 vs season target/carry share (opportunity gate inputs)|team_baselines/|
|18|P3.routes_gaps|PARTIAL|NGS separation/cushion; run gaps from pbp direction; no route participation|defense/raw|
|19|P3.qb_blitz|PASS|FTN EPA vs blitz / no-blitz per offense|defense/ARI_at_DAL.md|
|20|P4.slip_comparison|NOT_APPLICABLE|No slip supplied for this game|—|
|21|P4.injury_alerts|PARTIAL|Wed status logged; Thursday reports PENDING|injuries.json; this file Injury impact|
|22|P4.script_risk|PARTIAL|Backup-QB/workload risk noted from injuries; 10G labels pending|this file|
|23|P5.bundle|PARTIAL|Markdown/JSON bundle; no engine-versioned bundle|week8/|
|24|P5.provenance|PARTIAL|sha256 of inputs recorded below; engine code/model hash unavailable (nfl.py on user Mac)|this file|
|25|P5.source_preservation|PASS|Repo SQLite untouched; fixes in overlay|fixes/PATCH_SPEC.md|
|26|P6.live_policy|NOT_APPLICABLE|Pregame; live polling off|—|
|27|P7.ngs_targeted_charts|PARTIAL|NGS public leaderboards (sep/cushion/YACOE/TTT); per-game targeted charts not read|defense/raw|
|28|P7.all_routes|UNAVAILABLE|Route participation not in any public source loaded|—|
|29|P7.run_concepts|UNAVAILABLE|No verified run-concept source; film pending|film/|
|30|P7.strength_map|PARTIAL|Sharp alignment YPT + box rates; no side-level split|defense/ARI_at_DAL.md|
|31|P7.rb_suppression|PARTIAL|RB YPC/rush+rec allowed + game state; RB quality adj not applied|defense/ARI_at_DAL.md|
|32|P7.cb_suppression|UNAVAILABLE|Individual CB coverage stats are paid/not loaded|—|
|33|P7.panthers_rule|PARTIAL|QB NGS/blitz review for: Jacoby Brissett, Dak Prescott; exact OL/pass-rush matchup not charted|defense/ARI_at_DAL.md|
|34|P8.film|PARTIAL|Codex YouTube highlight notes done for ARI 2/6 games, DAL 2/6 (film/codex_out, still running; not yet verified vs pbp by this worker)|film/codex_out|
|35|P8.personnel|UNAVAILABLE|Personnel packages need film; depth chart formation only|rosters/|
|36|P8.scheme|PARTIAL|Coverage shells from Sharp (man/zone/MOFC); fronts/run fits need film|defense/ARI_at_DAL.md|
|37|P8.missed_looks|UNAVAILABLE|Pending verified film notes|film/|
|38|P8.film_notes|PARTIAL|Codex notes unverified; hypotheses only|film/codex_out|
|39|P9.weather|NOT_APPLICABLE|NOT_APPLICABLE: indoor/roof (ESPN indoor=true)|slate.json|
|40|P9.rest_travel|PASS|ARI last game 2026-10-25 (7 days rest); DAL last game 2026-10-27 (5 days). Time-zone change only from venue, no itineraries invented|ESPN team schedule API|
|41|P9.stakes|PARTIAL|Records from ESPN scoreboard; divisional/rematch not a 2026 rematch; playoff-odds not pulled|defense/ARI_at_DAL.md|
|42|P9.injury_spikes|PARTIAL|Exact-game availability: Wed designations; Thu/Fri + inactives pending|injuries.json|
|43|P9.turnovers|PARTIAL|Turnovers in pbp/baselines; rolling interpretation not modeled|team_baselines/|
|44|P9.situational_efficiency|PASS|3rd-down % and RZ TD % allowed|defense/ARI_at_DAL.md|
|45|P9.unclassified|PARTIAL|Roster moves reviewed (rosters/ROSTER_CHANGES.md); travel/coaching notes not reviewed|rosters/ROSTER_CHANGES.md|
|46|P10.espn|PARTIAL|ESPN PRWR/RSWR through Wk6 only|defense/SOURCES.md|
|47|P10.position|PASS|Sharp positional/alignment YPT (current per user)|defense/SOURCES.md|
|48|P10.scheme|PASS|Sharp man/zone/MOFC/MOFO|defense/SOURCES.md|
|49|P10.tendencies|PASS|Blitz %, box rates, sub % (Sharp + FTN)|defense/SOURCES.md|
|50|P10.advanced|PASS|EPA/play allowed from pbp|defense/ARI_at_DAL.md|
|51|P10.individual_db|UNAVAILABLE|Individual CB sites not loaded; PFF grades NOT required by user|—|
|52|P10G.script_gate|PARTIAL|Spread DAL -7/total 54.5 recorded; script label PENDING (accepted by user); underdog-script legs blocked until labeled|slate.json|
|53|MODEL.inputs|PARTIAL|Numbers sourced; identities roster-checked; Thu injuries pending|rosters/; injuries.json|
|54|MODEL.lineup|PARTIAL|Starting QB per ESPN depth chart; Questionables unresolved|rosters/ARI.json, DAL.json|
|55|MODEL.simulation|UNIMPLEMENTED|SIMULATION NOT RUN — user 100k engine outputs/nfl.py is on user Mac, not in repo|GAME_SCRIPT_2026-10-29.md|
|56|MODEL.calibration|UNIMPLEMENTED|No independent chronological validation without engine|—|
|57|TICKET.markets|UNAVAILABLE|FD/DK prop lines not pulled in this pass|—|
|58|TICKET.roles_matchups|PARTIAL|Soft-spot candidates pass role+volume screen; final after Thu injuries|defense/ARI_at_DAL.md|
|59|TICKET.correlation|UNIMPLEMENTED|No ticket built|—|
|60|TICKET.cap|NOT_APPLICABLE|No ticket built (6 target / 7 max applies when built)|—|

## Injury impact (ESPN injuries API 2026-10-29T09:07:59Z; Thursday official reports PENDING)

**ARI offense (vs DAL defense)**
- Tyler Allgeier RB — Questionable; practice: Allgeier (toe) didn't practice Wednesday, Darren Urban of the Cardinals' official site reports.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-29T00:16ZZ
- Michael Wilson WR — Questionable; practice: Wilson (ribs) was a limited participant in Wednesday's practice, Darren Urban of the Cardinals' official site reports.; depth chart next at WR: Simi Fehoko. src ts 2026-10-29T00:12ZZ
- Elijah Wilkinson OT — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at RT: Jedrick Wills Jr.. src ts 2026-10-29T00:09ZZ
- Jeremiyah Love RB — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at RB: Tyler Allgeier. src ts 2026-10-28T21:06ZZ
- Jon Gaines II G — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at RG: Hayden Conner. src ts 2026-10-27T13:11ZZ
- Carson Beck QB — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-27T13:11ZZ
- Tip Reiman TE — Out; practice: official Wed/Thu table not in source (Thu PENDING); no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-26T22:29ZZ
**ARI defense (faced by DAL)**
- Andrew Wingard S — Questionable; practice: Wingard (knee) was a limited participant at practice Wednesday, Darren Urban of the Cardinals' official site reports.; depth chart next at FS: Joey Blount. src ts 2026-10-29T01:16ZZ
- Mack Wilson Sr. LB — Questionable; practice: Wilson (knee) did not participate at practice Wednesday, Darren Urban of the Cardinals' official site reports.; depth chart next at MLB: Cody Simon. src ts 2026-10-29T01:12ZZ
- Kei'Trel Clark CB — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-29T00:10ZZ
- Zaven Collins LB — Questionable; practice: Thu PENDING; depth chart next at SLB: Baron Browning. src ts 2026-10-29T00:09ZZ
- Max Melton CB — Questionable; practice: Thu PENDING; depth chart next at NB: Kalen King. src ts 2026-10-27T13:11ZZ
- Walter Nolen III DT — Questionable; practice: Thu PENDING; depth chart next at RDT: L.J. Collier. src ts 2026-10-27T13:11ZZ
- IR (ARI): Jalen Brooks WR, James Conner RB

**DAL offense (vs ARI defense)**
- KaVontae Turpin WR — Questionable; practice: Turpin (ribs) did not participate in Wednesday's practice, Jon Machota of The Athletic reports.; depth chart next at PR: Jonathan Mingo. src ts 2026-10-29T01:07ZZ
- George Pickens WR — Questionable; practice: Pickens (shoulder/hamstring) was limited at Wednesday's practice, Jon Machota of The Athletic reports.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T22:20ZZ
- Drew Shelton OT — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-27T13:11ZZ
**DAL defense (faced by ARI)**
- Quinnen Williams DT — Questionable; practice: Williams (hamstring) was a limited participant in Wednesday's practice, Jon Machota of The Athletic reports.; depth chart next at LDE: LT Overton. src ts 2026-10-29T01:18ZZ
- Caleb Downs S — Questionable; practice: Downs (ankle) was a limited participant in Wednesday's practice, Jon Machota of The Athletic reports.; depth chart next at SS: Markquese Bell. src ts 2026-10-29T01:16ZZ
- Dee Winters LB — Questionable; practice: Winters (calf) did not participate in Wednesday's practice, Jon Machota of The Athletic reports.; depth chart next at RILB: Shemar James. src ts 2026-10-29T01:11ZZ
- IR (DAL): P.J. Locke S, Marist Liufau LB

Profile effect rule: a missing starter (CB1/S/edge/OL) is noted as a *direction* only (e.g. outside coverage may soften); Sharp/pbp allowance numbers are NOT adjusted and targets/carries are NOT redistributed without evidence (replacement's own snaps/targets). Questionable = scripted on low alts/fade, never cut; 90-min inactive approval goes to the user.

## Roster cross-check of named candidates
- Michael Wilson (ARI): FLAG-Q — Questionable — script low alts/fade, not cut. Wilson (ribs) was a limited participant in Wednesday's practice, Darren Urban of the Cardinals' official site reports.
- Jalen Brooks (ARI): REMOVE — Injured Reserve per ESPN injuries (2026-10-27T21:53Z): The Cardinals placed Brooks (wrist) on injured reserve Tuesday.
- George Pickens (DAL): FLAG-Q — Questionable — script low alts/fade, not cut. Pickens (shoulder/hamstring) was limited at Wednesday's practice, Jon Machota of The Athletic reports.
- Marvin Harrison Jr. (ARI): REMOVE — not on ARI ESPN roster (2026-10-29 05:25 EDT); not on any Sunday-team roster (traded to non-slate team, released, or IR)
- Emari Demercado (DAL): REMOVE — not on DAL ESPN roster (2026-10-29 05:25 EDT); not on any Sunday-team roster (traded to non-slate team, released, or IR)

## Provenance (sha256/16)
- slate.json: e7ace10e143abac4
- injuries.json: 184dbf2c1ed2f78d
- defense/ARI_at_DAL.md: 63a058ee2e434198
- rosters/ARI.json: 151c493e7248ed0b
- rosters/DAL.json: 874ca08c3302c68f
- ../fixes/fixes.sqlite: 50a82f6968d6fd46

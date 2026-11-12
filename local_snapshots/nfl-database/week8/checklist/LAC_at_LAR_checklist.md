# LAC @ LAR — Week 8 60-check manifest
Game 401873032, Sun Nov 01 04:05 PM ET, SoFi Stadium (outdoor), LAR -6.5 / 45.5. Built 2026-10-29 05:25 EDT. Status counts: {'PASS': 16, 'PARTIAL': 30, 'NOT_APPLICABLE': 3, 'UNAVAILABLE': 8, 'UNIMPLEMENTED': 3}

| # | Check | Status | Reason | Evidence |
|-|-|-|-|-|
|1|P1.pbp|PASS|Repo SQLite plays (ESPN PBP) Wk1–7 + nflverse via overlay|repo/data/nfl_matchups.sqlite; fixes/fixes.sqlite|
|2|P1.boxscores|PASS|player_stats + fix_player_game_usage|fixes/fixes.sqlite|
|3|P1.tackles_sacks|PARTIAL|fix_play_credits reconciled; tackler≠coverage defender|fixes/FIXES.md|
|4|P1.pressure|PARTIAL|Pressure is opponent-Sharp-allowed proxy + pbp sack/hit; no charted pressure source|defense/LAC_at_LAR.md|
|5|P1.ol_snaps|PARTIAL|nflverse participation snaps only; Wk7 participation lag possible|fixes/fixes.sqlite fix_participation|
|6|P1.air_yards|PARTIAL|NGS IAY per QB; per-target air yards via nflverse only where loaded|defense/raw|
|7|P1.redzone|PASS|RZ targets/goal-line carries in baselines|team_baselines/LAC.md, LAR.md|
|8|P1.scrambles|PARTIAL|fix_qb_rushing scramble flags from nflverse; ESPN PBP lacks explicit flag|fixes/fixes.sqlite fix_qb_rushing|
|9|P2.team_defense|PASS|Production + explosive counts per game|defense/LAC_at_LAR.md|
|10|P2.coverage|PASS|Sharp coverage pages dated Oct 20 = CURRENT per user (last games before slate)|defense/SOURCES.md|
|11|P2.individual_assignments|PARTIAL|Only PBP-named defenders on big plays (weak signal); no charted assignment source|team_baselines/|
|12|P2.weakest_link|PARTIAL|Alignment-level weakest link from Sharp ranks (see Soft spots); player-level unverified|defense/LAC_at_LAR.md|
|13|P2.pressure_trend|PARTIAL|ESPN PRWR through Wk6 only; pbp sack/hit trend|defense/LAC_at_LAR.md|
|14|P3.team_offense|PASS|QB/team production|team_baselines/|
|15|P3.player_roles|PASS|Roles + L3 vs season shares; roster-checked 2026-10-29 05:25 EDT|defense/LAC_at_LAR.md; rosters/|
|16|P3.ol_health|PARTIAL|OL designations from ESPN injuries; Thu practice pending|injuries.json|
|17|P3.target_hierarchy|PASS|L3 vs season target/carry share (opportunity gate inputs)|team_baselines/|
|18|P3.routes_gaps|PARTIAL|NGS separation/cushion; run gaps from pbp direction; no route participation|defense/raw|
|19|P3.qb_blitz|PASS|FTN EPA vs blitz / no-blitz per offense|defense/LAC_at_LAR.md|
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
|30|P7.strength_map|PARTIAL|Sharp alignment YPT + box rates; no side-level split|defense/LAC_at_LAR.md|
|31|P7.rb_suppression|PARTIAL|RB YPC/rush+rec allowed + game state; RB quality adj not applied|defense/LAC_at_LAR.md|
|32|P7.cb_suppression|UNAVAILABLE|Individual CB coverage stats are paid/not loaded|—|
|33|P7.panthers_rule|PARTIAL|QB NGS/blitz review for: Justin Herbert; exact OL/pass-rush matchup not charted|defense/LAC_at_LAR.md|
|34|P8.film|PARTIAL|Codex YouTube highlight notes done for LAC 2/6 games, LAR 2/6 (film/codex_out, still running; not yet verified vs pbp by this worker)|film/codex_out|
|35|P8.personnel|UNAVAILABLE|Personnel packages need film; depth chart formation only|rosters/|
|36|P8.scheme|PARTIAL|Coverage shells from Sharp (man/zone/MOFC); fronts/run fits need film|defense/LAC_at_LAR.md|
|37|P8.missed_looks|UNAVAILABLE|Pending verified film notes|film/|
|38|P8.film_notes|PARTIAL|Codex notes unverified; hypotheses only|film/codex_out|
|39|P9.weather|NOT_APPLICABLE|SoFi Stadium has a fixed translucent roof (ESPN flags indoor=false); open-air sides, so wind/rain effect is minimal|slate.json|
|40|P9.rest_travel|PASS|LAC last game 2026-10-18 (14 days rest); LAR last game 2026-10-25 (7 days). Time-zone change only from venue, no itineraries invented|ESPN team schedule API|
|41|P9.stakes|PARTIAL|Records from ESPN scoreboard; divisional/rematch not a 2026 rematch; playoff-odds not pulled|defense/LAC_at_LAR.md|
|42|P9.injury_spikes|PARTIAL|Exact-game availability: Wed designations; Thu/Fri + inactives pending|injuries.json|
|43|P9.turnovers|PARTIAL|Turnovers in pbp/baselines; rolling interpretation not modeled|team_baselines/|
|44|P9.situational_efficiency|PASS|3rd-down % and RZ TD % allowed|defense/LAC_at_LAR.md|
|45|P9.unclassified|PARTIAL|Roster moves reviewed (rosters/ROSTER_CHANGES.md); travel/coaching notes not reviewed|rosters/ROSTER_CHANGES.md|
|46|P10.espn|PARTIAL|ESPN PRWR/RSWR through Wk6 only|defense/SOURCES.md|
|47|P10.position|PASS|Sharp positional/alignment YPT (current per user)|defense/SOURCES.md|
|48|P10.scheme|PASS|Sharp man/zone/MOFC/MOFO|defense/SOURCES.md|
|49|P10.tendencies|PASS|Blitz %, box rates, sub % (Sharp + FTN)|defense/SOURCES.md|
|50|P10.advanced|PASS|EPA/play allowed from pbp|defense/LAC_at_LAR.md|
|51|P10.individual_db|UNAVAILABLE|Individual CB sites not loaded; PFF grades NOT required by user|—|
|52|P10G.script_gate|PARTIAL|Spread LAR -6.5/total 45.5 recorded; script label PENDING (accepted by user); underdog-script legs blocked until labeled|slate.json|
|53|MODEL.inputs|PARTIAL|Numbers sourced; identities roster-checked; Thu injuries pending|rosters/; injuries.json|
|54|MODEL.lineup|PARTIAL|Starting QB per ESPN depth chart; Questionables unresolved|rosters/LAC.json, LAR.json|
|55|MODEL.simulation|UNIMPLEMENTED|SIMULATION NOT RUN — user 100k engine outputs/nfl.py is on user Mac, not in repo|GAME_SCRIPT_2026-10-29.md|
|56|MODEL.calibration|UNIMPLEMENTED|No independent chronological validation without engine|—|
|57|TICKET.markets|UNAVAILABLE|FD/DK prop lines not pulled in this pass|—|
|58|TICKET.roles_matchups|PARTIAL|Soft-spot candidates pass role+volume screen; final after Thu injuries|defense/LAC_at_LAR.md|
|59|TICKET.correlation|UNIMPLEMENTED|No ticket built|—|
|60|TICKET.cap|NOT_APPLICABLE|No ticket built (6 target / 7 max applies when built)|—|

## Injury impact (ESPN injuries API 2026-10-29T09:07:59Z; Thursday official reports PENDING)

**LAC offense (vs LAR defense)**
- Brenen Thompson WR — Questionable; practice: Thompson (quadriceps/hamstring) did not participate at practice Wednesday.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T23:57ZZ
- Tre' Harris WR — Questionable; practice: Harris (hamstring) was a limited participant in Wednesday's practice.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T23:13ZZ
- Ladd McConkey WR — Questionable; practice: McConkey (concussion) was a full participant in Wednesday's practice.; depth chart next at WR: KeAndre Lambert-Smith. src ts 2026-10-28T22:36ZZ
- Kayode Awosika G — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at LG: Logan Taylor. src ts 2026-10-20T16:10ZZ
**LAC defense (faced by LAR)**
- Deane Leonard CB — Questionable; practice: Leonard (concussion) did not participate in Wednesday's practice, Alex Insdorf of BoltBeat.com reports.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-29T01:33ZZ
- Derwin James Jr. S — Doubtful; practice: Thu PENDING; depth chart next at SS: Tony Jefferson. src ts 2026-10-28T23:55ZZ
- Rodney Shelley CB — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-20T16:10ZZ
- Donte Jackson CB — Questionable; practice: Thu PENDING; depth chart next at RCB: Deane Leonard. src ts 2026-10-20T16:10ZZ
- IR (LAC): Denzel Perryman LB

**LAR offense (vs LAC defense)**
- Coleman Shelton C — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at C: Dylan McMahon. src ts 2026-10-28T23:32ZZ
- Colby Parkinson TE — Questionable; practice: Parkinson did not participate in Wednesday's practice due to a rib injury, Adam Grosbard of The Orange County Register reports.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T23:18ZZ
**LAR defense (faced by LAC)**
- Nate Landman LB — Questionable; practice: Landman (concussion) was a full participant in Wednesday's practice, Stu Jackson of the Rams' official site reports.; depth chart next at LILB: Grant Stuard. src ts 2026-10-29T00:49ZZ
- Trent McDuffie CB — Questionable; practice: McDuffie (groin) was a limited participant in Wednesday's practice, Stu Jackson of the Rams' official site reports.; depth chart next at RCB: Emmanuel Forbes Jr.. src ts 2026-10-29T00:44ZZ
- Joe Cardona LS — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T23:32ZZ
- IR (LAR): Terrance Ferguson TE, Davante Adams WR, Myles Garrett DE

Profile effect rule: a missing starter (CB1/S/edge/OL) is noted as a *direction* only (e.g. outside coverage may soften); Sharp/pbp allowance numbers are NOT adjusted and targets/carries are NOT redistributed without evidence (replacement's own snaps/targets). Questionable = scripted on low alts/fade, never cut; 90-min inactive approval goes to the user.

## Roster cross-check of named candidates
- Davante Adams (LAR): REMOVE — Injured Reserve per ESPN injuries (2026-10-28T20:59Z): Head coach Sean McVay said Wednesday that Adams had successful surgery on his left hamstring, and the Rams are hopeful that the wide receive
- Colby Parkinson (LAR): FLAG-Q — Questionable — script low alts/fade, not cut. Parkinson did not participate in Wednesday's practice due to a rib injury, Adam Grosbard of The Orange County Register reports.
- Marquez Valdes-Scantling (LAC): REMOVE — not on LAC ESPN roster (2026-10-29 05:25 EDT); now on [('PIT', 'Practice Squad')]

## Provenance (sha256/16)
- slate.json: e7ace10e143abac4
- injuries.json: 184dbf2c1ed2f78d
- defense/LAC_at_LAR.md: 96ad2bdb11563743
- rosters/LAC.json: 578dcf52a257d8f5
- rosters/LAR.json: 1457b78813411a2f
- ../fixes/fixes.sqlite: 50a82f6968d6fd46

# IND @ JAX — Week 8 60-check manifest
Game 401873028, Sun Nov 01 01:00 PM ET, EverBank Stadium (outdoor), JAX -10 / 46.5. Built 2026-10-29 05:25 EDT. Status counts: {'PASS': 16, 'PARTIAL': 31, 'NOT_APPLICABLE': 3, 'UNAVAILABLE': 7, 'UNIMPLEMENTED': 3}

| # | Check | Status | Reason | Evidence |
|-|-|-|-|-|
|1|P1.pbp|PASS|Repo SQLite plays (ESPN PBP) Wk1–7 + nflverse via overlay|repo/data/nfl_matchups.sqlite; fixes/fixes.sqlite|
|2|P1.boxscores|PASS|player_stats + fix_player_game_usage|fixes/fixes.sqlite|
|3|P1.tackles_sacks|PARTIAL|fix_play_credits reconciled; tackler≠coverage defender|fixes/FIXES.md|
|4|P1.pressure|PARTIAL|Pressure is opponent-Sharp-allowed proxy + pbp sack/hit; no charted pressure source|defense/IND_at_JAX.md|
|5|P1.ol_snaps|PARTIAL|nflverse participation snaps only; Wk7 participation lag possible|fixes/fixes.sqlite fix_participation|
|6|P1.air_yards|PARTIAL|NGS IAY per QB; per-target air yards via nflverse only where loaded|defense/raw|
|7|P1.redzone|PASS|RZ targets/goal-line carries in baselines|team_baselines/IND.md, JAX.md|
|8|P1.scrambles|PARTIAL|fix_qb_rushing scramble flags from nflverse; ESPN PBP lacks explicit flag|fixes/fixes.sqlite fix_qb_rushing|
|9|P2.team_defense|PASS|Production + explosive counts per game|defense/IND_at_JAX.md|
|10|P2.coverage|PASS|Sharp coverage pages dated Oct 20 = CURRENT per user (last games before slate)|defense/SOURCES.md|
|11|P2.individual_assignments|PARTIAL|Only PBP-named defenders on big plays (weak signal); no charted assignment source|team_baselines/|
|12|P2.weakest_link|PARTIAL|Alignment-level weakest link from Sharp ranks (see Soft spots); player-level unverified|defense/IND_at_JAX.md|
|13|P2.pressure_trend|PARTIAL|ESPN PRWR through Wk6 only; pbp sack/hit trend|defense/IND_at_JAX.md|
|14|P3.team_offense|PASS|QB/team production|team_baselines/|
|15|P3.player_roles|PASS|Roles + L3 vs season shares; roster-checked 2026-10-29 05:25 EDT|defense/IND_at_JAX.md; rosters/|
|16|P3.ol_health|PARTIAL|OL designations from ESPN injuries; Thu practice pending|injuries.json|
|17|P3.target_hierarchy|PASS|L3 vs season target/carry share (opportunity gate inputs)|team_baselines/|
|18|P3.routes_gaps|PARTIAL|NGS separation/cushion; run gaps from pbp direction; no route participation|defense/raw|
|19|P3.qb_blitz|PASS|FTN EPA vs blitz / no-blitz per offense|defense/IND_at_JAX.md|
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
|30|P7.strength_map|PARTIAL|Sharp alignment YPT + box rates; no side-level split|defense/IND_at_JAX.md|
|31|P7.rb_suppression|PARTIAL|RB YPC/rush+rec allowed + game state; RB quality adj not applied|defense/IND_at_JAX.md|
|32|P7.cb_suppression|UNAVAILABLE|Individual CB coverage stats are paid/not loaded|—|
|33|P7.panthers_rule|PARTIAL|QB NGS/blitz review for: Daniel Jones, Trevor Lawrence; exact OL/pass-rush matchup not charted|defense/IND_at_JAX.md|
|34|P8.film|PARTIAL|Codex YouTube highlight notes done for IND 2/6 games, JAX 3/6 (film/codex_out, still running; not yet verified vs pbp by this worker)|film/codex_out|
|35|P8.personnel|UNAVAILABLE|Personnel packages need film; depth chart formation only|rosters/|
|36|P8.scheme|PARTIAL|Coverage shells from Sharp (man/zone/MOFC); fronts/run fits need film|defense/IND_at_JAX.md|
|37|P8.missed_looks|UNAVAILABLE|Pending verified film notes|film/|
|38|P8.film_notes|PARTIAL|Codex notes unverified; hypotheses only|film/codex_out|
|39|P9.weather|PARTIAL|Forecast (Open-Meteo, pulled 2026-10-29 05:25 EDT) kickoff hr: 80.3°F, precip prob 33%, wind 14.6 mph gust 19.0 — 3-day-out forecast, re-pull Sat/Sun|https://api.open-meteo.com|
|40|P9.rest_travel|PASS|IND last game 2026-10-25 (7 days rest); JAX last game 2026-10-18 (14 days). Time-zone change only from venue, no itineraries invented|ESPN team schedule API|
|41|P9.stakes|PARTIAL|Records from ESPN scoreboard; divisional/rematch not a 2026 rematch; playoff-odds not pulled|defense/IND_at_JAX.md|
|42|P9.injury_spikes|PARTIAL|Exact-game availability: Wed designations; Thu/Fri + inactives pending|injuries.json|
|43|P9.turnovers|PARTIAL|Turnovers in pbp/baselines; rolling interpretation not modeled|team_baselines/|
|44|P9.situational_efficiency|PASS|3rd-down % and RZ TD % allowed|defense/IND_at_JAX.md|
|45|P9.unclassified|PARTIAL|Roster moves reviewed (rosters/ROSTER_CHANGES.md); travel/coaching notes not reviewed|rosters/ROSTER_CHANGES.md|
|46|P10.espn|PARTIAL|ESPN PRWR/RSWR through Wk6 only|defense/SOURCES.md|
|47|P10.position|PASS|Sharp positional/alignment YPT (current per user)|defense/SOURCES.md|
|48|P10.scheme|PASS|Sharp man/zone/MOFC/MOFO|defense/SOURCES.md|
|49|P10.tendencies|PASS|Blitz %, box rates, sub % (Sharp + FTN)|defense/SOURCES.md|
|50|P10.advanced|PASS|EPA/play allowed from pbp|defense/IND_at_JAX.md|
|51|P10.individual_db|UNAVAILABLE|Individual CB sites not loaded; PFF grades NOT required by user|—|
|52|P10G.script_gate|PARTIAL|Spread JAX -10/total 46.5 recorded; script label PENDING (accepted by user); underdog-script legs blocked until labeled|slate.json|
|53|MODEL.inputs|PARTIAL|Numbers sourced; identities roster-checked; Thu injuries pending|rosters/; injuries.json|
|54|MODEL.lineup|PARTIAL|Starting QB per ESPN depth chart; Questionables unresolved|rosters/IND.json, JAX.json|
|55|MODEL.simulation|UNIMPLEMENTED|SIMULATION NOT RUN — user 100k engine outputs/nfl.py is on user Mac, not in repo|GAME_SCRIPT_2026-10-29.md|
|56|MODEL.calibration|UNIMPLEMENTED|No independent chronological validation without engine|—|
|57|TICKET.markets|UNAVAILABLE|FD/DK prop lines not pulled in this pass|—|
|58|TICKET.roles_matchups|PARTIAL|Soft-spot candidates pass role+volume screen; final after Thu injuries|defense/IND_at_JAX.md|
|59|TICKET.correlation|UNIMPLEMENTED|No ticket built|—|
|60|TICKET.cap|NOT_APPLICABLE|No ticket built (6 target / 7 max applies when built)|—|

## Injury impact (ESPN injuries API 2026-10-29T09:07:59Z; Thursday official reports PENDING)

**IND offense (vs JAX defense)**
- Drew Ogletree TE — Questionable; practice: Ogletree (knee) was estimated as a limited participant on the Colts' official injury report Wednesday.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-29T00:12ZZ
- Anthony Gould WR — Questionable; practice: Gould (concussion) was estimated as a limited participant on the Colts' official injury report Wednesday.; depth chart next at PR: Josh Downs. src ts 2026-10-29T00:08ZZ
- Tyler Warren TE — Questionable; practice: Warren (groin) returned to practice as a limited participant Wednesday.; depth chart next at TE: Will Mallory. src ts 2026-10-28T20:01ZZ
- Matt Goncalves G — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at RG: Jalen Farmer. src ts 2026-10-28T19:56ZZ
**IND defense (faced by JAX)**
- Sauce Gardner CB — Questionable; practice: Gardner (calf) was estimated as a limited participant on the Colts' official injury report Wednesday.; depth chart next at LCB: Kenneth Harris. src ts 2026-10-29T00:15ZZ
- Tim Smith DT — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T19:56ZZ
- Bryce Boettcher LB — Questionable; practice: Thu PENDING; depth chart next at SLB: Austin Ajiake. src ts 2026-10-27T13:11ZZ
- Justin Walley CB — Questionable; practice: Thu PENDING; depth chart next at NB: Kapena Gushiken. src ts 2026-10-26T21:15ZZ
- IR (IND): Cam Taylor-Britt CB, Alec Pierce WR

**JAX offense (vs IND defense)**
- Jakobi Meyers WR — Questionable; practice: Meyers (hamstring) was a limited participant in Wednesday's practice due to a hamstring injury.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T20:16ZZ
**JAX defense (faced by IND)**
- Jahlani Tavai LB — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T20:09ZZ
- Ruke Orhorhoro DT — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T20:09ZZ
- Ross Matiscik LS — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-20T16:10ZZ
- Antonio Johnson S — Questionable; practice: Thu PENDING; depth chart next at FS: Kaevon Merriweather. src ts 2026-10-18T16:57ZZ
- IR (JAX): Anton Harrison OT

Profile effect rule: a missing starter (CB1/S/edge/OL) is noted as a *direction* only (e.g. outside coverage may soften); Sharp/pbp allowance numbers are NOT adjusted and targets/carries are NOT redistributed without evidence (replacement's own snaps/targets). Questionable = scripted on low alts/fade, never cut; 90-min inactive approval goes to the user.

## Roster cross-check of named candidates
- Jakobi Meyers (JAX): FLAG-Q — Questionable — script low alts/fade, not cut. Meyers (hamstring) was a limited participant in Wednesday's practice due to a hamstring injury.
- Alec Pierce (IND): REMOVE — Injured Reserve per ESPN injuries (2026-10-26T18:37Z): Colts head coach Shane Steichen said Monday that Pierce (heel) will "most likely not" have his 21-day practice window opened in Week 8, Jake

## Provenance (sha256/16)
- slate.json: e7ace10e143abac4
- injuries.json: 184dbf2c1ed2f78d
- defense/IND_at_JAX.md: 045d2744475e4507
- rosters/IND.json: ee262c174ee6a7ba
- rosters/JAX.json: f8deeb8e12c77fff
- ../fixes/fixes.sqlite: 50a82f6968d6fd46

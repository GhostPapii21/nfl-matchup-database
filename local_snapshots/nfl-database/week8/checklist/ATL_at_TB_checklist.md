# ATL @ TB — Week 8 60-check manifest
Game 401873025, Sun Nov 01 01:00 PM ET, Raymond James Stadium (outdoor), TB -2.5 / 44.5. Built 2026-10-29 05:25 EDT. Status counts: {'PASS': 16, 'PARTIAL': 31, 'NOT_APPLICABLE': 3, 'UNAVAILABLE': 7, 'UNIMPLEMENTED': 3}

| # | Check | Status | Reason | Evidence |
|-|-|-|-|-|
|1|P1.pbp|PASS|Repo SQLite plays (ESPN PBP) Wk1–7 + nflverse via overlay|repo/data/nfl_matchups.sqlite; fixes/fixes.sqlite|
|2|P1.boxscores|PASS|player_stats + fix_player_game_usage|fixes/fixes.sqlite|
|3|P1.tackles_sacks|PARTIAL|fix_play_credits reconciled; tackler≠coverage defender|fixes/FIXES.md|
|4|P1.pressure|PARTIAL|Pressure is opponent-Sharp-allowed proxy + pbp sack/hit; no charted pressure source|defense/ATL_at_TB.md|
|5|P1.ol_snaps|PARTIAL|nflverse participation snaps only; Wk7 participation lag possible|fixes/fixes.sqlite fix_participation|
|6|P1.air_yards|PARTIAL|NGS IAY per QB; per-target air yards via nflverse only where loaded|defense/raw|
|7|P1.redzone|PASS|RZ targets/goal-line carries in baselines|team_baselines/ATL.md, TB.md|
|8|P1.scrambles|PARTIAL|fix_qb_rushing scramble flags from nflverse; ESPN PBP lacks explicit flag|fixes/fixes.sqlite fix_qb_rushing|
|9|P2.team_defense|PASS|Production + explosive counts per game|defense/ATL_at_TB.md|
|10|P2.coverage|PASS|Sharp coverage pages dated Oct 20 = CURRENT per user (last games before slate)|defense/SOURCES.md|
|11|P2.individual_assignments|PARTIAL|Only PBP-named defenders on big plays (weak signal); no charted assignment source|team_baselines/|
|12|P2.weakest_link|PARTIAL|Alignment-level weakest link from Sharp ranks (see Soft spots); player-level unverified|defense/ATL_at_TB.md|
|13|P2.pressure_trend|PARTIAL|ESPN PRWR through Wk6 only; pbp sack/hit trend|defense/ATL_at_TB.md|
|14|P3.team_offense|PASS|QB/team production|team_baselines/|
|15|P3.player_roles|PASS|Roles + L3 vs season shares; roster-checked 2026-10-29 05:25 EDT|defense/ATL_at_TB.md; rosters/|
|16|P3.ol_health|PARTIAL|OL designations from ESPN injuries; Thu practice pending|injuries.json|
|17|P3.target_hierarchy|PASS|L3 vs season target/carry share (opportunity gate inputs)|team_baselines/|
|18|P3.routes_gaps|PARTIAL|NGS separation/cushion; run gaps from pbp direction; no route participation|defense/raw|
|19|P3.qb_blitz|PASS|FTN EPA vs blitz / no-blitz per offense|defense/ATL_at_TB.md|
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
|30|P7.strength_map|PARTIAL|Sharp alignment YPT + box rates; no side-level split|defense/ATL_at_TB.md|
|31|P7.rb_suppression|PARTIAL|RB YPC/rush+rec allowed + game state; RB quality adj not applied|defense/ATL_at_TB.md|
|32|P7.cb_suppression|UNAVAILABLE|Individual CB coverage stats are paid/not loaded|—|
|33|P7.panthers_rule|PARTIAL|QB NGS/blitz review for: Michael Penix Jr., Baker Mayfield; exact OL/pass-rush matchup not charted|defense/ATL_at_TB.md|
|34|P8.film|PARTIAL|Codex YouTube highlight notes done for ATL 3/6 games, TB 3/6 (film/codex_out, still running; not yet verified vs pbp by this worker)|film/codex_out|
|35|P8.personnel|UNAVAILABLE|Personnel packages need film; depth chart formation only|rosters/|
|36|P8.scheme|PARTIAL|Coverage shells from Sharp (man/zone/MOFC); fronts/run fits need film|defense/ATL_at_TB.md|
|37|P8.missed_looks|UNAVAILABLE|Pending verified film notes|film/|
|38|P8.film_notes|PARTIAL|Codex notes unverified; hypotheses only|film/codex_out|
|39|P9.weather|PARTIAL|Forecast (Open-Meteo, pulled 2026-10-29 05:25 EDT) kickoff hr: 79.6°F, precip prob 47%, wind 14.3 mph gust 18.1 — 3-day-out forecast, re-pull Sat/Sun|https://api.open-meteo.com|
|40|P9.rest_travel|PASS|ATL last game 2026-10-25 (7 days rest); TB last game 2026-10-25 (7 days). Time-zone change only from venue, no itineraries invented|ESPN team schedule API|
|41|P9.stakes|PARTIAL|Records from ESPN scoreboard; divisional/rematch not a 2026 rematch; playoff-odds not pulled|defense/ATL_at_TB.md|
|42|P9.injury_spikes|PARTIAL|Exact-game availability: Wed designations; Thu/Fri + inactives pending|injuries.json|
|43|P9.turnovers|PARTIAL|Turnovers in pbp/baselines; rolling interpretation not modeled|team_baselines/|
|44|P9.situational_efficiency|PASS|3rd-down % and RZ TD % allowed|defense/ATL_at_TB.md|
|45|P9.unclassified|PARTIAL|Roster moves reviewed (rosters/ROSTER_CHANGES.md); travel/coaching notes not reviewed|rosters/ROSTER_CHANGES.md|
|46|P10.espn|PARTIAL|ESPN PRWR/RSWR through Wk6 only|defense/SOURCES.md|
|47|P10.position|PASS|Sharp positional/alignment YPT (current per user)|defense/SOURCES.md|
|48|P10.scheme|PASS|Sharp man/zone/MOFC/MOFO|defense/SOURCES.md|
|49|P10.tendencies|PASS|Blitz %, box rates, sub % (Sharp + FTN)|defense/SOURCES.md|
|50|P10.advanced|PASS|EPA/play allowed from pbp|defense/ATL_at_TB.md|
|51|P10.individual_db|UNAVAILABLE|Individual CB sites not loaded; PFF grades NOT required by user|—|
|52|P10G.script_gate|PARTIAL|Spread TB -2.5/total 44.5 recorded; script label PENDING (accepted by user); underdog-script legs blocked until labeled|slate.json|
|53|MODEL.inputs|PARTIAL|Numbers sourced; identities roster-checked; Thu injuries pending|rosters/; injuries.json|
|54|MODEL.lineup|PARTIAL|Starting QB per ESPN depth chart; Questionables unresolved|rosters/ATL.json, TB.json|
|55|MODEL.simulation|UNIMPLEMENTED|SIMULATION NOT RUN — user 100k engine outputs/nfl.py is on user Mac, not in repo|GAME_SCRIPT_2026-10-29.md|
|56|MODEL.calibration|UNIMPLEMENTED|No independent chronological validation without engine|—|
|57|TICKET.markets|UNAVAILABLE|FD/DK prop lines not pulled in this pass|—|
|58|TICKET.roles_matchups|PARTIAL|Soft-spot candidates pass role+volume screen; final after Thu injuries|defense/ATL_at_TB.md|
|59|TICKET.correlation|UNIMPLEMENTED|No ticket built|—|
|60|TICKET.cap|NOT_APPLICABLE|No ticket built (6 target / 7 max applies when built)|—|

## Injury impact (ESPN injuries API 2026-10-29T09:07:59Z; Thursday official reports PENDING)

**ATL offense (vs TB defense)**
- Olamide Zaccheaus WR — Questionable; practice: Zaccheaus (shoulder) was a limited participant in Wednesday's practice, Tori McElhaney of the Falcons' official site reports.; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-29T00:07ZZ
- Jawaan Taylor OT — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at RT: Ethan Onianwa. src ts 2026-10-28T20:01ZZ
- Brian Robinson Jr. RB — Questionable; practice: Robinson (hamstring) officially didn't practice Wednesday, Tori McElhaney of the Falcons' official site reports.; depth chart next at KR: Olamide Zaccheaus. src ts 2026-10-28T19:58ZZ
**ATL defense (faced by TB)**
- Divine Deablo LB — Questionable; practice: Deablo (forearm) did not participate in Wednesday's practice, Tori McElhaney of the Falcons' official site reports.; depth chart next at RILB: Harold Perkins Jr.. src ts 2026-10-29T00:12ZZ
- Charles Snowden LB — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T20:01ZZ
- LaCale London DE — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T20:00ZZ
- Samson Ebukam DE — Questionable; practice: Thu PENDING; depth chart next at SLB: Jared Ivey. src ts 2026-10-28T20:00ZZ
- Avieon Terrell CB — Questionable; practice: Thu PENDING; no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-27T13:11ZZ
- Billy Bowman Jr. CB — Questionable; practice: Thu PENDING; depth chart next at NB: Mike Hughes. src ts 2026-10-27T13:11ZZ

**TB offense (vs ATL defense)**
- Kenny Gainwell RB — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); no ESPN depth-chart starter slot (not a listed starter). src ts 2026-10-28T20:35ZZ
- Emeka Egbuka WR — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at WR: Tez Johnson. src ts 2026-10-28T20:26ZZ
- Luke Goedeke OT — Questionable; practice: official Wed/Thu table not in source (Thu PENDING); depth chart next at RT: Benjamin Chukwuma. src ts 2026-10-27T13:11ZZ
**TB defense (faced by ATL)**
- Josiah Trotter LB — Questionable; practice: Trotter (illness) did not practice Wednesday, Brianna Dix of the Buccaneers' official site reports.; depth chart next at RILB: SirVocea Dennis. src ts 2026-10-29T00:19ZZ
- Yaya Diaby LB — Questionable; practice: Thu PENDING; depth chart next at SLB: David Walker. src ts 2026-10-28T02:05ZZ
- IR (TB): Josh Hayes CB, Christian Rozeboom LB

Profile effect rule: a missing starter (CB1/S/edge/OL) is noted as a *direction* only (e.g. outside coverage may soften); Sharp/pbp allowance numbers are NOT adjusted and targets/carries are NOT redistributed without evidence (replacement's own snaps/targets). Questionable = scripted on low alts/fade, never cut; 90-min inactive approval goes to the user.

## Roster cross-check of named candidates
- Brian Robinson (ATL): FLAG-Q — Questionable — script low alts/fade, not cut. Robinson (hamstring) officially didn't practice Wednesday, Tori McElhaney of the Falcons' official site reports.
- Emeka Egbuka (TB): FLAG-Q — Questionable — script low alts/fade, not cut. Egbuka (concussion/foot) practiced in a limited capacity Wednesday, Brianna Dix of the Buccaneers' official site reports.
- Kenny Gainwell (TB): FLAG-Q — Questionable — script low alts/fade, not cut. Gainwell (hip) was held out Wednesday due to the injury he sustained against the Panthers, Scott Smith of the Buccaneers' official site repo

## Provenance (sha256/16)
- slate.json: e7ace10e143abac4
- injuries.json: 184dbf2c1ed2f78d
- defense/ATL_at_TB.md: 8dea45b98f8618b8
- rosters/ATL.json: 18f076fd654bf99e
- rosters/TB.json: 32337292c85e4d29
- ../fixes/fixes.sqlite: 50a82f6968d6fd46

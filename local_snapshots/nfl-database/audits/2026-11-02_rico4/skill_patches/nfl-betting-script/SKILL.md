---
name: NFL betting script
description: >-
  Use this before any NFL projection, player prop, parlay or same-game-parlay
  leg, or betting slip: a mandatory research-first checklist every leg must
  pass, plus slip-building, simulation, staking, pre-mortem and tracking rules.
---
# NFL Betting Script (pre-projection checklist and slip routine)

Mandatory, in order, before any projection, prop, parlay leg or recommendation. Walk every leg through every step out loud and cite the source and freshness of each number. A HARD step that fails cuts the leg. If key data (official injury report, depth chart, Next Gen/charting tendencies) is missing or stale, make no recommendation. This is analysis for entertainment; never guarantee outcomes.

Sources (cross-check at least 2): NFL.com injury reports and depth charts, team sites, Next Gen Stats, nflverse/FTN charting, Pro-Football-Reference, ESPN, PFF, Sharp Football (coverage/blitz), Fantasy Points weekly WR-vs-CB matchups (label as estimates), official weather forecasts, beat reporters, Wikipedia coaching trees.

## 1. Game context, stadium, weather and injury report
- Game, date, week, home/away, venue, stadium type (dome, retractable roof and whether it's open or closed, outdoor), data timestamp.
- Starting QB (confirmed by coach or beat reporters), RB1/RB2, WR1/WR2/slot, TE, key OL.
- Weather forecast (outdoor): temp, wind speed, direction and gusts, rain/snow chance and amount, humidity, field condition. Wind 15+ mph or rain suppresses deep passing, QB yards and totals and favors runs and short throws; extreme cold or a wet field matters for skill players. Recheck close to kickoff. Domes and closed roofs are controlled. See the HARD rain rule in section 14.
- Pull the official injury report for both teams now; filter it in section 5.

## 2. Coaching staff and scheme (both teams)
- Offense: HC and OC/play-caller; pass- or run-first (early-down pass rate, neutral pass rate, under-center vs shotgun); coaching tree and what won at prior stops (win totals, offensive efficiency); pace; how they split RB carries; how they adjust to rain or a backup QB.
- Defense: HC and DC; man vs zone %, Cover 1/3/4/6 and two-high rate; 3-4 or 4-3 base; nickel rate; blitz rate and results (pressure, sack, turnover, EPA); prior scheme success.
- Write the lean in one line (e.g. "outside-zone, 55%+ early-down run rate").

## 3. Offensive and defensive personnel
- Offense: primary and secondary personnel groupings (11/12/21/22), how often, and when (early downs, red zone, 3rd down). Does it fit the play-caller's lean?
- Defense: base front (3-4/4-3), nickel and dime rates, and the coverage (man vs zone) they play against each of those offensive groupings.
- Is there an edge or disadvantage for the offense's primary or secondary personnel, and do any key defenders or scheme features create a mismatch?

## 4. Depth chart (current and official)
- Offense: QB, RB1/RB2, X/Z/slot, TE, OL. Defense: DL/EDGE, LBs, boundary CBs, slot CB, FS/SS, nickel usage.
- Note backups who enter for OUT players. Flag source conflicts; trust official team/NFL reports. Verify every player's current team.

## 5. Injury filter (HARD)
- Only official OUT (or IR/PUP) players create edges or adjustments.
- Questionable players: drop the leg one rung (Rico's ruling, Nov 1 2026). Questionable does not block a PRESS leg; it only takes the one-rung drop. Doubtful or OUT: don't bet legs on them and don't build on their absence before inactives.
- No leg that only gains if a questionable teammate sits.
- Edges from players already ruled OUT are allowed, mainly on defense (backup CB/S on his side or in the middle; DL/LB out on the side an RB runs to; weak edge rusher's side; pass rusher out helps protection). Note which OUT players don't affect the matchup.
- First game back from injury: no full-volume overs; check snap share.

## 6. Player baselines (last 2-3 seasons)
- QB: yards, attempts, comp %, TD/INT, rating, rushing if dual-threat; vs blitz (rate faced, comp %, sack rate, YPA/EPA); aggressiveness, air yards, CPOE.
- RB: carries, YPC, receiving; archetype (workhorse/power, explosive/versatile, committee); snap share; fit vs the front (gap vs zone, power vs speed).
- WR/TE: targets, receptions, yards, catch rate, target share, aDOT/air-yard share, YAC; archetype (alpha, volume/possession, deep/vertical, slot/specialist, contested catcher, separator, slant). Don't apply a defense's suppression of one archetype to a different one, especially a star.
- Trend: improving, steady or declining.

## 7. Recent form and current categories (last 4 games) (HARD)
Assign categories fresh every game from the last 4 games; when they differ from long-term labels, the last-4 category wins.
- Team: last 4 points scored/allowed, offensive/defensive efficiency, W/L, script trends.
- QB category with the numbers behind it (attempts, yards, rush yards, comp %, time to throw, results when pressured/blitzed): pocket passer, mobile/running QB, or struggles under pressure.
- Receiver category: high-reception route runner (steady 6-10+ catches on short/intermediate routes) or efficiency/big-play catcher (1-3 catches but 80-90+ yard games). Note targets, receptions, yards per game, catch rate, aDOT. Volume types get catches lines; big-play types get yards lines.
- RB: recent rush yards, YPC, receiving usage; confirm or update archetype from current usage.
- Hot/cold streaks, role changes, scheme adjustments.
- Hard gates: clears the exact line in 3 of the last 4 (or 3 of 3), one spike game doesn't count; only games with today's starting QB count (include backup-QB starts from prior seasons); snap and target share steady or rising; catches lines need targets per game x catch rate clearing the line with room to spare and catch rate 65%+; yards lines need targets x yards per target clearing it.

## 8. Matchup (HARD area check)
- Defense allowances: points and yards allowed, yards allowed to the position (WR/TE/RB), ranks.
- Area match (Next Gen Stats/charting): where his routes or runs go (left/middle/right, short/deep) vs where the defense leaks. An over into a defense's strength or an under into its weakness is cut.
- Coverage: man/zone, two-high rate, projected CB/S on him and how he fares vs that look; how often corners shut him down.
- Run direction vs weak side (injured or weak EDGE/DT); RB run-direction splits.
- QB vs blitz: bad blitz QB means favor quick throws and check-downs, fade deep legs. See the HARD QB rules in section 14.
- Red-zone target and carry share (for reading game script, not for adding TD legs).

## 8A. Defender coverage check (HARD, added Oct 31, 2026, user rule; no leg skips it)
Every WR/TE leg (and every RB receiving leg) must show real defender-level numbers. Stand-ins (the defender named on completions, outside-vs-slot splits) do NOT count. A leg missing this step is cut.
- Source 1, free and required: Pro Football Reference advanced defense, https://www.pro-football-reference.com/years/<season>/defense_advanced.htm. For each likely CB/S/LB in coverage: targets, completions, completion %, yards, yards per target, TDs and passer rating allowed. Refresh it every slate.
- Source 2: nflverse FTN charting (ftn_charting_<season>.parquet) for man vs zone and middle of the field open (two-high) vs closed (single-high), plus Sharp Football scheme pages.
- Optional, when the user is signed in on the box browser (read only): PropsMadness Pro (Man-vs-Zone filter, Matchup Analyzer), PFF, FTN.
- Map the player to his likely defender from depth charts and alignment (boundary vs slot, which side). Show: defender name, what he allows per game and per target, and whether he limits catches (low completion % allowed) or yards (low yards per target).
- Match his routes (public Next Gen Stats, FTN charting) to the area that defender or coverage covers.
- A catches over vs a defender allowing a low completion %, or a yards over vs a defender allowing low yards per target, is cut or moved down a rung unless the volume gate clears it with room.

## 9. Game flow
- Spread and total; can the underdog lead; blowout risk that pulls starters.
- Rushing legs: carries per game, carries in wins vs losses, carry share and who else takes carries. Trailing dries up RB carries; QB scrambles don't.
- (HARD) No RB rushing over on a team that could trail (definition in section 14) unless he averages 4+ targets per game; use a rush+rec line instead. No RB rushing under on a favorite of 3+ points that leads in 50%+ of sims: leading feeds carries.
- (HARD) Committee backs: rushing overs need a 60%+ carry share in 3 of the last 4. A blowout win doesn't guarantee carries when a second back closes games.
- Pace and neutral pass rate of the play-caller.

## 10. Price, models and line timing
- Two models must agree (projection sheet and shrunk alt-line model); if they disagree, the leg needs 4 of 4.
- (HARD) Our sim median must clear the line on every over (and sit below it on every under). Any price relaxation applies only on top of this, never instead of it.
- Check the calibration log by probability bucket. If a bucket has run 10+ points under its sims over the last 3+ weeks, shrink that bucket's probabilities before pricing.
- Our probability must beat the book's implied price (vig-in), checked against the sims. Consider alt lines alongside mains.
- Grab lines early when our number beats the price. Recheck any leg whose line moved more than half a point or 20 cents of price since we priced it.

## 11. Slip rules
- Tiers: Basic = 5-6 safest legs. Intermediate = 5-6 legs mixing stat types. Pro = 5-6 plus-money legs where the projection clears the line. Extreme/Pure Edge = about 4 alt lines around +150 to +220. Target hit chances run from about 1 in 10 to 1 in 85.
- Max 1-2 unders per slip. No player on more than one slip, including slips already placed.
- No two receivers splitting the same QB's targets on one slip.
- Correlation with placed slips: no leg that works against a placed leg (e.g. a QB's passing vs his team's RB rushing), and don't stack one player or game across many slips.
- Two backups per leg in the same price range that pass every step.
- Run 100,000-200,000 Monte Carlo draws per slip (share game script within a game) and report hit chance as 1 in X and whether it pays more than its odds.
- Recheck prices and inactives before placing (Sundays about 11:30 AM, 2:35 PM, 6:50 PM ET).

## 12. Bankroll
- Stake by tier from the bankroll, less on long shots (e.g. 0.5 unit Intermediate, 0.3 Pro, 0.2 Pure Edge). Never chase a loss with a bigger slip.
- Don't cash out to rebuild unless a player is ruled out or loses his role; every cash-out and re-bet pays the book's cut again.

## 13. Pre-mortem, tracking, learning
- Before locking: assume each leg lost; check news, injury returns, QB changes, game script, inflated hit rates, weather and correlation. Mark each leg keep, watch or swap.
- Track every leg live.
- Log every leg's hit or miss with its sim probability so we can check each week whether our probabilities are honest.
- Grade each miss by the step that failed and add the lesson to this script.

## 14. Hard rules learned from graded misses (HARD)
"Could trail" means: underdog, favorite by 3 or less, or trailing in 35%+ of sims in any quarter.
- No receiving-yards under on a check-down TE or RB (aDOT under 6 or 18%+ target share) whose team could trail. Trailing feeds him volume.
- No QB passing-yards under on a team that could trail.
- Rain counts for game-window hours with NWS hourly chance 50%+ (the gate's weather flag; gusts 20+ or sustained 15+ also flag), pulled within 2 hours of kickoff. If the forecast says it clears, treat rain as a first-half factor only. Rain is never the only reason for an under.
- QB yardage legs: projected attempts x expected completion % (last 4, adjusted for the defense's allowance, blitz rate and weather) x yards per completion must clear the line with room. QBs completing under about 60% recently are cut from overs. Check the opponent's blitz/pressure rate against the QB's sack rate and comp % vs blitz for every QB leg and for every receiver leg that depends on that QB.
- Yards-over cushion: at -150 or longer, last-4 median must be 20%+ above the line; at -113 to -149, 25%+ above and cleared the line by 10%+ in 3 of 4. Otherwise drop a rung.
- Deep-role check: if 40%+ of a receiver's recent yards came on deep targets and his QB rarely throws deep, or the defense plays two-high 55%+, use a catches line or a lower rung.
- RB receiving-yards overs need 6+ yards per target in 3 of 4 and an opponent allowing above-average RB receiving yards per target.
- Backs who get stuffed on the ground but catch passes get rush+rec lines, not straight rushing, unless the run matchup is clearly soft.
- Players averaging 3 or fewer targets: at most one per slip, none on Basic. A leg that needs one catch to hit is a coin flip, not a safe leg.
- WR/TE yards overs need 4+ targets in each of the last 3 games with the current QB, unless the line is 15 yards or less.
- New-role exception: when a starter at the same position is OUT, judge the replacement on games where he held that role (55%+ snaps). Questionable-dependency legs stay banned.
- About 2 hours before kickoff, recheck every leg against inactives and the hourly forecast and drop any leg whose reason no longer holds.
- Catches overs (any line 3.5+) need 5+ targets in 3 of the last 4 with the current QB, and no teammate in the same role (TE with TE, slot with slot) taking 28%+ of team targets over the last 4.
- QB room rule: a QB yardage over needs the projection from the completion-% gate to clear the line by 12%+. Below that, drop a rung or cut.
- Receiver legs inherit their QB's grade card (section 15). If the QB fails the card for this matchup, his receivers' yards overs are cut or moved down a rung, and catches overs need the target floor above.
- Snap-share gate waiver: on yards lines of 20 or less, a player who cleared the line in 4 of the last 4 with the current QB passes even with uneven snaps, if every other gate passes.
- New-role exception also covers vacated targets: when a WR/TE starter is OUT, rank every candidate for that role by snaps and routes in the role's games. Don't assume the depth-chart name gets it; bet the role only when one player clearly held it.
- Screen QB rushing props (yards and attempts) every week with the same gates. Mobile QBs facing weak edge contain are a recurring blind spot.

## 15. QB grade card (HARD for QB legs and dependent receiver legs)
Build a card for every slate QB from the current season's play-by-play (nflverse pbp; FTN charting n_pass_rushers 5+ as the blitz proxy; sack + QB hit as the pressure proxy). Swap in NGS/PFF pressure and blitz splits when available and say which source each number came from. Grade each component A-F by percentile among QBs with 40+ dropbacks (A 80th+, B 60th, C 40th, D 20th, F below). Save the table with the slate data.
- **Vs blitz:** comp %, YPA and sack rate on blitzed dropbacks.
- **No blitz:** comp % and YPA on standard rushes.
- **Protection:** overall sack rate and sack + hit rate.
- **Money downs:** 3rd/4th-down conversion rate on dropbacks.
- **Clutch:** Q4 and trailing comp %, YPA and EPA per dropback (one-score Q4 success rate as a tiebreak).
Matchup projection: blend the QB's vs-blitz and no-blitz YPA by the opponent's blitz rate, times projected attempts, adjusted for the opponent's comp % allowed and weather. Expected sacks = dropbacks × (blitz rate × blitzed sack rate + (1 − blitz rate) × unblitzed sack rate).
Gates:
- Vs-blitz D/F facing a defense that blitzes 35%+: no yardage or rushing over for that QB, and no receiver yards over that depends on him.
- No-blitz D/F facing a defense that blitzes under 25%: the same cut.
- Protection D/F with 3+ expected sacks: no passing-yards over, even if the yardage projection clears.
- Clutch D/F: no over that needs a trailing or comeback script. Volume can still rise when trailing, so a low clutch grade is never a reason for a passing under (the trailing-team rule in section 14 governs unders).
- Money-down F: discount long-drive-dependent legs (QB yards, TE/slot catches) by one rung.
- The card is a cut tool. A good grade doesn't make a leg; every other gate still applies.

## 16. Lessons from Oct 11, 2026 (evidence for the rules above)
- Check-down TE receiving-yards under on a team that trailed all game: 9 targets, 83 yards against a 43.5 line, 64 of them after halftime (section 14).
- QB passing-yards under on a 3-point underdog: 44 attempts, 267 yards against 211.5. 28 of the attempts came in the second half (section 14).
- Rain heavier before halftime than after: one trailing offense went from 73 passing yards in the first half to 210 in the second (section 14 rain rule).
- RB rushing under on a 7-point favorite that led from Q2: 15 carries, 62 yards against 36.5. Two RB rushing overs on teams that trailed: 9 carries (73 rush+rec vs 80/100) and 13–15 carries (45 vs 60) (section 9).
- Committee back on a team that won by 28: 3–4 carries, 22 yards against 46.5 while the other back ran for 64 (section 9).
- QB overs that failed the card or completion math: a 56% passer at 137 vs 190.5 (pre-game completion projection 176–188); a protection-D QB facing a 37% blitz in rain took 7 sacks, 155 vs 201, with our own median (194) under the line; a no-blitz-D QB took 4 sacks for 40 and finished 5 short (170 vs 175); a vs-blitz-D QB facing a 72% blitz threw for 96, and his TE's 40+ yards leg died at 16 (sections 10, 14, 15).
- Legs whose sim median sat below the line went 1-3 (section 10).
- The 0.55–0.70 sim bucket went 5 of 14 (36%) against an average sim of 0.61 (section 10 calibration check).
- Low-target catches legs: a TE line of 3.5 catches got 1 target while the teammate TE took 28%; a 3.5-catch WR got 3 targets (section 14 catches rule).
- Gate misses on producers we skipped: a WR who cleared a 16.5-yard line 4 of 4 was cut only on snaps and went for 65; a vacated-role WR the depth chart didn't favor got 9 targets for 80 while our pick got 1 target; two mobile QBs' rushing props were never screened (87 vs 30.5, 51 vs 18.5) (section 14).

## 17. Outside-model cross-check (before locking a full slate)
- After final projections, compare every leg and each game's side/total against an NFL Elo model and FTN's NFL betting model (FTN may need the user's login or pasted numbers; say so if unavailable).
- Agreement (same side, similar number) adds confidence.
- Where we disagree, the leg needs a documented reason the outside models may not price (an OUT player, area/coverage mismatch, QB grade card, weather hours). Without one, cut it or stake it smaller.
- Log each disagreement and grade it after the games to learn whose angle was sharper.

## 18. De-vig sharp lines (HARD)
- Always remove the book's margin before comparing. Pull both sides of the market (over and under) from sharp books (e.g. Pinnacle, Circa) when available, otherwise the consensus of FanDuel and DraftKings.
- Convert each side to implied probability, then normalize so both sides sum to 100% (multiplicative method; use power or Shin for big favorites or longshots). That de-vigged number is the market's true probability.
- Our probability must beat the de-vigged sharp probability (not the vig-in price) by at least 3 points for a leg to count as an edge. When only one side is posted, use the alt-ladder or the other book's line, and say which one was used.
- Report both the de-vigged probability and our probability for every leg.

## 19. Practice reports, wind and situational modifiers
- Practice reports: track DNP / limited / full from Wednesday through Friday for both teams. Flag trends early (e.g. DNP-DNP-limited). Status rules in section 5 still decide what counts; practice trends only tell us where to look and which lines to grab or avoid early.
- Hidden-starter losses: when a starting OT/OG/C or the slot CB is OUT, adjust the team's expected efficiency (EPA) even if season-long data doesn't show it. Backup OT: raise sack/pressure rate, cut deep-passing and QB yardage overs, favor quick-game catches. Backup slot CB: boost the opposing slot WR/TE (targets and catch rate), and check which receiver runs most routes from the slot.
- Wind: sustained wind 15+ mph (not just gusts) for the game hours cuts deep-passing legs, long-aDOT receivers, QB yardage overs, kickers and game-total Overs; favor run volume and short-target catches. Rain stays secondary (section 14).
- Situational modifiers (minor, never the only reason for a leg): rest edge (bye or extra days vs short week; a Monday-night team facing a team off Thursday), travel distance and time zones (west-to-east early kickoffs), and altitude (Denver). Note each as a small nudge in the team rating and the game script.

## 20. Matchup database and Next Gen Stats check (added Oct 29, 2026)
- The NFL Database teammate owns the matchup database. Its master prompt is at /workspace/nfl-database/MASTER_PROMPT.md and is the single source of truth for phases 1-8: ingest, defensive and offensive profiles, cross-reference alerts, output files, live checks, Next Gen Stats, and film notes. Read its profile files and matchup card before grading; don't rebuild them here.
- Before any prop evaluation, pull Next Gen Stats for both teams from public NGS pages only, never tracking feeds. PFF is an approved paid source for matchups and grades, but it must be cross-checked against a second dated source (a disagreement is a gate caution). Other paid-only stats not subscribed are marked missing and lower confidence; never estimate them.
- Use the one-page matchup card (master prompt 7G) as an input to sections 8 and 15: defensive strength map, route and gap profile, where the offense attacks the defense's weakness, QB blitz profile vs the defense's blitz rate, OL health in the last 48 hours, and green, yellow or red prop flags.
- (HARD) Panthers rule for every QB prop and every receiver leg that depends on that QB. Check four things: the opposing blitz rate is top 10, the opposing pass-rush win rate is top 10, there's an OL injury (especially LT or RT), and the QB's sack rate vs that blitz package. If any of the first three is true and the fourth is poor, flag CAUTION and discuss with the user before entry. Example: Bryce Young vs TB (top-5 edge pressure, Moton out, league-worst blitzed completion rate).
- Database alerts feed the pre-mortem (section 13): missed-opportunity flags, vulnerability flags (OL injury or pass-rush mismatch flipping a QB prop), and script-risk flags (backup QB start hurting a run prop).

## Star unders (approved by user Oct 14, 2026)
- Unders on star players (e.g. Allen rushing, Puka, Nix) are allowed ONLY with a specific, data-backed matchup reason that the stat will not hit (e.g. QB passing yards vs the #1 pass rush). Show the reason on the pick. Never take a star under on price alone.

## Nov 1 2026 lessons (lessons audit; the gate enforces the items marked GATE)
1. Weather alert (GATE): any open-air game with rain ≥50%, gusts ≥20 mph or sustained wind ≥15 mph raises a loud WEATHER ALERT. Look at rushing overs first, then re-check every placed leg in that game.
2. Game script drives RB volume: rain, a lopsided spread or a QB collapse means modeling the run share, not the normal pass split.
3. RB fixes A, D, E, F are on (GATE/sim). Fixes B and C, the RB 2-of-3 Phase 14 rule and the lead-back gate check were declined. Don't re-enable them.
4. RB scan (slate_scan): any active RB with ≥20% of carries in either of the last 2 games gets a rush-yds candidate. Role flips swap RB1/RB2. The depth-chart RB1 is passed by hand (depth_rb1). Rule 5 is unchanged.
5. Receiving legs (GATE for runs dated ≥ 2026-11-05) factor blitz rate, pressure rate, checkdown share, QB time to throw and targets under pressure.
6. Run the slate scan and the gate before any slip. A leg not passed by the gate never goes on a slip, and §11 is one slip per player.
7. Price every leg with sim_v6 (GATE ≥ 2026-11-05). Bias is calibrated; the old flat −8% / −3% / −5% cuts are retired.
8. Press tier (press_tier.py, live ≥ 2026-11-05) runs only after a normal gate PASS. It never rescues a cut.
9. PFF is an approved paid source for matchups and grades. Cross-check it against a second dated source. A disagreement, or a PFF under while PFF's own matchup says over, is a gate CAUTION, never a pass reason. PFF is never used for weather, game script or projections (GATE FAIL).
10. The postgame review lists edges missed by category (not in pool / cut by rule / wrong side / variance), ticket grades, defense dissection (rush 15+, rec 20+) and updates postmortems/WATCHLIST_2026.md.
11. Backtests are analysis only. The RB receiving game-script backtest (Wk3-8) found no profitable trigger, so no rule was added.
12. Phase 15: when a starter is out, check the backfield split and every slip's exposure to that game.

## Source-list rules (Rico, Nov 1 2026 22:47 ET; tools/run_gate.py + tools/srclist_rules.py enforce every item)
1. SRC-1 Weather: NWS (api.weather.gov) or Open-Meteo only, via tools/weather_forecast.py. Never PFF, never AccuWeather or any other site. The gate fails any other weather source, weather-block source or forecast provider.
2. SRC-2 PFF picks: re-price each pick at our book's current line and price (book, book_line, book_price, pulled_et within the odds age limit), and compute p with all three of our models (monte_carlo, bias, game_randomness). Record edge_basis "our_model". PFF's edge % is ignored: the gate fails any leg or pick whose edge comes from PFF, and any pff_pick leg not at our book line.
3. SRC-3 Sharp coverage: counts only when a second source agrees (StatRankings, FTN/nflverse charting, or our play-by-play). Record it as second_source {name, url_or_file, pulled_et, agrees} on the Sharp source (runs/<shared_src>/sharp_second_source.json). Sharp alone or disagreeing = SHARP CAUTION, and any leg whose coverage cites Sharp cannot be PRESS (tier BLOCKED).
4. SRC-4 Odds: pull with tools/odds_pregame.py windows (pull_odds.py --start/--end UTC); in-play and unknown-kickoff rows are dropped to odds_<tag>_inplay_dropped.csv and never priced. A missing line is NOLINE, never 0 (pull_props.py).
5. SRC-5 Feed weeks (runs dated 2026-11-05 on): every source, PFF input and PFF pick carries season, data_week and pulled_et (feed_stamps.json, tools/feed_week_check.py). The gate fails a wrong season, a label feed (injuries/news, weather, odds/props, PFF, depth/WR-CB) not on the run week, or a results feed (pbp, NGS, film, coverage, snaps) with data before last week. The StatRankings OL page stays in the source list under this rule. Run `python3 tools/feed_week_check.py <shared_src> --season 2026 --week N` before assembling.

## Rico 2026-11-01 additions (weather days ahead, coverage profile, backtest notes)
- **Check the weather days ahead, not 90 minutes before kickoff (live for runs dated ≥ 2026-11-05).** Slips get built days ahead, so at slip build run `python3 /workspace/nfl-database/tools/weather_forecast.py --week <N>`. It pulls the NWS and Open-Meteo multi-day forecasts for every open-air or unknown-roof game, takes the worse of the two, and writes `week<N>/weather_forecast/forecast_YYYY-MM-DD_HHMM.json`.
  - The flag fires on rain ≥50%, gusts ≥20 mph, or sustained wind ≥15 mph.
  - The run manifest must carry `weather_forecast`; `runs/2026-11-05_shared_src/assemble.py` adds it and fails preflight without it.
  - The run gate fails a run if the forecast is more than 24h old, or if any game in the run has no forecast or no numbers.
  - On a flag, passing and receiving OVERs in that game must be CUT, and the gate prints `WEATHER FORECAST ALERT`.
  - Re-run it with the daily Mon–Sat 10 AM refresh. The existing pre-kickoff Phase 11 recheck stays.
- **The defensive coverage profile is required on every receiving AND passing leg (runs ≥ 2026-11-05).** QB passing legs need the opponent's `coverage.man_zone` and `coverage.mof`, each sourced and no more than 48h old, the same as WR/TE legs. Otherwise the gate fails the leg.
- **Backtest notes (2026 Wk3–8, walk-forward; NOT rules; Rico decides):** full results are in `/workspace/nfl-database/backtests/{rb_ypc_floor,qb_return_caution,qb_pressure_blitz_weather,qb_vs_passrush_ol,missed_100_receivers,softened_edges}/RESULTS.md`.
  - The RB YPC floor and the QB-under-pressure cut did not hold up, so don't apply them.
  - QB back from injury, or a model built on the backup QB: flag the leg and recheck §7 with the current QB. Don't drop a rung automatically.
  - A pass-rush-vs-OL mismatch is not a reason to cut a WR/TE over. Those overs hit more often.
  - When an under is cut as soft-D or for a missing defender, look at the mirror over.
  - Aligned overs that were cut by P14 or MODEL-SUSPECT, or played a rung down, went 7/10 at full strength in Wk8.

## Rico rules 2026-11-02 (approved 05:01 ET; runs dated ≥ 2026-11-05; enforced by tools/rico4_rules.py via run_gate)
1. **PRESS manual review.** On a leg press_tier marks PRESS, a P14-only edge cut (edge < +3, shrunk edge ≤ 0, model p < .45, a median does not clear, MODEL-SUSPECT) becomes status MANUAL_REVIEW, not CUT. The leg carries the reason, all 3 model p (MC/bias/GR) and the book price + no-vig. The gate prints a "PRESS MANUAL REVIEW" section; these legs are NEVER live/auto-published, and Ghost6/Rico decide. Non-press legs keep the cut. Weather, inactives/injury, §11, the #3/#4 WR ban and the placed-ticket bar still cut (no MANUAL_REVIEW).
2. **Mirror over.** When an under is cut for soft D (P3), a missing/unverified defender (P4/ISS-05), no-unders-on-stars (P14 primary star), the trailing-team or clock-killing block (P13), build the mirror over at the LOWEST alt rung that clears (avg model p − no-vig ≥ .03, shrunk > 0, min p ≥ .45, every median over the line). It then goes through every normal phase. It records mirror_of = the cut under; with no clearing rung, the under records mirror.no_rung_reason. Gate fails if neither is present.
3. **Target-share pool.** WR/TE players with ≥22% target share (season, OR last 3 games with the current QB; nflverse pbp) join the player pool and slate_scan (trigger tgt_share22). The manifest needs a target_share_pool block (source nflverse pbp); every listed player needs a leg or a skip_reason. #3/#4 WRs stay banned.
4. **QB return.** Flag QB-RETURN when the team QB is back from missing 2+ games or the player's model was built on backup-QB games. Recheck §7 and recent form on current-QB games only (qb_return_recheck {current_qb, games, sec7, form_values}). There is NO automatic rung drop. The gate fails on a live QB-RETURN leg with no recheck, or on a rung_drop that cites the QB return.
Still OFF: YPC floor, pressure cuts.

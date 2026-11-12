# TNF JAX@BAL — leg build + pre-gate screen (NOT VETTED, NOT a card)
Kickoff Thu 2026-11-05 8:15 PM ET, M&T Bank Stadium (open air). Built Tue 2026-11-03 ~10:00 AM ET by Blitz. Script: build.py, output legs.json/build.log.
Sims: tools/sim_v6.py, Monte Carlo / Bias / Game Randomness, 100,000 each, seed 20261101 (oppadj still 1.0; see audit item 4, Rico decides).

## Status: GATE NOT RUN (tools/run_gate.py) — manifest incomplete. Nothing here may go on a slip.
Required inputs MISSING for this run (each would cut legs at the real gate):
- Week-9 ESPN WR/CB chart and per-defender numbers for JAX/BAL (Phase 4) -> defender_giving fails closed.
- Coverage man/zone + MOF for both defenses (Sharp cache has no JAX/BAL rows; nflverse FTN has no man/zone column).
- NGS, film, practice reports Wed–Fri, inactives (Phase 9/10/15).
- feed_stamps.json / feed_week_check not run.

## Inputs pulled (ET)
- Weather: tools/weather_forecast.py --week 9 at 09:55 -> week9/weather_forecast/forecast_2026-11-03_0955.json. JAX@BAL rain 41%, gust 10.1, wind 3.9: NO flag (Nov 2 10:02 forecast had 56% rain flag; cleared).
- Odds: tools/pull_odds.py --props-only, 1 event-odds call at 09:56 (FanDuel/DK/Pinnacle/PrizePicks/Underdog). Credits 3,623 -> 3,612 (11 used). odds/quota_log.csv.
- Spread/total: ESPN scoreboard (DraftKings) JAX -9.5, O/U 41.5.
- pbp: fresh nflverse play_by_play_2026 (through Nov 2 MNF), players; FTN charting thru wk8.
- Injuries: ESPN 2026-11-03: Lamar Jackson OUT; Huntley 'probably' won't play; Fagnano Q (ankle) = BAL QB used. Meyers Q, Justice Hill Q, Tuten DNP, Rodriguez LP.
- NO_PASS_YDS: no passing-yards legs built.

## Screen passes (edge>=+3, every model p>=.45, all medians clear, §7 3/4 with current QB, depth/#3-4 rules)
| Leg | FD | no-vig | MC/Bias/GR p | medians | last-4 (Lawrence) | notes |
|---|---|---|---|---|---|---|
| Brenton Strange rec yds over 35.5 | -114 | .500 | .571/.570/.541 | 41.0/41.9/38.9 | 95,68,44,55 | TE1; scheme_edge not all 4 |
| Strange rec yds over 29.5 [low] | -174 | .596 | .659/.658/.607 | same | | |
| Strange rec yds over 24.5 [low] | -250 | .670 | .724/.723/.675 | same | | -250 flag |
| Strange receptions over 3.5 | -122 | .514 | .562/.562/.526 | 4/4/4 | 7,7,5,2 | |
| Parker Washington receptions under 4.5 | -130 | .528 | .616/.618/.605 | 4/4/4 | 1,6,4,1 | JAX WR1 (21% tgt): star-under check pending |
| Trevor Lawrence rush yds under 12.5 | -114 | .500 | .637/.640/.638 | 8/8/8.2 | 0,25,11,10 | |
All BAL legs CUT: §7 MISSING (Fagnano has 1 game as the lead QB). Zay Flowers' over shows +32 edge but is a one-game-QB model artefact; it is cut.

## scheme_edge samples (four checks, each sourced)
- Zay Flowers rec yds over 45.5 (-114, no-vig .500): matchup OK (JAX allows 9.72 YPT to WR on 141 tgt vs league 8.07, nflverse pbp); scheme_fit OK (top zone short_middle 33% of 58 tgt; JAX 7.34 = league 7.34); script OK (BAL +9.5, total 41.5, ESPN/DK); form_trend FAIL (1 Fagnano game: 0 yds). Not SCHEME_EDGE.
- Brenton Strange rec yds over 35.5: matchup OK (BAL 7.75 YPT to TE on 48 vs 7.21); scheme_fit FAIL (short_left 34% of 35; BAL 6.00 vs 6.01); script FAIL (JAX -9.5 run-lean); form FAIL (last2 49.5 < last4 65.5).
- Parker Washington rec yds over 63.5: matchup OK (BAL 9.23 to WR vs 8.07); fit FAIL (short_left BAL 6.00 vs 6.01); script FAIL; form FAIL (last2 40.0 vs last4 52.8).
- Derrick Henry rec yds over 7.5: matchup OK (JAX 5.73 to RB vs 5.61); fit OK (short_right 6.15 vs 5.85); script OK; form FAIL (1 Fagnano game).
- Mark Andrews rec yds over 18.5: matchup FAIL (JAX 4.81 to TE vs 7.21); fit OK (7.34=7.34); script OK; form FAIL.
No leg reached SCHEME_EDGE.

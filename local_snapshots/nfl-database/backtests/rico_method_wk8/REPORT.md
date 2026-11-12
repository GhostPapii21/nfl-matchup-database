# Rico-method backtest, Week 8 2026 (TNF CAR@GB, Sunday 11 + SNF, MNF CHI@SEA). TEST ONLY: no bets.

## Integrity notes (read first)
- Reconstructed picks were locked in commit 3206cb8 (Nov 3 06:08 ET) and the slip method in 47223ba, both before grading.
- **Leak disclosure:** after the picks were locked but before grading, I opened week8/slips/slips_2026-11-01.md(.pre_snf.bak) to find the live legs. That file has graded Week 8 results appended to it. The picks were already committed, so they weren't affected, but I had seen some results before the replacement and slip steps ran. Both of those steps are mechanical (rules in slip_method.md) to limit how much that knowledge could matter. The analyst has also seen Week 8 postmortems in earlier sessions, so this is **not a blind test**.
- PFF: coverage and grades are locked on this account's tier, so it isn't used. Its season-to-date grades would also include Week 8 and later games.
- The reconstructed "read" is a **mechanical proxy** for the phase script, built from pbp and FTN data for weeks 1-7 plus pre-kick lines. It wasn't a hand-written per-game script. It uses: the player's last 4 games with the current QB; what the opponent allowed by position and market compared with the league (pbp weeks <8); opponent blitz rate (FTN weeks <8); and the nflverse closing spread and total, which are recorded but carry no weight. Not used: PFR Wayback, man/zone coverage and defender matchups (no point-in-time copy was pulled in this pass). The "reason" for each pick is the feature line in picks_locked.md.

## LIVE_READ picks (our actual pre-kick gated PASS legs, from manifest/build timestamps)
| Leg | Source (ET) | Actual | Result |
|---|---|---|---|
| Tre Tucker rec o3.5 -120 | runs/2026-11-01_LV@NYJ/run_manifest.json 11:41 | 0 | MISS |
| Puka Nacua rec o7.5 -138 | runs/2026-11-01_BONUS_SLIP build 11:53 | 11 | HIT |
| Stefon Diggs rec o3.5 (alt) -166 | BONUS_SLIP 11:53 | 3 | MISS |
| Jahmyr Gibbs rush o79.5 (alt) -162 | BONUS_SLIP 11:53 | 153 | HIT |
| Xavier Worthy rec o2.5 (alt) -225 | BONUS_SLIP_4PM build 11:58 | 3 | HIT |
| Matthew Stafford completions o22.5 -127 | DFS_SLIPS report 11:41 | 17 | MISS |
| Jaxon Smith-Njigba recyds o89.5 -166 | runs/2026-11-02_SEA_CHI_ghost6 05:08 Nov 2 (Ghost6 run) | 118 (ESPN box) | HIT |
Live total: 4/7 (57%), $10 flat **-$6.11**. Prices are the manifests' own FD prices, and alt prices are as recorded. The Rico-placed DFS/FD tickets are listed in the slips file, but they're Rico's picks, not our gated read, so they aren't graded here. Sources used live, from the manifests' sources blocks: nflverse pbp and FTN charting, the PFR advanced-defense cache (Rico exception), the PFF props cross-check, and FD lines.

## RECONSTRUCTED picks: 28 locked, then hard stops
Hard stops (hardstop_log.md). Weather (Open-Meteo, from the other worker's file) cut 5 receiving overs: Dotson (ATL@TB, 80% precip, 30.6 mph gust), Keenan Allen and Jakobi Meyers (IND@JAX, 20.6 mph gust), and Dulcich and Henry (NE@MIA, 65% precip). Their replacements were Ted Hurst rec u2.5, J. Taylor rush o48.5, Parker Washington rec u4.5, Kyle Williams recyds u23.5 and Ollie Gordon rush o58.5. Injuries: Kincaid and Ridley were Questionable, played, and were kept. Tez Johnson (ATL) has no Week 8 snaps, so his leg is VOID. Note that the weather cut removed Allen (actual 67, would have hit) and Meyers (24, would have missed).

Graded singles (27 non-void): **13/27 = 48.1%, -$29.52**. The 22 original picks went 45.5% (-$35.94). The 5 replacements went 3/5 (+$6.42).
By market: rec under 4/9 (-$18.36); rec over 0/1 (-$10); recyds over 4/8 (-$4.76); recyds under 3/5 (+$6.47); rushyds over 2/4 (-$2.89). Receptions unders killed the most slips.
Best: Tee Higgins recyds o72.5 (155), Jeanty recyds o27.5 (64), Mayer recyds o25.5 (53), Hubbard rush o67.5 (81). Worst: Kincaid u43.5 (86), Jeudy rec o2.5 (0 catches), Warren recyds o22.5 (0), J. Taylor rush o48.5 (23), and Kyle Williams u23.5 (43).

## Slips ($10 each, decimal product of pre-kick prices, approximation)
| Slip | Legs | Hits | Price | Result |
|---|---|---|---|---|
| S1 (8) | 8 | 3 | 145x | -$10 |
| S2 (8) | 8 | 3 | 184x | -$10 |
| S3 (7, 1 void) | 7 | 5 | 65x | -$10 |
| TNF 2-leg | 2 | 1 | 3.6x | -$10 |
| MNF 2-leg | 2 | 1 | 2.9x | -$10 |
| 7-leg variants S1/S2/S3 | 7 each | 3/3/5 | — | all -$10 |
All slips lost (0/8), **-$80**. No slip came within one leg of cashing; the best was S3 at 5/7. Full detail is in slips_graded.csv.

## Comparison with rules-only (FIRST version, backtests/current_rules_wk6_8 week 8; the rulebook_replay redo hadn't finished)
- Rules-only: 107 passed legs, 44.9% hit, -$167.19 at $10 flat, with no slip test in that version.
- Rico-method reconstructed: 27 legs, 48.1%, -$29.52. LIVE_READ: 7 legs, 57%, -$6.11. Combined: 34 legs, 50.0%, -$35.63.
- Overlap: 10 reconstructed legs are the same player, market and side as rules-only legs (A. Jones, McConkey, Q. Johnston, Sutton, J. Jefferson, Kincaid, K. Williams, Diggs recyds, Ted Hurst, P. Washington). Five more use the same player in a different market (Higgins, Ridley, Jeanty, Warren, J. Taylor). Of the live legs, Tucker and Puka were also in rules-only.
- Caught by Rico-method but not rules-only (same market): Higgins recyds o72.5 HIT and Mayer o25.5 HIT, plus Jeanty recyds o HIT (rules-only had his rush under). Missed by Rico-method but caught by rules-only: Gibbs rush o (live had it), Warren rush o 143, Bowers o70.5.
- Takeaway: the per-leg hit rate is slightly better and losses are much smaller because there are far fewer legs. Even so, about 48-50% at mostly -113 to -180 prices still loses, and 7-8 leg slips at that hit rate are expected to lose (0/8).

## Limits
Not blind (see the leak disclosure). The read is a mechanical proxy with no man/zone or defender data and no PFR Wayback. No spreads, totals or period lines were tested. Alt lines were only tested for the live legs, at their recorded prices. Odds API credits used: **0** (everything came from the existing pulls). MNF actuals come from the ESPN box. Prices are FD-first single-book prices, and parlay pricing is an approximation.

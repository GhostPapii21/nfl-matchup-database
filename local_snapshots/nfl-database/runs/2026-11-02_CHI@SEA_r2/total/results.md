# CHI@SEA MNF total / team totals / anytime TD — Blitz, 2026-11-02 ~7:55 AM ET
Kickoff 8:20 PM ET (Odds API commence 01:20Z), Lumen Field. fixed-model, copies only (total_sim.py reads tools/sim_v6_fix/sim_v6_src pbp; nothing in nfl-sim/, sb-fix/, sb-grades touched).
Sims: MC / Bias (last-4 current-QB, 2x regression) / GR (shared game shock + team shock + spread tilt), 100k each, seed 20261101.
NOTE: sim_v6 has no points or TD market, so this is a points/TD extension in the same 3-model design, not sim_v6 itself. Flag for Ghost6.
Odds: odds_t0743.csv (FD price of record, DK and Pinnacle for comparison), pulled 7:43 AM ET, in-play filter on (0 dropped). Fresh until 8:43 AM ET, then needs a re-pull.

## Market (FD)
Spread SEA -3 (-120) / CHI +3 (-102); ML SEA -178 / CHI +150. Total 46.5 -110/-110 (DK 46.5, Pinnacle 46.5 -106/-110).
Team totals: CHI 21.5 -113/-113 (nv .500), SEA 24.5 o-115/u-111 (nv .504/.496). Alt rungs are two-way, so each one is de-vigged on its own pair.

## Scoring profile (nflverse pbp Wk1-8, team_profile.py -> team_games.csv)
| | CHI (Caleb, 4 g) | SEA (Darnold, 5 g) |
|---|---|---|
| PF / PA per g | 30.8 / 23.3 | 24.8 / 21.6 |
| Game total avg | 54.0 (96, 12, 54, 54) | 46.4 |
| Plays/g | 67.0 | 66.0 (lg 60.8) |
| RZ trips/g, TD% | 5.0, 75% | 4.2, 62% |
| RZ trips allowed, TD% allowed (all 7 g) | 3.43, 71% | 2.14, 80% |
| Explosives for / allowed per g (rush 15+, rec 20+) | 5.5 / 4.0 | 4.4 / 2.4 |
| Turnovers / takeaways per g | 1.5 / 1.25 | 2.8 / 1.2 |
| O/U vs closing total (season) | 3-4 (Caleb games 3-1 O) | 3-4 (Darnold 3-2 O) |
Off TD/g: CHI-Caleb 3.25, SEA-Darnold 2.60 (lg 2.42). Defense allows: SEA 1.71 off TD/g + 1.29 FG; CHI 2.14 + 1.14.
**Outlier: CHI's Wk1 59-37 vs CAR (a 96-point game) is 1 of Caleb's 4 games.** Without it, Caleb games average 21.3 PF.
Roster (not modeled, direction only): SEA LT Charles Cross OUT (hurts SEA). CHI Montez Sweat back. "Jeffery Simmons on CHI" and "Quenton Nelson on SEA" are **UNVERIFIED** (Loeb video only, no official source), so they're not used. SEA RB: Charbonnet is back with 0 2026 games (MISSING sample).
Weather (SRC-1): Open-Meteo 7-11 PM ET has 2-4% precip chance, wind 3-5 mph, gusts 4-7, about 48F. NWS hourly: cloudy, 49-51F, 1 mph, 1-5% precip. No weather flag.

## Sims vs FD no-vig (full sample; sim_totals.md)
Shrunk = Ghost6 .5+.7(p-.5) minus nv; x0.7 = 0.7*(avg-nv). Medians are MC/Bias/GR.
| Market | FD | nv | MC | Bias | GR | avg | raw | G6 shrunk | x0.7 | medians |
|---|---|---|---|---|---|---|---|---|---|---|
| Total O44.5 | -142 | .554 | .615 | .539 | .602 | .585 | +3.1 | +0.5 | +2.2 | 50/47/50 |
| Total O45.5 | -128 | .529 | .601 | .525 | .588 | .571 | +4.2 | +2.1 | +3.0 | |
| Total O46.5 | -110 | .500 | .585 | .504 | .574 | .554 | +5.4 | +3.8 | +3.8 | |
| Total U46.5 | -110 | .500 | .415 | .496 | .426 | .446 | -5.4 | | | |
| CHI TT O20.5 | -132 | .537 | .625 | .574 | .582 | .594 | +5.6 | +2.8 | +3.9 | 24/23/24 |
| CHI TT O21.5 | -113 | .500 | .595 | .548 | .545 | .563 | +6.3 | +4.4 | +4.4 | |
| SEA TT U24.5 | -111 | .496 | .545 | .601 | .495 | .547 | +5.1 | +3.7 | +3.6 | 24/22/26 (GR median over the line) |
| SEA TT U23.5 | +122 | .426 | .496 | .557 | .447 | .500 | +7.4 | +7.4 | +5.2 | |
Model means: total 52.0 / 48.0 / 52.0. CHI 26.8 / 24.8 / 25.1. SEA 25.2 / 23.2 / 26.9.

**Robustness (sim_totals_exW1.md, same seed, CHI Wk1 removed):** total medians drop to 44/44/44. U46.5 goes to .536/.546/.543 (+4.2 raw, +2.9 shrunk). O46.5 becomes -4.2. CHI TT O21.5 drops to .481 (no edge). SEA TT U24.5 goes to .612/.601/.569 (+9.8 raw, +7.0 shrunk, all medians under).
=> The game-total lean flips with one blowout game. The over edge is not robust. SEA TT under holds in both versions.

## §7 (last 4 with current QB vs tonight's line)
- Game total 46.5. CHI-Caleb totals 96, 12, 54, 54: 3/4 over. SEA-Darnold Wk4-7 totals 53, 61, 31, 23: 2/4. **Over FAIL** (SEA side). Under fails on both sides.
- CHI TT 21.5: Caleb-game PF 59, 3, 31, 30. 3/4 over: PASS. But the edge disappears without Wk1.
- SEA TT 24.5: Darnold Wk4-7 PF 30, 29, 14, 20. 2/4 under: **FAIL**.

## Who scores (anytime TD; sim_atd.md; share = .4 TD share + .3 RZ-opp share + .3 inside-10 share, current-QB games, 25% shrink)
FD ATD has no "No" side. FD nv = FD implied / 1.025 (median FD vs Pinnacle two-way no-vig).
| Player | share | FD | nv | MC/Bias/GR | raw | G6 | x0.7 | note |
|---|---|---|---|---|---|---|---|---|
| D'Andre Swift (CHI) | .36 | -115 | .522 | .644/.602/.626 | **+10.2** | +6.5 | +7.2 | 6 of 13 Caleb-era TDs, 15 RZ carries, 10 inside-10. Scored in 3/4 Caleb games. SEA RBs scored 6 of 12 TDs allowed, 11/12 from RZ. **Clears.** |
| Caleb Williams rush (CHI) | .08 | +470 | .171 | .204/.183/.193 | +2.2 | +11.4 | +1.6 | under +3 raw; longshot shrink artifact. Pass |
| Colston Loveland (CHI) | .12 | +220 | .305 | .297/.269/.283 | -2.2 | +4.3 | -1.5 | TD in Wk6 and Wk7. No edge. Pass |
| Burden / Odunze / R. Johnson | | +230/+250/+310 | | <.21 | -13/-21/-5 | | | cut (Odunze has almost no RZ usage with Caleb) |
| JSN (SEA) | .19 | -110 | .511 | .402/.361/.424 | **-11.5** | -8.4 | -8.1 | Book prices him above his share. TDs in 2 of the last 4 Darnold games. Cut |
| AJ Barner (SEA) | .10 | +240 | .287 | .236/.209/.251 | -5.5 | | | cut. The CHI TE allowance is average (0.43 TD/g) |
| Cooper Kupp (SEA) | .08 | +300 | .244 | .199/.175/.211 | -4.9 | | | cut |
| SEA RB pool (any SEA RB TD) | .435 | Charbonnet +130, Wilson +330, Price +340, Holani +550 | ~.71 book proxy | .68/.63/.71 | about 0 to -4 | | | Individual RBs are **MISSING**: Charbonnet has no 2026 games, so the split is unknown. Wilson's model .50 assumes he keeps the RB1 role and is invalid. Re-check after the 6:45 PM ET inactives/role check |
G6 shrunk inflates every plus-money longshot (Caleb +11.4, Holani +17.9). Use raw or x0.7 for ATD.

## Verdict
- **Game total 46.5: PASS.** The full sample leans over (+5.4 raw), but that rests on one 96-point CHI game. Without it the lean flips to under (+4.2). §7 fails both ways. Cross out and Sweat back push toward the under. If forced, the lean is slightly under, but it isn't bettable.
- **Team totals:** SEA TT **U24.5 lean** (+5.1 raw full sample, +9.8 without the outlier, Cross out). Not cleared: GR median is 26 on the full sample and §7 is 2/4. CHI TT O21.5 does not clear (it's outlier-dependent).
- **Who scores:** **Swift anytime TD -115 is the one clear TD play** (avg .624 vs .522; every model ≥.60; 3/4 Caleb games). SEA's most likely scorer is "a SEA RB", but which one is unknown until Charbonnet's role shows up. JSN ATD at -110 is overpriced by our share model.
- **Conflicts with cleared legs:** none hard. Swift ATD fits Swift 4+ rec (same player, different stat: §11 / same-player stack flag, Rico decides). A SEA TT under leans mildly against JSN 100+ yds, but JSN's yards don't need SEA points. SEA scoring through the RBs in the red zone is consistent with JSN getting yards between the 20s. A total over isn't needed for either leg.
- Open items: re-pull odds before any use (1h freshness). 6:45 PM ET inactives (Charbonnet/Price role, Sweat/Simmons status). Ghost6 VETTED still needed; this report is not vetted.

# BONUS BET slip, 4 PM rebuild ($125 FanDuel bonus bet): projection report

**Slate:** the 4 PM window (LAC@LAR 4:05, KC@DEN 4:25, NE@MIA 4:25 ET), plus the SNF fallback (PHI@WSH 8:20 PM ET) that the owner allowed.
**Data pulled:** FanDuel odds at 11:57 ET (The Odds API, tag b1205). ESPN injuries at 11:52 ET. CBS inactives at 11:46 ET.
**Checklist:** /workspace/nfl-database/runs/2026-11-01_BONUS_SLIP_4PM/checklist.md. **Status:** UNVETTED. Ghost6 has to sign off.
**SHORT OF MINIMUM:** only 1 clean 4 PM leg was found. With the Diggs fallback (FLAGGED) the slip has 2 legs, which is below the 3-leg minimum. No padding was done.

## Phases run
2 legs × 15 phases = 30 rows. Carried-over gaps:
- Phase 4 uses the PFR cache, under the approved exception.
- Phase 5 pressure is a PROXY.
- Phase 9 NGS uses the nflverse backup.

## Sources used, by category
- **Core stats and play-by-play:** nflverse play-by-play and snap counts (through 10-29); ESPN depth charts; ESPN box scores.
- **Coverage and matchups:**
  - PFR advanced defense cache: per-defender numbers.
  - ESPN WR/CB cheatsheet: alignment.
  - Sharp Football coverage schemes: man/zone and MOF.
  - FTN charting: blitz rates.
- **Next Gen Stats:** the nflverse nextgen_stats backup.
- **Film:** official NFL YouTube highlights, matched to pbp rows.
- **Injuries and news:** ESPN injuries API (11:52 ET); CBS inactives (11:46 ET).
- **Weather:** api.weather.gov and Open-Meteo. DEN roof is open and wind is 6-7 mph.
- **Odds and props:** The Odds API b1205 (11:57 ET). FanDuel is the price of record, using main and alt ladders.

## Simulations
Monte Carlo, Bias and Game Randomness each ran 100,000 sims with seed 20261101 (sims4pm.py; output sims4pm_b1205.json). Every eligible 4 PM key-player ladder was simmed.

| Leg | MC p / med | Bias p / med | GR p / med |
|---|---|---|---|
| Xavier Worthy receptions O2.5 (alt) | .729 / 4 | .729 / 4 | .695 / 4 |
| Stefon Diggs receptions O3.5 (alt) | .665 / 4 | .665 / 4 | .677 / 5 |

## Projections and picks
- **Xavier Worthy receptions O2.5 @ -230 (FD alt; main 3.5 at +116/-154).**
  - Pricing: no-vig .652, avg p .718, edge +6.6, shrunk +0.1 (thin).
  - Opportunity: targets in the last 4 games with Mahomes were 2/7/7/6; receptions 2/4/7/3, so 3 of 4 clear 2.5.
  - Script: KC -1.5, a toss-up. Matched against DEN CB Riley Moss (50% comp).
- **Stefon Diggs receptions O3.5 @ -166 (FD alt), FLAGGED SNF fallback.**
  - Pricing: edge +8.7, shrunk +3.6.
  - Vetted in the 11:54 BONUS run. Not on any slip.

## Cuts (4 PM pool, after §11 exclusions)
- **Excluded by §11** (on placed slips): Stafford, Kyren, Corum (FD7 TD), Puka, Walker, Mahomes.
- **Blocked as underdogs by 10G:** all LAC (+6.5) and MIA (+7.5) players.
- **Failed the edge rule:**
  - Higbee: edge ≤ +1.9.
  - Rice and Kelce: medians below the line on every rung.
  - Sutton and Engram: medians far below the line (MODEL-SUSPECT).
  - Waddle: negative edge.
  - Stevenson rec, rec yds, rush and rush+rec: medians far below the line.
  - Douglas and Henry: edge ≤ +2.1.
- **Worthy rec yds O29.5 / O24.5:** the sims pass, but §7 fails. Yards in the last 4 were 20/70/73/11, only 2 of 4 over the line. This is the same reason the 08:46 cut was made. Worthy rec O3.5 also fails §7 (2 of 4).
- **J.K. Dobbins rush (every rung):**
  - Sim edge is +16, but that is implausible vs the market.
  - Phase 3 fails: KC holds RBs to ≤3.8 YPC.
  - Phase 6 fails: no clutch trailing script.
  - Phase 7 fails: carry share is under 60%, and he is a rush-only over with fewer than 4 targets on a possible trailer.
- **No FD line:** A.J. Brown, Henderson, Whittington, Parkinson.

## Risks and checks still to come
- **Coverage data:** the defender numbers come from the PFR cache pfr_def_adv_2026.html (10-29 06:02), under the approved exception (Rico, valid 2026-11-01, receiving legs).
- **Correlation:** Worthy shares KC exposure with Rico's Walker tickets. Different players, so §11 is OK.
- **LAC CBs:** Donte Jackson and McDuffie are Q. That is not load-bearing, because there is no LAR receiver leg.
- **Inactives:** check ~2:35 PM ET for Worthy and ~6:50 PM ET for Diggs. Reprice on a move over 0.5 or 20 cents.

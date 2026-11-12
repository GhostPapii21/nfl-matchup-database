# BONUS BET slip ($125 FanDuel bonus bet): projection report

**Slate:** what's left of Sunday Nov 1, 2026. Legs kick off at 1:00 PM ET (LV@NYJ, MIN@DET), 4:05 PM ET (LAC@LAR) and 8:20 PM ET (PHI@WSH).
**Data pulled:** FanDuel odds at 11:49 ET (The Odds API, tag b1149). ESPN injuries at 11:52 ET. CBS inactives at 11:46 ET (owner message pt113u).
**Checklist:** /workspace/nfl-database/runs/2026-11-01_BONUS_SLIP/checklist.md. **Status:** UNVETTED. Ghost6 has to sign off before this goes to the user.

Every source category was used, and all three sims ran.

## Phases run
4 legs × 15 phases = 60 rows. Results: 56 PASS, 0 FAIL, 0 MISSING. The other 4 are N/A: Phases 4 and 5 on the Gibbs leg, because it is pure rushing.
Gaps carried over:
- Phase 4 defender numbers come from the PFR cache (10-29), allowed under the approved exception.
- Phase 5 pressure is a PROXY.
- Phase 9 NGS uses the nflverse backup.

## Sources used, by category
- **Core stats and play-by-play:**
  - nflverse play-by-play and snap counts (through 10-29): volume, shares, recent form and carry share.
  - ESPN depth charts (07:14): roles. DET C McLaughlin is listed as C3.
  - ESPN box scores: second-source check on targets.
- **Coverage and matchups:**
  - PFR advanced defense cache: per-defender targets, comp% and YPT.
  - ESPN WR/CB cheatsheet: alignment.
  - Sharp Football coverage schemes: man/zone and MOF.
  - FTN charting via nflverse: blitz rates.
- **Next Gen Stats:** the nflverse nextgen_stats release (backup; nextgenstats.nfl.com is on hold per Ghost6). Gives separation, cushion and RYOE.
- **Film:** official NFL YouTube highlights, with every cited play matched to a pbp row (carried over from the game folders).
- **Injuries and news:** ESPN injuries API (11:52 ET re-pull), plus the CBS inactives the owner relayed (11:46 ET).
- **Weather:** api.weather.gov and Open-Meteo, from the game folders. DET is a dome; LAR and LV@NYJ have no wind flags.
- **Odds and props:** The Odds API b1149 (11:49 ET). FanDuel is the price of record, using main and alt ladders on both sides. DraftKings and Pinnacle are there for comparison.

## Simulations
Monte Carlo, Bias and Game Randomness each ran 100,000 sims with seed 20261101 (tools/sim_v6.py; scripts bonus_sims*.py; output bonus_sims.json).

| Leg | MC p / median | Bias p / median | GR p / median |
|---|---|---|---|
| Tre Tucker receptions O3.5 | .619 / 4 | .618 / 4 | .598 / 4 |
| Puka Nacua receptions O7.5 | .606 / 9 | .604 / 9 | .634 / 9 |
| Stefon Diggs receptions O3.5 | .665 / 4 | .665 / 4 | .677 / 5 |
| Jahmyr Gibbs rush yds O79.5 | .657 / 92.6 | .661 / 93.5 | .623 / 91.7 |

## Projections and picks
1. **Tre Tucker receptions O3.5, -120** (LV@NYJ, 1:00 PM ET)
   - Pricing: no-vig .510; edge +10.1, or +6.8 after shrink.
   - Why it passes:
     - Recent form: 4/4/5/5 catches in his last 4 games with Cousins.
     - Coverage: Azareye'h Thomas is allowing 70.8% completions.
     - Game script: toss-up, LV +1.5.
   - Backup if inactive: no qualified swap.
2. **Puka Nacua receptions O7.5, -138** (LAC@LAR, 4:05 PM ET)
   - Pricing: no-vig .542; edge +7.3, or +3.8 after shrink.
   - Why it passes:
     - Volume: last 4 with Stafford went 9/17/6/8.
     - Matchup: LAC allows 8.86 YPT to WRs.
     - Game script: LAR -6.5.
   - Backup: none qualified. The O6.5 rung at -260 has only +2.3 edge.
3. **Stefon Diggs receptions O3.5 (alt), -166** (PHI@WSH, 8:20 PM ET)
   - Pricing: de-vigged against the 4.5 main (+132/-178), no-vig .583; edge +8.7, or +3.6 after shrink.
   - Why it passes:
     - Recent form: 4/5/6 in 3 of 3 games with Daniels.
     - Context: McLaurin is on IR and Smith is out on the PHI side.
     - Coverage: DeJean is allowing 70.6% completions.
     - Game script: WSH -5.5.
   - Backup: none qualified.
4. **Jahmyr Gibbs rush yds O79.5 (alt), -162** (MIN@DET, 1:00 PM ET)
   - Pricing: de-vigged against the 87.5 main, no-vig .583; edge +6.5, or +2.0 after shrink.
   - Why it passes:
     - Role: carry share of 71%/100%/78%/88% over his last 4, and 6-8 targets a game.
     - Recent form: 99/46/151/116 yards. That clears 79.5 in 3 of 4, and the 107.5 median is above the §14 bar of 95.4 at -162.
     - Matchup and script: MIN allows 3.99 YPC (neutral); DET -3.5.
   - Backup: Gibbs O69.5 at -250 (edge +7.8, shrunk +0.3). It is the same player, though, so it does not cover him going inactive.

**Slip:** 4 legs, not 5-6. Nothing else passed the edge rule, 10G or the placed-ticket bars, and I did not pad the card. The full list of cut legs with the phase that cut each is in the checklist summary.

**Stack flags (the user decides):**
- Gibbs rush yds while Ticket 2 already has Gibbs 5+ receptions.
- Puka receptions while UD20 already has Puka o69.5 receiving yards.

## Risks and checks still to come
- **Puka:** his likely defender, LAC CB Donte Jackson, is still Questionable on ESPN as of 11:52 ET. If Jackson sits, Phase 4 has to be re-run before the 4:05 game (~2:35 PM ET). LAC CB McDuffie is also Q.
- **Diggs:** this is the 8:20 PM game. The inactives check is due ~6:50 PM ET.
- **Coverage data:** the defender numbers come from the PFR cache pfr_def_adv_2026.html (10-29 06:02). That falls under the approved exception (Rico, valid 2026-11-01, receiving legs) and misses roughly the last 2 games.
- **Low-confidence inputs:** pressure is a PROXY, and NGS is from the nflverse backup.
- **Reprice:** any line move over 0.5, or 20 cents, before kickoff means a reprice through Phase 14.
- **Placed-ticket moves since 08:47:** see line_moves_0847_1149.txt. Every move of 0.5 or more went toward the over, which supports the placed over tickets:
  - Lamb rec yds 80.5→86.5
  - Flowers 87.5→89.5
  - Warren rush+rec 91.5→92.5 (PP 90.5→92.5)
  - P. Washington 67.5→69.5
  - Bijan rec 3.5 at -148→-188 (price only)

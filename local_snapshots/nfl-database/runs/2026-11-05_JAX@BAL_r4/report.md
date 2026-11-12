# JAX @ BAL TNF — r4 (Ghost6 vet fixes), 2026-11-03 ~19:45 ET
r2 and r3 are untouched. The locked read is unchanged (sha256 76b563a3…5685). No new Odds API credits (3,575 remain); prices are from 19:15 ET. No Grok or OpenAI calls.

## Fixes
1. **rush_last4** now builds the window from games **played** (in pbp as rusher, receiver or passer for the team) and fills 0 carries. A game with snaps but no touch or target is still invisible, because there's no local snap file; FLAG.
   - The window is any-QB; **Rico decides** any-QB vs Fagnano-only.
   - N1 is now applied to RBs only (QB rush overs had been mislabelled N1).
   - Rush legs on the opposite side of a locked-read leg are cut as read AVOID.
2. Game-line legs now go through policy (game_lines.py → game_legs.csv) with §7 and last-2.
3. Dead code removed: the `and False` branch and the redundant rushrec override.
   - shop() now returns NO_QUOTE plus a flag instead of falling back to FD.
   - One output CSV (policy_legs.csv); the r3-style duplicates are gone.
4. No tests cover policy (tools/tests has none), so none were run.

## Rush-leg changes (r3 → r4), all 12 rush rungs: rush_changes_r3_r4.csv
- **J. Hill window: [3, 73, 7, 15] → [73, 0, 7, 15]**, now including the Wk6 at CLE game with 0 carries.
  - **Under 13.5 is still a FAIL at 2/4:** 0 and 7 are under, but 73 and **15** are over 13.5. Ghost6's 3/4 counts 15 as under, which it isn't. Still **CUT**; last-2 [7, 15] is a DOWNGRADE.
  - Over 13.5 / 9.5 / 4.5: unchanged (CUT on N1, plus §7 on 13.5 and 9.5).
- **Henry** (window unchanged [102, 58, 45, 53]): under 69.5 stays PASS. **Over 49.5 goes PASS-DOWNGRADE → CUT** (opposite of read edge 1). Overs 69.5 / 59.5 stay CUT.
- **Lawrence** (unchanged [0, 25, 11, 10]): under 12.5 stays PASS. Overs 9.5 / 4.5 are still CUT, but the reason changed from N1 to read AVOID; N1 doesn't apply to QBs.

## Game-line checks
Method: final and halftime scores from pbp for each team's last 4 games. TT under means team points < line. Spread -X covers if margin > X. 1H spread uses halftime margin.

| leg | last 4 | §7 | last-2 | status | best price |
|---|---|---|---|---|---|
| BAL TT under 14.5 | pts [30, 10, 13, 10] | **PASS 3/4** (Ghost6 confirmed) | OK | PASS | FD -120 (only FD has 14.5; Pinnacle U16.5 -143) |
| JAX -10 | margins [5, 2, -3, 35] | FAIL 1/4 | DOWNGRADE | **CUT** | Pinnacle -104 |
| JAX -9.5 | same | FAIL 1/4 | DOWNGRADE | CUT | FD -120 |
| JAX 1H -6.5 | 1H margins [10, -7, -3, 28] | FAIL 2/4 | DOWNGRADE | **CUT** | DK/Pinnacle -102 |

## SGP and correlation
**There's no FD SGP quote in our data.** The Odds API pull has no SGP pricing, and getting one would mean FD's private API or a logged-in page, both off-limits. So **correlation is unpriced**.
- Henry U and BAL TT U are positively correlated (same BAL-stalls script). Lawrence U is mildly correlated (JAX leading, kneel-downs).
- The product of singles: -114 × -114 × -120 → 1.877 × 1.877 × 1.833 = **6.46 decimal (about +546)**.
- FD SGP pricing generally haircuts positively correlated legs, so the real SGP will likely pay less than +546. With no priced edge on any leg (anchored ≤ +0.2, flag), a haircut parlay compounds the vig and the haircut.
- JAX -10 is cut anyway, and mostly duplicates BAL TT U.

**Recommendation: SINGLES first.** The slip is listed as optional/info only. Take it only if FD's SGP price is ≥ about +500 when Rico checks it in-app himself.

## r4 card
**Singles (playable):**
1. Henry rush U69.5: DK/FD -114 (Pinnacle U70.5 -118). §7 3/4, last-2 OK.
2. Lawrence rush U12.5: FD/Pinnacle -114. §7 3/4, last-2 OK.
3. BAL TT U14.5: FD -120. §7 3/4, last-2 OK.

Off-read (singles only): Strange rec yds O35.5 (FD -114; P4 CAUTION) and P. Washington rec U4.5 (DK -125).

**Optional slip (3 legs, same game, unpriced correlation):** Henry U69.5 + Lawrence U12.5 + BAL TT U14.5. §11 OK. No TD legs, no pass-yds legs.

**Removed from r3:** JAX -10 as a 4th leg (CUT, 1/4) and JAX 1H -6.5 single (CUT, 2/4).
All edges are flag-only until 2026-11-10 (date gate). Full tables: gate_table.md, checklist.md.

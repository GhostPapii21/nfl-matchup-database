# Week 11 focus 9: research summary (MANUAL RUN, requested Sat Nov 21 3:48 PM AST)

**Vet status: VETTED by Ghost6 4:18 PM AST, paper only, research only until NFL-49/56 pass; re-check props at kickoff.**

**SIMULATION NOT RUN. RESEARCH ONLY, PAPER ONLY, NOT PICKS.**
- NFL-49 and NFL-56 are unmet (projection_ready=false).
- Labels are capped at Lean: the packet is over 24 hours old and predates the final injury reports.
- The fix list is in FIXES.md. Each game folder has report.md and checklist.md.

**All prices are STALE.** Props, alt ladders and book game lines are from The Odds API, Fri Nov 20 6:33 AM AST. Re-check every price at kickoff; a move of more than 0.5 or 20 cents means a reprice. Rico's consensus lines are from Sat 3:47 PM AST.

**Totals:** every total number below is a season-average cross-check, not a projection.
- There has been no miss audit of this method.
- Game-total unders failed the PR #25 backtest (per the Week 10 scheduled report).
- The selective-edge study found game-total samples too small, pointing the wrong way.

**Rush-yard unders:** none is shown to meet the 18-5 study criteria. That study (Weeks 8-9, n=23) required an RB 60% carry gate (QBs exempt) plus a model edge vs no-vig of +5 points or more, and no model ran here.

**Alt floors:** the repo's selective-edge fit found gated rush-yard alt-over floors not shown to beat their price (about -10 to -13 points vs break-even). Because of this, Ghost6 moved Cook 79.5 to WATCH at 4:18 PM AST.

## Revised top leans (all paper only, prices STALE)
| # | Game | Lean | Price (STALE, Nov 20) | Key support | Kill-switch |
|---|---|---|---|---|---|
| 1 | BAL@CAR | Derrick Henry rush U62.5 | DK U63.5 -111; FD 62.5 -114 | Last 4: 45, 53, 57, 10; carries falling. RB gate PASS 3 of 4 (Week 9 was 52%) | BAL favored; line 55.5 or lower |
| 2 | MIA@BUF | Josh Allen rush U27.5 (the MIA@BUF research lean) | DK -109 | 6 of 9 under including scrambles; blowout script; MIA allows 11.5 QB rush yards a game | Close at half; line 24.5 or lower |
| 3 | LV@DEN | Bo Nix rush U10.5 | MGM -110 | 8 of 9 under (one 73-yard spike); DEN lead script | Line 8.5 or lower; DEN trails |
| 4 | TB@DET | Baker Mayfield rush U10.5 (void if inactive) | FD -114 | 3 of 4 recent under; plantar fascia | Inactive; line 7.5 |
| 5 | NO@CHI | Total under 48.5 | Rico 48.5 | Rain 84-89%, 15 mph; NO missing both tackles and its center; cross-check about 44.1 | Rain clears; non-offensive TDs |
| 6 | JAX@NYG | Total under 46.5 | Rico 46.5 | Heavy rain in the second half; JAX defense 2nd; JAX C out. The cross-check is only 1.5 under (noise) | Rain timing; turnovers |
| 7 | CIN@WAS | Total under 54.5 (thin) | Rico 54.5 | Cross-check about 49 on season averages, but about 52.4 on CIN's last-4 form (37.5 a game) | Total already at 52.5; Dax Hill out |

Downgraded or removed by the vet:
- Cook rush alt 79.5 is now WATCH (Ghost6 4:18 PM AST). Rush alt-over floors ran about -10 to -13 points vs break-even; the price is -192 juice and STALE. Rung 79.5 at DK -192, with 69.5 for the blowout trim; 7 of 8 hits, 27% cushion.
- MIN@SF U46.5 is now WATCH, until a Cousins-adjusted script projection exists.
- Emmett Johnson is removed (fails the 60% carry gate, 1 of 4).
- The Rice 80+ row is WATCH / do-not-play.

**Candidate SGP:** none qualifies in any game. Each report keeps a WATCH-only shadow build that names the blocking gate on every leg.

**Side list, 80+ yard long shots (all WATCH / do-not-play, edges STALE):**
- Rice: +3.3 at FD +290. Blocked by no verified defender, the wind, the #3 WR ban and a stale edge.
- Monangai: +10.3, BLOCKED (under 60% of carries).
- Kittle: +2.7, under the +3 bar.

**Weather:**
- Receiving overs cut: ARI@KC (wind), NO@CHI (rain and wind), JAX@NYG (rain), MIA@BUF (Open-Meteo gust 21), CIN@WAS (Open-Meteo gusts 21-24).
- MIN@SF is borderline (PoP 67%, 0.00 in): recheck, not a cut.
- Clean: BAL@CAR, LV@DEN, TB@DET (dome).

**Stale or unknown inputs:**
- Prices from Nov 20.
- Alt totals, half/quarter lines and Pinnacle are NOLINE.
- Man/zone is 2025 only.
- No receiver has a verified main defender.
- Beck props are VOID.
- The NYG starter is unconfirmed (McCarthy per the depth chart; Winston 6 appearances vs McCarthy 4).
- CIN and WAS official Saturday statuses weren't seen.
- SF's Friday table was blank.

---

## ARI@KC (KC -15.5, 40.5)
- **Matchups (ESTIMATE):**
  - McBride vs Bolton (6.1 YPT) and Tranquill (5.8); KC allows 65.5 TE yards a game.
  - Kelce and Rice vs the ARI secondary.
- **Leans:** none at Lean. The ARI team total under is WATCH: the cross-check (ARI about 18.6) is far above the 12.5 implied, so the market has priced the Johnson downgrade.
- **WATCH:** Mahomes rush U9.5 (4 of 9 under). The Kelce and Rice floors are weather-cut.
- **Do not play:** Emmett Johnson (1 of 4 at 60%), Allgeier, Love, Knight, Ott. Walker is OUT. Beck props are VOID.
- **Injury swings:** Beck OUT and Josh Johnson starts. Walker III, Trey Smith and Jaylon Moore are OUT.

## BAL@CAR (CAR -3, 43.5)
- **Matchups (ESTIMATE):**
  - Flowers vs Will Lee III (5.9) and Marco Wilson (5.6).
  - McMillan vs Wiggins (6.5) and a backup CB, with Humphrey OUT.
- **Lean:** Henry rush U62.5. RB gate PASS 3 of 4; the Week 9 game was 52% and is disclosed.
- **WATCH:** Young rush U7.5 (6 of 9, but BAL allows 22 QB rush yards a game); Hubbard rushing (only a deep rung qualifies).
- **Do not play:** J. Hill, Ali, Etienne, Dillon, Brooks, Tyus.
- **Injury swings:** BAL is without Humphrey, Hawkins and Madubuike. Brissett starts.

## MIA@BUF (BUF -16.5, 44.5)
- **Matchups (ESTIMATE):**
  - M. Washington vs Igbinosun (5.3), with Benford OUT.
  - Shakir vs Marshall (10.0) and C. Johnson (11.3).
- **Lean:** Allen rush U27.5 (DK -109), the MIA@BUF research lean.
- **WATCH:**
  - Cook alt 79.5 (DK -192, STALE; 69.5 trim). Moved to WATCH by Ghost6 on the alt-floor evidence.
  - MIA team total under (cross-check against it).
  - Washington and Shakir floors (gust-cut).
- **Do not play:** J. Wright, Achane, R. Davis, Ty Johnson. O. Gordon's rushing over is blocked (trailing team, 2.5 targets a game).
- **Injury swings:** Benford and D. Williams OUT; Kincaid Doubtful; Ed Oliver Q (SI, Sat).

## NO@CHI (CHI -11.5, 48.5), WEATHER FLAG
- **Matchups (ESTIMATE, all weather-cut):**
  - Olave vs Jaylon Johnson (10.4).
  - Burden vs McKinstry (9.1), with Emerson OUT.
- **Lean:** total under 48.5 (cross-check about 44.1).
- **WATCH:** Swift rushing (deep rung only); C. Williams rush U17.5.
- **Do not play:** Kamara, K. Miller, Etienne, Estimé, Monangai, R. Johnson. No Shough under.
- **Injury swings:** NO OL Fuaga, Richards and McCoy are OUT. CHI nickel K. Gordon is OUT.

## TB@DET (DET -4.5, 46.5), dome
- **Matchups (ESTIMATE):** St. Brown vs Parrish (7.2) and McCollum (6.1), with Winfield and Hayes OUT.
- **Lean:** Mayfield rush U10.5 (void if inactive).
- **WATCH:**
  - St. Brown 49.5 floor (now in the checklist).
  - Gibbs is weakened: TB's run D is 2nd and DET C Mays is OUT.
- **Do not play:** Irving, Gainwell, Tucker, Vaki. The Jameson Williams floor is under the #3 WR ban.

## JAX@NYG (JAX -6, 46.5), WEATHER FLAG
- **NYG starter unconfirmed:** McCarthy per the depth chart; Winston has 6 appearances vs McCarthy's 4.
- **Matchups (ESTIMATE, weather-cut):**
  - Nabers vs Hunter and M. Brown.
  - P. Washington vs Banks (4.7).
- **Lean:** total under 46.5. The cross-check is only 1.5 points under, which is noise; the lean rests on the rain and the JAX defense.
- **WATCH:** Lawrence rush OVER. His under is 5 of 9 and 2 of 4 at 10.5; NYG allows 32.4 QB rush yards a game.
- **Do not play:**
  - McCarthy rush under (stays NO PLAY).
  - Backs: Tuten, Rodriguez, Abdullah, Skattebo, Singletary, Harris, Tracy.

## LV@DEN (DEN -10.5, 40.5), clean
- **Matchups (ESTIMATE):** Waddle and Sutton vs Stokes (8.6) and Masses (10.6), but their logs are volatile; Bowers (Q).
- **Lean:** Nix rush U10.5.
- **WATCH:** LV team total under (cross-check about 22.1 vs 15.0 implied, from Cousins-era games).
- **Do not play:** Jeanty (under 60%), M. Washington, Dobbins, Coleman, Harvey, Badie.

## MIN@SF (SF -3, 46.5), Mexico City
- **Matchups (ESTIMATE):** Jefferson vs SF CBs around 7.0-7.2 YPT; Kittle vs Metellus (7.0), but MIN allows 35 TE yards a game (2nd). Addison (OUT) is removed from the table.
- **Leans:** none. Total under 46.5 is WATCH until a Cousins-adjusted script projection exists.
- **WATCH:** Kittle 39.5 floor (now in the checklist; Phase 11 borderline, not a fail).
- **Do not play:** A. Jones, Mason, CMC, K. Black, J. James.
- **Injury swings:** Murray and Addison OUT, Cousins starts; Evans Q but expected to play.

## CIN@WAS (CIN -6, 54.5), MNF
- **Matchups (ESTIMATE):**
  - Chase vs Douglas (6.7), Amos and Robertson.
  - Diggs vs T. Davis (4.8) and DJ Turner (5.6).
- **Lean:** total under 54.5, thin. The cross-check is about 49 on season averages and about 52.4 on CIN's last-4 form; CIN's last 4 game totals were 48, 79, 51, 56.
- **WATCH:** Daniels rush U36.5; Diggs and A. Williams floors (gust-cut).
- **Do not play:** Chase Brown, Perine, T. Brooks, R. White, Croskey-Merritt.
- **Injury swings:** Risner OUT, Dax Hill expected to play, Dugger Q, Burks on IR; WAS White and Q. Martin Q. These are secondary sources.

---
Research only. Not validated. Not betting advice.

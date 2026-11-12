# Pressure / checkdown layer + re-grade — Week 8, Sun Nov 1, 2026
Written Sat Oct 31, 2026 ~8:40 PM ET. This responds to Rico pt659u.
Nothing was posted, sent or bet. No PFR pulls. Film reads stay UNVERIFIED.

**Scripts:**
- src/pressure_checkdown.py (data)
- src/pressure_scan.py (re-grade, 100k × 3 per engine)
- Output: pressure_scan.csv

## Sources (all public, cached on the box)
- **Blitz:** FTN charting 2026 via nflverse (`/tmp/ftn.parquet`, weeks 1–8), `n_blitzers > 0` per dropback.
  - In this feed, "blitz" equals "5+ pass rushers" on every play (identical rates), so they're reported as one number.
- **Pressure:** nflverse 2026 pbp has no `was_pressure`, and the 2026 participation file 404s (only 2025 is cached).
  - Pressure is therefore a **proxy**: (sack OR QB hit OR scramble) / dropbacks, from nflverse pbp 2026.
- **Time to throw:** NGS passing 2026, season row (week 0), `src/ngs_passing.parquet`. League average for qualifiers is 2.85s.
- **Target shares by blitz, RB YPT allowed, QB-adjusted:** nflverse pbp 2026 joined to FTN, with RB position from the nflverse roster.
  - League RB yards per target is **5.54** (targets basis).
  - The 1.85 "MIN RB YPT" in the alt-card file was a bad denominator (I used the wrong count as the denominator). On a consistent targets basis, MIN allowed **4.04**.

## 1. Defenses: blitz and pressure-proxy rates (league: blitz .313, pressure .202)
| Def | Blitz season | Blitz L4 | Pressure season | Pressure L4 | Faces |
|---|---|---|---|---|---|
| MIN | **.714** (league-high range) | .664 | **.286** | .261 | Gibbs/Goff |
| DEN | .355 | .339 | .270 | .282 | Walker/Mahomes |
| LAC | .270 | .280 | .217 | .212 | Puka, Kyren/Stafford |
| CLE | .237 | .263 | .211 | .243 | Warren/Rodgers |
| IND | .215 | .206 | .181 | .190 | Tuten/Lawrence |

## 2. QBs: time to throw, checkdown, who gets it when blitzed
| QB | TTT (NGS) | aDOT all / blitzed | Behind-LOS share | RB target share all / blitzed / pressured / clean |
|---|---|---|---|---|
| Goff | 2.84 | 8.0 / **6.0** | .192 | .205 / **.169** / .211 / .205 |
| Stafford | 2.73 | 8.2 / 8.3 | .149 | .205 / .136 / .133 / .214 |
| Rodgers | 2.74 | 7.4 / 6.4 | **.297** | .211 / .133 / .130 / .220 |
| Lawrence | 2.72 | 8.2 / 9.2 | .162 | .134 / .103 / .238 / .120 |
| Mahomes | 2.79 | 6.3 / 6.5 | **.328** | .222 / .229 / .158 / .230 |

**Target share when blitzed vs not:**
- **Goff:** St. Brown .38 vs .28 and LaPorta .24 vs .15 go **up**. Gibbs .14 vs .20 and J. Williams .11 vs .20 go **down**.
  - Goff beats the blitz to his slot WR and TE, not the back.
- **Stafford:** Nacua .21 vs .24 (about flat). Kyren drops out of the top 5 when blitzed (.17 clean).
- **Rodgers:** Bernard .25 vs .11 and Metcalf .27 vs .22 go **up**. Warren is not in the top 5 when blitzed (.067 vs .174).
  - Bernard, not Warren, is the blitz outlet.
- **Lawrence:** Tuten .086 vs .074 (flat). P. Washington and Strange lead.
- **Mahomes:** Walker .167 vs .152 (slightly up).

**Player yards per target, blitzed vs not:**

| Player | Blitzed | Not blitzed |
|---|---|---|
| Gibbs | 6.6 | 6.5 |
| Warren | 6.2 | 8.8 |
| Tuten | 5.6 | 10.9 |
| Kyren | 3.1 | 6.5 |
| Nacua | 6.8 | 8.2 |

Blitzed samples are only 5–17 targets.

**Target multiplier applied in the sims:**
- Formula: (opponent L4 blitz × blitzed share + (1 − blitz) × clean share) / season share, shrunk 50%.

| Player | Multiplier |
|---|---|
| Gibbs | **0.942** |
| Walker | 1.004 |
| Puka | 1.001 |
| Tuten | 0.991 |
| Warren | 1.015 |
| Kyren | 1.005 |

- **High-blitz flag:** MIN's blitz rate **hurts** Gibbs targets, the opposite of the usual checkdown boost, because Goff funnels to St. Brown and LaPorta.
  - MIN's blitzing would **boost** LaPorta and St. Brown (St. Brown recyds is barred on Ticket 2).
  - None of the other card defenses blitz above average except DEN (mild).
  - No deep-WR leg on the card is hurt.

## 3. RB yards per target allowed, QB/offense-adjusted
Adjusted = league × (allowed / expected from the offenses' RB YPT in their other games).

| Def | Allowed | Expected from offenses faced | Ratio | Adj YPT | vs league 5.54 |
|---|---|---|---|---|---|
| MIN | 4.04 | 4.74 (GB, CHI, TB, MIA, NO, IND) | .85 | **4.72** | below |
| CLE | 3.89 | 5.94 | .65 | **3.63** | well below |
| IND | 7.74 | 5.29 | 1.46 | **8.12** | well above |
| LAC | 4.53 | 6.60 | .69 | 3.81 | below |
| DEN | 5.06 | 5.36 | .94 | 5.23 | ~avg |

- **Rico's point holds:** MIN faced weak RB-receiving offenses, and adjusting lifts it from 4.04 to 4.72, but it's still below average.
- CLE gets *tougher* after adjustment. IND stays very soft (Tuten +).
- In both engines, the RB opponent YPT factor was multiplied by 1 + 0.5 × (ratio − 1) (the same 50% shrink as oppadj).

**§14 RB receiving-yards gate re-test** (needs 6+ YPT in 3 of 4 AND a defense above average after adjustment):
- **Gibbs:** 2 of 4 (8.1, 3.1, 9.3, 4.5) and MIN adjusted 4.72 is below average → **still CUT**, although the engines now pass 30+ (G .566, BG .581).
- **Warren:** 3 of 4 ✓, but CLE adjusted 3.63 → **still CUT** (engines .476/.476 at 25+).
- **Tuten:** 4 of 4 ✓ and IND 8.12 ✓ → PASS.
- **Gibbs as receiving vs rush+rec:**
  - Receiving is blocked by §14.
  - **Rush+rec O121.5 (−113) now passes both engines**: G .531 (+3.3/+2.4), BG .561 (+6.3/+4.5).
  - It was G +1.1 before, a fail. The lift comes from the MIN adjustment net of the 0.942 target cut.

## 4. Re-grade (shared rule: raw ≥ +3, shrunk > 0, p ≥ .45 on BOTH; before → after)
| Leg | FD | No-vig | G6 p | BG p | G6 raw/shrunk | BG raw/shrunk | Verdict |
|---|---|---|---|---|---|---|---|
| Puka 9+ rec | +124 | .417 | .501 → .501 | .510 → .509 | +8.4/+8.4 | +9.2/+8.9 | PASS (LAC low blitz, neutral) |
| Puka 8+ rec | −138 | .542 | .593 | .593 → .592 | +5.1/+2.3 | +5.0/+2.3 | PASS |
| Walker 90+ rush | +104 | .462 | .499 | .532 | +3.7/+3.7 | +7.0/+6.0 | PASS (rushing; pressure n/a) |
| Tuten 20+ rec yds | +158 | .365 | .455 | .507 | +9.0/+10.4 | +14.2/+14.0 | PASS (IND soft, low blitz) |
| Tuten 15+ rec yds | −102 | .476 | .514 | .568 | +3.8/+3.4 | +9.2/+7.2 | PASS |
| **Warren O90.5 rush+rec** | −113 | .500 | .532 → **.526** | .582 → .575 | **+2.6**/+1.8 | +7.5/+5.3 | **FAIL G6 raw <3 → DROPPED** (CLE tougher on RBs after adjustment; Bernard is the blitz outlet) |
| Warren 25+ rec yds | +114 | .440 | .476 | .476 | +3.6/+4.3 | +3.6/+4.3 | engines pass; **§14 CUT** (CLE adj 3.63) |
| **Gibbs O121.5 rush+rec** | −113 | .498 | .509 → **.531** | .535 → **.561** | +3.3/+2.4 | +6.3/+4.5 | **REVIVED: PASS**. Flag: same player as Ticket 2 Gibbs 5+ rec (different market, positively correlated); Rico override needed under §11 |
| Gibbs 30+ rec yds | −106 | .485 | .533 → .566 | .546 → .581 | +8.1/+6.1 | +9.6/+7.1 | §14 CUT + T2 correlation |
| Kyren 4+ rec | +114 | .437 | .531 | .468 | +9.4/+8.5 | +3.1/+4.0 | PASS; still same QB as Puka (alt only); weak when blitzed |
YPC legs: Walker + Gibbs rush+rec = 2, the cap.

## Revised cards
**A. Best-edge, 3 legs (all clean, no placed-player overlap): Puka 9+ rec +124, Walker 90+ rush +104, Tuten 20+ rec yds +158.**
- About **+1079**. Hit chance G6 **11.4%**, BG **13.7%**; breakeven 8.5%.

**A+. Add Gibbs O121.5 rush+rec −113 (Rico override on the Gibbs Ticket-2 overlap).**
- About **+2122**. Hit chance G6 6.0%, BG 7.7%; breakeven 4.5%.

**S. Safer, 3 legs: Puka 8+ −138, Walker 90+ +104, Tuten 15+ −102.**
- About **+597**. Hit chance G6 15.2%, BG 17.9%; breakeven 14.4%.
- G6 margin is thin.

**S+. Add Gibbs rush+rec.**
- About **+1213**. Hit chance G6 8.1%, BG 10.0%; breakeven 7.6%.

## What changed and why
- **Warren is out.** CLE's RB defense is tougher than it looked once you account for the offenses it faced (.65 ratio). Rodgers throws to Bernard, not Warren, when blitzed, and my engine falls to +2.6 raw.
- **Gibbs is back in, as rush+rec only.** The QB-quality adjustment softens MIN (4.04 → 4.72). His receiving still fails §14, and MIN's 71% blitz rate cuts his targets about 6%, because Goff throws to St. Brown and LaPorta under the blitz.
- **Puka, Walker and Tuten are unchanged.** Their opponents blitz at or below league rate. IND's adjusted RB softness supports Tuten.

## Caveats
- **Pressure is a proxy:** sack/hit/scramble, not true NGS pressure. True 2026 `was_pressure` and `number_of_pass_rushers` aren't published yet (the participation file 404s).
- **Blitz-split samples are small** (5–17 targets per player), which is why the target multiplier is shrunk 50%.
- **11:30 AM ET inactives checks still apply** (recheck Puka and Walker at 2:35 PM):
  - **Gibbs:** check the DET backfield split; drop if he's limited.
  - **Tuten:** confirm he's JAX's lead back.
  - **MIN:** watch for any blitz-heavy defensive coordinator news.

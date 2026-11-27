# PHI @ DAL — Thu Nov 26, 2026, 4:30 PM ET, AT&T Stadium (retractable roof, status unannounced) — Thanksgiving game 2
**SCHEDULED RUN** (fired Nov 26 8:58 AM ET). Research only. `projection_ready` = false → no picks, no slips. **CHECKLIST VETTED: NO (pending Ghost6).**

| Item | Value |
|---|---|
| Packet | `pregame/packets/2026_12_PHI_DAL` @ main 2b33647, **Updated Nov 25 6:31 PM ET** (23:31:47Z) |
| Built before final injury report? | **YES.** After 6:31 PM: DAL Mingo OUT 7:36 PM, Locke (S) OUT 7:40 PM, Moore (CB) status 10:19 PM, Thompson (S) Q; PHI Ebiketie OUT 5:25 PM / J. Jones (CB) OUT 5:23 PM were just before. **All labels capped at Lean.** The packet engine also does not reflect the PHI QB change (Hurts IR → Joe Milton III, 3rd start). |
| Book prices | Packet Nov 25 6:26 PM ET; repo direct_lines Nov 26 3:17 AM ET. Odds API credits spent: 0 |
| Weather | NWS hourly (api.weather.gov, generated Nov 26 8:34 AM ET): 4 PM 53°F, wind 10 mph, 0% precip, sunny; Open-Meteo (9:00 AM ET): 52°F, wind 12.6 gust 19.7 at 4 PM, dry. **No weather flag.** Roof status: NOT CONFIRMED (SharpShotPicks listed closed in prior run, unofficial) |
| Tools | gh api read-only, ESPN injuries (9:00 AM ET), NWS + Open-Meteo, prior-run nflverse/StatRankings/Sharp/sims (seed 20261101, 3×100k) |
| Live checks | ESPN injuries 9:00 AM ET; inactives NOT posted (due ~3:00 PM ET); DK site 403 (not bypassed) |


## Five-line summary
1. **Script:** DAL controls (−8.5 / −9 Pinnacle, total 47.5–48.5, DAL ML −480 / PHI +370). Milton's 53% completions and 10 sacks in two starts meet a DAL defense that blitzes only 25%: Milton is F with no blitz (4.15 YPA, n=64).
2. **Market:** spread flat since Nov 24 (FD −8.5 throughout; Pinnacle −8.5→−9 on Nov 25); total FD 48.5→47.5, Pinnacle 47.5→48.5: books disagree by 1 on the total. Everything the model likes (PHI offense bad) is already priced.
3. **No leg survives every gate.** Barkley is under the 60% carry rule (used share 49%), Javonte unders are MODEL-SUSPECT and §9-blocked, receiving legs are cut on P4. Only a thin Dak rush over 9.5 stays as a Lean.
4. **80+ watch:** Lamb 3★ (p80 .627, blend .620 vs FD −172 BE 63.2% → −1.2), Pickens 2★ (.490; blend .457 vs +136 BE 42.4% → **+3.3, only rung that clears +3, FD-only, defender inferred, so WATCH**), Javonte 2★ (−4.8), D. Smith 1★ (−4.0).
5. **Injuries help DAL receivers:** PHI CB Jonathan Jones OUT and LB Ebiketie OUT against the #30 WR pass D; DAL TE Ferguson OUT, S Locke OUT, G Booker OUT.


## Game script
| Scenario | Prob (judgment) | Flow |
|---|---|---|
| **Base** DAL controls | ~55% | DAL leads 10–17 at half; PHI leans on Barkley/Milton legs (Milton ~27% of carries); DAL runs Javonte late; PHI garbage-time targets to Smith/Lemon |
| **Flip A** PHI hangs on the ground | ~30% | DAL run D #32 (5.37 YPC, 113 RB rush); Barkley + Milton keep it within a score into Q4, under hits |
| **Flip B** blowout | ~15% | Milton sacks/turnovers, DAL +20; Javonte 4Q volume, PHI pass volume up |
Period read: DAL H1 spread (Pinnacle −4.5, FD −6.5) is a hypothesis only: no modeled probability, NOT A LEG.


## Breakdown
### Injuries and depth (ESPN API Nov 26 9:00 AM ET; newest entry 10:19 PM ET Nov 25)
| Team | OUT / IR | Questionable | Matters because |
|---|---|---|---|
| PHI | CB Jonathan Jones OUT; LB Arnold Ebiketie OUT; LB Zack Baun IR; WR Dontayvion Wicks IR; QB Hurts IR (Milton starts) | none listed | Woolen/Ringo play more; thinner LB/pass rush; Milton = low-sample QB |
| DAL | TE Jake Ferguson OUT; S P.J. Locke OUT; WR Jonathan Mingo OUT; G Tyler Booker OUT; CB DaRon Bland IR | S Jalen Thompson (back from IR), CB Devin Moore (ESPN lists IR + 'questionable': conflicting, UNKNOWN) | TE targets reallocate (Spann-Ford 6.8% share); interior OL hurt for Javonte |
Inactives ~3:00 PM ET. Missing ≠ healthy.

#### Carried from the 4:01 AM manual run (same packet; sims seed 20261101, 3×100k, prior-run numbers; RB share tables there used a 50% cut: **the saved 60%-of-carries rule now applies and is stricter**)

### Breakdown
**PHI offense (Milton):**
- Card (n=64 dropbacks, LOW-SAMPLE):
  - Vs blitz: 8.45 YPA, 65% completions (A, small n).
  - **No blitz: 4.15 YPA, 47% (F).**
  - Sack rate 15.6% (F), 3rd/4th-down conversions 24% (F), EPA/dropback −0.28.
- **DAL defense:** StatRankings man 46.6% (#2), zone 51.8% (#31), single-high 58.1% (#7), **blitz 25.1% (#27)**. Sharp: man 22.3 / zone 69.3 / MOF-closed 55.7. Sharp also has DAL as man-heavy relative to the league, so the two roughly agree.
- **Key read:** DAL rarely blitzes, and Milton is at his worst without the blitz. DAL's defense is still weak overall: 28.75 pts allowed (#29), YPC 5.37 (#32), RB rush 113 (#28).
- DAL pass rush: Q. Williams 19 pressures / 8 sacks, Gary 18, Ezeiruaku 14. PHI OL and Milton's holding of the ball explain the 10 sacks in 2 games.

**DAL offense (Dak):**
- Card: vs blitz 7.0 YPA (C), no blitz 7.26 (C), **sack rate 3.4% (A)**, 3rd/4th-down 45% (A).
- **PHI defense:** StatRankings man 39.5% (#9), single-high 57.7% (#8), blitz 26.5% (#25). Sharp: man 17.5 / zone 74.3. That is a level disagreement on man, so **SHARP CAUTION**.
- PHI allowed 24.4 pts, WR yds 184.5 (#30), pressure 12.3% (#29). Dak should be clean.
- Lamb has 34.7% of targets L3. Pickens is at 23.7% and rises vs the blitz (27.7% blitzed vs 19.4% non-blitzed).

**Receiver seesaw:**
- DAL: Lamb/Pickens dominate. Pickens' by-game targets were 6, 4, 0, 18, 10, a volatile seesaw with Lamb.
- PHI: Cooper 23.6 / Smith 21.8 / Lemon 21.8 with Milton. Smith missed W8–10, then got 12 targets in W11.

**RB run direction:** not computed (MISSING). DAL's RB rush D is #28 and PHI allows the matchup baseline.

**Red zone:** DAL scores efficiently. PHI's offense has been stuck at 14.9 pts.

### RB carry share and the 50% rule
| RB | Share (role window) | Verdict |
|---|---|---|
| Barkley | 52% (W9), 65% (W11); Milton takes 27% of carries | PASS (borderline) |
| Shipley | 15% (W11) | DNP |
| E. Mitchell | 12% (W9) | DNP |
| Javonte | 61% L3 (season 65.5%) | PASS |
| Goodson | 0% L2 | DNP |

### Defender matchups: ALL INFERRED, NONE VERIFIED, so receiving legs are CUT (P4)
**DAL receivers vs PHI DBs:**
- Quinyon Mitchell (RCB1, FP): 59 targets, 53%, 5.7 yds/target.
- Woolen: 8.4 yds/target. He moves up with J. Jones OUT.
- DeJean (NB/FS): 6.3 yds/target, 4 TDs.
- Mukuba (FS): 10.0 yds/target, 4 TDs.
- Inferred: Lamb faces DeJean in the slot and Mitchell outside. Not verified.

**PHI receivers vs DAL DBs:**
- Bland: 57 targets, 8.7 yds/target, 5 TDs, but only 57% snaps L3.
- Durant (RCB1): 9.3. Porter (LCB1): no PFR row with 8+ targets (UNKNOWN). Caleb Downs (NB): 78% completions, 8.6.
- Thompson (S, questionable, back from IR) adds depth.

### Coverage profile
- StatRankings primary; Sharp cross-check (see Breakdown).
- Per-route splits by coverage: MISSING (paywalled).

### Pressure and blitz
- DAL blitzes 25.1% (#27); Milton is F with no blitz. PHI blitzes 26.5% (#25); Dak's protection grade is A.
- **D-line weak spots:**
  - PHI: Ebiketie OUT; Carter has 85% snaps.
  - DAL: Booker (G) OUT, which hurts the interior OL. Not D-line, but it matters for Javonte.

## Opportunity and volume table
Packet opportunity layer (dashboard `opportunity`, built Nov 25 6:32 PM ET from nflverse PBP through W11/12). Label is my read from packet inputs: EXPANDING = L3 share ≥ window +3 pts; SHRINKING = L3 ≤ window −3 pts or role split cutting carries; EFFICIENCY-DRIVEN = yards/target or YPC well above the position norm on thin volume (<5 tgt / <12 car); else VOLUME-SUPPORTED. Packet model medians are research numbers, not edges.

| Player | Tm | Pos | Team att (pass/rush) | Share window / L3 / used | Proj tgt or car (mean) | Proj yds median [p25–p75] | FD line | Packet P(over line) | Last-5 yds (tgt/car) | Label (my read) | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Makai Lemon | PHI | WR | 33.5/25.9 | 20.8% / 24.4% / 20.0% | 6.0 | 34.6 [18–55] | 29.5 | 0.58 | 19(6), 67(8), 57(9), 61(9), 3(3) | OPPORTUNITY EXPANDING | — |
| Dallas Goedert | PHI | TE | 33.5/25.9 | 17.5% / 12.8% / 13.1% | 3.9 | 20.9 [9–37] | 30.5 | 0.33 | 61(8), 48(7), 30(4), 50(6), 38(1) | SHRINKING | — |
| DeVonta Smith | PHI | WR | 33.5/25.9 | 37.8% / 37.8% / 32.2% | 9.5 | 56.4 [33–85] | 63.5 | 0.45 | 65(8), 75(14), 41(12) | VOLUME-SUPPORTED | LOW-SAMPLE (≤3 logged games; packet roster-move/role artefact risk) |
| Darius Cooper | PHI | WR | 33.5/25.9 | 15.1% / 22.1% / 15.9% | 4.7 | 28.3 [12–50] | 30.5 | 0.47 | 9(2), 17(3), 19(6), 25(8), 59(5) | OPPORTUNITY EXPANDING | — |
| Elijah Mitchell | PHI | RB | 33.5/25.9 | 14.3% / 14.3% / 11.9% | 3.5 | 14.9 [6–27] | n/a | — | 23(4), 3(6), 20(4) | VOLUME-SUPPORTED | LOW-SAMPLE (≤3 logged games; packet roster-move/role artefact risk) |
| Saquon Barkley | PHI | RB | 33.5/25.9 | 50.0% / 63.2% / 49.3% | 10.9 | 42.2 [24–67] | 64.5 | — | 8(2), 62(7), 30(13), 22(13), 75(17) | OPPORTUNITY EXPANDING | <60% used share → carry-share DNP rule (Rico 60%) |
| Dameon Pierce | PHI | RB | 33.5/25.9 | 68.5% / 68.5% / 61.0% | 13.3 | 46.9 [30–69] | n/a | — | 14(11), 35(12), 47(14) | SHRINKING | LOW-SAMPLE (≤3 logged games; packet roster-move/role artefact risk) |
| Elijah Mitchell | PHI | RB | 33.5/25.9 | 25.0% / 25.0% / 22.3% | 5.3 | 16.1 [7–32] | n/a | — | 11(3), 34(11), 6(3) | VOLUME-SUPPORTED | LOW-SAMPLE (≤3 logged games; packet roster-move/role artefact risk); <60% used share → carry-share DNP rule (Rico 60%) |
| Tank Bigsby | PHI | RB | 33.5/25.9 | 53.8% / 53.8% / 48.0% | 10.5 | 41.4 [24–65] | n/a | — | 55(14) | SHRINKING | LOW-SAMPLE (≤3 logged games; packet roster-move/role artefact risk); <60% used share → carry-share DNP rule (Rico 60%) |
| CeeDee Lamb | DAL | WR | 38.4/29.1 | 35.0% / 35.3% / 36.7% | 12.5 | 84.8 [54–126] | 87.5 | 0.49 | 74(12), 58(11), 195(16), 72(13), 132(12) | VOLUME-SUPPORTED | — |
| George Pickens | DAL | WR | 38.4/29.1 | 23.6% / 29.1% / 26.8% | 9.0 | 68.7 [35–114] | 68.5 | 0.51 | 73(11), 57(6), 48(4), 145(18), 102(10) | OPPORTUNITY EXPANDING | — |
| Ryan Flournoy | DAL | WR | 38.4/29.1 | 12.0% / 9.5% / 11.5% | 4.0 | 30.0 [13–55] | 29.5 | 0.51 | 70(4), 38(4), 53(3), 71(7), 11(1) | VOLUME-SUPPORTED | — |
| Javonte Williams | DAL | RB | 38.4/29.1 | 72.5% / 68.4% / 70.8% | 17.1 | 62.0 [42–88] | 76.5 | — | 155(25), 56(24), 101(20), 63(16), 67(18) | SHRINKING | — |
| Tyler Goodson | DAL | RB | 38.4/29.1 | 24.3% / 28.2% / 25.8% | 6.6 | 20.8 [9–38] | n/a | — | 12(3), 0(2), 38(10), 14(7), 77(12) | OPPORTUNITY EXPANDING | <60% used share → carry-share DNP rule (Rico 60%) |

Sim-based low/mid/high tables (p10/median/p90) from the 4:01 AM run are in `../2026-11-26_W12_THANKSGIVING/PHI@DAL/REPORT.md`. Where packet and sim disagree, both are shown in Projections; a disagreement is a no-edge flag, not an overrule of Rico's reads.

## 80-yard / explosive watch (WATCH only, never a pick)
Watch block source: `dashboard/data/2026_12_PHI_DAL.json` @ main 2b33647, `generated_utc` Nov 25 6:31 PM ET, board_built Nov 25 6:32 PM ET. Prices: FD rungs from `pregame/direct_lines/2026_12_PHI_DAL.json` retrieved Nov 26 3:17 AM ET (repo file; Odds API credits spent: 0). Live DK/FD website check from box: DraftKings public endpoint returned HTTP 403 Access Denied (not bypassed) → MISSING; FanDuel site not separately fetched (repo direct pull used).

- PHI_vs_DAL: defense 80+ games allowed rank 24/32, explosive-plays-allowed rank 8/32 (1 = best defense); implied pts 19.5
- DAL_vs_PHI: defense 80+ games allowed rank 17/32, explosive-plays-allowed rank 13/32 (1 = best defense); implied pts 28.5

| Player | Tm | Type | ★ | p80 | p100 | Tgt/Car | YPG | Style | Why (model) | Blend | FD 79.5 (now) BE | Blend−BE | FD 99.5 (now) BE | Dash book80 (Nov 25 6:26 PM ET) | Def gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DeVonta Smith | PHI | rec | 1 | 0.296 | 0.163 | 9.8 | 60.3 | volume | tier B receiver: 11.3 targets and 60 yards a game; 9.8 projected targets; team only expected to score 20; a teammate's absence add | 0.333 | +168 / 37.3% | -4.0 pts | +320 / 23.8% | +168 / 37.3% | soft #29 (176.8 vs 148.4) |
| CeeDee Lamb | DAL | rec | 3 | 0.627 | 0.474 | 14.2 | 99.9 | explosive | alpha receiver: 13.5 targets and 100 yards a game; 14.2 projected targets; team expected to score 28; offense averaging 282 passin | 0.620 | -172 / 63.2% | -1.2 pts | +126 / 44.2% | -158 / 61.2% | soft #30 (184.5 vs 148.4) |
| George Pickens | DAL | rec | 2 | 0.490 | 0.311 | 10.5 | 90.0 | explosive | alpha receiver: 9.3 targets and 90 yards a game; 10.5 projected targets; team expected to score 28; offense averaging 282 passing  | 0.457 | +136 / 42.4% | +3.3 pts | +270 / 27.0% | +136 / 42.4% | soft #30 (184.5 vs 148.4) |
| Javonte Williams | DAL | rush | 2 | 0.404 | 0.253 | 18.1 | 73.8 | — | 18.1 carries a game; favored by about 9 | 0.452 | +100 / 50.0% | -4.8 pts | +220 / 31.2% | +100 / 50.0% | middle #20 (100.9 vs 92.7) |

**Multi-book view (every reachable book at 0 credits).** Only FanDuel posts the 79.5 / 99.5 alt rungs in the repo feeds; DK, Pinnacle, BetMGM, BetRivers, Fanatics, bet365-style feeds carry the MAIN line only. A non-FD book is shown at an 80+ rung only if its main line is exactly 79.5 (or 99.5); otherwise 80+ = MISSING. Main-line Over price/BE shown so line disagreement is visible. Flag = any book ≥5 implied pts off the others at the same line, or lines ≥2 yds apart.

| Player | Book | Main line | Over (BE) | Under (BE) | 80+ rung | 100+ rung | Flag |
|---|---|---|---|---|---|---|---|
| DeVonta Smith | fanduel | 63.5 | -113 (53.1%) | -113 (53.1%) | FD +168 | FD +320 | lines span 3y ex-bovada |
| DeVonta Smith | draftkings | 64.5 | -114 (53.3%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| DeVonta Smith | pinnacle | 65.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| DeVonta Smith | betmgm | 66.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 3y ex-bovada |
| DeVonta Smith | betrivers | 64.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 3y ex-bovada |
| DeVonta Smith | betonlineag | 64.5 | -114 (53.3%) | -114 (53.3%) | MISSING | MISSING | lines span 3y ex-bovada |
| DeVonta Smith | bovada | 74.5 | +130 (43.5%) | -170 (63.0%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| CeeDee Lamb | fanduel | 89.5 | -113 (53.1%) | -113 (53.1%) | FD -172 | FD +126 | lines span 4y ex-bovada |
| CeeDee Lamb | fanduel | 87.5 | -113 (53.1%) | -113 (53.1%) | FD -172 | FD +126 | lines span 4y ex-bovada |
| CeeDee Lamb | draftkings | 91.5 | -110 (52.4%) | -114 (53.3%) | MISSING | MISSING | lines span 4y ex-bovada |
| CeeDee Lamb | pinnacle | 87.5 | -116 (53.7%) | -104 (51.0%) | MISSING | MISSING | lines span 4y ex-bovada |
| CeeDee Lamb | betmgm | 90.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 4y ex-bovada |
| CeeDee Lamb | betrivers | 89.5 | -114 (53.3%) | -117 (53.9%) | MISSING | MISSING | lines span 4y ex-bovada |
| CeeDee Lamb | betonlineag | 91.5 | -114 (53.3%) | -114 (53.3%) | MISSING | MISSING | lines span 4y ex-bovada |
| CeeDee Lamb | bovada | 111.5 | +170 (37.0%) | -230 (69.7%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| CeeDee Lamb | circasports | 88.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 4y ex-bovada |
| George Pickens | fanduel | 68.5 | -113 (53.1%) | -113 (53.1%) | FD +136 | FD +270 | lines span 2y ex-bovada |
| George Pickens | draftkings | 69.5 | -114 (53.3%) | -110 (52.4%) | MISSING | MISSING | lines span 2y ex-bovada |
| George Pickens | pinnacle | 68.5 | -113 (53.1%) | -107 (51.7%) | MISSING | MISSING | lines span 2y ex-bovada |
| George Pickens | betmgm | 69.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 2y ex-bovada |
| George Pickens | betrivers | 70.5 | -115 (53.5%) | -114 (53.3%) | MISSING | MISSING | lines span 2y ex-bovada |
| George Pickens | betonlineag | 69.5 | -114 (53.3%) | -114 (53.3%) | MISSING | MISSING | lines span 2y ex-bovada |
| George Pickens | bovada | 79.5 | +130 (43.5%) | -170 (63.0%) | +130 (43.5%) | MISSING | bovada alt-style skew (excluded) |
| George Pickens | circasports | 70.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 2y ex-bovada |
| Javonte Williams | fanduel | 76.5 | -113 (53.1%) | -113 (53.1%) | FD +100 | FD +220 | lines span 4y ex-bovada |
| Javonte Williams | draftkings | 73.5 | -111 (52.6%) | -113 (53.1%) | MISSING | MISSING | lines span 4y ex-bovada |
| Javonte Williams | pinnacle | 76.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 4y ex-bovada |
| Javonte Williams | betmgm | 76.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 4y ex-bovada |
| Javonte Williams | betrivers | 77.5 | -117 (53.9%) | -114 (53.3%) | MISSING | MISSING | lines span 4y ex-bovada |
| Javonte Williams | fanatics | 75.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 4y ex-bovada |
| Javonte Williams | betonlineag | 76.5 | -115 (53.5%) | -112 (52.8%) | MISSING | MISSING | lines span 4y ex-bovada |
| Javonte Williams | bovada | 93.5 | +215 (31.7%) | -295 (74.7%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| Javonte Williams | circasports | 75.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 4y ex-bovada |

**Honest record (held-out 2025-26):** 3★ hit 51%, 2★ 43%, 1★ 35%; vs FanDuel Weeks 8–9 prices starred rungs +8.7% ROI on 68 rungs (not significant); model-beats-price-by-3+ rungs −47%. Every 80+ entry = WATCH unless blend clears best-price break-even by +3 AND gates pass. A back's star never overrides the 60% carry rule; a strong 80+ read argues for keeping that player's lower alt-floor leg.

## Brainstorm (9 angles) and critical review
| # | Angle (number) | Verdict | Reason / case against |
|---|---|---|---|
| 1 | PHI offense struggles vs DAL no-blitz man/single-high (Milton F no-blitz 4.15 YPA, DAL blitz 25.1% #27) | **KEEP (direction)** | Priced: PHI team total ~19.5, ML +370 unchanged Nov 24→26; n=64 dropbacks; against: DAL D allows 28.75 pts (#29) |
| 2 | DeVonta Smith over 63.5 (sim .64, 37.8% L3 share, 14 tgt in W10) | **WEAKEN** | Packet median 56.4 [33–85], P(over) .45; Milton 53%; PHI trailing helps but Jones-out helps DAL more; P4 cut |
| 3 | Makai Lemon over 29.5 (sim .67, packet .58, L3 share 24%, EXPANDING) | **WEAKEN** | 2-3 game QB sample; P4 cut; Milton 2-3 game sample |
| 4 | Lamb 80+ (3★, p80 .627, 14.2 proj tgt, PHI WR D #30) | **KEEP as WATCH** | Fully priced (FD −172, BE 63.2% vs blend .620). Against: PHI top-quartile corner Q. Mitchell (5.7 yds/tgt) probably shadows; defender inferred |
| 5 | Pickens 80+ (2★, +3.3 vs FD, L3 share 29%, EXPANDING; Lamb/Pickens seesaw 6/4/0/18/10 tgt) | **WEAKEN** | Single book; p25–p75 35–114; held-out model-beats-price rungs lost −47%; Mitchell/Woolen coverage unverified |
| 6 | Javonte under rush 76.5 (sim .33 over) | **DROP** | §9 favorite leads → under barred; MODEL-SUSPECT −12.2 |
| 7 | Barkley rush over 64.5 (DAL run D #32) | **DROP** | Used share 49.3% (<60% rule); PHI +8.5 trails; <1 target/g, so §9 blocks rush-only |
| 8 | Dak rush over 9.5 (sim .546, +4.6) | **KEEP (thin Lean)** | PHI D allows pressure 12.3% (#29), Dak sack rate 3.4%; against: sim median 12 vs line 9.5 is a 2.5-yd edge; one non-QB-keeper game flips it |
| 9 | Roof open vs closed | **DROP** | 53°F, wind 10, 0% precip either way |
**Strongest case against:** the whole slate of PHI-negative angles is already in an −8.5 line that has not moved in 48 h and a −480 ML; our only positive signals are small QB-rush and one-book Pickens rung, both inside the model's own error.


## Market table (labels capped at Lean)
| Leg | Our fair p | Pinnacle no-vig | FD no-vig | DK | Edge pts | Best price / BE | Movement | Label | Driver | Kill-switches |
|---|---|---|---|---|---|---|---|---|---|---|
| Dak Prescott rush O9.5 | .546 (sim avg) | n/a | O .500 (−113/−113) | n/a | +4.6 | FD −113, BE 53.05% (p .546 > BE by +1.5 only) | stable | **LEAN, thin** | clean pocket, scramble/QB keeper | Line ≥11.5; Dak inactive; DAL up 20+ early |
| Barkley rush O64.5 | .546 | .506 | .500 | — | +4.6 | FD −113 | — | **CUT** (used share 49.3% <60%; §9) | — | — |
| Javonte rush U76.5 / rush+rec U89.5 | .67 / .637 | — | .500 / .502 | — | +17 / +13.5 | FD −113 / −115 | — | **CUT** (§9, MODEL-SUSPECT) | — | — |
| Lamb / Pickens / Smith / Javonte 80+ | blend .620 / .457 / .333 / .452 | MISSING | n/a (alt ladder) | MISSING | −1.2 / **+3.3** / −4.0 / −4.8 vs FD BE | FD −172 (63.2%) / +136 (42.4%) / +168 (37.3%) / +100 (50.0%) | not tracked | **WATCH** | explosive / volume | P4 defender; inactives; Milton benched |
| DAL −8.5 / PHI +8.5 | none | DAL −9: .500 (−107/−106) | −110/−110 (.500) | −8.5 −111/−108 | — | — | flat | **NO PLAY** | — | — |
| Total 47.5–48.5 | none | 48.5 O−107/U−107 (.500) | 47.5 O−120/U+100 | 48.5 −106/−113 | — | — | books 1 pt apart | **NO PLAY** | — | — |
| DAL H1 −4.5 (Pinnacle) | none | ~.507 | FD −6.5 | — | — | Pinnacle −4.5 | — | **NOT A LEG** | — | — |

### Line movement (first seen → now)
| Market | Book | Nov 24 1:11 AM ET | Nov 24 6:18 PM ET | Nov 24 10:40 PM ET | Nov 25 6:26 PM ET | 3:17 AM ET direct (Nov 26) | Net move |
|---|---|---|---|---|---|---|---|
| spread | open | — | DAL -1.5 (-115 PHI/-105 DAL) | DAL -1.5 (-115 PHI/-105 DAL) | DAL -1.5 (-115 PHI/-105 DAL) | DAL -1.5 (-115 PHI/-105 DAL) | +0 pts |
| spread | fanduel | DAL -8.5 (-120 PHI/-106 DAL) | DAL -8.5 (-113 PHI/-115 DAL) | DAL -8.5 (-113 PHI/-115 DAL) | DAL -8.5 (-113 PHI/-113 DAL) | DAL -8.5 (-110 PHI/-110 DAL) | +0 pts |
| spread | pinnacle | DAL -8.5 (-106 PHI/-106 DAL) | DAL -8.5 (-106 PHI/-106 DAL) | DAL -8.5 (-106 PHI/-106 DAL) | DAL -9 (-108 PHI/-105 DAL) | DAL -9 (-107 PHI/-106 DAL) | -0.5 pts |
| spread | draftkings | — | DAL -8.5 (-108 PHI/-111 DAL) | DAL -8.5 (-108 PHI/-111 DAL) | DAL -8.5 (-108 PHI/-111 DAL) | DAL -8.5 (-108 PHI/-111 DAL) | +0 pts |
| spread | consensus | — | DAL -8.5 (-110 PHI/-109 DAL) | DAL -8.5 (-110 PHI/-109 DAL) | DAL -8.5 (-110 PHI/-110 DAL) | DAL -8.5 (-110 PHI/-110 DAL) | +0 pts |
| total | open | — | 49.5 (O-115/U-105) | 49.5 (O-115/U-105) | 49.5 (O-115/U-105) | 49.5 (O-115/U-105) | +0 pts |
| total | fanduel | 48.5 (O-111/U-115) | 48.5 (O-106/U-120) | 48.5 (O-106/U-120) | 48.5 (O-106/U-120) | 47.5 (O-120/U+100) | -1 pts |
| total | pinnacle | 47.5 (O-108/U-106) | 48 (O-108/U-108) | 48 (O-109/U-107) | 48 (O-107/U-109) | 48.5 (O-107/U-107) | +1 pts |
| total | draftkings | — | 47.5 (O-115/U-105) | 47.5 (O-115/U-105) | 47.5 (O-116/U-103) | 48.5 (O-106/U-113) | +1 pts |
| total | consensus | — | 48.5 (O-104/U-112) | 48 (O-108/U-110) | 47.5 (O-119/U-102) | 48.5 (O-106/U-111) | +0 pts |
| moneyline | open | — | — | — | — | PHI -102 / DAL -120 | PHI ML -102→-102 |
| moneyline | fanduel | PHI +360 / DAL -460 | PHI +380 / DAL -500 | PHI +380 / DAL -500 | PHI +370 / DAL -480 | PHI +370 / DAL -480 | PHI ML +360→+370 |
| moneyline | pinnacle | PHI +337 / DAL -422 | PHI +337 / DAL -421 | PHI +337 / DAL -422 | PHI +343 / DAL -430 | PHI +345 / DAL -433 | PHI ML +337→+345 |
| moneyline | draftkings | — | PHI +363 / DAL -469 | PHI +363 / DAL -469 | PHI +370 / DAL -480 | PHI +343 / DAL -440 | PHI ML +363→+343 |
| moneyline | consensus | — | PHI +370 / DAL -477 | PHI +370 / DAL -477 | PHI +370 / DAL -480 | PHI +365 / DAL -475 | PHI ML +370→+365 |

"open" row = packet `open` feed (pipeline source, unverified; see Open items). Spread rows are home-team line; prices listed away/home. News ties: none found for the Nov 24 moves in the packet roster-move list; cannot tie to timestamped news (UNKNOWN).

### De-vig, main markets (own computation from repo direct_lines, Nov 26 3:17 AM ET)
| Market | Book | Line | Away/Over price | Home/Under price | Implied A / B | Sum | No-vig A | No-vig B | Hold |
|---|---|---|---|---|---|---|---|---|---|
| spread | fanduel | DAL -8.5 | PHI -110 | DAL -110 | 52.4% / 52.4% | 104.8% | 50.0% (PHI) | 50.0% (DAL) | 4.8% |
| spread | pinnacle | DAL -9 | PHI -107 | DAL -106 | 51.7% / 51.5% | 103.1% | 50.1% (PHI) | 49.9% (DAL) | 3.1% |
| spread | draftkings | DAL -8.5 | PHI -108 | DAL -111 | 51.9% / 52.6% | 104.5% | 49.7% (PHI) | 50.3% (DAL) | 4.5% |
| spread | betmgm | DAL -8.5 | PHI -110 | DAL -108 | 52.4% / 51.9% | 104.3% | 50.2% (PHI) | 49.8% (DAL) | 4.3% |
| spread | betrivers | DAL -8.5 | PHI -109 | DAL -110 | 52.2% / 52.4% | 104.5% | 49.9% (PHI) | 50.1% (DAL) | 4.5% |
| spread | bet365 | DAL -8.5 | PHI -109 | DAL -111 | 52.2% / 52.6% | 104.8% | 49.8% (PHI) | 50.2% (DAL) | 4.8% |
| spread | williamhill_us | DAL -8.5 | PHI -109 | DAL -110 | 52.2% / 52.4% | 104.5% | 49.9% (PHI) | 50.1% (DAL) | 4.5% |
| total | fanduel | 47.5 | Over -120 | Under +100 | 54.5% / 50.0% | 104.5% | 52.2% (Over) | 47.8% (Under) | 4.5% |
| total | pinnacle | 48.5 | Over -107 | Under -107 | 51.7% / 51.7% | 103.4% | 50.0% (Over) | 50.0% (Under) | 3.4% |
| total | draftkings | 48.5 | Over -106 | Under -113 | 51.5% / 53.1% | 104.5% | 49.2% (Over) | 50.8% (Under) | 4.5% |
| total | betmgm | 48 | Over -108 | Under -110 | 51.9% / 52.4% | 104.3% | 49.8% (Over) | 50.2% (Under) | 4.3% |
| total | betrivers | 48 | Over -108 | Under -112 | 51.9% / 52.8% | 104.8% | 49.6% (Over) | 50.4% (Under) | 4.8% |
| total | bet365 | 48.5 | Over -110 | Under -110 | 52.4% / 52.4% | 104.8% | 50.0% (Over) | 50.0% (Under) | 4.8% |
| total | williamhill_us | 48.5 | Over -107 | Under -113 | 51.7% / 53.1% | 104.7% | 49.4% (Over) | 50.6% (Under) | 4.7% |
| moneyline | fanduel | ML | PHI +370 | DAL -480 | 21.3% / 82.8% | 104.0% | 20.5% (PHI) | 79.5% (DAL) | 4.0% |
| moneyline | pinnacle | ML | PHI +345 | DAL -433 | 22.5% / 81.2% | 103.7% | 21.7% (PHI) | 78.3% (DAL) | 3.7% |
| moneyline | draftkings | ML | PHI +343 | DAL -440 | 22.6% / 81.5% | 104.1% | 21.7% (PHI) | 78.3% (DAL) | 4.1% |
| moneyline | betmgm | ML | PHI +375 | DAL -475 | 21.1% / 82.6% | 103.7% | 20.3% (PHI) | 79.7% (DAL) | 3.7% |
| moneyline | betrivers | ML | PHI +335 | DAL -455 | 23.0% / 82.0% | 105.0% | 21.9% (PHI) | 78.1% (DAL) | 5.0% |
| moneyline | bet365 | ML | PHI +360 | DAL -470 | 21.7% / 82.5% | 104.2% | 20.9% (PHI) | 79.1% (DAL) | 4.2% |
| moneyline | williamhill_us | ML | PHI +340 | DAL -460 | 22.7% / 82.1% | 104.9% | 21.7% (PHI) | 78.3% (DAL) | 4.9% |

Working: no-vig A = implied(A)/(implied(A)+implied(B)), implied(-x)=x/(x+100), implied(+x)=100/(x+100). Source direct_lines retrieved Nov 26 3:17 AM ET; per-book main line = the two-sided line whose prices are closest to even.

## Projections (market-anchored, UNVALIDATED)
| Item | Value |
|---|---|
| Score range | DAL 28.25 / PHI 19.75 (anchored to −8.5, 48); engine 49.9 −0.79 is pre-Milton so not used; range DAL 24–34, PHI 13–24 (judgment) |
| Lamb rec | packet 84.8 [54–126], sim 95 [39–174], line 87.5 |
| Pickens rec | packet 68.7 [35–114], sim 71 [23–145], line 68.5 |
| D. Smith rec | packet 56.4 [33–85], sim 78 [37–132], line 63.5 |
| Barkley rush | packet 42.2 [24–67], role-window sim ~70, line 64.5 (DNP anyway) |
| Javonte rush | packet 62.0 [42–88], sim 64 [36–101], line 76.5 |


## Open items (re-check before 4:30 PM ET)
- Inactives ~3:00 PM ET: Thompson, Moore (DAL); any PHI QB change; Mingo/Ferguson/Locke confirmations; Roof status.
- Verified defender alignments MISSING (paywalled). NGS not checked. Run-direction splits MISSING. Official roof status MISSING.
- Packet 'open' feed for this game (DAL −1.5, ML PHI −102/DAL −120) contradicts every book (−8.5, −480): UNRELIABLE, not used. True opener (Outlier/odds history) NOT CHECKED.
- Several packet RB rows (Pierce, Bigsby, E. Mitchell dup) have ≤3 logged games: LOW-SAMPLE artefacts.


## Sources and freshness
| Source | Time (ET) |
|---|---|
| Packet + dashboard watch block @ main 2b33647 | built Nov 25 6:31 PM; read Nov 26 ~9:00 AM |
| direct_lines (FD/DK/Pinnacle/BetMGM/BetRivers/Fanatics) | Nov 26 3:17 AM |
| price freezes ×4 | Nov 24 1:11 AM → Nov 25 6:26 PM |
| ESPN injuries | Nov 26 9:00 AM |
| NWS hourly (FWD grid) / Open-Meteo | 8:34 AM / 9:00 AM |
| nflverse, StatRankings, Sharp, sims | prior run 3:49–4:05 AM |


*Research only. Not validated. Not betting advice.*

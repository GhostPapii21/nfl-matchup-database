# CHI @ DET — Thu Nov 26, 2026, 1:00 PM ET, Ford Field (dome) — Thanksgiving game 1
**SCHEDULED RUN** (Blitz routine "NFL enhanced edge analysis", fired Thu Nov 26 8:58 AM ET). Research only. `projection_ready` = false → labels are research, not picks, no slips. **CHECKLIST VETTED: NO (pending Ghost6).**

| Item | Value |
|---|---|
| Packet | `pregame/packets/2026_12_CHI_DET` (repo main @ 2b33647, merged PR #133 at Nov 26 5:13 AM ET), **Updated Nov 25 6:31 PM ET** (23:31:45Z) |
| Built before final injury report? | **YES.** Packet pulled ESPN injuries 6:31 PM ET Nov 25; later designations (CHI: Gordon OUT 6:53 PM, Stevenson Q 6:56 PM, D'Marco Jackson Q 10:14 PM; DET: Rakestraw OUT 10:20 PM, Clark Q 8:04 PM, Wonnum Q 7:56 PM, Gill-Howard→IR 10:23 PM) came after. **All labels capped at Lean.** |
| Book prices | Packet: Nov 25 6:26 PM ET (direct pulls, no Odds API). Fresher: repo `direct_lines/2026_12_CHI_DET.json` Nov 26 3:17 AM ET. Odds API credits spent: 0 (reserve 950 untouched). |
| Weather | INDOOR (dome) — packet status INDOOR; no weather flag |
| Tools used | gh api (read-only contents API, no clone), ESPN injuries API (pulled 9:00 AM ET), nflverse (via prior 3:49 AM ET pull + packet), StatRankings/Sharp coverage (3:59 AM ET, prior run), sim_v6 seed 20261101 3×100k (prior 4:01 AM run outputs reused, inputs unchanged) |
| Live checks | ESPN injuries 9:00 AM ET; **NFL.com inactives NOT YET POSTED** (due ~11:30 AM ET); DraftKings public site → HTTP 403 (not bypassed) |


## Five-line summary
1. **Script:** close, high-tempo dome game (CHI −1.5 / DET +1.5, total 55.5–56). Both run D's are walls (DET #1 RB rush allowed 59.8, CHI #7), so volume goes through the air and Gibbs/Caleb are the swing legs.
2. **Market move:** DET +2.5 → +1.5 (FD/DK; Pinnacle +1) and CHI ML −146 → −122 since Nov 24 1:11 AM ET; total flat 55.5. The money came before the late CB injuries (Rakestraw/Gordon), so those are priced in the 3:17 AM lines.
3. **Only surviving edge (Lean):** Caleb Williams rush UNDER 22.5 (model p .695 vs no-vig .50; median 14; last-5 rush yds 3/18/1/16/11). Everything else = WATCH/manual review/cut.
4. **80+ watch:** Gibbs 3★ (p80 .471), St. Brown 2★ (.383), Burden 1★ (.327). None clears best-price break-even by +3 (Gibbs −9.2, St. Brown −9.0, Burden −0.6). The sim says Gibbs 80+ is .755 but the watch model says .471: the two internal models disagree by 28 pts, so no edge.
5. **Cuts:** Swift/Monangai (used share 45%/31% < 60% rule), every receiving leg (no verified defender), all passing yards, spread/total/ML (no validated engine).


## Game script
| Scenario | Prob (judgment) | Flow |
|---|---|---|
| **Base** trade scores | ~50% | CHI blitzes 35.9% into Goff (A vs blitz); DET balanced, Gibbs 20+ carries; one-score game into Q4 |
| **Flip A** CHI leads early | ~30% | CHI no-blitz offense (Caleb 8.65 YPA, A) beats DET single-high 57%; DET passes more, St. Brown/Gibbs targets up, Gibbs rush capped |
| **Flip B** DET leads by 10+ | ~20% | CHI pass-heavy, Swift/Monangai carries drop, Gibbs 25+ carries |
Period lean: none (FD Q1 10.5 and H1 27.5 priced; no model, the M2 total method failed validation: MAE 11.22 vs close 9.88).


## Breakdown
### Injuries and depth (ESPN API pulled Nov 26 9:00 AM ET; newest entry 10:23 PM ET Nov 25)
| Team | OUT / IR | Questionable | Matters because |
|---|---|---|---|
| CHI | CB Kyler Gordon (nickel) OUT; RB Roschon Johnson OUT | CB Tyrique Stevenson (groin), LB D'Marco Jackson (elbow) | slot CB thin vs St. Brown; Johnson out does not change Swift/Monangai split |
| DET | CB Ennis Rakestraw OUT; DT Skyler Gill-Howard IR; **C Cade Mays IR (since Nov 22)** | S Chuck Clark (hamstring), DE/LB DJ Wonnum (back) | CB2 + interior DL thin; backup center vs CHI's #2 sack rate (9.5%) |
Missing ≠ healthy: players not on the ESPN list are UNKNOWN until inactives (~11:30 AM ET). Rico rule: Questionable cleared/cut at inactives.

#### Carried from the 4:01 AM manual run (same packet; sims seed 20261101, 3×100k, prior-run numbers; RB share tables there used a 50% cut: **the saved 60%-of-carries rule now applies and is stricter**)

### Breakdown
**CHI offense (Caleb Williams):**
- Caleb card (FTN, 2026): faces blitz 49% of dropbacks. Vs blitz 7.15 YPA, 59% completions (C). No blitz 8.65 YPA (A). Sack rate 6.8% (C), 3rd/4th-down conversions 42% (B).
- **DET defense:** StatRankings man 38.2% (#10), zone 59.2%, single-high 57.4% (#10), blitz 29.8% (#19). Sharp cross-check: man 20.3 / zone 74.8 / MOF-closed 48.5. The two disagree on man level, so this is **SHARP CAUTION**; StatRankings is primary.
- DET allowed 18.6 points (#5) and 59.8 RB rush yds (#1, YPC 3.42), but 69 TE yds (#29). This is the Loveland angle. His prop is 52.5 against a median of 37, so the model does not like the over.
- DET pass rush: Hutchinson 27 pressures (52% snaps L3, managed load), McNeill 16, Wonnum 12 (questionable), Gill-Howard OUT.
- **Weak spot:** DT depth without Gill-Howard, plus RCB2 with Rakestraw out. Ya-Sin starts RCB, Dorsey is LCB2.

**DET offense (Goff):**
- Goff card: vs blitz 8.36 YPA, 71.6% completions (A). No blitz 8.08 (B). Sack rate 6.2% (B).
- **CHI defense:** StatRankings man 35.1% (#14), zone 64.3%, blitz 35.9% (#11). Sharp: man 25.6 / zone 69.9.
- CHI allowed 18.9 points (#6), RB rush 70.9 (#7), YPC 4.13. Sack rate 9.5% (#2), packet blitz 33%.
- CHI pressure: Sweat 17, Booker 14, Jarrett 9.
- Secondary: Gordon OUT, Hicks OUT, Stevenson questionable. If Stevenson sits, Phillips/Muhammad play more. Muhammad allows 8.8 yds/target.
- Goff's blitzed target tree goes heavier to St. Brown (34% blitzed vs 27% non-blitzed) and LaPorta (22% vs 16%). CHI blitzes a lot, which supports St. Brown volume. The sim median is 72 vs a line of 82.5, so it does not support the yardage over.

**Receiver seesaw:**
- DET: St. Brown / LaPorta / J. Williams / Gibbs all sit at 15–24% L3 shares. Williams and TeSlaa trade deep targets.
- CHI: Burden 23.4 / Loveland 19.1 / Odunze 18.1 / Raymond 14.9 L3. Roughly a 4-way split, so there is no alpha to lean on.

**RB run direction:**
- Gibbs: 4.95 YPC season against CHI's 4.13 YPC allowed. DET OL direction splits were not computed (MISSING).
- Red zone: CHI defense RZ TD% is in the packet. DET's 28.3 points per game come mostly from RZ efficiency.

**Opponent box-score context:**
- DET went under the closing total in 4 of its last 5.
- CHI scores and closing totals are in team_games_2026_out.txt.

### RB carry share and the 50% rule (any RB projected under 50% of team carries = DO NOT PLAY)
| RB | Season share | L3 | By game (last 5) | Verdict |
|---|---|---|---|---|
| Gibbs | 75.8% | 71.4% | .88/.59/.71/.65/.79 | PASS |
| Vaki | 12.6% | 11.0% | — | DNP |
| Swift | 50.0% | 57.8% | .48/.73/.77/.55/.39 | **DNP**: 39% in W11, the only game with Monangai active; 44% average when both played |
| Monangai | 20.2% | — | 24% in W11 | **DNP** |

### Defender matchups: ALL INFERRED, NONE VERIFIED
Who covers whom is not in any free source (no shadow/alignment data; the StatRankings alignment tables are paywalled). Every receiving leg is therefore **MISSING the main defender → CUT (P4)**.

**DET receivers vs CHI DBs** (PFR 2026 coverage, depth chart dated 2:01 AM ET today):
- Jaylon Johnson (LCB1): 49 targets, 69% completions, 11.2 yds/target. He has been beaten.
- Stevenson (RCB1, questionable): 8.9 yds/target, 4 TDs allowed.
- Gordon (NB) OUT, so Blackwell (NB2) likely covers the slot. Inferred: St. Brown sees Blackwell often.
- Safeties: Thieneman 6.0 yds/target; Cam Lewis 9.6, 3 TDs.

**CHI receivers vs DET DBs:**
- McCreary (NB): 63 targets, 7.4 yds/target, 4 TDs. Inferred: Burden in the slot.
- Ya-Sin: 5.0 yds/target. D.J. Reed: 9.1. Clark (S, questionable): 4.8.
- LB coverage: Campbell 8.2 yds/target, 4 TDs, which matters for Loveland.

### Coverage profile
- StatRankings is primary, from the free headline rates only. Sharp is a cross-check and is not mixed in. Details under Breakdown.
- Splits by coverage (yds/route vs man/zone) are paywalled, so those are **MISSING**.

### Pressure and blitz
- CHI defense blitzes 35.9% (StatRankings #11); packet sack rate 9.5% (#2). Goff vs blitz: A.
- DET defense blitzes 29.8% (#19). Caleb vs blitz: C, vs no blitz: A, so DET's lower blitz rate helps Caleb.
- **DL weak spots:**
  - DET without Gill-Howard (DT) has less interior depth.
  - CHI's pass rush is Sweat (73% snaps) and Booker.

## Opportunity and volume table
Packet opportunity layer (dashboard `opportunity`, built Nov 25 6:32 PM ET from nflverse PBP through W11/12). Label is my read from packet inputs: EXPANDING = L3 share ≥ window +3 pts; SHRINKING = L3 ≤ window −3 pts or role split cutting carries; EFFICIENCY-DRIVEN = yards/target or YPC well above the position norm on thin volume (<5 tgt / <12 car); else VOLUME-SUPPORTED. Packet model medians are research numbers, not edges.

| Player | Tm | Pos | Team att (pass/rush) | Share window / L3 / used | Proj tgt or car (mean) | Proj yds median [p25–p75] | FD line | Packet P(over line) | Last-5 yds (tgt/car) | Label (my read) | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Luther Burden III | CHI | WR | 31.5/32.1 | 22.1% / 24.4% / 23.2% | 6.5 | 47.8 [27–75] | 60.5 | 0.40 | 95(8), 130(4), 56(9), 97(10), 10(3) | VOLUME-SUPPORTED | — |
| Colston Loveland | CHI | TE | 31.5/32.1 | 21.3% / 20.0% / 21.0% | 5.8 | 38.5 [21–61] | 52.5 | 0.36 | 65(7), 69(12), 65(9), 54(6), 29(3) | VOLUME-SUPPORTED | — |
| Rome Odunze | CHI | WR | 31.5/32.1 | 18.6% / 18.9% / 18.9% | 5.3 | 37.9 [19–62] | 47.5 | 0.42 | 39(4), 69(5), 87(6), 60(7), 45(4) | VOLUME-SUPPORTED | — |
| Kalif Raymond | CHI | WR | 31.5/32.1 | 12.0% / 15.6% / 13.5% | 3.8 | 19.6 [7–36] | 25.5 | 0.40 | 18(2), 0(2), 14(3), 32(7), 14(4) | OPPORTUNITY EXPANDING | — |
| D'Andre Swift | CHI | RB | 31.5/32.1 | 56.1% / 65.8% / 45.1% | 12.2 | 34.2 [19–54] | 46.5 | — | 44(16), 78(22), 69(27), 31(12), 51(13) | SHRINKING | teammate-out bump +5.1pts; <60% used share → carry-share DNP rule (Rico 60%) |
| Kyle Monangai | CHI | RB | 31.5/32.1 | 43.2% / 43.2% / 31.0% | 8.5 | 23.5 [10–44] | 34.5 | — | 31(10), 146(30), 18(8) | SHRINKING | LOW-SAMPLE (≤3 logged games; packet roster-move/role artefact risk); <60% used share → carry-share DNP rule (Rico 60%) |
| Amon-Ra St. Brown | DET | WR | 29.3/28.2 | 27.8% / 24.7% / 26.5% | 6.9 | 52.6 [31–83] | 82.5 | 0.26 | 153(11), 46(8), 86(10), 98(5), 37(6) | SHRINKING | — |
| Jahmyr Gibbs | DET | RB | 29.3/28.2 | 17.9% / 16.5% / 17.3% | 4.5 | 22.3 [10–40] | 35.5 | 0.33 | 27(6), 15(4), 0(1), 99(8), 20(5) | VOLUME-SUPPORTED | — |
| Jameson Williams | DET | WR | 29.3/28.2 | 17.5% / 15.3% / 16.6% | 4.3 | 38.6 [17–67] | 57.5 | 0.35 | 91(9), 70(6), 31(2), 50(7), 93(4) | EFFICIENCY-DRIVEN | — |
| Sam LaPorta | DET | TE | 29.3/28.2 | 17.5% / 17.6% / 17.5% | 4.5 | 27.8 [11–51] | 44.5 | 0.34 | 18(2), 33(5), 32(5), 16(4), 62(6) | VOLUME-SUPPORTED | — |
| Jahmyr Gibbs | DET | RB | 29.3/28.2 | 79.0% / 79.3% / 79.1% | 18.4 | 82.7 [58–114] | 92.5 | — | 116(29), 153(23), 74(20), 153(22), 98(23) | VOLUME-SUPPORTED | — |

Sim-based low/mid/high tables (p10/median/p90) from the 4:01 AM run are in `../2026-11-26_W12_THANKSGIVING/CHI@DET/REPORT.md`. Where packet and sim disagree, both are shown in Projections; a disagreement is a no-edge flag, not an overrule of Rico's reads.

## 80-yard / explosive watch (WATCH only, never a pick)
Watch block source: `dashboard/data/2026_12_CHI_DET.json` @ main 2b33647, `generated_utc` Nov 25 6:31 PM ET, board_built Nov 25 6:32 PM ET. Prices: FD rungs from `pregame/direct_lines/2026_12_CHI_DET.json` retrieved Nov 26 3:17 AM ET (repo file; Odds API credits spent: 0). Live DK/FD website check from box: DraftKings public endpoint returned HTTP 403 Access Denied (not bypassed) → MISSING; FanDuel site not separately fetched (repo direct pull used).

- CHI_vs_DET: defense 80+ games allowed rank 18/32, explosive-plays-allowed rank 11/32 (1 = best defense); implied pts 28.5
- DET_vs_CHI: defense 80+ games allowed rank 15/32, explosive-plays-allowed rank 18/32 (1 = best defense); implied pts 27.0

| Player | Tm | Type | ★ | p80 | p100 | Tgt/Car | YPG | Style | Why (model) | Blend | FD 79.5 (now) BE | Blend−BE | FD 99.5 (now) BE | Dash book80 (Nov 25 6:26 PM ET) | Def gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Luther Burden III | CHI | rec | 1 | 0.327 | 0.175 | 7.5 | 69.9 | explosive | tier B receiver: 7.1 targets and 70 yards a game; team expected to score 28; a teammate's absence adds targets | 0.334 | +194 / 34.0% | -0.6 pts | +390 / 20.4% | +194 / 34.0% | tough #9 (134.1 vs 148.4) |
| Rome Odunze | CHI | rec | 0 | 0.232 | 0.107 | 6.1 | 59.8 | explosive | team expected to score 28; a teammate's absence adds targets | 0.241 | +300 / 25.0% | -0.9 pts | +580 / 14.7% | +300 / 25.0% | tough #9 (134.1 vs 148.4) |
| Amon-Ra St. Brown | DET | rec | 2 | 0.383 | 0.229 | 8.3 | 72.9 | volume | alpha receiver: 8.8 targets and 73 yards a game; team expected to score 27; the FanDuel price moves this from 1 to 2 stars; model  | 0.471 | -128 / 56.1% | -9.0 pts | +174 / 36.5% | -128 / 56.1% | middle #20 (152.8 vs 148.4) |
| Jahmyr Gibbs | DET | rush | 3 | 0.471 | 0.355 | 21.9 | 111.2 | — | 21.9 carries a game; the FanDuel price moves this from 2 to 3 stars; model 47% vs FanDuel 66%: a big disagreement, check the QB an | 0.568 | -194 / 66.0% | -9.2 pts | +116 / 46.3% | -194 / 66.0% | tough #7 (70.9 vs 92.7) |

**Multi-book view (every reachable book at 0 credits).** Only FanDuel posts the 79.5 / 99.5 alt rungs in the repo feeds; DK, Pinnacle, BetMGM, BetRivers, Fanatics, bet365-style feeds carry the MAIN line only. A non-FD book is shown at an 80+ rung only if its main line is exactly 79.5 (or 99.5); otherwise 80+ = MISSING. Main-line Over price/BE shown so line disagreement is visible. Flag = any book ≥5 implied pts off the others at the same line, or lines ≥2 yds apart.

| Player | Book | Main line | Over (BE) | Under (BE) | 80+ rung | 100+ rung | Flag |
|---|---|---|---|---|---|---|---|
| Luther Burden III | fanduel | 60.5 | -113 (53.1%) | -113 (53.1%) | FD +194 | FD +390 | lines span 3y ex-bovada |
| Luther Burden III | draftkings | 60.5 | -113 (53.1%) | -111 (52.6%) | MISSING | MISSING | lines span 3y ex-bovada |
| Luther Burden III | pinnacle | 60.5 | -118 (54.1%) | -103 (50.7%) | MISSING | MISSING | lines span 3y ex-bovada |
| Luther Burden III | betmgm | 59.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 3y ex-bovada |
| Luther Burden III | betrivers | 62.5 | -114 (53.3%) | -117 (53.9%) | MISSING | MISSING | lines span 3y ex-bovada |
| Luther Burden III | fanatics | 60.5 | -120 (54.5%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Luther Burden III | betonlineag | 60.5 | -118 (54.1%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Luther Burden III | bovada | 70.5 | +135 (42.6%) | -180 (64.3%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| Luther Burden III | circasports | 62.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Rome Odunze | fanduel | 47.5 | -113 (53.1%) | -113 (53.1%) | FD +300 | FD +580 | lines span 3y ex-bovada |
| Rome Odunze | draftkings | 46.5 | -114 (53.3%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Rome Odunze | pinnacle | 49.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Rome Odunze | betmgm | 49.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 3y ex-bovada |
| Rome Odunze | betrivers | 49.5 | -114 (53.3%) | -117 (53.9%) | MISSING | MISSING | lines span 3y ex-bovada |
| Rome Odunze | betonlineag | 46.5 | -116 (53.7%) | -111 (52.6%) | MISSING | MISSING | lines span 3y ex-bovada |
| Rome Odunze | bovada | 56.5 | +140 (41.7%) | -185 (64.9%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| Rome Odunze | circasports | 47.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Amon-Ra St. Brown | fanduel | 82.5 | -113 (53.1%) | -113 (53.1%) | FD -128 | FD +174 | lines span 2y ex-bovada |
| Amon-Ra St. Brown | draftkings | 83.5 | -110 (52.4%) | -114 (53.3%) | MISSING | MISSING | lines span 2y ex-bovada |
| Amon-Ra St. Brown | pinnacle | 83.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 2y ex-bovada |
| Amon-Ra St. Brown | betmgm | 84.5 | -105 (51.2%) | -125 (55.6%) | MISSING | MISSING | lines span 2y ex-bovada |
| Amon-Ra St. Brown | betrivers | 84.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 2y ex-bovada |
| Amon-Ra St. Brown | betonlineag | 83.5 | -114 (53.3%) | -114 (53.3%) | MISSING | MISSING | lines span 2y ex-bovada |
| Amon-Ra St. Brown | bovada | 103.5 | +175 (36.4%) | -240 (70.6%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| Amon-Ra St. Brown | circasports | 82.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 2y ex-bovada |
| Jahmyr Gibbs | fanduel | 92.5 | -113 (53.1%) | -113 (53.1%) | FD -194 | FD +116 | lines span 3y ex-bovada |
| Jahmyr Gibbs | draftkings | 93.5 | -111 (52.6%) | -113 (53.1%) | MISSING | MISSING | lines span 3y ex-bovada |
| Jahmyr Gibbs | pinnacle | 92.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Jahmyr Gibbs | betmgm | 91.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 3y ex-bovada |
| Jahmyr Gibbs | betrivers | 93.5 | -114 (53.3%) | -117 (53.9%) | MISSING | MISSING | lines span 3y ex-bovada |
| Jahmyr Gibbs | betonlineag | 92.5 | -114 (53.3%) | -114 (53.3%) | MISSING | MISSING | lines span 3y ex-bovada |
| Jahmyr Gibbs | bovada | 113.5 | +200 (33.3%) | -275 (73.3%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| Jahmyr Gibbs | circasports | 90.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |

**Honest record (held-out 2025-26):** 3★ hit 51%, 2★ 43%, 1★ 35%; vs FanDuel Weeks 8–9 prices starred rungs +8.7% ROI on 68 rungs (not significant); model-beats-price-by-3+ rungs −47%. Every 80+ entry = WATCH unless blend clears best-price break-even by +3 AND gates pass. A back's star never overrides the 60% carry rule; a strong 80+ read argues for keeping that player's lower alt-floor leg.

## Brainstorm (10 angles) and critical review
| # | Angle (number that prompted it) | Verdict | Reason / case against |
|---|---|---|---|
| 1 | Caleb rush UNDER 22.5 (L5 rush yds 3/18/1/16/11, sim median 14, p .695) | **KEEP (Lean)** | Against: one 30-yd scramble beats it (sim p90 38); close games and DET single-high (57%) invite scrambles. Rico rule: rush unders are the one historically gated market; held-out "model beats price by 3+" rungs lost −47% ROI, so size small |
| 2 | Gibbs rush O92.5 / 79.5+ floor (sim .627/.755, 79% share, 29/23/20/22/23 carries L5) | **WEAKEN → MANUAL_REVIEW** | Against: CHI #7 RB D; packet opportunity median only 82.7 yds (18.4 car) and watch p80 .471 vs sim .755; sim_v6 runs +12 on lead RBs (DEBUG_LOG item 3) |
| 3 | Gibbs receiving over 35.5 (research reads lean) | **DROP** | Packet median 22.3 [10–40]; model P(over) .33; one-source lean |
| 4 | J. Williams over 57.5 (reads: WR2 vs CHI WR2 leak) | **DROP** | Sim median 46, packet 38.6, EFFICIENCY-DRIVEN (4.3 tgt); both models under the line; no verified defender |
| 5 | Loveland UNDER 52.5 / under 5.5 rec (DET TE allowed 69.1 yds #29 says over; model says under) | **WEAKEN** | TE leak is season-long, last game 29 yds on 3 tgt; model P(over) .30–.36; P4 cut. Against: the TE leak is real (#29) |
| 6 | Late CB injuries (Rakestraw, Gordon) → pass-heavy, receivers up | **WEAKEN** | Already priced: props pulled 3:17 AM after both designations; passing yards never a leg; no verified defender |
| 7 | DET backup C (Mays IR) vs CHI sack rate #2 and 35.9% blitz | **KEEP (risk note)** | Goff is A vs blitz (8.36 YPA, 71.6%) and DET sack rate allowed 6.1%; no leg, but lowers DET-side confidence |
| 8 | Total 55.5 under/over (DET under 4 of last 5, CHI led at half 8 of 10) | **DROP** | No validated total model (M2 corr −0.046); market flat at 55.5 |
| 9 | CHI RB timeshare (Swift 45% used, Monangai 31%) unders | **DROP** | <60% used-share DNP rule; Monangai 146 yds in one game = one long run |
| 10 | Thanksgiving short week / division / dome | **DROP** | Both 4 days rest, same trip; no measurable edge in packet |
**Strongest case against the overall read:** the market has already moved a full point toward DET, our only edge is a rushing under on a QB with a 6.8% sack rate and an 8.5-yd gap built on a 5-game log; the held-out record says model-beats-price rungs lose money.


## Market table (labels capped at Lean: packet pre-dates final injury report)
| Leg | Our fair p (source) | Pinnacle no-vig | FD no-vig | DK | Edge pts | Best price / break-even | Movement | Label | Driver | Kill-switches |
|---|---|---|---|---|---|---|---|---|---|---|
| **Caleb Williams rush U22.5** | .695 (sim mc .699/bias .693/gr .694; seed 20261101; baseline = 3-model median 14) | U .487 (O-116/U-104) | U .500 (−113/−113) | n/a | **+20.8 vs Pinn / +19.5 vs FD** (flag: >+3) | FD U −113, BE 53.05% (Pinnacle −104 BE 50.98%, sharp-ref). p .695 > BE → +EV by model only | line 22.5 stable in packet | **LEAN (research)** | rushing role decline + spy look | Line ≤19.5 (reprice); designed-run news; Caleb 30+ yd scramble early; inactive news; inactives ~11:30 AM |
| Gibbs rush O92.5 | .627 sim / packet median 82.7 | O .491 | .500 | O92.5 −114 | +12.7 sim / −7 packet | FD −113 (BE 53.05%); Circa 90.5 | line 92.5 FD/DK/Pinn | **WATCH, MANUAL_REVIEW** (MODEL-SUSPECT +12.4) | volume (79% share) | Inactives, Gibbs snap news |
| Gibbs alt 79.5+ / 69.5+ | .755 / .839 sim; watch p80 .471 | — | .622 / .713 | n/a | +13.3 / +12.6 sim; −9.2 vs watch blend | FD −194 (BE 66.0%) / −310 | — | **WATCH** | alt floor | same |
| Burden/Odunze/St. Brown 80+ | blend .334/.241/.471 | MISSING | — | MISSING | −0.6/−0.9/−9.0 | FD +194 (34.0%) / +300 (25.0%) / −128 (56.1%) | — | **WATCH** | explosive | P4 defender missing |
| Spread CHI −1.5 / ML CHI −122 | none | DET +1 −104/CHI −108 (ref) ; ML CHI .526 | spread .500 | DET +1.5 −113/CHI −106 | — | — | −1 pt toward DET | **NO PLAY** | no engine | — |
| Total 55.5 | none | O .495/U .504 at 55.5 (packet); line 56 at 3:17 AM | O .504 | O .488 (packet) | — | — | flat | **NO PLAY** | — | — |

### Line movement (first seen → now)
| Market | Book | Nov 24 1:11 AM ET | Nov 24 6:18 PM ET | Nov 24 10:40 PM ET | Nov 25 6:26 PM ET | 3:17 AM ET direct (Nov 26) | Net move |
|---|---|---|---|---|---|---|---|
| spread | open | — | DET -2.5 (-105 CHI/-115 DET) | DET -2.5 (-105 CHI/-115 DET) | DET -2.5 (-105 CHI/-115 DET) | DET -2.5 (-105 CHI/-115 DET) | +0 pts |
| spread | fanduel | DET +2.5 (-120 CHI/-106 DET) | DET +2.5 (-115 CHI/-111 DET) | DET +1.5 (-118 CHI/-108 DET) | DET +1.5 (-113 CHI/-113 DET) | DET +1.5 (-108 CHI/-112 DET) | -1 pts |
| spread | pinnacle | DET +2.5 (-109 CHI/-103 DET) | DET +2 (-108 CHI/-105 DET) | DET +1 (-109 CHI/-105 DET) | DET +1.5 (-105 CHI/-108 DET) | DET +1 (-108 CHI/-104 DET) | -1.5 pts |
| spread | draftkings | — | DET +2.5 (-108 CHI/-111 DET) | DET +1.5 (-107 CHI/-112 DET) | DET +1.5 (-106 CHI/-113 DET) | DET +1.5 (-106 CHI/-113 DET) | -1 pts |
| spread | consensus | — | DET +2.5 (-111 CHI/-108 DET) | DET +1.5 (-107 CHI/-111 DET) | DET +1.5 (-109 CHI/-110 DET) | DET +1.5 (-109 CHI/-111 DET) | -1 pts |
| total | open | — | 53.5 (O-110/U-110) | 53.5 (O-110/U-110) | 53.5 (O-110/U-110) | 53.5 (O-110/U-110) | +0 pts |
| total | fanduel | 55.5 (O-108/U-118) | 54.5 (O-122/U-104) | 55.5 (O-108/U-118) | 55.5 (O-115/U-111) | 55.5 (O-112/U-108) | +0 pts |
| total | pinnacle | 55.5 (O-104/U-110) | 55.5 (O-105/U-109) | 55.5 (O-105/U-109) | 55.5 (O-105/U-109) | 56 (O-106/U-110) | +0.5 pts |
| total | draftkings | — | 55.5 (O-104/U-115) | 55.5 (O-104/U-115) | 55.5 (O-104/U-115) | 55.5 (O-114/U-105) | +0 pts |
| total | consensus | — | 55.5 (O-105/U-115) | 55.5 (O-104/U-115) | 55.5 (O-107/U-111) | 55.5 (O-115/U-107) | +0 pts |
| moneyline | open | — | CHI +115 / DET -140 | CHI +115 / DET -140 | CHI +115 / DET -140 | CHI +115 / DET -140 | CHI ML +115→+115 |
| moneyline | fanduel | CHI -146 / DET +124 | CHI -142 / DET +120 | CHI -126 / DET +108 | CHI -122 / DET +104 | CHI -122 / DET +104 | CHI ML -146→-122 |
| moneyline | pinnacle | CHI -136 / DET +121 | CHI -128 / DET +114 | CHI -117 / DET +104 | CHI -118 / DET +105 | CHI -118 / DET +105 | CHI ML -136→-118 |
| moneyline | draftkings | — | CHI -138 / DET +117 | CHI -121 / DET +102 | CHI -120 / DET +101 | CHI -120 / DET +102 | CHI ML -138→-120 |
| moneyline | consensus | — | CHI -137 / DET +115 | CHI -125 / DET +105 | CHI -121 / DET +100 | CHI -120 / DET +100 | CHI ML -137→-120 |

"open" row = packet `open` feed (pipeline source, unverified; see Open items). Spread rows are home-team line; prices listed away/home. News ties: none found for the Nov 24 moves in the packet roster-move list; cannot tie to timestamped news (UNKNOWN).

### De-vig, main markets (own computation from repo direct_lines, Nov 26 3:17 AM ET)
| Market | Book | Line | Away/Over price | Home/Under price | Implied A / B | Sum | No-vig A | No-vig B | Hold |
|---|---|---|---|---|---|---|---|---|---|
| spread | fanduel | DET +1.5 | CHI -108 | DET -112 | 51.9% / 52.8% | 104.8% | 49.6% (CHI) | 50.4% (DET) | 4.8% |
| spread | pinnacle | DET +1 | CHI -108 | DET -104 | 51.9% / 51.0% | 102.9% | 50.5% (CHI) | 49.5% (DET) | 2.9% |
| spread | draftkings | DET +1.5 | CHI -106 | DET -113 | 51.5% / 53.1% | 104.5% | 49.2% (CHI) | 50.8% (DET) | 4.5% |
| spread | betmgm | DET +1 | CHI -110 | DET -108 | 52.4% / 51.9% | 104.3% | 50.2% (CHI) | 49.8% (DET) | 4.3% |
| spread | betrivers | DET +1.5 | CHI -113 | DET -108 | 53.1% / 51.9% | 105.0% | 50.5% (CHI) | 49.5% (DET) | 5.0% |
| spread | bet365 | DET +1.5 | CHI -108 | DET -112 | 51.9% / 52.8% | 104.8% | 49.6% (CHI) | 50.4% (DET) | 4.8% |
| spread | williamhill_us | DET +1.5 | CHI -109 | DET -110 | 52.2% / 52.4% | 104.5% | 49.9% (CHI) | 50.1% (DET) | 4.5% |
| total | fanduel | 55.5 | Over -112 | Under -108 | 52.8% / 51.9% | 104.8% | 50.4% (Over) | 49.6% (Under) | 4.8% |
| total | pinnacle | 56 | Over -106 | Under -110 | 51.5% / 52.4% | 103.8% | 49.6% (Over) | 50.4% (Under) | 3.8% |
| total | draftkings | 55.5 | Over -114 | Under -105 | 53.3% / 51.2% | 104.5% | 51.0% (Over) | 49.0% (Under) | 4.5% |
| total | betmgm | 56 | Over -108 | Under -110 | 51.9% / 52.4% | 104.3% | 49.8% (Over) | 50.2% (Under) | 4.3% |
| total | betrivers | 55.5 | Over -107 | Under -114 | 51.7% / 53.3% | 105.0% | 49.2% (Over) | 50.8% (Under) | 5.0% |
| total | bet365 | 55.5 | Over -113 | Under -107 | 53.1% / 51.7% | 104.7% | 50.6% (Over) | 49.4% (Under) | 4.7% |
| total | williamhill_us | 55.5 | Over -107 | Under -113 | 51.7% / 53.1% | 104.7% | 49.4% (Over) | 50.6% (Under) | 4.7% |
| moneyline | fanduel | ML | CHI -122 | DET +104 | 55.0% / 49.0% | 104.0% | 52.9% (CHI) | 47.1% (DET) | 4.0% |
| moneyline | pinnacle | ML | CHI -118 | DET +105 | 54.1% / 48.8% | 102.9% | 52.6% (CHI) | 47.4% (DET) | 2.9% |
| moneyline | draftkings | ML | CHI -120 | DET +102 | 54.5% / 49.5% | 104.1% | 52.4% (CHI) | 47.6% (DET) | 4.1% |
| moneyline | betmgm | ML | CHI -120 | DET +100 | 54.5% / 50.0% | 104.5% | 52.2% (CHI) | 47.8% (DET) | 4.5% |
| moneyline | betrivers | ML | CHI -127 | DET +105 | 55.9% / 48.8% | 104.7% | 53.4% (CHI) | 46.6% (DET) | 4.7% |
| moneyline | bet365 | ML | CHI -121 | DET +101 | 54.8% / 49.8% | 104.5% | 52.4% (CHI) | 47.6% (DET) | 4.5% |
| moneyline | williamhill_us | ML | CHI -122 | DET +102 | 55.0% / 49.5% | 104.5% | 52.6% (CHI) | 47.4% (DET) | 4.5% |

Working: no-vig A = implied(A)/(implied(A)+implied(B)), implied(-x)=x/(x+100), implied(+x)=100/(x+100). Source direct_lines retrieved Nov 26 3:17 AM ET; per-book main line = the two-sided line whose prices are closest to even.

## Projections (market-anchored, UNVALIDATED)
| Item | Value |
|---|---|
| Score range | CHI 28.5 / DET 27 anchored to CHI −1.5, 55.5 (engine core/period_engine_v0 50.1 −0.794 bias = 49.3; matchup_pair CHI 24.7–DET 25.5; **no edge claimed**, M2 failed) |
| Caleb rush | baseline L5 mean 9.8 → sim median 14 [p10 1 / p90 38]; line 22.5; adj: DET man 38%/single-high 57% (spy), 4–5 carries, no designed runs |
| Gibbs rush | packet 82.7 [58–114] vs sim 105 [63–155] vs line 92.5 — range is the disagreement, treat as no edge |
| St. Brown rec | packet 52.6 [31–83], sim 72 [27–137], line 82.5 (both under; P4 cut) |
| Burden rec | packet 47.8 [27–75], sim 54, line 60.5 |


## Open items (re-check before 1:00 PM ET)
- **Inactives ~11:30 AM ET (NFL.com):** Stevenson, D. Jackson, Clark, Wonnum; Swift/Monangai/Ahmed (elevated RB) usage; re-run if Stevenson out.
- Verified defender alignments: MISSING (paywalled) → every receiving leg cut. NGS live page: not checked. Film N/A.
- Gibbs OL run-direction splits: MISSING. Outlier/odds-history true opener: NOT CHECKED (packet `open` feed shows DET −2.5/ML −140 which contradicts earliest FD/Pinnacle snapshots (CHI favored): treated as unreliable).
- Reprice all legs at 11:45 AM; 3:17 AM prices are 8+ hours old.


## Sources and freshness
| Source | Time pulled (ET) |
|---|---|
| Packet brief.md/packet.json + dashboard/data JSON (watch block) @ main 2b33647 | read Nov 26 ~9:00 AM; built Nov 25 6:31 PM |
| direct_lines JSON (FD/DK/Pinnacle/BetMGM/BetRivers/Fanatics) | Nov 26 3:17 AM |
| Price freezes (4 snapshots Nov 24 1:11 AM – Nov 25 6:26 PM) | repo |
| ESPN injuries API | Nov 26 9:00 AM |
| nflverse, StatRankings, Sharp coverage, PFR, sims | prior run 3:49–4:05 AM |


*Research only. Not validated. Not betting advice.*

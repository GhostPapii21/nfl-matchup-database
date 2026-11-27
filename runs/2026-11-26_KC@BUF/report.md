# KC @ BUF — Thu Nov 26, 2026, 8:20 PM ET, Highmark Stadium (outdoor) — Thanksgiving game 3 — **WEATHER FLAG**
**SCHEDULED RUN** (fired Nov 26 8:58 AM ET). Research only. `projection_ready` = false → no picks, no slips. **CHECKLIST VETTED: NO (pending Ghost6).**

| Item | Value |
|---|---|
| Packet | `pregame/packets/2026_12_KC_BUF` @ main 2b33647, **Updated Nov 25 6:31 PM ET** (23:31:49Z) |
| Built before final injury report? | **YES.** Designations after 6:31 PM ET: KC Jaylon Moore (RT) OUT 9:51 PM, Norman-Lott (DT) OUT 9:54 PM, Woods (DT) Q 9:59 PM; BUF Sanders (DT) Q 10:11 PM (Benford, D. Williams, Kincaid Q were posted earlier that day). **All labels capped at Lean.** |
| Book prices | Packet Nov 25 6:26 PM ET; repo direct_lines Nov 26 3:17 AM ET. Odds API credits spent: 0 |
| Weather (kickoff 8:20 PM) | **NWS hourly (generated 8:42 AM ET): 8 PM 37°F, 13 mph, rain 100%; 9 PM 37°F, 13 mph, 99%; 10 PM 12 mph, 94%.** Open-Meteo (9:00 AM ET): 8 PM 37.3°F, 0.19 in/hr, wind 19.2 mph, gust 41.4; 9 PM 0.31 in/hr, 15.9 / gust 33.1; 7 PM 21.7 / gust 49.7. Packet (NWS 6:31 PM Nov 25): 38°F, NE 15, 98% rain; flags WIND_15_PLUS, PRECIP_50_PLUS. NWS vs Open-Meteo differ on wind (13 vs 19 mph): both ≥10 with heavy rain |
| Tools | gh api read-only, ESPN injuries (9:00 AM ET), NWS + Open-Meteo, prior-run nflverse/StatRankings/Sharp, weather history scripts, sims seed 20261101 3×100k |
| Live checks | ESPN injuries 9:00 AM ET; inactives NOT posted (due ~6:50 PM ET); DK site 403 (not bypassed) |


## Five-line summary
1. **Script:** cold rain + wind, run-first, field-position game; worst weather in H1. BUF −2.5 (FD/Pinnacle −2.5/−3, DK −3), total **46.5 FD / 46 Pinnacle / 45.5 DK**, ML BUF −152 / KC +128. KC D allows the fewest points (15.4, #1), BUF #4 (18.25).
2. **Market move:** total 48.5 → 46.5 (FD) / 48 → 46 (Pinnacle) / 47.5 → 45.5 (DK) since Nov 24; spread/ML flat. Roughly half of the weather edge is already priced; DK is still the lowest at 45.5.
3. **Lean edges (UNVALIDATED):** Mahomes rush U11.5 (sim .647; RT Moore OUT is the counter), H1 U23.5 (empirical .711 in rain+wind vs ~.52 no-vig), alt total U52.5 (FD −260, no-vig .681; shrunk judgment p ≈ .80).
4. **80+ watch:** Cook 3★ (p80 .492; blend .531 vs FD −132 BE 56.9% → −3.8), Emmett Johnson 2★ (.390; blend .475 vs −128 BE 56.1% → −8.6). WATCH only; EJ's sim says 80+ is .708 but the watch model .475 (disagreement 23 pts).
5. **Cuts:** every passing/receiving OVER (weather gate), receiving unders (P4), Allen rush U (MODEL-SUSPECT 16 off), Cook rush-only O (§9), Ott/Davis/Ty Johnson rushing (<60% share).


## Game script
| Scenario | Prob (judgment) | Flow |
|---|---|---|
| **Base** grind | ~55% | Q1–Q2 heaviest rain/gusts (Open-Meteo 8 PM 19/41, 9 PM 16/33): Cook/EJ volume, short passes, punts, FG risk; H1 ≈ 17–20 total. Q3–Q4 wind eases (10 PM ~12–14), one-score game |
| **Flip A** turnover-driven | ~25% | wet-ball fumble/short field gives cheap TDs; total climbs without passing efficiency |
| **Flip B** BUF pulls away | ~20% | BUF pressure (#4, 37.5% blitz, Rousseau 39 pressures) vs KC backup RT: sacks/turnovers, BUF +10, Cook closes; total still under |
Period read: H1 under fits base and both flips. H1 spread has no model: not a leg.

**Weather evidence (outdoor 2019–25 vs closing total; hindsight-selected, n small):** rain+wind≥10: 76% under, mean −5.7 (n=38); rain: 69%/−3.9 (n=94); all outdoor ~50%. P(actual < close+6): .688 outdoor / .830 rain / .895 rain+wind. H1 ≤23: .558/.638/.711. **Caveat:** recorded-weather flag biases toward games where rain fell; forecast-based p is lower, so I shrink to ~.80 (judgment).


## Breakdown
### Injuries and depth (ESPN API Nov 26 9:00 AM ET; newest entry 10:11 PM ET Nov 25)
| Team | OUT / IR | Questionable | Matters because |
|---|---|---|---|
| KC | RB Kenneth Walker III OUT (groin); **RT Jaylon Moore OUT**; DT Omarr Norman-Lott OUT; TE Jared Wiley IR; FB VanSumeren IR | DT Peter Woods (neck), TE Noah Gray (ribs) | EJ starts 3rd straight (81%/74% carry share); BUF #4 pressure vs backup RT; KC pass rush = Karlaftis only |
| BUF | none OUT | CB Christian Benford (groin), TE Dalton Kincaid (thumb/ankle), RG O'Cyrus Torrence, DT T.J. Sanders (shoulder), LB Dorian Williams (calf) | If Benford out, Hairston/Strong start; if Kincaid out, Knox gains; Torrence RG vs Woods/DT depth |
Inactives ~6:50 PM ET.

#### Carried from the 4:01 AM manual run (same packet; sims seed 20261101, 3×100k, prior-run numbers; RB share tables there used a 50% cut: **the saved 60%-of-carries rule now applies and is stricter**)

### Breakdown
**KC offense (Mahomes):**
- Card: vs blitz 7.84 YPA (B), no blitz 8.12 (A), sack rate 3.7% (A), aDOT 6.29 (short, which suits the rain).
- **BUF defense:** StatRankings man 28.3% (#22), **zone 71.4%**, two-high 51.9%, **blitz 37.5% (#8)**. Sharp: man 18.1 / zone 74.9, which agrees (zone-heavy).
- Packet: BUF allows 18.25 pts (#4), YPA 6.09 (#3), pressure 20% (#4), and **RB receiving 39 yds (#25), a soft spot for EJ.**
- BUF rush leaders: Rousseau 39 pressures / 10 sacks, Oliver 14, Chubb 14. **Rousseau vs KC's backup RT is the biggest mismatch on the field.**

**BUF offense (Allen):**
- Card: vs blitz 7.78 YPA (B), no blitz 8.52 (A), sack rate 6.4% (C), 3rd/4th-down 43.5% (A).
- **KC defense:** StatRankings man 43.0% (#7), zone 55.9%, two-high 52.5%, blitz 28.3% (#22). Sharp: man 18.8 / zone 77.3. That is a level disagreement on man, so **SHARP CAUTION**.
- KC allows 15.4 pts (#1), YPC 3.42, RZ TD 31.8% (#1), but **TE yds 71.5 (#30)** and pressure only 12.5% (#28). Allen should have time; the weather is the limiter.
- KC pass rush is concentrated: Karlaftis 31 pressures, then a drop to C. Jones at 10.

**Receiver seesaw:**
- BUF spreads it out: Moore 21.4 / Shakir 16.3 / Coleman 13.3 / Knox 11.2 / Ty Johnson 11.2 L3.
- Allen's blitzed tree shifts toward Shakir (20%), Coleman and Kincaid. Kincaid is questionable; if he sits, Knox gains.
- KC: Rice 17.9 / Kelce 14.2 / Worthy 12.3 / EJ 10.4 / Downs 9.4. Rice has been back for 4 games.

**RB run direction:** not computed (MISSING). KC run D: YPC 3.42 allowed (tough). BUF run D: the packet RB rush rank and the soft spot vs RB receiving.

**Red zone:** KC's defense is #1 in RZ TD% (31.8%), which supports field goals over TDs (and FGs are shaky in this wind).

### RB carry share and the 50% rule
| RB | Share | Verdict |
|---|---|---|
| EJ | 81% (W10), 74% (W11) with Walker out | PASS |
| Ott | 16% (W11) | DNP |
| Cook | 68.9% L3, 65.3% season | PASS |
| Ray Davis | 5.8% | DNP |
| Ty Johnson | pass-down role | DNP rushing |

### Defender matchups: ALL INFERRED, NONE VERIFIED, so receiving legs are CUT (P4)
**BUF receivers vs KC DBs** (depth chart 2:01 AM ET):
- Nohl Williams (LCB1): 56 targets, 45%, 4.5 yds/target. Elite.
- Delane (RCB1): 8.2 yds/target.
- Fulton: 4.6. Sneed (NB2): 79%, 7.9. Canady (NB1): no 8+ target row.
- Conner (S): 10.1 yds/target. That, plus KC's weak TE defense, points to Knox/Kincaid.

**KC receivers vs BUF DBs:**
- Igbinosun (RCB1): 52 targets, 44%, 5.3.
- Benford (LCB1, questionable): 6.2. Hairston: 5.8. Alford (NB): 5.2.
- Bishop (FS): 6.5. Hamlin: 11.3.
- **If Benford sits, Hairston/Strong start.**

### Pressure and blitz
- BUF blitzes 37.5% (#8), pressure #4, vs a KC OL missing RT Jaylon Moore. Mahomes is B vs the blitz.
- KC pressure ranks #28 (12.5%), blitz 28.3%. Allen should be clean, and his no-blitz grade is A.
- **D-line weak spots:**
  - KC: Norman-Lott (DT) OUT; KC's pass rush is a one-man show (Karlaftis).
  - BUF: Torrence (RG) questionable.

### Weather evidence (outdoor games 2019–25, measured against the closing total; script _shared/hist/weather_hist.py, alt_under_hist.py)
| Subset | Under % | Mean (actual − close) | n |
|---|---|---|---|
| All outdoor | ~50% | ~0 | — |
| Rain | 69% | −3.9 | 94 |
| **Rain + wind ≥10 mph** | **76%** | **−5.7** | **38** |
| Rain + wind ≥15 mph | 67% | −5.9 | 15 |
| Wind ≥15 (any) | 54% | −1.2 | — |
| Wind ≥20 (any) | 47% | — | 32 |

**P(actual < close + k):**

| k | Outdoor | Rain | Rain + wind |
|---|---|---|---|
| +6 | .688 | .830 | .895 |
| +8 | .739 | .862 | .921 |

**H1 ≤ 23:** .558 overall, .638 in rain, .711 in rain + wind.

**Other effects:**
- YPA: 7.09 → 6.58 at 20+ mph wind. Rain + wind ≥15 gives 6.30 vs 7.13 dry.
- XP%: 94.5% → 89.7% at 20+ mph.
- FG%: not monotonic with wind (selection effect: teams avoid long kicks).
- Packet rain model (211 team-games): KC pass yds 252 → 214, BUF 232 → 197. Receiver yards fall about 16%.

**CAVEAT:** the rain flag comes from recorded game weather (hindsight), which selection-biases it toward games where rain actually fell. Tonight's forecast is 88–100%, which reduces but does not remove that bias. The sample is small (n=38).

## Opportunity and volume table
Packet opportunity layer (dashboard `opportunity`, built Nov 25 6:32 PM ET from nflverse PBP through W11/12). Label is my read from packet inputs: EXPANDING = L3 share ≥ window +3 pts; SHRINKING = L3 ≤ window −3 pts or role split cutting carries; EFFICIENCY-DRIVEN = yards/target or YPC well above the position norm on thin volume (<5 tgt / <12 car); else VOLUME-SUPPORTED. Packet model medians are research numbers, not edges.

| Player | Tm | Pos | Team att (pass/rush) | Share window / L3 / used | Proj tgt or car (mean) | Proj yds median [p25–p75] | FD line | Packet P(over line) | Last-5 yds (tgt/car) | Label (my read) | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Travis Kelce | KC | TE | 31.6/26.6 | 16.5% / 15.2% / 16.3% | 4.6 | 27.8 [13–47] | 46.5 | 0.31 | 44(8), 67(7), 72(6), 30(2), 74(7) | VOLUME-SUPPORTED | — |
| Xavier Worthy | KC | WR | 31.6/26.6 | 16.5% / 13.1% / 15.5% | 4.3 | 19.3 [7–35] | 20.5 | 0.47 | 11(6), 13(6), 48(6), 0(3), 38(4) | SHRINKING | — |
| Rashee Rice | KC | WR | 31.6/26.6 | 22.5% / 19.2% / 21.5% | 6.0 | 33.1 [17–55] | 47.5 | 0.35 | 88(9), 53(8), 49(7), 82(6), 53(6) | SHRINKING | — |
| Emmett Johnson | KC | RB | 31.6/26.6 | 11.7% / 14.8% / 14.4% | 4.1 | 20.5 [10–39] | 30.5 | 0.35 | 18(3), 17(3), 128(5), 70(7), 38(4) | OPPORTUNITY EXPANDING | — |
| Tyquan Thornton | KC | WR | 31.6/26.6 | 20.0% / 20.0% / 20.1% | 5.6 | 37.6 [17–65] | n/a | — | 22(2), 111(8) | VOLUME-SUPPORTED | LOW-SAMPLE (≤3 logged games; packet roster-move/role artefact risk) |
| Emmett Johnson | KC | RB | 31.6/26.6 | 39.9% / 61.4% / 73.1% | 16.1 | 56.9 [30–95] | 81.5 | — | 6(3), 15(1), 34(6), 101(22), 105(23) | OPPORTUNITY EXPANDING | teammate-out bump +24.6pts; role window short |
| Khalil Shakir | BUF | WR | 28.7/33.7 | 18.3% / 17.0% / 17.8% | 4.5 | 26.5 [12–48] | 39.5 | 0.38 | 34(6), 64(6), 58(4), 26(3), 101(9) | VOLUME-SUPPORTED | — |
| DJ Moore | BUF | WR | 28.7/33.7 | 22.0% / 22.3% / 22.1% | 5.6 | 30.7 [13–54] | 48.5 | 0.32 | 11(2), 82(7), 25(5), 90(6), 91(10) | VOLUME-SUPPORTED | — |
| Keon Coleman | BUF | WR | 28.7/33.7 | 14.3% / 13.8% / 14.1% | 3.6 | 17.2 [6–33] | 22.5 | — | 59(6), 4(3), 17(6), 11(3), 17(4) | VOLUME-SUPPORTED | — |
| Dalton Kincaid | BUF | TE | 28.7/33.7 | 14.5% / 14.5% / 14.5% | 3.7 | 20.3 [8–37] | 38.5 | 0.25 | 7(2), 38(8), 86(6), 28(3), 58(3) | VOLUME-SUPPORTED | — |
| Ty Johnson | BUF | RB | 28.7/33.7 | 11.3% / 11.7% / 11.5% | 3.0 | 14.5 [4–29] | 15.5 | — | 24(2), 19(3), 36(2), 4(1), 55(8) | VOLUME-SUPPORTED | — |
| James Cook | BUF | RB | 28.7/33.7 | 74.5% / 75.5% / 72.2% | 20.0 | 78.9 [55–109] | 82.5 | — | 95(22), 80(21), 107(31), 157(18), 89(22) | VOLUME-SUPPORTED | — |

Sim-based low/mid/high tables (p10/median/p90) from the 4:01 AM run are in `../2026-11-26_W12_THANKSGIVING/KC@BUF/REPORT.md`. Where packet and sim disagree, both are shown in Projections; a disagreement is a no-edge flag, not an overrule of Rico's reads.

## 80-yard / explosive watch (WATCH only, never a pick)
Watch block source: `dashboard/data/2026_12_KC_BUF.json` @ main 2b33647, `generated_utc` Nov 25 6:31 PM ET, board_built Nov 25 6:32 PM ET. Prices: FD rungs from `pregame/direct_lines/2026_12_KC_BUF.json` retrieved Nov 26 3:17 AM ET (repo file; Odds API credits spent: 0). Live DK/FD website check from box: DraftKings public endpoint returned HTTP 403 Access Denied (not bypassed) → MISSING; FanDuel site not separately fetched (repo direct pull used).

- KC_vs_BUF: defense 80+ games allowed rank 14/32, explosive-plays-allowed rank 17/32 (1 = best defense); implied pts 22.0
- BUF_vs_KC: defense 80+ games allowed rank 29/32, explosive-plays-allowed rank 22/32 (1 = best defense); implied pts 24.5

| Player | Tm | Type | ★ | p80 | p100 | Tgt/Car | YPG | Style | Why (model) | Blend | FD 79.5 (now) BE | Blend−BE | FD 99.5 (now) BE | Dash book80 (Nov 25 6:26 PM ET) | Def gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Emmett Johnson | KC | rush | 2 | 0.390 | 0.239 | 19.4 | 46.3 | — | 19.4 carries a game; a teammate's absence adds carries; the FanDuel price moves this from 1 to 2 stars; model 39% vs FanDuel 56%:  | 0.475 | -128 / 56.1% | -8.6 pts | +178 / 36.0% | -128 / 56.1% | middle #11 (77.8 vs 92.7) |
| James Cook | BUF | rush | 3 | 0.492 | 0.327 | 21.8 | 108.5 | — | 21.8 carries a game; the FanDuel price moves this from 2 to 3 stars | 0.531 | -132 / 56.9% | -3.8 pts | +178 / 36.0% | -132 / 56.9% | tough #8 (71.1 vs 92.7) |

**Multi-book view (every reachable book at 0 credits).** Only FanDuel posts the 79.5 / 99.5 alt rungs in the repo feeds; DK, Pinnacle, BetMGM, BetRivers, Fanatics, bet365-style feeds carry the MAIN line only. A non-FD book is shown at an 80+ rung only if its main line is exactly 79.5 (or 99.5); otherwise 80+ = MISSING. Main-line Over price/BE shown so line disagreement is visible. Flag = any book ≥5 implied pts off the others at the same line, or lines ≥2 yds apart.

| Player | Book | Main line | Over (BE) | Under (BE) | 80+ rung | 100+ rung | Flag |
|---|---|---|---|---|---|---|---|
| Emmett Johnson | fanduel | 81.5 | -113 (53.1%) | -113 (53.1%) | FD -128 | FD +178 | lines span 3y ex-bovada |
| Emmett Johnson | draftkings | 81.5 | -114 (53.3%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Emmett Johnson | pinnacle | 80.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| Emmett Johnson | betmgm | 83.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 3y ex-bovada |
| Emmett Johnson | betrivers | 83.5 | -113 (53.1%) | -118 (54.1%) | MISSING | MISSING | lines span 3y ex-bovada |
| Emmett Johnson | betonlineag | 81.5 | -114 (53.3%) | -114 (53.3%) | MISSING | MISSING | lines span 3y ex-bovada |
| Emmett Johnson | bovada | 81.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| Emmett Johnson | circasports | 81.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| James Cook | fanduel | 82.5 | -113 (53.1%) | -113 (53.1%) | FD -132 | FD +178 | lines span 3y ex-bovada |
| James Cook | draftkings | 80.5 | -112 (52.8%) | -112 (52.8%) | MISSING | MISSING | lines span 3y ex-bovada |
| James Cook | pinnacle | 82.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |
| James Cook | betmgm | 83.5 | -115 (53.5%) | -115 (53.5%) | MISSING | MISSING | lines span 3y ex-bovada |
| James Cook | betrivers | 82.5 | -117 (53.9%) | -114 (53.3%) | MISSING | MISSING | lines span 3y ex-bovada |
| James Cook | betonlineag | 81.5 | -114 (53.3%) | -114 (53.3%) | MISSING | MISSING | lines span 3y ex-bovada |
| James Cook | bovada | 100.5 | +205 (32.8%) | -280 (73.7%) | MISSING | MISSING | bovada alt-style skew (excluded) |
| James Cook | circasports | 81.5 | -110 (52.4%) | -110 (52.4%) | MISSING | MISSING | lines span 3y ex-bovada |

**Honest record (held-out 2025-26):** 3★ hit 51%, 2★ 43%, 1★ 35%; vs FanDuel Weeks 8–9 prices starred rungs +8.7% ROI on 68 rungs (not significant); model-beats-price-by-3+ rungs −47%. Every 80+ entry = WATCH unless blend clears best-price break-even by +3 AND gates pass. A back's star never overrides the 60% carry rule; a strong 80+ read argues for keeping that player's lower alt-floor leg.

## Brainstorm (10 angles) and critical review
| # | Angle (number) | Verdict | Reason / case against |
|---|---|---|---|
| 1 | Alt total UNDER 52.5 (FD −260, no-vig .681; history .83–.895 in rain/wind) | **KEEP (Lean)** | Against: hindsight weather flag, n=38, 46.5 close already includes weather (−2 since Nov 24), wind ≥20 alone only 47% under, turnovers create short fields |
| 2 | H1 UNDER 23.5 (Pinn +102 / FD −115; H1≤23 .711 in rain+wind) | **KEEP (Lean)** | Worst weather in H1; against: same selection bias; two good offenses can score on a short field; kickers only a small boost |
| 3 | Mahomes rush UNDER 11.5 (sim .642/.643/.654; ~2 carries/g, 0 in W11) | **KEEP (Lean)** | Against: RT Moore out + Rousseau pressure may force scrambles; rain can increase QB keeps |
| 4 | Emmett Johnson 80+ rush (73% share, 22–23 carries, Walker out, weather boosts rush) | **WEAKEN → WATCH/MANUAL_REVIEW** | Sim .708 vs watch .475; 2-game role window (LOW-SAMPLE); priced at −128 (56%); sim_v6 lead-RB bias +13 |
| 5 | Cook 80+ (3★; KC defense 80+ games rank #29 of 32) | **KEEP as WATCH** | Priced −132 (56.9%) vs blend .531; BUF −2.5 favorite could trail so §9 forces rush+rec; Cook rush+rec MODEL-SUSPECT +13 |
| 6 | Receiving overs (Rice, Moore, Shakir) | **DROP** | Weather gate: rain+wind cuts yards ~16%, YPA 7.1→6.3–6.6 |
| 7 | Receiving unders (Kelce 46.5: packet median 27.8, P(over) .31) | **WEAKEN** | P4: no verified defender; KC TE yds allowed #30 helps Knox/Kincaid not Kelce; line already shaded |
| 8 | KC RT Moore OUT vs Rousseau (39 pressures, 10 sacks) | **KEEP (direction)** | Supports under/ BUF script; market spread flat at −2.5/−3; no clean prop |
| 9 | KC D #1 in points allowed + RZ TD 31.8% #1 → FGs, FG kicking risk in 40 mph gusts | **KEEP (supports 1–2)** | Wind alone not monotone for FG%; double counts with 1–2 |
| 10 | Allen rush UNDER 38.5 (sim .796) | **DROP** | MODEL-SUSPECT: 16 yds off; last-5 1/30/15/5/0 carries W11 (Josh Allen had 0 carries; check) |
**Strongest case against:** the weather is real but famous: the total has fallen 2 points everywhere, DK is already at 45.5, and the −260 alt price embeds the same fear. Our empirical rate comes from games that were recorded as rainy, which flatters the forecast case.


## Market table (labels capped at Lean)
| Leg | Our fair p | Pinnacle no-vig | FD no-vig | DK | Edge pts | Best price / BE | Movement | Label | Driver | Kill-switches |
|---|---|---|---|---|---|---|---|---|---|---|
| **Mahomes rush U11.5** (Pinn U12.5 −115) | .647 (sim) | at 12.5: n/a (one side) | .500 (−113/−113) | n/a | +14.7 (flag; model-suspect no) | FD U −113, BE 53.05% | stable | **LEAN** | RT out/short passing, few designed runs | RT-out scramble games; line ≤9.5; inactive news |
| **H1 U23.5** | .711 empirical (rain+wind) / .638 rain | ~.52 (Pinn +102 U) | FD −115 | n/a | ~+19 empirical; shrunk ~+12 | Pinnacle +102, BE 49.5% | not tracked (H1 total) | **LEAN** | weather in H1 | NWS rain <50% or gusts <20 mph at 6:50 PM; H1 line ≤21.5 |
| **Alt total U52.5** | ~.80 (judgment, shrunk from .895/.83) | alt n/a | .681 (FD −260) | n/a | +12 vs no-vig; +8 vs BE .722 | FD −260, BE 72.2% | main −2 pts | **LEAN** | rain+wind | Main total ≤43.5 (thins), rain forecast <50%, wind <10 |
| Alt U51.5/53.5/54.5 | .87–.92 empirical | — | .658/.705/.723 | — | — | FD −230/−295/−330 | — | same | same | same |
| EJ rush O81.5 / 59.5+ 69.5+ 79.5+ | .676; .910/.824/.708 sim | — | .500; .718/.628/.529 | — | +17.6 sim; −8.6 vs watch blend | FD −113; −320/−200/−128 | — | **WATCH, MANUAL_REVIEW** (MODEL-SUSPECT, LOW-SAMPLE) | volume | EJ share <60%; Walker back |
| Cook rush O82.5 / rush+rec O94.5 | .598 / .628 | — | .500 / .500 | — | +9.8 / +12.8 | FD −113 | — | **CUT (§9)** / **MANUAL_REVIEW** (suspect +13) | — | — |
| Cook 80+ | blend .531 | MISSING | n/a | MISSING | −3.8 | FD −132 (56.9%) | — | **WATCH** | volume | — |
| Spread BUF −2.5 / ML BUF −152 | none | BUF −3: KC .517 / BUF .483; ML BUF .583 | KC .478 / BUF .522 at −2.5; ML BUF .579 | −3: −117/−102 | — | — | flat | **NO PLAY** | — | — |
| Receiving overs / unders | — | — | — | — | — | — | — | **CUT** (weather / P4) | — | — |

### Line movement (first seen → now)
| Market | Book | Nov 24 1:11 AM ET | Nov 24 6:18 PM ET | Nov 24 10:40 PM ET | Nov 25 6:26 PM ET | 3:17 AM ET direct (Nov 26) | Net move |
|---|---|---|---|---|---|---|---|
| spread | open | — | BUF -2.5 (-105 KC/-115 BUF) | BUF -2.5 (-105 KC/-115 BUF) | BUF -2.5 (-105 KC/-115 BUF) | BUF -2.5 (-105 KC/-115 BUF) | +0 pts |
| spread | fanduel | BUF -2.5 (+100 KC/-128 BUF) | BUF -2.5 (-102 KC/-125 BUF) | BUF -2.5 (-102 KC/-125 BUF) | BUF -2.5 (-102 KC/-125 BUF) | BUF -2.5 (+100 KC/-120 BUF) | +0 pts |
| spread | pinnacle | BUF -3 (-117 KC/+103 BUF) | BUF -2.5 (+102 KC/-115 BUF) | BUF -2.5 (+103 KC/-116 BUF) | BUF -2.5 (+103 KC/-116 BUF) | BUF -3 (-114 KC/+101 BUF) | +0 pts |
| spread | draftkings | — | BUF -3 (-120 KC/+100 BUF) | BUF -3 (-120 KC/+100 BUF) | BUF -3 (-120 KC/+100 BUF) | BUF -3 (-117 KC/-102 BUF) | +0 pts |
| spread | consensus | — | BUF -3 (-111 KC/-109 BUF) | BUF -3 (-111 KC/-109 BUF) | BUF -3 (-109 KC/-111 BUF) | BUF -3 (-117 KC/-102 BUF) | +0 pts |
| total | open | — | 50.5 (O-110/U-110) | 50.5 (O-110/U-110) | 50.5 (O-110/U-110) | 50.5 (O-110/U-110) | +0 pts |
| total | fanduel | 48.5 (O-111/U-115) | 47.5 (O-113/U-113) | 47.5 (O-113/U-113) | 46.5 (O-113/U-113) | 46.5 (O-110/U-110) | -2 pts |
| total | pinnacle | 48 (O-112/U-104) | 47 (O-110/U-106) | 47 (O-111/U-106) | 46.5 (O-108/U-106) | 46 (O-107/U-109) | -2 pts |
| total | draftkings | — | 47.5 (O-107/U-112) | 47.5 (O-102/U-117) | 46.5 (O-108/U-111) | 45.5 (O-114/U-106) | -2 pts |
| total | consensus | — | 47.5 (O-106/U-112) | 47.5 (O-104/U-111) | 46.5 (O-109/U-110) | 46.5 (O-104/U-110) | -1 pts |
| moneyline | open | — | KC +125 / BUF -150 | KC +125 / BUF -150 | KC +125 / BUF -150 | KC +125 / BUF -150 | KC ML +125→+125 |
| moneyline | fanduel | KC +132 / BUF -156 | KC +128 / BUF -152 | KC +128 / BUF -152 | KC +128 / BUF -152 | KC +128 / BUF -152 | KC ML +132→+128 |
| moneyline | pinnacle | KC +131 / BUF -148 | KC +128 / BUF -144 | KC +129 / BUF -146 | KC +129 / BUF -146 | KC +133 / BUF -150 | KC ML +131→+133 |
| moneyline | draftkings | — | KC +126 / BUF -149 | KC +126 / BUF -149 | KC +125 / BUF -148 | KC +127 / BUF -151 | KC ML +126→+127 |
| moneyline | consensus | — | KC +125 / BUF -151 | KC +125 / BUF -151 | KC +125 / BUF -151 | KC +128 / BUF -152 | KC ML +125→+128 |

"open" row = packet `open` feed (pipeline source, unverified; see Open items). Spread rows are home-team line; prices listed away/home. News ties: none found for the Nov 24 moves in the packet roster-move list; cannot tie to timestamped news (UNKNOWN).

### De-vig, main markets (own computation from repo direct_lines, Nov 26 3:17 AM ET)
| Market | Book | Line | Away/Over price | Home/Under price | Implied A / B | Sum | No-vig A | No-vig B | Hold |
|---|---|---|---|---|---|---|---|---|---|
| spread | fanduel | BUF -2.5 | KC +100 | BUF -120 | 50.0% / 54.5% | 104.5% | 47.8% (KC) | 52.2% (BUF) | 4.5% |
| spread | pinnacle | BUF -3 | KC -114 | BUF +101 | 53.3% / 49.8% | 103.0% | 51.7% (KC) | 48.3% (BUF) | 3.0% |
| spread | draftkings | BUF -3 | KC -117 | BUF -102 | 53.9% / 50.5% | 104.4% | 51.6% (KC) | 48.4% (BUF) | 4.4% |
| spread | betmgm | BUF -3 | KC -118 | BUF -102 | 54.1% / 50.5% | 104.6% | 51.7% (KC) | 48.3% (BUF) | 4.6% |
| spread | betrivers | BUF -3 | KC -118 | BUF -104 | 54.1% / 51.0% | 105.1% | 51.5% (KC) | 48.5% (BUF) | 5.1% |
| spread | bet365 | BUF -2.5 | KC +102 | BUF -122 | 49.5% / 55.0% | 104.5% | 47.4% (KC) | 52.6% (BUF) | 4.5% |
| spread | williamhill_us | BUF -3 | KC -118 | BUF -102 | 54.1% / 50.5% | 104.6% | 51.7% (KC) | 48.3% (BUF) | 4.6% |
| total | fanduel | 46.5 | Over -110 | Under -110 | 52.4% / 52.4% | 104.8% | 50.0% (Over) | 50.0% (Under) | 4.8% |
| total | pinnacle | 46 | Over -107 | Under -109 | 51.7% / 52.2% | 103.8% | 49.8% (Over) | 50.2% (Under) | 3.8% |
| total | draftkings | 45.5 | Over -114 | Under -106 | 53.3% / 51.5% | 104.7% | 50.9% (Over) | 49.1% (Under) | 4.7% |
| total | betmgm | 46.5 | Over -108 | Under -110 | 51.9% / 52.4% | 104.3% | 49.8% (Over) | 50.2% (Under) | 4.3% |
| total | betrivers | 46.5 | Over -113 | Under -108 | 53.1% / 51.9% | 105.0% | 50.5% (Over) | 49.5% (Under) | 5.0% |
| total | bet365 | 45.5 | Over -112 | Under -108 | 52.8% / 51.9% | 104.8% | 50.4% (Over) | 49.6% (Under) | 4.8% |
| total | williamhill_us | 45.5 | Over -113 | Under -107 | 53.1% / 51.7% | 104.7% | 50.6% (Over) | 49.4% (Under) | 4.7% |
| moneyline | fanduel | ML | KC +128 | BUF -152 | 43.9% / 60.3% | 104.2% | 42.1% (KC) | 57.9% (BUF) | 4.2% |
| moneyline | pinnacle | ML | KC +133 | BUF -150 | 42.9% / 60.0% | 102.9% | 41.7% (KC) | 58.3% (BUF) | 2.9% |
| moneyline | draftkings | ML | KC +127 | BUF -151 | 44.1% / 60.2% | 104.2% | 42.3% (KC) | 57.7% (BUF) | 4.2% |
| moneyline | betmgm | ML | KC +130 | BUF -155 | 43.5% / 60.8% | 104.3% | 41.7% (KC) | 58.3% (BUF) | 4.3% |
| moneyline | betrivers | ML | KC +123 | BUF -150 | 44.8% / 60.0% | 104.8% | 42.8% (KC) | 57.2% (BUF) | 4.8% |
| moneyline | bet365 | ML | KC +128 | BUF -153 | 43.9% / 60.5% | 104.3% | 42.0% (KC) | 58.0% (BUF) | 4.3% |
| moneyline | williamhill_us | ML | KC +130 | BUF -155 | 43.5% / 60.8% | 104.3% | 41.7% (KC) | 58.3% (BUF) | 4.3% |

Working: no-vig A = implied(A)/(implied(A)+implied(B)), implied(-x)=x/(x+100), implied(+x)=100/(x+100). Source direct_lines retrieved Nov 26 3:17 AM ET; per-book main line = the two-sided line whose prices are closest to even.

## Projections (market-anchored, UNVALIDATED)
| Item | Value |
|---|---|
| Score range | BUF 23 / KC 20.5, total ≈ 43.5 = market 46.5 − weather residual 2–4 (judgment). No validated engine (period_engine total bias +0.794, no edge vs market) |
| H1 | ≈ 17–20 total (judgment); market H1 23.5 |
| Mahomes rush | sim median 7.7 [0 / 23], line 11.5 |
| Cook rush | packet 78.9 [55–109], sim 91 (wx carry boost 1.0727), line 82.5 |
| EJ rush | packet 56.9 [30–95] (mean share 39.9% window vs 73.1% used), sim ~95 (role window W10–11), line 81.5 |
| Receivers (rain-adj = dry × ~0.84) | Rice sim 47 → ~40 (line 47.5); Moore 38 → ~32 (48.5); Kelce 36 → ~31 (46.5) |


## Open items (re-check before 8:20 PM ET)
- **Inactives ~6:50 PM ET:** Benford, Kincaid, Torrence, Sanders, D. Williams (BUF); Woods, Gray (KC); RB depth.
- **Weather reprice at 3–4 PM and 6:50 PM ET** (NWS hourly + Open-Meteo); if rain probability <50% or gusts <20 mph the under ladders die.
- Verified defenders MISSING; NGS not checked; run-direction splits MISSING; no 3-model game/H1 engine (P15 incomplete for those legs → SIMULATION NOT RUN for total/H1).
- Why Josh Allen had 0 carries in W11 (Kyle Allen played W8–11 per nflverse): unverified.
- Pinnacle's Mahomes 12.5 de-vig needs both sides; packet true opener (Outlier) NOT CHECKED; packet 'open' feed total 50.5 / BUF −2.5 is consistent with first-seen FD 48.5.


## Sources and freshness
| Source | Time (ET) |
|---|---|
| Packet + dashboard watch block @ main 2b33647 | built Nov 25 6:31 PM; read Nov 26 ~9:00 AM |
| direct_lines (FD/DK/Pinnacle/BetMGM/BetRivers/Fanatics) | Nov 26 3:17 AM |
| price freezes ×4 | Nov 24 1:11 AM → Nov 25 6:26 PM |
| ESPN injuries | Nov 26 9:00 AM |
| NWS hourly (BUF grid) generated 8:42 AM; Open-Meteo 9:00 AM; packet NWS 6:31 PM Nov 25 | as shown |
| nflverse, StatRankings, Sharp, weather history, sims | prior run 3:49–4:05 AM |


*Research only. Not validated. Not betting advice.*

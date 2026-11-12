# TNF WAS@NYG (Week 10): game-script, scenarios, props, value and slip grades. RESEARCH ONLY
Written about 6:00 PM ET, Thu Nov 12, 2026. Kickoff 8:15 PM ET, MetLife Stadium, outdoors, field turf.
Input: GhostPapii21/nfl-matchup-database main **fb9167b** (packet refresh 22:11Z = 5:11 PM ET). Main was re-checked at 5:39 PM ET and is unchanged.
Gates: `projection_ready` = false. NFL-44/45 are open. Phase 15 inactives are NOT_YET (they post about 6:45 PM ET). The 7 PM price freeze is not done. Every read is capped at **Lean**.
Engine cross-check: **Ghost6 10k pre-gate preview, main fb9167b, seed 20261112, pre-inactives, no injury adjustments, research only.** It is not the official 100k. The official 100k is BetGuru's at about 7:10 PM ET, gated on inactives and the 7 PM freeze.
No simulation was run for this report. The game-script numbers below are **script-based** (scenario-weighted, closed-form normal approximations in `script_layer.py`). Leg probabilities are closed-form (`legs.py`, `script_layer.py`).

## 1. Rule gates (Rico's rules) applied to every leg
| Gate | Rule | Status |
|---|---|---|
| G-RB | DO-NOT-PLAY any back under 60% of his team's carries | **Skattebo FAIL**: 58% of NYG carries in the 6 games he played (98/169), 46% over the 8-game window (98/214). **White FAIL**: 31% over the window (54/177), 34% in the games he played. Every Skattebo and White leg is rule-fail. The Skattebo rushing UNDER 63.5 stays a **flag only**. |
| G-DEF | No receiving leg without a verified main defender | `coverage_assignment_verified=false` in the repo (research/week9_cb_safety_profiles/README.md), and PFF gives projections only. **Every receiving leg is "rule-fail: defender unverified"**. Probabilities are shown for reference only. |
| G-STATUS | Status from the official report; inactives are not out yet | Skattebo is **expected to play** per the official report (Hamstring, LP/FP/FP, no designation; giants.com and commanders.com, read about 5:35 PM ET) and reporters (Schefter via theScore, Rapoport/NFL.com, NBC). He is **not** confirmed active until about 6:45 PM ET. The ESPN live list still shows him "Out", which conflicts with the official report, so the official report wins. |
| G-STATUS | Practice-report confirmations (secondary sources; the official report wins) | WAS C Lucas Patrick OUT (concussion) and TE Colson Yankoff OUT (knee). NYG LB Malik Harrison Q (groin). Daniels, McCarthy and Nabers were full on Thursday. McLaurin is on IR for the season (commanders.com, Oct 28). Burks has no designation but was DNP Wednesday, and ESPN lists him Out (unresolved). Croskey-Merritt is on IR. |
| G-PASSYDS | Passing-yards ban | Honored. No passing-yards reads. |

## 2. Projected score: game-script (script-based) vs Ghost6 10k pre-gate preview
| Source | NYG | WAS | Total | NYG margin | NYG win | NYG -1.5 | NYG -2.5 | Over 40.5 |
|---|---|---|---|---|---|---|---|---|
| **Game script (script-based, scenario-weighted, not a sim)** | **21.5** | **18.3** | **39.8** | **+3.3** | 59.5% | 55.2% | 52.2% | 47.7% |
| Ghost6 10k pre-gate preview (fb9167b, seed 20261112, pre-inactives, no injury adj., research only) | 20.4 (median 20) | 21.2 (median 20) | 41.6 (median 41) | -0.8 | 48.6% | 44.3% | 41.9% | 51.9% |
| Market (Pinnacle no-vig) | | | 40.5 | NYG -2.5 | 53.7% | | 48.2% (NYG +103) | 51.4% |

**Why they differ.** The preview runs with opponent-defense conditioning disabled (`defense_interaction: DISABLED_opponent_allowed`, h2h off). It has no weather and no injuries. The script, by contrast, leans on four things:
- NYG's elite pass defense: 3rd in pass yards allowed, 2nd in yards per attempt, 3rd in explosive passes.
- WAS's 32nd-ranked third-down offense.
- Rain: 75-78% chance of rain cuts WAS pass yards from 222 to about 198, measured over 211 rain team-games.
- WAS's thinned skill group: McLaurin and Croskey-Merritt on IR, Burks doubtful.

So the script is lower on WAS points (18.3 vs 21.2) and on the total (39.8 vs 41.6). The preview's WAS lean agrees with the market's move toward WAS (section 5). The script's NYG lean does not. Win-probability scores were coin-flip level in the NFL-49 backtest, so the preview is **not a side read**. The script is not validated either. Because the two disagree, the side is **Pass**.

### Script scenarios (weights are analyst judgment)
| Scenario | Weight | Score | Flow and prop effect |
|---|---|---|---|
| Base: rain grind | 50% | NYG 21-18 | Field-position game. NYG targets go to Nabers and Likely. WAS gets short Daniels throws and White carries. |
| NYG early lead | 25% | NYG 27-14 | NYG runs late (more Skattebo, less Nabers/Likely volume). WAS pass catchers get catch-up volume. |
| WAS leads / upset | 25% | WAS 23-17 | NYG passes more (Nabers/Likely up), Skattebo carries drop, Daniels scrambles more. |
Every slip below stacks NYG pass-catcher overs with Skattebo overs. In scenarios 2 and 3 those pull against each other.

### Flow by half and quarter (script-based)
| | Q1 | Q2 | Q3 | Q4 | 1H | 2H |
|---|---|---|---|---|---|---|
| NYG | 4.5 | 7.8 | 3.3 | 6.0 | 12.3 | 9.3 |
| WAS | 3.3 | 6.0 | 3.8 | 5.3 | 9.3 | 9.0 |
The Q1 rate is low (rain, scripted openers). Q2 is the highest-scoring quarter (two-minute drill). The 2H is roughly even. 1H/2H/quarter market prices are MISSING from the packet, so there is no de-vig row for them.

## 3. Side and total reads (capped at Lean) with de-vig
Consensus no-vig is the mean of the DK/FD/Pinnacle no-vig at the same line (packet 22:11Z = 5:11 PM ET). Edge = our probability minus Pinnacle no-vig, or minus consensus when Pinnacle does not post that line.
| Market | Posted line (FD / DK / Pin) | Pinnacle no-vig | Consensus no-vig | Our prob (script) | Ghost6 10k preview | Edge (script) | Best price | Tier |
|---|---|---|---|---|---|---|---|---|
| NYG -1.5 | -110 / -115 / (Pin posts -2.5) | n/a | 50.6% | 55.2% | 44.3% | +4.6 | FD -110 | **Pass** (script and preview conflict; reverse line movement against NYG) |
| NYG -2.5 | n/a / n/a / +103 | 48.2% | 48.2% | 52.2% | 41.9% | +4.0 | Pin +103 (reference) | **Pass** |
| WAS +2.5 | n/a / n/a / -113 | 51.8% | 51.8% | 47.8% | 58.1% | -4.0 | Pin -113 | **Pass** (the preview leans WAS, but win-prob scores were coin-flip level in the backtest) |
| NYG ML | -122 / -125 / -122 | 53.7% | 53.2% | 59.5% | 48.6% | +5.8 | FD/Pin -122 | **Pass** (same driver as the spread; conflict) |
| Under 40.5 | -105 / -105 / +100 | 48.6% | 48.8% | 52.3% | 48.1% | +3.7 | Pin +100 / FD,DK -105 (retail breakeven 51.2%) | **Lean, low** (rain, total down 1 against 95% Over handle; the preview has no edge) |
| Over 40.5 | -115 / -115 / -112 | 51.4% | 51.2% | 47.7% | 51.9% | -3.7 | | **Pass** (preview 51.9% vs retail -115 breakeven 53.5%: no edge) |
| NYG 1H 3-way | MISSING | MISSING | MISSING | ~50% (script, about 14% tie mass) | n/a | n/a | n/a | **N/A** (no price) |
The total and team-points layer is superseded by BetGuru's official 100k at about 7:10 PM ET.

## 4. Props and value (reference only; gates applied)
| Read | Market | Our prob | Gate | Tier |
|---|---|---|---|---|
| A.Williams receiving yards UNDER 37.5 | FD -113 (no-vig 50.0%) | ~58% (rain forecast 31.4, median 25.7) | rule-fail: defender unverified | Flag only |
| Likely receptions OVER 4.5 | FD +102 (no-vig 46.2%; Pin 47.2%) | ~52% (forecast 5.3 rec; 5 of 8 games with 5+) | rule-fail: defender unverified | Flag only |
| Skattebo rushing UNDER 63.5 | FD -113 | ~55% (WAS 8th in YPC allowed, 6th in explosive runs; hamstring return; 55% snaps last game) | G-RB FAIL (58% carry share) | **Flag only** |
| Nabers receiving yards 66.5 | FD -113/-113 | ~48-50% (rain-adjusted 71.7 mean; NYG pass D irrelevant here, WAS pass D 27th) | rule-fail: defender unverified | Pass |

## 5. Movement summary
- **Reverse line movement toward WAS.** The public is on NYG: CLEATZ 5:22 PM ET shows NYG -1.5 at 69% of tickets and 69% of handle; CLEATZ 10:52 AM had 73%/88% at -2.5; SI/DK had 69% of spread bets; VSiN had more than three-quarters. That is a 66-75% range. Meanwhile DK moved NYG -2.5 to -1.5, and the ML moved -142 to -125 (DK), -134 to -122 (FD), and -136 to -122 (Pinnacle).
- **Pinnacle price flip.** Pinnacle held NYG -2.5 but flipped the price from -106/-106 to **NYG +103 / WAS -113**, so WAS +2.5 is now the favored side of the number (NYG no-vig 48.2%).
- **Total.** It dropped 41.5 to 40.5 (DK/FD) and 41.0 to 40.5 (Pinnacle), even though CLEATZ shows 64% of tickets and 95% of handle on the Over. That is reverse movement toward the Under.
- These are first-seen-by-pipeline numbers, not true openers.

## 6. Brainstorm (8 angles) and critical review
| # | Angle | Review | Case against |
|---|---|---|---|
| 1 | Rain (75-78%) cuts pass efficiency, so Under 40.5 | **KEEP (Lean, low)** | Both red-zone defenses are bottom-3 (NYG 31st, WAS 29th TD rate allowed), so drives that get there score 7. The preview is at 51.9% Over. |
| 2 | WAS last on 3rd down (31.1%) vs NYG 11th; supports NYG / WAS team total under | **WEAKEN** | Reverse movement and the Pinnacle flip point at WAS. The preview has WAS at 21.2. |
| 3 | NYG pass D elite vs WAS WRs, so Diggs/Williams unders | **WEAKEN** to flag | Defender unverified (G-DEF). Burks out would concentrate targets. |
| 4 | WAS D 29th vs TEs, so Likely overs | **WEAKEN** to flag | G-DEF fail. Rain cuts his yards-per-target to 5.9. Theo Johnson takes TE2 snaps. |
| 5 | NYG pass pro 28th (9% sacks) vs WAS 42.6% blitz rate: drive killers | **WEAKEN** | WAS pressure rate is only 25th. McCarthy's 63-attempt sample is small. |
| 6 | Reverse movement plus Pinnacle flip: fade the public NYG side | **KEEP as caution** (main reason the side is Pass) | Not a buy signal without a model edge. The ML only moved about 10-14 cents. |
| 7 | Skattebo back from hamstring with a capped workload: rushing under | **Flag only** (G-RB) | No designation, two full practices. 18 touches last game. |
| 8 | McCarthy at 9.87 YPA on 63 attempts will regress, hurting NYG passing overs | **KEEP** (lowers Nabers/Likely ladders) | Hip was a full practice. WAS pass D is 27th. |
| 9 | Daniels scrambles more in rain and in negative script | **DROP** | Left-elbow listing. 25+ rushing in only 3 of 6 games (31/69/103 vs 10/23/16). |

## 7. Inactives kill-switch list (check about 6:45 PM ET)
| If... | Then |
|---|---|
| Skattebo inactive | Every Skattebo leg voids (FD reprices the SGP). Singletary/Harris split. Under 40.5 slightly stronger. |
| McCarthy inactive (Winston starts) | NYG passing ladders drop (Winston 6.19 YPA, 5 INT). Rebuild every NYG receiving read. Side moves further toward WAS. |
| Nabers or Likely inactive | All NYG pass-catcher legs reprice. The other one gains targets. |
| Burks **active** | Williams, Okonkwo and Diggs lose about 3.5 targets combined (hurts Slip D and the screenshot slip's Diggs leg). |
| Burks inactive (expected per ESPN) | Small target bump for Williams and Okonkwo. |
| Daniels limited or inactive | Everything on the WAS side reprices (Mariota). |
| White inactive / Ekeler role change | White 25+ voids. Ekeler/Allen split. |
| NYG LB Harrison out (Q) | Small: WAS RB/TE short game. |
| CB Colton Hood (ESPN Out vs official FP) or Amik Robertson (LP Wed) | Coverage changes, though receiving legs are gate-failed anyway. |
| Weather change (NWS rain under 50%) | Withdraw the Under lean. |

## 8. Slip grades
All leg probabilities are closed-form and market-anchored. "Joint" multiplies the legs as if independent; same-player and same-team correlation pushes the true joint higher, so a range is given. The price is the SGP total as logged. FD alt-ladder leg prices are MISSING.

**bet-log.csv TNF pending:** 4 slips, 31 leg rows. Total pending stake **$318** (A $125 + B $18 + C $75 + D $100). The screenshot slip (7-pick +950 boosted to +1235, $65) is **not** in bet-log.csv: there is no matching ID, price, stake or leg set, so it is a **fifth slip**. With it, TNF exposure is $383. bet-log.csv was not edited.

| Slip | Price / stake | Legs that pass the gates | Rule-fail legs | Joint (indep / adj) | Book implied | EV | Verdict |
|---|---|---|---|---|---|---|---|
| D (6 legs) | +335 / $100 | none | Skattebo 30+ R+R (G-RB); Likely 3+ rec, Nabers 60+, Diggs 3+ rec, Williams 15+, Fields 10+ (G-DEF) | 18.9% / 19-24% | 23.0% | -$18 | **Gate FAIL, 6/6 legs.** Least-bad price. C+ on price, FAIL on rules |
| A (8 legs) | +413 / $125 | Under 54.5 (~86%) | Skattebo 25+ rush (G-RB); Likely 20+, Nabers 40+, Fields 15+, Okonkwo 15+, Williams 20+, Diggs 25+ (G-DEF) | 13.6% / 14-19% | 19.5% | -$38 | **Gate FAIL, 7/8.** C- |
| C (7 legs) | +559 / $75 | NYG 1H 3-way (~45-50%, no price) | Skattebo 40+ R+R (G-RB); Likely 4+ rec, Likely 30+, Diggs 3+ rec, Williams 15+, Nabers 60+ (G-DEF) | 5.4% / 5-9% | 15.2% | -$48 | **Gate FAIL, 6/7.** D |
| B (10 legs) | +1179 / $18 | Under 55.5 (~87.5%) | Skattebo 30+ R+R (G-RB); 8 receiving legs (G-DEF) | 2.0% / 2-5% | 7.8% | -$14 | **Gate FAIL, 9/10.** F (lottery) |
| **Screenshot (7 legs)** | +950, 30% boost to +1235 on $10; $65 stake, $711 payout (effective 9.94-to-1, implied 9.1%) | Daniels 25+ rush (QB, not covered by G-RB; ~47%, Lean cap) | Skattebo 50+ R+R (~80%) and White 25+ rush (~76%) (G-RB); Fields 2+ rec (~72%), Diggs 30+ (~62%), Likely 40+ (~56%), Nabers 50+ (~63%) (G-DEF) | 4.5% / 5-8% | 9.1% | about -$33 (-$13 to -$33 depending on correlation) | **Gate FAIL, 6/7.** D. Daniels 25+ is the weakest leg; Likely 40+ is next. |

## 9. Phase / status ledger
PASS (auto): 1, 2, 3, 5, 11, 12. PARTIAL: 4, 6, 7, 8 (who-covers-whom MISSING), 9, 10, 13 (no FD alt ladders, no true opener), 14 (script-based plus Ghost6 10k preview; official 100k pending about 7:10 PM ET). PENDING: 15 (inactives about 6:45 PM ET).

## Sources and freshness (ET)
- Packet: nfl-matchup-database fb9167b, 5:11 PM ET (DK/FD/Pinnacle prices, NWS weather, nflverse PBP/rosters/injuries, FTN via nflverse, PFR).
- W1-9 PBP: data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet (carry shares, Daniels/White/Skattebo/Fields logs).
- Official injury reports: giants.com (10:10 AM ET) and commanders.com reg-10, both read about 5:35 PM ET.
- Reporters (about 5:35 PM ET): NBC Sports (Nov 11), theScore (Schefter), NFL.com (Rapoport).
- McLaurin IR: commanders.com, Oct 28.
- Splits: CLEATZ (5:22 PM and 10:52 AM ET), SI, VSiN.
- Ghost6 10k pre-gate preview: main fb9167b, seed 20261112, n=10000 (`ghost6_10k_preview_result.json`, copied from /workspace/tnf_preview/result.json at 5:38 PM ET).
- PFF/FTN model: not used (owner-supplied only).

Research only

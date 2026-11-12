# CHI@SEA MNF 2026-11-02: JSN 89.5/99.5 + Kupp/Barner rec ladders. Tag: fixed-model, copies only
Sim: tools/sim_v6_fix/sim_v6.py (staged Bias fix, not live), 3 models x 100k, seed 20261101, spread SEA -3, n_games 7. Same result with SIMV6_SRC=r2/src and with the default sim_v6_src. The JSN 89.5 run reproduces the earlier numbers (.704/.574/.647).
Odds: The Odds API pull at 6:10 AM ET (odds_m0610.csv). FD quotes are from 6:10 AM ET and DK from 6:09 AM ET. In-play filter is on and 0 rows were dropped. Alt-rung no-vig = alt implied / main-market overround.

| Leg | FD price | FD nv | DK price | DK nv | MC p (med) | Bias p (med) | GR p (med) | Edge vs FD (MC/Bias/GR, pp) | Clear +3 | §7 |
|---|---|---|---|---|---|---|---|---|---|---|
| JSN O89.5 yds | -166 | .588 | -161 | .584 | .704 (119.0) | .574 (101.2) | .647 (115.4) | +11.6 / -1.4 / +5.9 | 2/3 | 3/4 (76,102,134,150) |
| JSN O99.5 yds | -114 alt / -113 main | .500 | -118 alt | .512 | .640 | .509 | .592 | +14.0 / +0.9 / +9.2 | 2/3 | 3/4 |
| Kupp O1.5 rec | -490 | .777 | -434 | .768 | .682 (2) | .571 (2) | .691 (2) | -9.5 / -20.6 / -8.6 | 0/3 | 3/4 (1,2,5,2) |
| Barner O2.5 rec | -210 | .634 | -196 | .625 | .505 (3) | .509 (3) | .487 (2) | -12.9 / -12.5 / -14.7 | 0/3 | 3/4 (1,3,3,4) |
| Barner O3.5 rec | +124 | .417 | +127 | .416 | .317 | .291 | .330 | -10.0 / -12.6 / -8.7 | 0/3 | 1/4 |

I verified §7 from the pbp (Weeks 4-7, all Darnold-only starts). JSN went 76, 102, 134, 150. Kupp caught 1, 2, 5, 2. Barner caught 1, 3, 3, 4.

Verdicts:
- JSN O89.5: 2 of 3 models clear, so it's press-eligible on the model gate. Under R1, MC is far above the book, so it goes to MANUAL_REVIEW.
- JSN O99.5: 2 of 3 models clear (Bias +0.9 does not), so it's press-eligible on the model gate. MANUAL_REVIEW under R1. This is the larger edge of the two rungs.
- Kupp O1.5: CUT. The models are 9-21pp under the book, even though §7 passes.
- Barner O2.5: CUT. The models are 13-15pp under the book.
- Barner O3.5: CUT. It fails both the models and §7.

Caveats:
- Bias-dup fix is not live (swap runs 11:45 PM ET). Results are copies only.
- The edges are raw model p minus no-vig. No calibration shrink layer is applied beyond what is inside sim_v6.
- Injury inputs are from the r2 pull this morning and go stale under the 6h rule around 11 AM ET. Muhammad/inactives are not known yet.
- Odds go stale after 1h, so reprice at 6:50 PM ET.

## Swift (CHI) receptions. Odds pulled 6:38 AM ET (odds_m0638.csv), fixed-model, copies only
| Leg | FD price / no-vig | DK price / no-vig | MC p (med) | Bias p (med) | GR p (med) | Raw edge vs FD (MC/Bias/GR, pp) | Clear +3 | §7 (Caleb Wks 1,2,6,7: 1,5,4,4) |
|---|---|---|---|---|---|---|---|---|
| Swift O2.5 rec | -174 alt (main 3.5 +140/-188, overround 1.070) / .594 | -175/+137 main / .601 | .681 (3) | .674 (3) | .655 (3) | +8.7 / +8.0 / +6.1 | 3/3 | 3/4 |
| Swift O3.5 rec | +140 main, +138 alt / .390 | +142 alt / .391 | .469 | .463 | .477 | +7.9 / +7.3 / +8.7 | 3/3 | 3/4 |

- Shrink: no fixed shrink factor is defined. The nfl-betting-script SKILL (§ calibration) only shrinks a probability bucket if it has run 10+ pts under its sims for 3+ weeks. Raw edges are reported above.
- Underdog check: PASS / not a block. §14 "could trail" rules only block unders. CHI +3 trailing feeds RB check-down volume, which is a tailwind for these overs. The run_gate DOG RB EXCEPTION only waives blocks on underdog RB legs.
- Engine inputs: the sim uses the engine's own pbp features. The non-blitz/blitz target split (14.5% / 6%) and SEA's RB allowance are not separate model inputs, so they serve as context only.
- RB coverage LB: UNVERIFIED. pbp_participation_2026.parquet in r2/src is corrupt (bad parquet footer), and there is no public source this run.

## SEA RB-coverage defender (Swift named-defender check), 6:45 AM ET
- SEA vs RB targets, Weeks 1-7 (nflverse pbp in r2/src): 44 targets, 38 catches, 223 yds (86% catch rate, 5.1 yds/catch).
- Proxy = first tackler on RB catches: E.Jones 7 solo + 1 assist, D.Witherspoon 4+3 (CB), D.Thomas 3+2, J.Jobe 3, N.Emmanwori 3. pass_defense_1 on RB targets: only U.Nwosu (2 PBUs).
- Named LB (proxy, not true coverage data): **Ernest Jones IV** (primary), **Drake Thomas** (secondary). These are not on the latest injury report, so presumed active. Tyrice Knight is listed with no status. Nwosu is Doubtful and Patrick O'Connell is Questionable.
- Not available: PFR SEA advanced page (fetch timed out; the r2 copy is a 5KB stub). nflverse pbp_participation_2026 returns 404 publicly (the local copy is corrupt). True targets/catches allowed in coverage per LB are UNVERIFIED.
- Read: supports Swift overs. SEA allows short, high-percentage RB catches, and the coverage LBs make tackles after the catch rather than breaking up passes. Caution: this is a tackle proxy, not coverage attribution.

## PFR second source: SEA LB pass coverage (Firecrawl scrape 6:40 AM ET, raw: pfr_sea_adv_fc.json/.html)
Source: https://www.pro-football-reference.com/teams/sea/2026_advanced.htm (Defense advanced, Pass Coverage). These are TOTAL targets in coverage, not split by RB.
| LB | G/GS | Tgt | Cmp | Cmp% | Yds | Y/Cmp | Y/Tgt | TD | INT | Rat | DADOT | YAC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ernest Jones IV | 7/7 | 38 | 24 | 63.2 | 190 | 7.9 | 5.0 | 0 | 1 | 64.6 | 4.7 | 110 |
| Drake Thomas | 5/5 | 17 | 10 | 58.8 | 72 | 7.2 | 4.2 | 1 | 1 | 63.8 | 2.1 | 65 |
| Tyrice Knight | 7/3 | 7 | 5 | 71.4 | 31 | 6.2 | 4.4 | 0 | 0 | 80.1 | 4.1 | 26 |
- Agreement with pbp proxy: YES on who covers. Jones is the most-targeted SEA coverage LB (38, team high), then Thomas (17), matching the tackle proxy order (Jones 7 solo, Thomas 3). Short DADOT (2.1-4.7), with YAC making up most of the yards, fits RB/TE check-down coverage.
- Caution for Swift overs: both LBs hold receivers to about 63-64% completion and 4-5 yds per target with low ratings. That's stingy per target, but the volume is there (SEA allows 6.29 RB tgt/g). Read: supports catch-count overs (volume and the 86% RB catch rate overall), and is neutral-to-negative for yardage.
- No public positional split was found (PFR does not split coverage targets by receiver position).

## Burden (CHI) receptions: fixed-model, copies only. Odds 6:50 AM ET (odds_m0650.csv), raw_burden.json
Shrink p' = 0.5 + 0.7(p - 0.5). FD main 4.5 is +118/-158 (overround 1.071). DK main 4.5 is +119/-152 (overround 1.060).
| Leg | FD / nv | DK / nv | MC p (shr) | Bias p (shr) | GR p (shr) | Raw edge pp | Shrunk edge pp | Clear +3 shrunk | §7 Caleb (5,3,8,4) |
|---|---|---|---|---|---|---|---|---|---|
| O3.5 | -188 alt / .609 | -180 alt / .607 | .642 (.549) | .630 (.541) | .604 (.523) | +3.3/+2.1/-0.5 | -6.0/-6.8/-8.6 | 0/3 | 3/4 |
| O4.5 | +118 main / .428 | +118 alt, +119 main / .431 | .453 (.467) | .440 (.458) | .459 (.471) | +2.5/+1.2/+3.1 | +3.9/+2.9/+4.3 | 2/3 | 2/4 FAIL |
Medians: 4 for all three models. The pbp check confirms the Caleb-game targets (5, 7, 8, 4) and catches (5, 3, 8, 4).
Note: the shrink moves sub-.50 probabilities UP toward .50, so the O4.5 "edge" after shrink is created by the shrink itself (raw edge is only 1-3pp).
Verdicts:
- O3.5: CUT. No model clears after shrink, and only MC clears raw (+3.3).
- O4.5: CUT. It fails §7 (2/4), and its edge comes from the shrink.

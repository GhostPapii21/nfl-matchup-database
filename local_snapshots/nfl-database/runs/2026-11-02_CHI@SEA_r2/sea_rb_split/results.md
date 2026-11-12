# SEA RB split — CHI@SEA MNF 2026-11-02 8:15 PM ET (Tag: fixed-model, copies only)
Written 8:35 AM ET. Odds: The Odds API pulled 8:18 AM ET (odds_m0818.csv, 0 in-play rows) -> STALE after 9:18 AM ET. Sims: sims.py -> raw_sims.json (tools/sim_v6_fix unedited, 3x100k, seed 20261101, SEA -3). Usage: usage.py -> usage.md (nflverse pbp 2026 Wk1-7, pbp 2025, snaps 2026).
NOT VETTED by Ghost6.

## 1. Jadarian Price status: STILL ON IR (as of 8:20 AM ET)
- seahawks.com/team/transactions (fetched 8:20 AM ET): last Price entry 10/03 "Placed RB Jadarian Price on injured reserve". No activation through the latest entry (10/27). Charbonnet activated from reserve 10/22.
- Brady Henderson (X, Oct 31 4:47 PM ET): Price "still on IR — also has no game designation, but Macdonald conveyed some uncertainty as to whether he'll be activated this week." https://x.com/BradyHenderson/status/2116633063484748161
- Corbin Smith (X, Oct 31 4:45 PM ET): "isn't on the 53-man roster at this time... Could mean a move is coming." Nov 1 (Oct 31 11:03 PM ET): Macdonald said they had roster decisions to make to activate him.
- Practice: limited Thu, full Fri (Henderson/Condotta, Oct 30 7:16 PM ET).
- No beat post since Nov 1 on activation (X search 8:19 AM ET). Deadline 4 PM ET today. Books still post Price rush 28.5 (FD/DK). RECHECK at 4 PM ET.

## 2. SEA backfield usage (2026, Darnold = Wk3-7)
| Wk | Wilson car/sh/snap% | Holani car/tgt/snap% | Other |
|---|---|---|---|
| 3 | 9 (.50) 36% | 3 car, 5 tgt (5-48) 36% | Price 5 car 28% |
| 4 | 21 (.64) 60% | 7, 1 tgt 37% | — |
| 5 | 20 (.77) 59% | 4, 4 tgt (4-24) 41% | — |
| 6 | 14 (.54) 32% | 5, 0 tgt 58% (trailing) | V.Jones 4 car |
| 7 | 24 (.59) 48% | 5, 2 tgt 36% | V.Jones 5 car |
- Wilson = early-down back (~18 car/g with Darnold). Holani = passing-down/receiving back (12 of 14 RB targets in Darnold games ~2.4 tgt/g, ~36-58% snaps). V.Jones OUT tonight.
- With Price on IR: 3-back rotation (Charbonnet + Wilson + Holani), not two. Charbonnet's 2025 role was the early-down/goal-line role Wilson now holds, so Wilson's carries are the ones at risk.
- Workload: Mike-Shawn Dugar (X, Oct 31 4:55 PM ET): "Even if they're on pitch counts, having Jadarian Price & Zach Charbonnet should allow for a good eval." No direct Macdonald/OC quote on a Charbonnet snap count found -> MISSING. Charbonnet was LIMITED Fri after 4 full practices (Henderson). Treat as capped.

## 3. Comps
- Josh Jacobs 2026 return (Wk7): 52% snaps, 11 car-36, 7 tgt 5-55. Wk8: 71%, 21-39, 6-6-13. Jacobs is a lead back with ~58-81% carry share and 15% target share; Charbonnet never had that role.
- Charbonnet 2025 (16 g): 11.6 car (39% share), 45.6 rush yds, 1.5 tgt (5% share), 1.25 rec, 9.0 rec yds per game. 2+ rec in 7/16; 0 targets in 5/16. Rush yds >32.5 in 11/16; rec yds >7.5 in 8/16. (2025 snap% not in local file -> MISSING.) He was a 2-down/goal-line back, not a receiving back. Jacobs comp does NOT transfer to receptions.
- §7: 0 games in 2026 (and 0 with Darnold) -> no sample -> §7 FAIL = CUT. MANUAL_REVIEW does not cover it: R1 converts only P14-edge cuts on PRESS legs, and press tier isn't live until runs dated 11-05; §7 is not a P14 cut. sim_v6 can't run him either ("no active games before cutoff") -> SIMULATION NOT RUN. Only path is Rico/Ghost6 overriding by hand, outside the gate.

## 4. Charbonnet receptions angle — CUT
- CHI allows 3.7 RB rec/g (25th), 35.3 RB rec ypg; top-3 man rate (Sharp 29.9%, StatRankings 39.4% #9). SEA RB target rate falls to .04-.10 vs man-heavier D (DEN/KC), ~.18 vs zone (sea_rb_targets_why.md).
- Pressure -> checkdowns: Darnold blitz/pressure target split by player is MISSING (FTN blitzer join returned zeros; no public pressure field in pbp). CHI's pressure is mostly 4-man with 7 dropping, which takes away the checkdown more than it creates one. No evidence that pressure raises SEA RB targets.
- Even if checkdowns rise, Holani (the receiving back) gets them, not Charbonnet (5% share in 2025).
- Named CHI defender: not mapped (LB/S coverage numbers not pulled) -> P4 MISSING -> cut regardless.
- FD Rec O1.5 +134 / U -180 -> no-vig over .399. 2025 hit rate 7/16 = .44 at full role; capped workload + CHI man + Holani pull it below .40. No edge. FD rec yds 7.5 -113/-113 (nv .500); 2025 8/16 = .50 -> fair, no edge.

## 5. Lines (FD price of record, DK comparison, pulled 8:18 AM ET)
| Player | Market | FD | DK |
|---|---|---|---|
| Charbonnet | rush yds | 32.5 -113/-113; alts 24.5 -198, 29.5 -138, 19.5 -290 | 32.5 -115/-109 |
| Charbonnet | rec | 1.5 +134/-180 | 1.5 +127/-162; 2.5 +411 |
| Charbonnet | rec yds | 7.5 -113/-113 | 7.5 -118/-107 |
| Charbonnet | rush+rec | 44.5 -113/-113 | 45.5 -111/-114; 39.5 -157 |
| Wilson | rush yds | 19.5 -113/-113; alts 14.5 -180, 9.5 -310 | 19.5 -113/-111 |
| Price | rush yds | 28.5 -113/-113 | 28.5 -110/-114 |
| Holani | all | NOLINE (FD and DK) | NOLINE |
| Any | rush att | NOLINE (not in feed) | NOLINE |
Overround on -113/-113 = 1.061; alt nv = implied/1.061.

## 6. Models (sim_v6_fix 3x100k, seed 20261101). p = MC / Bias / GR, median in ()
Wilson scenarios use the engine's carry_boost (target share x ~27 SEA RB car/g / his weighted 17.2 car).
| Leg | Scenario | MC | Bias | GR | nv | raw | G6 shrink | x0.7 |
|---|---|---|---|---|---|---|---|---|
| Wilson rush O19.5 | base (his Wk1-7 role) | .950 (64) | .998 (76) | .915 (64) | .500 | +45.4 | +31.8 | +31.8 |
| Wilson rush O19.5 | Price IR, Charb capped (W 45%) | .868 (44) | .970 (53) | .831 (44) | .500 | +39.0 | +27.3 | +27.3 |
| Wilson rush O19.5 | Price IR, Charb full (W 35%) | .773 (34) | .900 (40) | .738 (34) | .500 | +30.4 | +21.3 | +21.3 |
| Wilson rush O19.5 | Price active (W 28%) | .663 (27) | .787 (31) | .640 (27) | .500 | +19.7 | +13.8 | +13.8 |
| Wilson rush O14.5 -180 (nv .603) | Price active | .760 | .892 | .753 | .603 | +19.1 | +13.4 | +13.4 |
| Price rush O28.5 (nv .500)* | if activated, base | ~.62/.59/.60 at 29.5; .572/.540/.552 at 32.5 | | | | | | |
| Holani rec O1.5 | base | .504 (2) | .394 (1) | .483 (1) | NOLINE | — | — | — |
| Holani recyds O9.5 | base | .555 (12.6) | .455 (9.3) | .564 (11.9) | NOLINE | — | — | — |
| Charbonnet (all) | — | SIMULATION NOT RUN (0 games in 2026 pbp) | | | | | | |
*Price: 3-game sample, 1 with Darnold.

Read: every Wilson median sits 7-56 yds above a 19.5 market. The book is pricing Wilson at ~5-7 carries, i.e. Charbonnet as the lead early-down back. Our scenarios can't see a role the market expects because Charbonnet has no 2026 data. MODEL-SUSPECT (median 12+ off market main) in every scenario except Price-active (+7). Treat the model edge as a blind spot, not edge.

## 7. Verdict per leg
| Leg | Verdict | Why |
|---|---|---|
| Charbonnet rec O1.5 (+134) | CUT | §7 no sample; SIM NOT RUN; P4 defender MISSING; 5% tgt share 2025; Holani is the receiving back; CHI 25th in RB rec allowed + top-3 man. |
| Charbonnet rec yds O7.5 | CUT | same; 2025 hit .50 = fair. |
| Charbonnet rush O32.5 / alts / rush+rec 44.5 | CUT | §7 no sample; SIM NOT RUN; committee (39% share 2025, now 3 backs) fails 60% rule; capped workload. |
| Charbonnet unders (mirror R2) | CUT | R2 only applies to unders cut for P3/P4/star/P13 reasons; these are §7/no-sim cuts. Also no sim, so no rung can be shown to clear. |
| Wilson rush O19.5 / O14.5 | CUT | MODEL-SUSPECT (median 34-64 vs 19.5 in Price-IR scenarios); 60% carry share only 2 of last 4 (.64,.77 pass; .54,.59 fail) -> committee FAIL; role is being taken by Charbonnet. Not PRESS (press not live before 11-05), so no MANUAL_REVIEW. |
| Wilson rush U19.5 | CUT | all three models put it at 2-35% (p<.45). Mirror over is the cut above. |
| Price rush O28.5 | CUT | still on IR; 1 Darnold game -> §7 impossible; models only ~+5-7 at 29.5 if active. |
| Holani rec/rec yds | CUT | NOLINE at FD/DK; models ~.39-.50 on 1.5 rec; Bias median 1 rec. |

**Bottom line:** No SEA RB leg clears. Price is still on IR (official transactions page, 8:20 AM ET). It's a 3-back committee, not two. Charbonnet has 0 2026 games, so §7 and sim_v6 both block him. The Jacobs comp (52% snaps, 7 targets) doesn't fit: Charbonnet averaged 1.5 targets in 2025, and Holani is Seattle's receiving back. The one real signal is the market: Wilson at 19.5 means books expect Charbonnet to lead on early downs.

## Rechecks
- 4:00 PM ET: Price activation (seahawks.com transactions, beat X). If activated, rerun with the Price-active scenario.
- 6:45 PM ET inactives: Charbonnet active, Holani role, Price.
- Odds go STALE at 9:18 AM ET; re-pull before use.
- Gaps: CHI LB/S per-defender coverage (P4), Darnold pressure target split (P5, FTN join), Charbonnet 2025 snap%, no coach quote on pitch count.

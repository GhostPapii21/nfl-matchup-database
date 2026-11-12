# CONSENSUS card — Ghost6 × BetGuru — Week 8, Sun Nov 1, 2026
Written Sat Oct 31, 2026 ~8:05 PM ET. Nothing posted, messaged or bet. FD prices: fd_now.csv (6:53 PM ET) + BetGuru's no-vig column (7:37 PM ET snapshot).
Note: runs/betguru_20261031T194324/ was **not found** on the box. BetGuru numbers are taken from the card appended to week8/betguru_three_groups_2026-11-01.md.
Ghost6 sims for the new legs: phase_walk/ghost6_bg_legs_sims.json (script /tmp/g6sim3.py, seeded, 100k × 3 models).

## 1. BetGuru's four new legs through Ghost6 Phases 1–10G
| Leg | P1 log (PBP) | P2 matchup / 8A | P3 projection | §14 checks | 9 / 10 | 10G | Verdict |
|---|---|---|---|---|---|---|---|
| Cook 70+ rush (-210) | 57,135,154,75,111,95 (13–25 car); L4 median 103 | BAL run D 3.82 YPC / EPA -0.079 (tough; league 4.33) | 19.5 car × ~4.2 (YPC regressed 50% to league, scaled by opponent) → median 82 = FD main 82.5 | cushion ✓ (103 ≥ 84) | no weather flag (BUF venue not rechecked; GAP) | BUF -3 toss-up 0.85 | PASS gates, **FAILS my edge** |
| K. Walker 80+ rush (-144) | 173,117,70,177,128,36 (Wk7 14-36 at SEA); L4 median 99 | DEN run D 4.72 YPC / EPA +0.031 (soft) | 20 car × ~5.4 → median 100 vs FD main 85.5 | cushion ✓ barely (99 ≥ 96) | DEN 60–62F, 6–8 mph, 11% | KC -1.5 toss-up 0.85 (swing: KC pass rate) | PASS, **model-suspect** (both engines ~15 yds over market) |
| Higgins 60+ yds (-186) | 59,95,90,157,22,148; targets L3 16,4,7 ✓ | **8A:** TEN CBs Flott 9-6 66.7%, 9.2 YPT; A. Taylor 15-13 86.7%, 6.9; M. Harris 16-11 68.8%, 7.3 (PFR cache Oct 29, STALE). Soft, no shadow evidence → PASS | 8.3 tgt × .66 → median 78 vs FD main 70.5 | L4 median ~119 ≥ 72 ✓ | CIN 70F, calm | CIN -12.5 (BG uses -10) blowout 1.00; Q4-sit risk | **BARRED by slip rule** (see §3) |
| Puka 8+ rec (-138) | catches 5,9,17,6,8 (5 games); targets 9,12,24,7,10 | **8A:** LAC Tarheeb Still 11-5 45.5%, 6.5 YPT (tough); D. Jackson (Q) 9-6 66.7%, 7.7; Cam Hart 16-10 62.5%, 10.4 YPT. Mixed → PASS-CAUTION; depends on D. Jackson status | 12.9 tgt × .726 → mean 9.4, median 9 (bias 8) vs FD 7.5 | catch rule: 5+ tgt in 3 of 4 ✓; no teammate ≥28% (Adams IR) ✓ | indoor | LAR -6.5 moderate fav, possession 1.00 | PASS |

Puka 8+ and Puka 70+ are the same player: card at most one.

## 2. Engine reconciliation (union), same rule for both sides
Rule: edge = sim avg − FD no-vig. **Shrink-30**: p' = 0.5 + 0.7·(p − 0.5), then edge = p' − no-vig. PASS needs raw ≥ +3 **and** shrink edge > 0. (BetGuru's own shrink-30 kept Puka at +5.1 unshrunk, so his method differs; this applies one formula to both.)
| Leg | FD | No-vig | G6 MC/Bias/GR → avg | G6 raw / shrink | BG MC/Bias/GR → avg | BG raw / shrink | Both pass? |
|---|---|---|---|---|---|---|---|
| Walker 80+ rush | -144 | .556 | .639/.605/.625 → .623 | +6.7 / +3.0 | .730/.616/.688 → .678 | +12.2 / +6.9 | **YES** |
| Puka 8+ rec | -138 | .542 | .619/.535/.613 → .589 | +4.7 / +2.0 | .622/.531/.626 → .593 | +5.1 / +2.3 | **YES** |
| Gibbs 70+ rush | -250 | .673 | .713/.677/.697 → .696 | +2.3 / −8.6 | .812/.701/.750 → .754 | +8.1 / +0.5 | NO (disputed) |
| Cook 70+ rush | -210 | .638 | .615/.580/.608 → .601 | −3.7 / −6.7 | .774/.654/.736 → .722 | +8.4 / +1.7 | NO (disputed) |
| Higgins 60+ yds | -186 | .613 | .651/.622/.642 → .638 | +2.5 / −1.6 | .748/.652/.750 → .716 | +10.3 / +3.8 | NO (disputed; also barred) |
| Flournoy 3+ rec | -240 | .660 | .683/.622/.676 → .660 | 0.0 / −4.8 | .674 avg | +1.4 / −3.8 | NO (both) |
| Tuten 60+ rush | -158 | .577 | .580/.544/.572 → .565 | −1.2 / −2.2 | .572 | −0.5 / −2.3 | NO (both) |
| Metcalf 40+ yds | -225 | .652 | .618/.594/.616 → .609 | −4.3 / −10.2 | .534 | −11.8 / −16.6 | NO (both) |
| Puka 70+ yds | -290 | .701 | .683/.649/.673 → .668 | −3.3 / −18.2 | .629 | −7.2 / −21.1 | NO (both) |
| A. Williams 3+ | -200 | .623 | .622/.556/.617 → .598 | −2.5 / −5.4 | .550 | −7.3 / −8.8 | NO (both) |
| Gibbs R+R 90+/100+ | not posted | — | .713 / .628 | — | .836 (90+) | — | GAP (unpriced) |
My previous card compared against vig-in implied prices. Against no-vig, all five of my priced legs still fail. **I withdraw them.**

**Why the engines differ**
- **Volume.** Both use similar carry and target means; BetGuru's do not appear lower. The gap is in medians. On rushing, BetGuru runs 10–20 yds above FD mains by his own note. Mine: Cook 82 (market 82.5), Gibbs 94 (87.5), Walker 100 (85.5).
- **Efficiency.** I regress YPC 50% toward league and scale by the opponent's YPC allowed (BAL 3.82 → Cook down; DEN 4.72 → Walker up). That's better supported: RB YPC stabilizes slowly (6 games is noise-dominated, e.g. Walker 36 on 14 carries in Wk7, Gibbs 46 on 15 in Wk4) and lines up with the market. BetGuru's higher rushing medians look like unregressed season YPC.
- **Game randomness.** Mine is mean-preserving: a shared team-volume lognormal (σ .22) plus a spread-signed script tilt, so GR ≈ MC. BetGuru's GR is systematically higher (e.g. McBride .932, Flournoy .87, Downs .89), so it shifts the mean up instead of adding variance. A randomness model that raises hit rates on nearly every over isn't supported. Mine is the better-founded assumption.
- **Dispersion.** I use NB volume (gamma shape 8) plus bootstrapped per-play yards from 2026 PBP, which may be slightly wide. Neither engine is calibrated (no logged graded weeks yet).

## 3. Correlation risk
- **Three RB rushing overs** (Gibbs, Cook, Walker) on BetGuru's card: model error is shared (the same YPC assumption pushes all three above market), so the three aren't independent. His .157 joint is overstated; plus all three are toss-up spreads (0.85) where a negative script hits rushing first.
- **Gibbs:** Ticket 2 has Gibbs 5+ receptions. Same player, so injury or snaps would sink both. Rico allows the different prop. Flag.
- **Cook:** Ticket 2 has Cook rush+rec. Rush 70+ makes up most of rush+rec, so the two are nearly the same outcome and double the exposure. Rico allows it. HIGH flag.
- **Higgins 60+ rec yds vs the open FD SGP's Higgins 50+ rec yds:** this is the **same market** (Alternate Receiving Yds), a higher rung. 60+ hitting implies 50+ hits; 50+ missing means both miss. Skill §11 says "no player on more than one slip, including placed" → **BARRED**, not just flagged.
- **Walker + Puka:** different games, no shared QB. Independent.

## 4. CONSENSUS card (passes both engines' edge test + every gate)
| # | Leg | FD | G6 avg | BG avg | No-vig | Gates |
|---|---|---|---|---|---|---|
| 1 | Kenneth Walker III 80+ rush yds (KC -1.5 @ DEN) | -144 | .623 | .678 | .556 | P1–4 ✓, 9 ✓ (DEN 60F, 8 mph), 10 ✓ (PFR STALE), 10G toss-up 0.85 ✓; CAUTION: both engines are ~15 yds above the FD main 85.5 |
| 2 | Puka Nacua 8+ receptions (LAR -6.5 vs LAC) | -138 | .589 | .593 | .542 | P1–4 ✓, 8A PASS-CAUTION, 10G 1.00 ✓; bias median 8 = rung |
**2 legs, ≈ +192** (1.694 × 1.725 = 2.92). Hit: G6 .367 (1 in 2.7), BG .402 (1 in 2.5). Book no-vig .301 → both engines have the card +EV. No padding to six: no other leg passes both engines.
**Inactives 11:30 AM ET (Puka/Walker at 4:05/4:25 → also recheck 2:35 PM):**
- Drop Puka if he's limited or downgraded, or if D. Jackson's status flips the coverage. (D. Jackson out raises Puka; Still shadowing is a risk.)
- Drop Walker if KC lists another RB active in a split role, or if his Wk7 14-carry usage repeats in the actives news.
- Reprice either leg on a 20-cent move.

## 5. Disputed legs (BetGuru passes, Ghost6 fails)
| Leg | BetGuru | Ghost6 | Crux |
|---|---|---|---|
| Gibbs 70+ rush -250 | .754, +8.1 / +0.5 | .696, +2.3 / −8.6 | YPC vs MIN (#1 EPA D per BG); my median 94 vs market 87.5 |
| Cook 70+ rush -210 | .722, +8.4 / +1.7 | .601, −3.7 | BAL 3.82 YPC allowed; my median 82 = market |
| Higgins 60+ yds -186 | .716, +10.3 / +3.8 | .638, +2.5 / −1.6 | blowout/Q4-sit; **barred anyway** (SGP 50+) |
| Gibbs R+R 90+ | .836 | .713 | unpriced |
Rejected by both: Flournoy 3+, Tuten 60+, Metcalf 40+, Puka 70+, A. Williams 3+.
Film reads stay UNVERIFIED (BetGuru reliability note).

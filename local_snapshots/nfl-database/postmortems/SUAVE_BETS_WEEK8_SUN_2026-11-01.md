# Suave Bets NFL Week 8 Sunday postmortem (2026-11-01)
Written 2026-11-01 ~10:50 PM ET by Blitz for Rico (requested via Einstein). READ-ONLY inputs:
- Picks: /workspace/sb-grades/data/grades/nfl-week8-sun.json (11 legs, sourceBot BetGuru, priced FD 2026-10-31 ~10:05 AM ET)
- Ledger: /workspace/sb-grades/results/ledger.json (BetGuru grades, graded 2026-11-01 10:28 PM ET from ESPN summary boxes)
- Our finals: playlogs/2026_wk8/*_box.json, *_script.md, *_plays.md (ESPN summary API, pulled after finals)
- Reused (not redone): 2026-11-01_1pm.md, 2026-11-01_4pm.md, RB_MISSES, WEEK8_SUNDAY_1PM, WEEK8_SUNDAY_MISSED_EDGES (+BETGURU_XCHECK), WEEK8_DEFENSE_DISSECTION, backtests/{p6_rush_exception,ol_dl_gap,rb_rec_script}

## 0. Verification
All 11 actuals and results in the ledger match our final ESPN boxes. Record confirmed **Sunday 6-5**; Week 8 9-6 with TNF (ledger summary). By grade, Sunday only: **B 2-2, B- 2-0, C+ 2-3** (confirmed from the pick file grades; the ledger's by_grade summary includes TNF, so it shows B 3-2, B- 2-1, C 1-0, C+ 3-3).
Data notes: our 1 PM postmortem tables were built from near-final boxes before OT (McBride 6-64, J. Williams 23-54, Higgins "100"). Finals are McBride 7-72 on 8 tgt, Williams 24-56, Higgins 10-155. The ESPN finals below win.

Market check: the summed break-even probability of the 11 FD prices is **≈5.97 expected wins; actual 6**. Flat 1u: **+0.61u**. The card did exactly what the market priced. This week shows no edge either way.

## 1. Per-leg verdicts
| # | Leg (grade, FD) | Actual | Result | Verdict |
|-|-|-|-|-|
|1|Chris Godwin Jr. 4+ rec (B, -225)|0 rec, 1 tgt|MISS|**Weather/script.** Rain game (5.7 mm, gusts 26; ESPN 76% precip). TB ran 56 times and threw **3** passes. Godwin's one target was Q1 4:10, "B.Mayfield pass incomplete deep left to C.Godwin". It was not a slot in-breaker, so the "Cover 3 in-breakers" reason never came into play. Today's weather rule (50%+ / 20+ gusts) would have cut it; it is already a regression fixture. Not randomness.|
|2|Trey McBride 8+ rec (B, -122)|7-72-1 on 8 tgt|MISS by 1|**Rung choice plus a QB change.** Brissett went 10/23 and was replaced by Minshew in Q3. McBride had 2 catches from Brissett (Q1 9:00, Q2 2:30) and 5 from Minshew. His last target, Q5 9:22 incomplete (M.Hooker), was the 8th-catch chance. The script read (ARI trailing) was right: ARI threw 46. **BetGuru's own Sat board had McBride 7+ (-225); it would have hit.** The card used the 8+ "middle rung" against the low-rung rule.|
|3|Chase Brown 4+ rec (B, -102)|8-46 on 9 tgt|HIT|**Right result, wrong reason.** The rationale was "role holds in a CIN blowout". The game was actually a 43-36 OT shootout with Burrow at 48 att. Volume came from pass volume, not a blowout. Luck on the script, but a solid floor (19% target share).|
|4|Mason Taylor 3+ rec (B, -138)|3-19 on 5 tgt|HIT (exact)|**Thin hit.** Catches came at Q2 10:44, Q2 9:22 and Q3 2:21. Two late targets fell incomplete (Q4 4:40 H.Masses, Q4 0:27 deep). G. Wilson (12) and A. Mitchell (9) took 68% of the targets in a 71-pt shootout. The "close game" reason held, but this was a coin-flip margin.|
|5|Puka Nacua 9+ rec (B-, +124)|11-80-1 on 12 tgt|HIT|**For the stated reason.** Alpha share: 12 of 25 LAR targets (48%) in a low-volume blowout (Stafford 25 att). Earned.|
|6|Khalil Shakir 40+ rec yds (B-, -130)|5-64 on 6 tgt|HIT|**Mostly for the reason.** He got volume, though the script was a BUF 36-10 blowout, not the "balanced shootout" predicted (total went 46 under 54.5). He cleared by 24 on a 26-yd long (J.Allen to Shakir, 26 yds). Lamar's Q1 exit created the blowout.|
|7|Bhayshul Tuten 70+ rush (C+, +106)|16-104-1|HIT|**For the stated reason** (JAX -10 positive script; won 42-7). The efficiency was explosive-driven: one 39-yd TD run. Without it he had 15-65. This is the case for the game-script RB rule (our pipeline cut his O59.5 at P7; already fixed).|
|8|Kenneth Walker III 90+ rush (C+, +102)|21-69 (3.3 YPC, long 10)|MISS|**Matchup/efficiency.** Volume was right (88% of KC carries). DEN's front held him to 3.3. KC threw 41 times (64% pass rate) while leading most of the game. E. Johnson took passing downs (5 tgt, 5-128-1, 73-yd TD Q2 7:40). The pick lowered from the model's 100+ to 90+, but even a 70+ rung misses at 69. The model median of 132 was the error. KC run block 28th vs DEN DL ~6th (PFF, use-with-crosscheck). The OL-DL gap rule was already rejected by backtest.|
|9|Tee Higgins 70+ rec yds (C+, -120)|10-155-2 on 11 tgt|HIT|**Right player, wrong script.** The rationale expected a blowout Q4 sit, so the rung was lowered. The game was an OT shootout (TEN led 13-0). He would have hit even at 120+. Volume and the CB mismatch were real; the script was luck.|
|10|Javonte Williams 80+ rush (C+, +100)|24-56 (2.3 YPC, long 6)|MISS|**Efficiency, not volume.** The script read was right (DAL led to Q4, 39 DAL rushes) and so was the volume (24 car, 62%). He got zero runs over 6 yds. 9 of 24 carries went for ≤1 yd, including a goal-line fumble at Q1 2:33 (recovered for a DAL TD) and runs of -2/-1 at the ARZ 4/5. The ARI front (Ma.Wilson, D.Stills, Gibbens) stacked the box against a heavy-personnel run look ("B.Jones reported in as eligible" appears repeatedly). Mostly randomness plus box count, with no injury.|
|11|Zay Flowers 6+ rec (C+, -160)|0 on 5 tgt|MISS|**QB injury.** Lamar was hurt on his first pass, Q1 10:04, which was the incompletion to Flowers. Huntley and then **Joe Fagnano** (QB3) played the rest (BAL QBs 12/26, 91 yds). Flowers' other targets were a Q2 1:21 INT (Igbinosun), Q3 14:54 incomplete short middle, Q3 8:12 incomplete (G.Rousseau defended) and Q3 1:11 incomplete (D.Hamlin). Mostly uncatchable or contested short throws from QB3. Weather was dry (0.0 mm, gusts 11). The pick's own defender note (NB Dee Alford) never showed up in the PBP. The opportunity gate was **MIXED** and the price was the steepest on the card (-160). Our gate cut his O6.5 (P5 blitz rule).|

## 2. Top lessons
1. **Weather/environment is the biggest single killer, and today's rule covers it.** Godwin died on 3 team passes, and the rule would have cut him. Gap: the Suave picks were priced Sat 10 AM with no weather field. The weather gate must run again at T-90 on the Suave card, not just in our pipeline.
2. **Low-rung discipline costs or saves whole legs.** McBride 8+ missed where BetGuru's own 7+ hit. Higgins and Tuten hit easily at their rungs. Every pick says "middle rung", which conflicts with Rico's standing "use low alt rungs" rule.
3. **RB rush overs fail on efficiency, not volume.** Walker had 88% share at 3.3 YPC and Williams 62% share at 2.3. Both volume reads were right. This matches the 4 PM lesson (efficiency floor) and is NOT the rejected OL-DL rule. It asks whether YPC at the line clears against the defense's adjusted YPC allowed.
4. **Returning-QB fragility and QB-dependent receivers.** Flowers' leg relied on Lamar in his first game back after 3 missed games. An injury to the QB zeroes the WR. The pick itself said the model was Huntley-based (stale inputs).
5. **Hits that came from the wrong script are not proof.** Brown and Higgins hit in a shootout the card called a blowout, and Shakir hit in a blowout called a shootout. Grade wins on their rationale so lucky hits don't raise confidence.

## 3. Missed slate edges (no Suave leg)
| Player | Line | Type | Why he won |
|-|-|-|-|
|Bucky Irving TB|27-170-1|RB1 early-down/zone|Rain run-fest (TB 56 rushes); ATL front collapsed in the 2nd half|
|Kenny Gainwell TB|25-140|RB2 committee/change-of-pace|Same game. Volume split near 50/50 in a 56-carry game; never in our pool|
|Mike Washington Jr. LV|25-83|RB1 volume back|LV led the 38-33 shootout late; carry volume. A modest yardage edge only|
|Tony Pollard TEN|21-117-2|RB1 one-cut/zone|TEN led 13-0 early and stayed close; CIN run D soft (7 explosives allowed). Cut at P6|
|Jahmyr Gibbs DET|23-153-1|RB1 home-run/dual|Close game with DET leaning on the run; gate cut (P14 median/§11)|
|Tyler Allgeier ARI|11-147-1|RB power/early-down|Explosive runs vs DAL (3 rush explosives allowed) once Minshew stabilized; cut at P6|
|Michael Wilson ARI|8-111-1 on 15 tgt|WR2 outside/possession (counted as a WR2 here, so the #3/#4 ban doesn't apply)|ARI threw 46 times; Minshew's 2-minute drill (Q4 0:50, 0:27, 0:06 TD)|
|Emmett Johnson KC|5-128-1 (+1-15 rush)|RB2 passing-down/receiving|KC 64% pass rate; 73-yd catch-and-run TD. Never in the pool|
|Braelon Allen NYJ|21-147-1|RB1 power|Shootout with an efficient run game; never in the pool|
|Adonai Mitchell NYJ|7-142-1 on 9 tgt|WR2 vertical|Shootout plus soft LV pass D (9 explosives allowed)|
|Jaylen Warren PIT|17-143-1|RB1 dual|PIT 27-6 control script; P14 median cut|
|Harold Fannin Jr. CLE|10-154 on 12 tgt|TE move/slot|CLE trailing, Watson 39 att; we leaned under|
|Ja'Marr Chase CIN|11-141-1 on 16 tgt|WR1 alpha|Shootout volume (34% share)|
|Darnell Washington PIT|3-94|TE blocking/YAC|Variance (few targets, big YAC)|
Pattern: 9 of 14 are RBs or come from run scripts. Fixes A/D/E/F, the script-RB rule and press already target this. Emmett Johnson, Gainwell and B. Allen were **never in the candidate pool** (pool-construction gap, already logged).

## 4. Grade calibration
B 2-2 (50%), B- 2-0, C+ 2-3 (40%). Implied break-evens by grade: B ≈58%, B- ≈51%, C+ ≈53%. Grades did **not** separate outcomes. B underperformed its prices, and the misses split across B (2) and C+ (3). n=11 is far too small for any conclusion (one leg flips any bucket). The scores are tightly bunched (62-71) on a scale that can't express a real difference. Track across Weeks 8-12 before recalibrating.

## 5. Proposed changes (checked against today's decisions)
| # | Proposal | Status |
|-|-|-|
|1|Run the Phase 11 weather gate again at T-90 on every Suave/BetGuru card leg (Godwin fixture)|**NEW** (the rule exists; applying it to the Suave card is new). No backtest needed; weather rule already adopted|
|2|Suave card rung selection must follow the low-alt-rung rule ("middle rung" → lowest rung clearing break-even). McBride 7+ vs 8+|**NEW** (enforcing an existing rule). A backtest of rung choice across Wk6-8 is advisable|
|3|RB rush-over efficiency floor: sim YPC at the line must clear the defense's adjusted YPC allowed (Walker, Williams)|**NEEDS BACKTEST**. Proposed in the 4 PM postmortem, not yet tested. Distinct from the rejected OL-DL gap|
|4|Returning-QB fragility: a WR/TE leg whose QB is in his first game back after 2+ missed games drops one rung and a caution flag; Huntley-based model inputs = stale|**NEEDS BACKTEST** (was proposed in the 1 PM postmortem as Phase 13 QB-health)|
|5|A published card can't carry a leg whose opportunity gate is MIXED (Flowers)|**NEW**. No backtest needed (consistency rule); Rico's call|
|6|Grade wins on their rationale ("script as predicted? Y/N") in the ledger|**NEW**. Process only|
|7|RB2 receiving backs in high-pass scripts (E. Johnson)|**ALREADY REJECTED** (rb_rec_script backtest). Watch only; retest ~Wk12|
|8|KC OL vs DEN DL for Walker|**ALREADY REJECTED** (ol_dl_gap). Not re-proposed|
|9|Tuten/Gainwell/Irving run-script backs|**ALREADY DONE** (game-script RB rule, fixes A/D/E/F, press tier)|
|10|P6 60% exception (Pollard/Allgeier cuts)|**ALREADY REJECTED**; retest ~Wk12|
|11|PFF inputs (KC run-block 28th)|**ALREADY DONE** (PFF cross-check rule)|
|12|Rule 5|**PENDING RICO**. Not touched|

## 6. Questions / disagreements for BetGuru
1. **Rung choice:** your Sat 7:10 PM board (betguru_three_groups) had McBride **7+ (-225)**, but the Suave card shipped **8+ (-122)**. Who moved the rung, and why "middle rung" on every leg instead of Rico's low-alt-rung rule?
2. **`no_inputs: true`** is set on all 11 picks. What does it mean? Were the props published without the full input set (your board noted the CB/S and route inputs MISSING)?
3. **Flowers** shipped with opportunity verdict **MIXED** and the "model is Huntley-based" caveat at -160. Why was it not cut? Did any QB-health check run?
4. **Weather:** picks were priced Sat 10 AM with no weather field. Was the Godwin leg re-checked against the Sunday rain forecast before publish?
5. **Ledger market labels split one market in two:** "Rush Yds (alt)" (TNF) vs "Rushing Yards (alt)" (Sun), and "Rec Yds (alt)" vs "Receiving Yards (alt)". by_market therefore reports them separately. Can it be normalized?
6. **Ledger by_grade mixes TNF and Sunday** (B 3-2 vs Sunday 2-2). Can we get a per-batch split?
7. The grades themselves: no disagreement. All 11 actuals and results match our ESPN finals.
8. Minor: your xcheck lists PP $20 "Higgins FS ≈37.5" while our 1 PM file says ≈23. One of them is from a pre-OT box. Please confirm which is final.

## BetGuru answers (received Nov 1, 2026, ~10:40 PM ET)
- The card was built by a one-off script (/workspace/sb-grades/incoming/build_1031.py) around 10:05 AM ET Saturday, with rungs typed in by hand. Nothing checked it before or after it shipped: no rung re-pick, weather, QB-health or MIXED gate.
- McBride 8+ was the original hard-coded rung. BetGuru's 7+ board came about 9 hours later and actually cut McBride, but the card was never rebuilt from it. "Middle rung" is a fixed text string on every leg.
- no_inputs: true means the picks shipped without an inputs block, so the app skipped validation (pick-grades.ts lines 119-134). The same flag is on cfb-week9 and nba-oct31.
- Flowers: compare.csv rated him MIXED, but the script prints "opportunity gate: passed" for every leg. No QB-health check exists anywhere in the pipeline.
- Godwin: no weather check ran.
- Market names: proposed grouping on market_key() in grade_results.py (not applied).
- Batch split: a by_batch grouping in the grade_results.py summary (not applied).
- Correction: Higgins fantasy points final = 37.5 HIT (10 rec, 155 yds, 2 TD). Our ~23 came from a box pulled before overtime. The ticket is PP $40 (6-pick), not $20.

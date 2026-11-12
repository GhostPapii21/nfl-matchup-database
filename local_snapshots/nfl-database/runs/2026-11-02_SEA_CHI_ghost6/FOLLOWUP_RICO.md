# Follow-up for Rico: CHI@SEA (Ghost6, independent), 2026-11-02 ~05:30 ET
Sources: [A] nflverse play_by_play_2026 (src/, pulled 05:04 ET, through 11-01). [B] ESPN summary box scores (src/fu/sum_*.json, pulled ~05:20 ET). [C] nflverse snap_counts_2026 (src/fu/snaps.parquet). [D] FanDuel via The Odds API (src/odds.json, 05:05 ET). [A] and [B] agree to the yard on every RB line below.

## 1) CHI run D vs RBs (RB carries only, no QB/WR runs, no 2-pt tries)
| Wk | Opp | Car | Yds | YPC | RBs |
|---|---|---|---|---|---|
| 1 | CAR | 19 | 91 | 4.79 | Hubbard 10-49, Dillon 5-28, Brooks 4-14 |
| 2 | MIN | 25 | 113 | 4.52 | A. Jones 23-105, Dallas 2-8 |
| 3 | PHI | 15 | 82 | 5.47 | Barkley 15-82 |
| 4 | NYJ | 14 | 59 | 4.21 | B. Allen 14-59 |
| 5 | GB | 22 | 64 | 2.91 | Lloyd 10-31, K. Johnson 7-26, Strong 5-7 |
| 6 | ATL | 11 | 62 | 5.64 | Bijan 9-61, B. Robinson 2-1 |
| 7 | NE | 13 | 44 | 3.38 | Stevenson 6-22, Kiner 4-13, Henderson 3-9 |
| **Tot** | | **119** | **515** | **4.33** | league RB YPC 4.18 [A] |

Rico's screenshot lines are all correct. "4.9+" is not: the full season is **4.33**. Weeks 1–4 + 6 come to 84-407 = 4.85; the last two (GB, NE) come to 35-108 = **3.09**. Note that CHI faced only 17 RB carries per game (games got out of hand, or opponents passed).
Seattle side: SEA RBs average **3.58 YPC** (184 carries; 26.3 RB carries/gm) [A]. SEA's own D allows 3.40 to RBs. Matchup estimate: (3.58/4.18)×(4.33/4.18)×4.18 ≈ **3.7 YPC** for SEA RBs tonight. A mildly soft CHI run D does not turn a 3.6-YPC offense into a 4.9 one.

## 2) Seattle backfield
Carries / rush yds by week [A=B]:
| | W1 | W2 | W3 | W4 | W5 | W6 | W7 |
|---|---|---|---|---|---|---|---|
| Wilson | 2-3 | 21-92 | 9-14 | 21-81 | 20-61 | 14-52 | 24-100 |
| Holani | 8-29 | 4-13 | 3-10 | 7-18 | 4-7 | 5-20 | 5-11 |
| Price (IR since W3) | 10-52 | 13-52 | 5-15 | – | – | – | – |
| V. Jones (OUT) | – | – | – | – | – | 4-20 | 5-8 |

Snap % [C]: Wilson 6/41/36/60/59/32/48. Holani 46/26/36/37/41/58/36 (he's the passing-down back: 5 targets in W3, 4 in W5). Price 48/34/28. RB targets are tiny: Wilson 9 total, Holani 14.
- **Charbonnet:** 0 snaps in 2026. He tore his ACL in the Jan 17 divisional round, had surgery Feb 12, was activated from PUP Oct 22, and was inactive W7. This week's practice: Full Thu, Limited Fri, Full Sat; no designation (ESPN: espn.com/nfl/story/_/id/50340383). In 2025 he was the power back: 730 rush yds, team-high 12 rush TDs, splitting with K. Walker (NFL.com: nfl.com/news/seahawks-rb-zach-charbonnet-knee-off-injury-report-set-for-season-debut-vs-bears).
- **Macdonald quotes** (komonews.com Monday Night Matchup; seahawks.com audio): "He's a three-down back…" and "we have a plan for how much and what types of plays he's going to have… It might waver a little bit." **There is no carry or snap number.**
- **Price** is still on IR. An activation would come Monday (PFT/NBC), and it is not confirmed.
- **Market [D]:** Charbonnet rush 32.5 / rush+rec 44.5 / rec 7.5; Price rush 28.5; Wilson rush 19.5. The book prices Charbonnet as RB1.
- **My read:** Charbonnet is the nominal RB1 on a managed plan, about 35–45% of RB carries (~9–12). Wilson gets ~25–40% (drops ~10 points if Price is activated). Holani keeps third downs. **Confidence is low**: no 2026 data and no stated cap.

**Model re-run** (src: fu_rb_sims.txt; 100k each, seed 20261101). Inputs: SEA RB carries from 2026 [A], Poisson; GR adds a game-margin script with spread -3 and SD 13.5. YPC is the league RB carry distribution × 0.886 matchup multiplier. Shares: Charbonnet U(.30,.50) for MC and Beta(4,6) for GR; Wilson U(.25,.45), minus .12 in the 50% of sims where Price is active. Bias was dropped (it duplicates MC). No-vig at -113/-113 is .500.
| Leg (FD) | MC p / med | GR p / med | Edge MC/GR | Shrunk GR | Verdict |
|---|---|---|---|---|---|
| Charbonnet o32.5 rush | .637 / 38 | .528 / 34 | +13.7 / +2.8 | +2.0 | **CUT**: 1/2 models; §7 has no 2026 games; snap plan unknown |
| Charbonnet o44.5 rush+rec | .630 / 52 | .545 / 48 | +13.0 / +4.5 | +3.2 | **CUT**: §7 (0 games); share is an assumption, not data |
| Wilson o19.5 rush | .669 / 27 | .600 / 24 | +16.9 / +10.0 | +7.0 | **CUT**: §7 4/4 (81, 61, 52, 100), but all came as the lead back. Now Rule 5 backup with the role cut by Charbonnet (and maybe Price); the result depends entirely on my assumed share |
| Price o28.5 | – | – | – | – | **BLOCK**: on IR, not activated |
These sims are assumption-driven (the shares are not observed), so no SEA RB leg is eligible. Re-run after inactives (~6:45 PM ET) only if Price is ruled inactive AND a beat reporter gives a snap or carry number.

## 3) CHI pass D: strong vs weak passing opponents [A, cross-checked with B]
| Wk | Opp (QB) | Att | Yds | YPA | 20+ | EPA/db | Top WR (tgt-rec-yds) |
|---|---|---|---|---|---|---|---|
| 1 | CAR (Young) | 38 | 361 | 9.5 | 5 | +.25 | Coker 9-8-138 (2 TD), McMillan 8-5-75 |
| 5 | GB (Love) | 31 | 367 | 11.8 | 6 | +.48 | Watson 8-6-143 (2 TD), Golden 7-6-123 |
| 6 | ATL (Penix) | 33 | 225 | 6.8 | 4 | -.31 | Dotson 5-3-87, London 10-4-62; Pitts 5-60 (2 TD) |
| 7 | NE (Maye) | 30 | 321 | 10.7 | 2 | +.37 | A.J. Brown 6-3-48; volume went to RB/TE (Stevenson 5-93, Henry 7-71) |
| **Strong** | | 132 | 1274 | **9.65** | 17 (4.3/g) | | Top WR ≥87 yds in 3 of 4 |
| 2 | MIN (Wentz) | 20 | 143 | 7.2 | 2 | +.02 | Jefferson 6-3-55 |
| 3 | PHI | 26 | 153 | 5.9 | 1 | -.72 | D. Smith 8-6-65 |
| 4 | NYJ (G. Smith) | 15 | 119 | 7.9 | 1 | -.27 | I. Williams 2-73 |
| **Weak/low-vol** | | 61 | 415 | **6.80** | 4 (1.3/g) | | Top WR ≤73 |

(Pass yards, att and 20+ counts exclude sacks. ESPN box [B] matches C/ATT/YDS for all seven games.)

**GB game: middle-of-field open or closed.** I found no public per-game MOF or coverage split: Sharp, FTN, NGS and SumerSports only publish season-level numbers. I did not use paywalled PFF/FTN data. The nflverse participation 2026 file (which carries coverage type) is not published. So MOF for W5 is **UNDETERMINED**, and I won't guess. What the public recaps say:
- NGS via Packers Wire: Love went 6/8 on throws of 20+ air yards for 258 yds, the 2nd-most in the NGS era (packerswire.usatoday.com, 2026/10/11).
- SI Packers On SI: Watson's 42 TD was a **bust** ("corner turning Watson loose… safety playing over the top"), which points to a single-high or busted rotation. His 53 TD came on 3rd-and-22, "deep middle", over S Thieneman (packers.com calls it "double coverage", which points to a 2-high or bracket look). Golden had 36 and 50 deep up the sideline as contested catches. Johnson was "beaten twice deep" (SI Bears report card). Muhammad struggled outside after Stevenson's hamstring injury.
- NFL/Savant: Love's aDOT was 9.4 and he was pressured on 14.7% of dropbacks.
**Flag:** CHI was beaten deep against both shells. The failures were execution, busts and rookie-safety play. A scheme exploit can't be shown from public data. CHI season numbers (Sharp, Oct 27): MOF closed 53.6% / open 42.0%, man 29.9% / zone 65.8%, blitz 41.4% (FTN [A]).

**Expected vs JSN tonight:** mostly single-high/zone with heavy pressure (41% blitz), and possibly Johnson matched outside. JSN is primarily a slot/inside receiver, so expect zone match plus a safety lean or bracket on 3rd downs. JSN's target share drops to 29.7% when CHI-style blitzes come (n=64), versus 33.9% otherwise [A/FTN]. This is a single-source season tendency, so the SRC-3 caution stays and PRESS stays blocked.

## Verdict changes
- **JSN o89.5 rec yds (-166): PASS, unchanged.** Strong passing offenses averaged 9.65 YPA against CHI, and their top WR hit ≥87 in 3 of 4 games (the exception is NE, which funneled to TE/RB). That supports the leg. The new risk is a volume cap if SEA leans on the run with Charbonnet; that is already in the pre-mortem.
- **Kupp o24.5/29.5: CUT, unchanged.** Shrunk edge is ≤0. He's a #2/#3 role, and CHI's damage to WRs went to the top WR.
- **SEA RBs: all CUT/BLOCK** (table above). No change to "no slip from this game".

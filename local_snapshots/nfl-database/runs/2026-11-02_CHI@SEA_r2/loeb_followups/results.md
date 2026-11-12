# Loeb follow-ups — CHI@SEA MNF 2026-11-02 (Tag: fixed-model, copies only)
Sim: tools/sim_v6_fix (sims.py subclasses Engine and only scales the target column; the engine is unedited), 3 models x 100k, seed 20261101, SEA -3. pbp runs Wk1-7 (both teams had a Wk8 bye). Raw output: raw_sims.json, usage: usage.py.
Odds: The Odds API, pulled 8:05 AM ET (odds_m0805.csv), 0 in-play rows. The FD main price is -113/-113, so the overround is 1.061. Alt no-vig = alt implied / 1.061. Recheck the odds after 9:05 AM ET (1h freshness rule).
Injuries: ESPN feed pulled 5:15 AM ET, plus seahawks.com Week 8 injury report, seahawks.com/team/transactions and chicagobears.com/team/transactions (fetched about 8:10 AM ET).
Edge columns: raw = avg p - nv. G6 = Ghost6 30% shrink (0.5+0.7(p-0.5) - nv). x0.7 = 0.7 x raw.

## Status verification
- Monangai: OUT (thumb/toe). Source: seahawks.com report and ESPN (Ben Johnson, Oct 31). Roschon Johnson is the RB2 behind Swift. Zavier Scott was signed to the active roster 10/27 (CHI official).
- Shaheed: OUT (knee). Source: seahawks.com Saturday report. Also OUT: Cross (Josh Jones starts at LT) and Velus Jones. Nwosu is DOUBTFUL.
- Price: still on IR as of the last check. He has no designation and was a full participant Fri and Sat, but SEA must activate him by 4 PM ET today. Macdonald said "let the transaction speak for itself." FD still posts Price rush 28.5.
- Simmons on CHI: VERIFIED OFFICIAL. chicagobears.com transactions, 10/29: acquired DL Jeffery Simmons from TEN.
- Nelson on SEA: VERIFIED OFFICIAL. seahawks.com transactions, 10/27: G Quenton Nelson acquired from IND. He's a guard, not an LT, so he doesn't replace Cross.
- Sweat: suspension lifted 10/23 (CHI official).
- Odeyingbo: placed on Reserve/Injured 10/17 (CHI official). His 3 sacks are not available tonight.
- Rusher alignment (which side each rusher lines up on vs Josh Jones): UNKNOWN. I found no public source.

## Coverage check (Loeb's "top-5 man" claim)
Sharp Football has CHI at 29.9% man, ranked **#3**. StatRankings CoverageIQ has 39.4% (#9). Both agree on direction. **Loeb is right.** Our 29.9% IS a top-3 man rate, so last turn's "disagrees" was wrong. Source: src/coverage_profile.json, pulled Nov 2 5:09 AM ET, under 48h old.
SEA: 90.0% zone (#1) and 60.6% two-high (MOF open).

## 1. Roschon Johnson (CHI RB) — CUT
- Caleb games (Wk1, 2, 6, 7): no stats in Wk1-2, 13 car-51 yds and 2-2-22 in Wk6, 2 car-13 yds and 0 tgt in Wk7. Even with Monangai out in Wk4-7, his carry share was only 7/21/39/7%. Targets were 1, 7 (with Bagent), 2, 0.
- Loeb's "#2 target vs MOFO" doesn't show up in the volume: 2 targets in 2 Caleb games where he had stats.
- FD has rush yds 12.5 (-113/-113), alt 9.5 at -172 (nv .596) and 4.5 at -440. FD posts no receptions or rec-yds market (NOLINE).

| Leg | MC | Bias | GR | nv | raw | G6 | x0.7 |
|---|---|---|---|---|---|---|---|
| Rush O12.5 | .603 (16.5) | .602 (17.1) | .558 (14.9) | .500 | +8.8 | +6.1 | +6.1 |
| Rush O9.5 -172 | .681 | .682 | .627 | .596 | +6.7 | +3.8 | +4.7 |
| Rec O0.5 (no line) | .439 | .440 | .375 | — | — | — | — |

- Why it's cut, even though the models show edge:
  - Committee rule: a rushing over needs a 60%+ carry share in 3 of the last 4. He's at 7-39%, so FAIL.
  - §7 at 12.5 with Caleb: 2 of 2 games with stats, but no stats in Wk1-2, so an insufficient sample. FAIL.
  - Model sample is only 4 games.
  - Swift had 73% of carries in Wk7.
- Receiving legs fail the Phase 2 opportunity gate and have no line, so no defender check was needed.

## 2. Jadarian Price (SEA RB) — CUT (can't pass §7)
- Not activated yet. His only games are Wk1-2 (Lock) and Wk3 (Darnold): 10-52, 13-52, 5-15 rushing and 2/2/3 targets. That's 1 game with the current QB, so §7 is impossible and the Phase 2 share can't be computed.
- The SEA backfield is now Charbonnet (2026 debut, coming off an ACL) + Wilson + Holani, maybe Price. That's a committee, so the 60% carry-share rule fails for every back.
- Loeb's "40% target rate vs man" doesn't apply here, because SEA's RBs face CHI's defense, not SEA's. And it's a 3-game sample.
- Recheck at the 4 PM ET activation deadline and at inactives (6:45 PM ET). It stays cut either way.

## 3. Shaheed OUT → JSN rerun
- Shaheed's target share in Darnold games (Wk3-7): .07/.14/.14/.17/.11, average .126. SEA has played no game without him, so there's no direct sample.
- If his targets are split in proportion to everyone else's share, JSN (.318) gains about +.046, a x1.144 target bump. The conservative case is x1.07 (Horton/Charles soak up outside snaps).
- Kupp (.11) and Barner (.15) get the same multipliers.
- Pass rush is modeled as mostly a 4-man rush with 7 in coverage (FTN: 11 of 19 sacks came on a straight 4-man rush; sack rate 8.6% blitz vs 8.2% non-blitz). Seven in coverage and CHI's top-3 man rate fit Loeb's JSN-vs-man note (about 4 targets per 10 routes). Sack leaders: Booker 4 (6 QB hits), Gordon 4, Sweat 2. Odeyingbo 3 is on IR. Simmons is added.
- The LT downgrade (Josh Jones) is a caution, not a cut: pressure cuts are OFF, and the backtest found that a pass-rush mismatch is not a WR-over cut. No model adjustment was made.

| JSN rec yds (FD 99.5 -113/-113, nv .500) | MC | Bias | GR | raw | G6 | x0.7 | medians |
|---|---|---|---|---|---|---|---|
| base (no boost) | .607 | .500 | .576 | +6.1 | +4.3 | +4.3 | 114.2/99.1/111.6 (Bias median is just under 99.5) |
| x1.07 | .658 | .548 | .622 | +10.9 | +7.6 | +7.6 | 122.4/106.1/119.9 |
| x1.144 | .705 | .597 | .664 | +15.5 | +10.9 | +10.9 | 130.6/114.0/128.2 |
| alt 89.5 -166 (nv .588), x1.07 | .726 | .617 | .685 | +8.8 | +6.2 | +6.2 | all medians clear |

- §7 at 99.5: 3 of 4 (76, 102, 134, 150). PASS.
- **JSN 100+ HOLDS.** With the Shaheed boost, all three models are ≥ .548 and every median clears.
- At the base case, the Bias median sits 0.4 yards under the line. If anyone wants extra cushion, 89.5 also clears.
- Kupp yds O24.5 (-162, nv .583): base .575/.482/.583, -4.7. At x1.144 it's .623/.529/.644, +2.2. Under +3 → **CUT** (closer to fair, still no edge).
- Barner rec O2.5 (-210, nv .638): base .581/.488/.545, -9.7. At x1.144 it's .660/.578/.615, -1.7 → **CUT**. O3.5 (+124, nv .421): x1.144 gives .454/.358/.446, -2.2 → **CUT**.

## 4. Eric Saubert (SEA TE) — CUT
- 1, 2, 0, 1 targets (Wk2, 3, 6, 7), 2-4% share, about 4 targets total all season. Not a top-2 target earner, so he fails Phase 2.

## Verdict
- **JSN rec yds 99.5: still holds**, and gets stronger with Shaheed out.
- Roschon Johnson, Price, Saubert, Kupp and Barner: all cut.
- **Correction to last turn:** Loeb's "CHI top-5 man" is supported by our own data (Sharp #3).
- **Not vetted by Ghost6.**

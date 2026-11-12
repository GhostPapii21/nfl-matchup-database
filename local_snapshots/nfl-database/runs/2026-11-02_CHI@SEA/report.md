# MNF Wk8 CHI @ SEA (Mon Nov 2, 2026) nfl-game-script-run
Kickoff 8:15 PM ET, Lumen Field (open-air). Weather (NWS/Open-Meteo, pulled 5:04 AM ET): 3% precip, wind 4.1 mph, no flag. SEA −3.
Odds of record: FanDuel, pulled **5:05 AM ET** (DK and Pinnacle used to compare). Routines at 4:30 PM and 6:50 PM ET reprice. pbp data runs through 2026-11-01. Neither team has played Week 8 yet (CHI Wk7 Thu vs NE, SEA Wk7 vs KC).

## Injuries
- **CHI:** Monangai OUT (fix A applied: Roschon Johnson). CB Malik Muhammad Q (toe). Kmet IR, LB D'Marco Jackson Q.
- **SEA:** LT Cross OUT (Josh Jones starts). Shaheed OUT. QB Lock Q (backup). Nwosu D. Charbonnet returns. J. Price IR (FD line dropped).
- **Check at 6:50 PM:** Muhammad (if he's out, JSN's defender becomes J. Johnson or Stevenson; re-run P4), Charbonnet (backfield split), Lock.

## Result
**No live legs. GATE: PASS (05:13 ET).**

**Model note, BUG-2026-11-02-BIASDUP:** the Bias model gives the same numbers as MC (K_BIAS = SHRINK_K = 30). Only two votes are independent: MC and GR.

### JSN rec yds over 89.5 at −166: MANUAL REVIEW on the numbers. Gate status is CUT because film is UNVERIFIED.
- **p (MC/Bias/GR):** .711/.715/.647. The no-vig price is .588. Edge (MC+GR) +.091. Medians 119.1/115.2.
- **Both independent votes clear.**
- **Defenders.** PFR team advanced defense runs through Week 7 (pulled 5:10 AM ET):

| CHI defender | Targets | Cmp % | YPT | Rating | Status |
|---|---|---|---|---|---|
| Malik Muhammad (ESPN Wk8 WRCB matchup) | 31 | 54.8 | 8.4 | 79.9 | Q |
| Jaylon Johnson | 31 | 77.4 | 14.4 | 129.4 | |
| Tyrique Stevenson | 20 | 60.0 | 11.5 | 139.4 | |

  - PFF (11/1): Johnson's coverage grade is 36.8.
  - JSN lines up L 39%, slot 28%, R 33%. CHI doesn't shadow him.
  - Gordon in the slot has 2 targets.
- **Scheme:** CHI plays man 30% (Sharp) / 39% (StatRankings) and single-high 54%. CHI blitzes 41% (4th).
- **§7 (Darnold games only, L4):** 76, 102, 134, 150, so 3 of 4 clear.
- **§14:** median 118 ≥ 107.4.
- **Rung:** one rung below the main 99.5, because the model margin is ≥ 8.5.
- **Darnold vs. the blitz:** grade C. Expected sacks 2.9, so the §15 receiver cut doesn't apply.
- **Panthers-rule CAUTION:** LT Cross is out.
- **Press tag:** matchup, coverage, script, QB and §7 all align, and both MC and GR clear. It's a press candidate. The MODEL-SUSPECT flag (median 119 vs FD 99.5) turns it into MANUAL REVIEW.
- **Why it can't go live:** Phase 10 film is UNVERIFIED (YouTube captions returned 429).
- **Other rungs:**
  - 79.5 at −245: edge +.072. §7 3 of 4.
  - 99.5 at −113: edge +.114, but §7 3 of 4 and §14 requires median ≥ 124 (it's 118), so it fails.
  - 109.5 and up: §7 fails.
- I agree with keeping it out tonight only because film isn't verified. BetGuru's Week 3 defender data was stale. The current numbers make the matchup stronger.

### Swift rush yds under 59.5 at −113: CUT
- **My projection:** about 16 carries (model 16.2; 15.7 a game without Monangai) × about 3.45 YPC vs SEA (Swift 4.10 × SEA adjustment .84; SEA allows 3.40 YPC to RBs) = about 56 yards.
- **Model p, under:** .656/.658/.624. **Model p, over:** .344/.342/.376. Medians 51.4/50.0. Edge on the under is about +.14.
- **Rico's Oct 14 star-under reason:** SEA's 3.40 YPC allowed and Swift's RYOE of −0.44. That's enough to get past the star-unders rule.
- **Correction to BetGuru:** SEA held 4 of 7 opponents under 4.0 YPC, not 5 (by game: 3.52, 4.12, 2.80, 4.59, 4.36, 2.78, 3.12).
- **Why it's cut:** §7 under QB-RETURN. In Williams-only games Swift ran for 124, 45, 44 and 78, so the under hit only 2 of 4. Film is also unverified.
- **Do I agree with BetGuru?** I agree with the direction, not the bet. It fails a hard rule. If you use any-QB games instead (58, 43, 44, 78), it hits 3 of 4.

### Darnold pass over 238.5: CUT
- p .523/.570. Edge +.038.
- Backup LT, so no QB yardage overs. §7: 168, 195, 278, 257 is 2 of 4. CHI blitzes 41%.
- I agree with BetGuru.

### Loveland and Burden unders: CUT
- **Loveland rec yds u42.5:**
  - MODEL-SUSPECT: median 30 against the FD line of 42.5, because the model mixes in Kmet-era and backup-QB games.
  - In Williams games he went 0, 3, 65, 69, so the under hit 2 of 4.
  - "Could trail" rule for check-down TE unders. The TE defender mapping isn't ruled (ISS-05).
- **Burden rec yds u51.5:** in Williams games 63, 32, 95, 130, so the under hit only 1 of 4.
- I agree with BetGuru. Using current-QB games only confirms the model contamination.

### Other cuts
- **Williams pass over:** edge +.007, and 10G (underdog over).
- **Odunze:** edge < .03 or negative.
- **Swift rush+rec under and receiving overs:** 10G.
- **Roschon Johnson:** run suppression (≤ 3.8), 10G, MODEL-SUSPECT.
- **Kupp:** no edge.
- **Barner unders:** CHI is soft vs TEs (8.61 YPT), ISS-05.
- **E. Wilson over:** MODEL-SUSPECT. Charbonnet is back.
- **JSN receptions over:** §7 hit 2 of 4. Muhammad allows a 54.8% completion rate.

## Risks and disclosures
- Coverage profile: Sharp (updated Oct 27), cross-checked against StatRankings. They agree.
- Per-defender numbers come from a PFR WebSearch snippet. A direct fetch got a Cloudflare 403.
- I glanced at Ghost6's REPORT/checklist head (they had JSN o89.5 with film marked "PASS"). I didn't use their numbers.
- None of tonight's players are on a placed slip, so there are no same-player stacks.
- I didn't mark anything VETTED.

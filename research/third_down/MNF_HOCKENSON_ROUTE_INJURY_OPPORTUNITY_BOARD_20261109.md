# Bills at Vikings · Verified Hockenson routes + game-script and injury stress test

**As-of:** 2026-11-09 morning ET, prior to 20:15 ET kickoff. **Research-only, not a trained main NFL model, not Lightning, not calibrated probabilities**. Snapshot market thresholds may differ by sportsbook and move before kickoff.

**Source-locked machine output:** [MNF route opportunity scenarios JSON](mnf_week9_route_opportunity_scenarios_20261109.json). Calculation: [Python module](mnf_week9_route_opportunity_scenarios.py). [Regression tests](../../test_nfl_mnf_week9_route_opportunity.py). GitHub Actions: [MNF route opportunity audit](https://github.com/GhostPapii21/nfl-matchup-database/actions/workflows/nfl-mnf-route-opportunity-audit.yml). Separate event-level Wentz third-down study: [QB drive survival](WENTZ_2025_2026_THIRD_DOWN_PREGAME_READOUT_20261109.md).

## First principle: routes, not raw seasonal receptions

T.J. Hockenson **2026 charted routes / Minnesota dropbacks** and targets:

| Week | Game | Routes | Team dropbacks | Rate | Targets |
|---|---|---:|---:|---:|---:|
| 1 | GB (Wentz relief) | 23 | 31 | 74.2% | 5 |
| 2 | CHI (Wentz starts) | 18 | 24 | 75.0% | 4 |
| 3 | TB | 20 | 34 | 58.8% | 4 |
| 7 | IND | 19 | 29 | 65.5% | 5 |
| 8 | DET | 22 | 33 | 66.7% | 5 |
| **Total** | with Jefferson active, excluding injury exit | **102** | **151** | **67.55%** | **23** |

The targets/route ratio across selected games is **23/102=22.55%**. This is not the QB-specific Hockenson conversion. Wentz across 2025–26: **37 Hockenson targets / 208 passes = 17.79%; 29 catches/37 targets =78.38%; 253 receiving yards/29 catches=8.72 yards per catch**. Two independent approaches give comparable target forecasts.

**Critical exclusions:** Week 4 Hockenson had 31 routes and 13 receptions **while Jefferson missed the game**. Week 5 he left very early and ran one route. Do not let either unusual role define his Week 9 target opportunity.

Charted route sources: [PlayerProfiler](https://www.playerprofiler.com/nfl/tj-hockenson/) W1-3, [RotoWire W7](https://www.rotowire.com/football/article/nfl-box-score-breakdown-week-7-recap-usage-stats-144024), [RotoWire W8](https://aws-prod-web9.rotowire.com/football/article/nfl-box-score-breakdown-week-8-recap-usage-stats-145045). Charted routes are **not official NFL play-by-play** and vendors differ by approximately two routes across the full year. RotoWire W7 was 19/29 routes/dropbacks; W8 22/33. Do not claim route-by-blitz and Hockenson blocking fraction were observed individually in Wentz third-down sample.

## Four plausible scripts, source inputs with explicit unfitted assumptions

The calculation estimates dropbacks as **Wentz throws + sacks + scrambles** and Hockenson routes as that total × hypothesized route share. Targets = routes × 22.55% historical targets/route, receptions = targets × historical Wentz 78.38% catch rate. Yards = receptions × 8.72 Wentz-era historical yards/catch. Not a trained conditional estimate, nor a probability distribution.

| Game script | Wentz throws | Dropbacks | Hock routes | Targets | Rec | Yds |
|---|---:|---:|---:|---:|---:|---:|
| Vikings offense low-volume | 24 | 28 | 18.5 | 4.2 | **3.3** | **28** |
| Competitive | 30 | 36 | 24.8 | 5.6 | **4.4** | **38** |
| Trailing and pass-heavy | 38 | 46 | 32.2 | 7.3 | **5.7** | **50** |
| Hockenson needed to block more (55% route) | 30 | 36 | 19.8 | 4.5 | **3.5** | **31** |

Hockenson DraftKings **over 4.5 receptions +103** vs FanDuel **over 4.5 −114** as captured around 04:08 ET Nov9; receiving yardage 41.5 commonly quoted. Underlying thresholds are not proof of an edge, and the same threshold at different prices has different break-even requirements. [Tracked market prices](https://edgelabs.bet/nfl/props?market=player_receptions), [receiving yards](https://edgelabs.bet/nfl/props?market=player_reception_yds).

**Decision:** Hockenson 4.5 catches and 41.5 yards are **PASS/BORDERLINE at base**; O4.5 has a real path if 35+ attempts and 70%+ route use; under strengthens in low volume or TE pass-protection games. BUF has allowed **43 catches, 494 yards to *all* opposing TEs through seven games**; that's a positional allowance, not an individual Hockenson prediction or route matchup assignment. Wentz's 2025–26 third-down PBP targeted Hockenson eight times, six completions, four first downs, confirming chain-moving role, NOT proving they were blitz checkdowns.

## Same scenario test, Jefferson and Addison

For Jefferson use explicitly *shrunk, assumption-based* 27/29/31% target shares by game script; 70% catch rate and 12.5 yards/catch. His actual Wentz 2026-only share 12/39=30.8%, only two appearances; do not treat this as a precise stable rate. Addison uses historical Wentz **37/188 =19.7% targets/pass** and **23/37=62.2% catches/target** from 2025–26, plus an unfitted 12.5 yards/catch. These are *scenario illustrations*.

| Wentz throws | Jefferson catches / yards | Addison catches / yards | Hockenson catches / yards |
|---|---:|---:|---:|
| 24 | 4.5 / 57 | 2.9 / 37 | 3.3 / 28 |
| 30 | **6.1 / 76** | **3.7 / 46** | **4.4 / 38** |
| 38 | 8.2 / 103 | 4.6 / 58 | 5.7 / 50 |

Tracked prop references: Jefferson **6.5 rec, 77.5 yards FanDuel** (DraftKings often 79.5 yards); Addison **3.5 rec, 39.5 yards**; Hockenson **4.5 rec, 41.5 yards**. At 30 throws Jefferson is close to BOTH thresholds, so no high-conviction over or under. Addison 3.5 sits at the projection boundary, with lower 2026 Wentz catch efficiency a strong warning; even an assumed 46-yard mean is exposed to lack of explosive opportunity and Buffalo CB assignments. The 38-throw case boosts all three receiving projections, but Minnesota also needs to sustain drives under Wentz's high third-down sack history.

## Injury and personnel impact gates (official final *weekly* status)

| Side | Player(s) | Status | Football opportunity mechanism |
|---|---|---|---|
| MIN offense | Kyler Murray | **OUT** | Carson Wentz starts; distinct QB accuracy, sacks and target shares |
| MIN offense | Jauan Jennings | **OUT** | Previous WR3 routes open; do NOT give all routes to Hockenson or Addison |
| MIN offense | Demond Claiborne | **OUT** | Backfield distribution may shift toward Jones/Mason/Dallas; Dallas may still handle third-down protection and checkdowns |
| MIN offense | Christian Darrisaw | **No final designation** | Expected tackle availability helps Wentz vs BUF edge pressure |
| MIN defense | S Theo Jackson, Jay Ward | **QUESTIONABLE** | Deep safety depth/disguise risk in Flores zone behind blitz; can aid Allen/Moore/Kincaid seams if absent, but must be confirmed |
| MIN defense | CB Isaiah Rodgers, OLB Andrew Van Ginkel | **No designation** | Full Saturday practice; cannot assume CB/edge weakness based on early-week listed injuries |
| BUF offense | LT Dion Dawkins | **QUESTIONABLE**; DNP all practices | Significant possible pass-block and Cook run-block loss versus frequent MIN pressure |
| BUF offense | LG Alec Anderson | **QUESTIONABLE**; LP Saturday | May affect interior pockets, Cook rushing and QB Allen scrambles |
| BUF offense | WR Joshua Palmer | **OUT** | More BUF WR snaps/targets available to Moore/Shakir/Coleman, not automatically guaranteed |
| BUF offense | RT Spencer Brown, WR Shakir, TE Kincaid | **No designation** | Brown returned to FP; Shakir FP Saturday; Kincaid cleared after chest concern |
| BUF defense | DL Greg Gaines | **QUESTIONABLE** | If out, interior rotational depth may decline and Jones/Mason rush efficiency rise (not quantified) |
| BUF defense | CB Dee Alford | **No designation** | Expected slot coverage availability; no assumed Addison easy matchup |
| BUF defense | Jordan Hancock | **QUESTIONABLE** | Possible activation, mainly depth; don't credit WR1 coverage shift without lineup proof |

Official injury sources: [Vikings](https://www.vikings.com/news/bills-injury-report-week-9-2026-nfl-season) and [Bills](https://www.buffalobills.com/news/buffalo-bills-injury-report-vs-vikings-week-9). **Questionable ≠ inactive** and no designation ≠ guarantee of full snap share. Final inactives expected around 90 minutes before kickoff; this morning-only audit cannot replace them.

## Defensive context / release gates

- MIN defense through W8: 73.6% blitz, 46.4% pressure (TruMedia Bills official), 25 sacks, 86.5% team zone (Sharp snapshot), 3.1 TE catches and 39 TE yards to *all* opponent TEs per game. Allen can produce scrambles on broken rush lanes but Flores may contain edges. No charted Allen pressure-to-scramble conditional rates supplied; avoid inventing 30.5 rush-yard over probabilities.
- BUF defense: 254.7 **net** passing yards allowed/game (not QB individual gross pass yards), 97.4 rushing yards allowed/game, 43 opposing TE receptions/7 games. BUF showed 64.5% blitz vs BAL W8 after <=39% earlier; use distinct conventional front-four and high-blitz scenarios, not one projected blitz certainty.
- Bills rushes (217) exceed official throws (205) through 7 games, with James Cook III 138 carries/707 rush yards including Week5 OT. MIN allowed 4.53 yards/carry to RBs, so Cook 18-22 carries × 4.1–4.5 YPC roughly 74–99 yards. **Over 79.5** has stronger game-mechanism support than **over 84.5**, but the Dawkins/Anderson OL scenario can negate it. No EV or calibrated edge.
- Shakir 3.5 catches is more mechanism-aligned than 4.5 (book differences); MIN WR target share 60.4% allowed, with quick pressure outlets a reason to see opportunities. Coleman and Kincaid role uncertainty matters. Palmer OUT modestly raises available BUF receiver roles.
- Avoid labeling every BUF CB as weak or assuming Jefferson faces one CB. Buffalo CB Benford / Igbinosun / Hairston, slot Alford, S Bishop/Hamlin rotate. No named snap-by-snap defender responsibility or guaranteed shadow matchup is verified.
- **No model release** until game-day availability, true opponent-adjusted route/pressure charting, team drive-survival + dropbacks, timestamped book line and distribution calibration can be validated. These are **observed means and hypothetical scenarios**, not individual over hit probabilities.

## Priority read

**Hockenson 4.5 receptions:** Borderline/PASS; his 68–70% route use makes five catches reachable in an elevated-pass game; a protection-heavy 55% route outcome moves mean down to ~3.5 catches. If Minnesota trails, measure survival and Wentz pass attempts rather than automatically upping every target.

**Jefferson 6.5 receptions or 77.5 yards:** Borderline in 30-attempt scenario, 38-attempt upside but possible Wentz sack stall; no automatic under. **Addison 3.5 receptions:** similarly game-script sensitive; no under certainty.

**Most consequential injury update:** Dawkins/Anderson for Buffalo passing+run efficiency and Jackson/Ward for Minnesota safety support. **The player most susceptible to a tactical deployment change is Hockenson** because TE protection routes can move independently of team passing volume.

**Research production status:** No production writes, baseline weights or NFL-13 files changed.

# Wentz 2025 third-down sacks vs Jefferson and Hockenson 2026 prop thresholds

**As-of:** Morning of Monday 2026-11-09; Bills–Vikings has not kicked off. **Status:** HISTORICAL RESEARCH, not calibrated or deployed NFL projection. Sources are original Vikings 2025 gamebooks, official player logs, and the audited nflverse 2025 Wentz dropbacks in [source-locked machine scorecard](wentz_third_down_jefferson_hockenson_props_20261109.json). Check individual source URLs in JSON.

The receiving columns are **full-game outcomes**. Brief Max Brosmer relief played in Weeks 3 and 8; do not attribute *every* completion in those full-game box scores to Wentz. The 3rd-down sacks are Wentz-specific, verified from individual third-down dropbacks.

| 2025 Wentz start | Wentz third-down sacks | All Vikings team third downs | Wentz official total-game throws | Jefferson catches / receiving yards | Hockenson catches / yards |
|---|---:|---:|---:|---:|---:|
| W3 vs CIN | 2 | 4/12 (33.3%) | 20 | 5 / 75 | 5 / 49 |
| W4 at PIT | 4 | 4/14 (28.6%) | 46 | 10 / 126 | 4 / 39 |
| W5 at CLE | 2 | 3/9 (33.3%) | 34 | 7 / 123 | 6 / 38 |
| W7 vs PHI | 1 | 7/15 (46.7%) | 42 | 5 / 79 | 6 / 43 |
| W8 at LAC | 2 | 3/11 (27.3%) | 27 | 7 / 74 | 2 / 26 |

2025 QB pass attempts are from [official NFL Wentz game log](https://www.nfl.com/players/carson-wentz/stats/logs/2025/). [Jefferson 2025 official log](https://www.nfl.com/players/justin-jefferson/stats/logs/2025/), [Hockenson 2025 official log](https://www.vikings.com/team/players-roster/t-j-hockenson/logs/2025/reg/).

## Exact threshold grading

**High third-down sack** sample = Wentz sacked at least twice on third down; four of five starts. The **bad team third-down** sample (<35% conversions) happens to be the same four games in this tiny dataset; it does **not** independently corroborate the sack correlation.

| Prop threshold | All five 2025 Wentz starts | Four high-sack / below-35%-conversion games |
|---|---:|---:|
| Jefferson over 70.5 receiving yards (71+) | 5/5 | 4/4 |
| Jefferson over 77.5 receiving yards (78+) | 3/5 | 2/4 |
| Jefferson 7+ receptions (line 6.5) | 3/5 | 3/4 |
| Jefferson 8+ receptions (line 7.5 or over 7) | 1/5 | 1/4 |
| Hockenson over 4.5 receptions (5+) | 3/5 | 2/4 |

**Key distinction:** An offer of **7+ catches** requires seven, while **over seven catches** requires eight. Confirm actual sportsbook threshold, odds, and game-time quote. No net expected value or prop probability was calculated from these five games.

## The mechanism the projection engine should capture

- Wentz's **four** third-down sacks vs Pittsburgh did **not** prevent Jefferson's 10/126; 46 Wentz attempts created enough volume. Hockenson had 4/39.
- Wentz's **two** third-down sacks vs Chargers coincided with only **27** Wentz pass attempts and backup QB relief. Jefferson had 7/74, near a 77.5-yard threshold; Hockenson had 2/26.
- Wentz's only **one** third-down sack vs Philadelphia still accompanied 42 attempts; Jefferson 5/79, Hockenson 6/43, Addison 9/128. A successful 46.7% third-down team day does **not** guarantee Jefferson 7+ receptions.
- In Wentz's 2025 five starts, **Jefferson remained a reliable moderate-yardage option** despite sack exposure; 77.5+ was not as reliable as 70.5+. **Hockenson's 4.5 reception threshold was substantially more variable.**
- **No single pressure-to-under coefficient should be fit** from sacks alone. Receiving volume depends on team passing attempts, passer release timing, receiver target share by down/score, route participation and protections, air yards, opponent coverages, plus substitutions.
- Counterexample to "trailing implies more QB throws": W8 blowout loss 10–37 led to 27 Wentz attempts, five full-game sacks and late QB substitution; drive survival and offense snaps can cap attempts even when trailing.
- Buffalo's seven-game 2026 defense allowed 41.9% opposing third downs and 254.7 net passing yards per game, so this matchup may **not** reproduce Wentz's tougher 2025 third-and-long distribution.

## Cross-year caution, not pooled in five-start scorecard

- 2026 Week 1 Wentz **relief** game: Jefferson **8/92**, Hockenson **4/36** (full-game team totals include early Kyler Murray possessions).
- 2026 Week 2 Wentz full start: Jefferson **3/55**, Hockenson **3/29**.
- These explain why we should not call Jefferson 70+ automatic based on five 2025 games: recent 2026 Wentz-led lower-volume game failed. They are **not** a like-for-like pair of full Wentz starts.

**Pregame recommendation gate:** Don't convert 5/5 or 4/4 into a confident probability. Treat Jefferson alternate 70+ yards differently from 78+, and receptions 7+ separately from 8+. At Hockenson 4.5 catches require projected pass attempts, expected Hockenson routes (vs pass blocking), and Buffalo TE coverage/pressure response. No certified edge without book price and calibrated blind backtesting.

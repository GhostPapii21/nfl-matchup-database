# Next Gen Stats and PFR advanced receiving inputs (Phase 3, item B)

`test_advanced.py`: season-to-date values as of before each game (15+ prior targets), standardized, each tested as a
multiplier on top of the receiver projection (Poisson GLM, offset log(projection)); fit 2022-2024, test 2025-2026.

| Feature | Yards per 1 SD | Targets per 1 SD | Passes both checks (significant in fit, better on test)? |
|---|---|---|---|
| Broken tackles per catch (PFR) | +2.5% | +1.7% | Yards: yes |
| YAC above expectation (NGS) | +1.0% | +3.4% | Targets: yes |
| Drop rate (PFR) | 0.0% | -1.8% | Targets: yes |
| Cushion (NGS) | -3.0% | -2.3% | No: significant in fit, worse on test |
| Separation (NGS) | -1.0% | +0.6% | No |
| Share of team intended air yards (NGS) | +1.9% | 0.0% | No |

Decision: **not wired into the live projection.** The three that pass improve test deviance by 0.1-0.3%: real but too
small to justify a game-day dependency on NGS/PFR weekly files, which post with a lag. Re-test after the season on all of
2026; the data is now pulled weekly by `pregame/sources.py`.

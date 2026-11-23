# Side-by-side candidates for the 80-yard stars (from Nov 23, 2026)

How new ideas get in without disturbing the board: (1) pass a held-out test on past seasons; (2) run next to the live
stars for 3-4 weeks, saved before kickoff and graded after (`snapshot.py`, `grade.py`); (3) only then replace anything,
as one switch in `dashboard/watch_model.json`.

## Step 1 results (`study.py`; fit 2022-24, held out 2025-26; base held-out log loss 0.26911, Brier 0.07834)
| Candidate | Log loss | Brier | z | Passed |
|---|---|---|---|---|
| Streakiness: game-to-game spread | 0.26910 | 0.07833 | -0.2 | No |
| Streakiness: share of 80+ games | 0.26945 | 0.07850 | 0.8 | No |
| Streakiness: 20+ yard catch rate | 0.26914 | 0.07830 | -0.8 | No |
| **Rising role: last game's target share vs season** | **0.26838** | **0.07825** | **2.1** | **Yes** |
| Rising role: 3-game trend | 0.26912 | 0.07834 | -0.5 | No |
| Man vs zone fit with this defense (2025 held out) | worse (0.38965 vs 0.38857) | worse | 1.3 | No; and 2026 coverage data is not published, so it could not run live |

Streakiness matches the Nov 14 finding (deep profile and hot hand did not help 100+ yards): once targets and yards a game
are in, how swingy a player is adds nothing we can measure.

## Step 2 (running now)
`dashboard/watch.py` `shadow_role`: the board's receiver 80+ chance plus 0.219 x log(last game's target share / season
share) on the logit scale (weight fit on 2022-26 with the board's own weights fixed, z 2.6). Stored as `shadow` on each
receiver; the live stars never use it. First game: CIN@WAS, Nov 23 (`live/2026_11_CIN_WAS.json`, saved before kickoff).

## Season by season (`by_season.py`; hold out one season, fit on all the others)
| Held out | Rising role: log loss / Brier, base -> with | Stars hit, base -> with |
|---|---|---|
| 2023 | 0.27365 -> 0.27277 / 0.08297 -> 0.08279 (better) | 39.5% (200) -> 40.0% (195) |
| 2024 | 0.28286 -> 0.28355 / 0.08634 -> 0.08672 (worse) | 39.0% (154) -> 39.8% (161) |
| 2025 | 0.26266 -> 0.26170 / 0.07609 -> 0.07596 (better) | 36.7% (166) -> 36.5% (167) |

Rising role helped in 2 of 3 seasons, with a small effect; the weight points the same way every year (z 2.0 / 3.1 / 2.0).
Streakiness and man vs zone each helped in 1 of 3, by tiny amounts. Rising role stays in the side-by-side run; it has to
beat the live stars on the weekly grading before it replaces anything.

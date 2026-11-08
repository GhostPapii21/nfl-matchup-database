# Week 9 Day 1 projection simulations and walk-forward trial

**Run date:** 2026-11-08. **Status:** research-only; no calibrated model or bet-eligible recommendation.

## Three candidate models

1. **Season empirical:** bootstrap from all verified Weeks 1–8 player-game outcomes with a recorded positive opportunity for that market; zero production in an eligible opportunity game is retained.
2. **Rolling-five empirical:** bootstrap from the latest five positive-opportunity game outcomes; zero production in those games is retained.
3. **Opponent-shrunk rolling-five:** bootstrap the last five opportunity-game outcomes after multiplying by 1 + alpha × (capped opponent allowed-rate factor − 1). Factors are capped at 0.75–1.25; alphas match the repo's development values (passing yards .50; receptions 1.00; receiving yards .25; rushing yards .50). This is an experimental, unapproved candidate.

For each available DraftKings/FanDuel line, 100,000 seeded bootstrap draws estimate mean, 10th/50th/90th percentiles, and over/push/under rates. These are empirical resampling frequencies, not calibrated probabilities. Forecasts are conditional on the player appearing in the same-team verified history; injury, snap-limit, weather, and game-script uncertainty are not simulated. Missing history and current-team mismatches are excluded, not imputed. This export does not distinguish a healthy active player's zero-opportunity game from an inactive game; those games cannot safely be included or excluded.

## Walk-forward trial

Weeks 5–8 forecasts use only prior-week player and opponent data; player test and training rows require positive market opportunity, while zero outcomes despite an opportunity remain included. Season-mean and rolling-five are scored on Weeks 5–8. Opponent-shrunk rolling-five is scored only on Weeks 7–8 because its market alphas were selected using Weeks 5–6 in the existing research audit. These are point-forecast MAE and signed bias, not probability calibration. Historical prop lines are unavailable in the research package, so Brier score/log loss cannot be computed.

| Market | Candidate | Window | n | MAE | Bias (forecast − actual) | Zero outcomes |
|---|---|---|---:|---:|---:|---:|
| player_pass_yds | opponent_shrunk_rolling5 | W7-W8 | 55 | 77.23 | 16.33 | 3 |
| player_pass_yds | rolling5_mean | W5-W8 | 111 | 68.59 | 3.74 | 3 |
| player_pass_yds | rolling5_mean | W7-W8 | 55 | 77.23 | 16.33 | 3 |
| player_pass_yds | season_mean | W5-W8 | 111 | 66.38 | 1.95 | 3 |
| player_pass_yds | season_mean | W7-W8 | 55 | 72.76 | 12.72 | 3 |
| player_reception_yds | opponent_shrunk_rolling5 | W7-W8 | 377 | 21.24 | 0.44 | 42 |
| player_reception_yds | rolling5_mean | W5-W8 | 770 | 21.00 | -0.09 | 83 |
| player_reception_yds | rolling5_mean | W7-W8 | 377 | 21.24 | 0.44 | 42 |
| player_reception_yds | season_mean | W5-W8 | 770 | 20.99 | -0.29 | 83 |
| player_reception_yds | season_mean | W7-W8 | 377 | 21.22 | 0.02 | 42 |
| player_receptions | opponent_shrunk_rolling5 | W7-W8 | 377 | 1.43 | 0.13 | 39 |
| player_receptions | rolling5_mean | W5-W8 | 770 | 1.49 | 0.01 | 76 |
| player_receptions | rolling5_mean | W7-W8 | 377 | 1.43 | 0.13 | 39 |
| player_receptions | season_mean | W5-W8 | 770 | 1.49 | -0.01 | 76 |
| player_receptions | season_mean | W7-W8 | 377 | 1.44 | 0.10 | 39 |
| player_rush_yds | opponent_shrunk_rolling5 | W7-W8 | 172 | 21.85 | -3.36 | 3 |
| player_rush_yds | rolling5_mean | W5-W8 | 346 | 20.46 | -2.40 | 5 |
| player_rush_yds | rolling5_mean | W7-W8 | 172 | 21.85 | -3.36 | 3 |
| player_rush_yds | season_mean | W5-W8 | 346 | 20.58 | -2.43 | 5 |
| player_rush_yds | season_mean | W7-W8 | 172 | 22.09 | -3.41 | 3 |

**Holdout read (Weeks 7–8):** the season mean has the lower MAE for passing yards (72.76 vs. 77.23) and is effectively tied for receiving yards (21.22 vs. 21.24). Rolling-five has the lowest receptions MAE (1.43 vs. 1.44 for season mean); the opponent factor does not improve it further. Opponent-shrunk and rolling-five tie for rushing MAE (21.85), slightly below season mean (22.09). These results do not identify one winner across markets. Player-game rows overlap by team and week, so the counts are not independent; the holdout is only two weeks.

## Three-model agreement screen

The next table contains only lines where all three empirical simulations point the same direction (each model above 60% or below 40%) and the same-team history has at least five opportunity games. These are raw historical bootstrap frequencies, not calibrated hit probabilities, and are not bet recommendations.

| Kickoff | Player | Market | Book line | Direction | Raw model range | Mean range | n |
|---|---|---|---:|---|---:|---:|---:|
| 4:25 PM ET | Trey McBride | receptions | DraftKings 6.5 | Over | 100–100% | 7.6–8.2 | 8 |
| 4:25 PM ET | Ashton Jeanty | receiving_yards | FanDuel 35.5 | Over | 88–100% | 47.0–55.8 | 8 |
| 4:25 PM ET | Ashton Jeanty | receiving_yards | DraftKings 35.5 | Over | 88–100% | 47.0–55.7 | 8 |
| 4:05 PM ET | Ladd McConkey | receptions | DraftKings 4.5 | Under | 83–100% | 2.4–2.8 | 6 |
| 4:25 PM ET | Jaxon Smith-Njigba | receiving_yards | DraftKings 93.5 | Over | 80–88% | 116.1–123.2 | 8 |
| 4:25 PM ET | Jaxon Smith-Njigba | receiving_yards | FanDuel 94.5 | Over | 80–88% | 116.0–123.1 | 8 |
| 4:05 PM ET | Woody Marks | rushing_yards | DraftKings 64.5 | Under | 80–86% | 38.6–46.0 | 7 |
| 4:25 PM ET | Tre Tucker | receiving_yards | FanDuel 34.5 | Over | 75–80% | 56.4–59.2 | 8 |
| 4:25 PM ET | Tre Tucker | receiving_yards | DraftKings 34.5 | Over | 75–80% | 56.6–59.4 | 8 |
| 4:25 PM ET | AJ Barner | receiving_yards | DraftKings 25.5 | Under | 75–80% | 22.6–25.4 | 8 |
| 4:25 PM ET | AJ Barner | receiving_yards | FanDuel 24.5 | Under | 75–80% | 22.6–25.4 | 8 |
| 1:00 PM ET | Jahmyr Gibbs | rushing_yards | DraftKings 96.5 | Over | 72–80% | 110.7–113.1 | 7 |
| 1:00 PM ET | Amon-Ra St. Brown | receiving_yards | DraftKings 77.5 | Under | 72–80% | 72.4–81.3 | 7 |
| 4:05 PM ET | Dalton Schultz | receiving_yards | DraftKings 36.5 | Under | 71–80% | 28.6–46.1 | 7 |
| 4:25 PM ET | George Kittle | receiving_yards | FanDuel 68.5 | Over | 71–80% | 60.6–67.9 | 7 |
| 1:00 PM ET | Amon-Ra St. Brown | receiving_yards | FanDuel 76.5 | Under | 71–80% | 72.4–81.8 | 7 |
| 8:20 PM ET | Emeka Egbuka | receiving_yards | DraftKings 50.5 | Under | 67–80% | 35.3–39.9 | 6 |
| 4:05 PM ET | Quentin Johnston | receiving_yards | DraftKings 29.5 | Over | 67–80% | 33.7–37.9 | 6 |
| 4:05 PM ET | Tre Harris | receiving_yards | DraftKings 29.5 | Over | 67–80% | 42.7–49.0 | 6 |
| 4:05 PM ET | Quentin Johnston | receiving_yards | FanDuel 31.5 | Over | 67–80% | 33.7–38.0 | 6 |

## Current slate coverage

| Kickoff | Simulated book-market rows |
|---|---:|
| 1:00 PM ET | 156 |
| 4:05 PM ET | 72 |
| 4:25 PM ET | 165 |
| 8:20 PM ET | 78 |

## Excluded rows

The CSV omits player-market rows with no verified same-team history or fewer than two positive-opportunity games. Missing forecasts do not mean zero production. This run excluded: Joe Milton passing yards and Gardner Minshew passing yards (no history); Zach Charbonnet rushing yards (one eligible historical game); Chris Godwin receiving yards (no verified same-team history). These gaps also mean those players' current lines cannot be compared by this simulation.

## Model audit

The repo's previously staged opponent-adjustment check and this zero-inclusive rerun differ in sample definition. In this run, opportunity games with zero output are retained, and the W7–8 holdout is compared side-by-side across all candidates in the table. Treat the new result as the relevant trial for this specific eligibility definition. The opponent adjustment remains experimental and uncalibrated.

# Opportunity check

A defense that allows 66 yards a game to tight ends spreads those yards over every tight end it faced. The question for a
prop is narrower: **does this game give this player the chance to get to the number?** The Opportunity tab answers it in
two parts and simulates the game 20,000 times.

## 1. Volume: how many chances he gets

- **Team plays:** the offense's own pace averaged with the plays this defense allows.
- **Pass/run mix:** the offense's pass-attempt share of plays, moved by the script the market implies. A team favoured by
  7 passes about 7% less and runs about 8% more (capped at 10%).
- **Weather:** the measured rain and wind effect on attempts (`research/weather/README.md`).
- **His share:** 60% his share over the window, 40% his share over the last three games. Teammates listed Out or Doubtful
  free up their share; 80% of it is spread over the rest in proportion to their own shares.
- **Volume correction:** in testing, share x team volume overstated what players got by about 12% for pass catchers and
  15-20% for backs (in-game injuries, rotation, lost work), most at the top. A fitted correction (2024-2025 games) is
  applied: targets = 0.048 + 0.877 x raw; carries = 0.589 + 0.799 x raw.
- **Swings:** targets and carries vary game to game with his own history's spread (gamma-Poisson), plus 25% uncertainty
  in the share itself.

## 2. Efficiency: what he does with each chance

- **Catch rate and yards per catch:** his own, blended with the league average for his position (40 targets / 25 catches
  of league data), then moved half way toward what this defense allows to his position.
- **Each catch's yards** are drawn from the league's real per-catch results for his position (last season), scaled to his
  yards per catch, so long catches happen as often as they really do.
- **Backs:** yards per carry blended with the league (60 carries), moved half way toward what this defense allows to
  backs, with each carry drawn from real per-carry results.

## What the tab shows

Targets, catches and median yards; the middle half of outcomes; the chance of 20+ through 120+ yards and of each catch
count; how many targets he needs for 70 yards and how often he gets them; the defense's yards to his position and his
slice of it; his own hit counts over the window; and every input used.

## Testing (`python3 -m dashboard.backtest_opportunity`)

Every past game from week 5 on, 2024-2026, using only what was known before the game (no weather or injury inputs, which
are not stored historically). The volume correction was fitted on 2024-2025; 2026 is the check it never saw.

2026 holdout, 865 pass-catcher games and 251 running-back games. Brier score: lower is better. The baseline is how often the
player hit that number in his own previous games.

| Stat | Line | Hit rate | Simulation said | Brier, simulation | Brier, own history |
| --- | --- | --- | --- | --- | --- |
| Receiving yards | 40+ | 33.5% | 30.4% | 0.174 | 0.185 |
| Receiving yards | 60+ | 18.2% | 17.0% | 0.122 | 0.129 |
| Receiving yards | 70+ | 12.8% | 12.7% | 0.094 | 0.101 |
| Receiving yards | 80+ | 9.9% | 9.5% | 0.079 | 0.086 |
| Receiving yards | 100+ | 4.7% | 5.3% | 0.039 | 0.045 |
| Receptions | 4+ | 34.3% | 32.7% | 0.176 | 0.184 |
| Receptions | 6+ | 13.8% | 14.1% | 0.092 | 0.099 |
| Rushing yards | 50+ | 39.4% | 34.5% | 0.188 | 0.205 |
| Rushing yards | 70+ | 23.1% | 20.5% | 0.139 | 0.154 |
| Rushing yards | 90+ | 14.7% | 11.8% | 0.100 | 0.110 |
| Carries | 15+ | 32.7% | 25.8% | 0.166 | 0.168 |

The simulation beats the player's own history at every line. Calibration is close for pass catchers; its rare 60%+ calls
for 70-80 yards run hot (small samples). For backs in 2026 it runs a few points low. Full tables, including calibration by
bucket: `dashboard/results/opportunity_backtest.md`.

## Limits

It is not compared with prop prices yet, so it is not an edge by itself: an edge needs the chance to beat the price's
break-even. It does not know coverage assignments, snap-level routes, or news after the packet was built. Research only.

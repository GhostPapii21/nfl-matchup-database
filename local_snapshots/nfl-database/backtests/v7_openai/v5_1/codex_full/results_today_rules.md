# EXPLORATORY / POST-HOC — NOT AN EDGE. v5.1 CODEX full rerun (gpt-6.1-sol), Nov-4 rules applied after grading was visible

Post-lock: apply Nov-4 rules to codex reads and grade. Pre-registered arm = v5.1 selector (strong+agree).
Exploratory arm (POST-HOC, disclosed): lean|strong + agree, because gpt-6.1-sol tagged only 3/149 legs 'strong'.
Rules: no TD/pass-yds (already), N1 cut (RB rushyds OVERS only: <60% of non-QB team carries over prior <=3 games),
§7 3-of-4 cut (last 4 games played per snap counts, zero-touch=0, line cleared on pick side >=3), last-2 both-against = downgrade FLAG,
arms A/B/C: edges flag-only; arm CT: Rico +1/+3 anchored tiers (<+1 cut, +1..+3 lean, >=+3 full; former +7 = flag), sims flag-only (none used),
best saved pre-kick price at same line (lines_noact), slips 3-4 legs <=5 per game DAY, one slip per player, $10.

Model p = market-anchored (Platt b≈0.02 ⇒ p≈no-vig), so Brier(model)≈Brier(market); reported as market Brier on picked side.


## A pre-registered v5.1 (strong+agree)

|   week |   W |   L |   hit |   priced |   pl |   roi |
|-------:|----:|----:|------:|---------:|-----:|------:|
|      7 |   0 |   1 |     0 |        1 |  -10 |    -1 |

TOTAL 0-1 hit 0.0 priced 1 P/L $-10.00 ROI -100.0%; market Brier 0.247 (n=1)

Slips: none (fewer than 3 eligible legs per day)

## B A + Nov-4 rules

|   week |   W |   L |   hit |   priced |   pl |   roi |
|-------:|----:|----:|------:|---------:|-----:|------:|
|      7 |   0 |   1 |     0 |        1 |  -10 |    -1 |

TOTAL 0-1 hit 0.0 priced 1 P/L $-10.00 ROI -100.0%; market Brier 0.247 (n=1)

Slips: none (fewer than 3 eligible legs per day)

## C0 EXPLORATORY lean|strong+agree, no Nov-4 rules

UNRESOLVED (no nflverse player-game row; not graded, not dropped silently):
|   week | game    | player       | market   | side   |   line |   price |
|-------:|:--------|:-------------|:---------|:-------|-------:|--------:|
|      3 | PHI@CHI | devontasmith | recyds   | over   |   71.5 |    -110 |
|      5 | TB@DAL  | tedhurstiii  | recyds   | over   |   16.5 |    -111 |
|      6 | NO@NYG  | camskattebo  | rushyds  | over   |   41.5 |    -112 |

|   week |   W |   L |   hit |   priced |      pl |    roi |
|-------:|----:|----:|------:|---------:|--------:|-------:|
|      3 |  10 |  15 | 0.4   |       25 | -61.077 | -0.244 |
|      4 |  10 |  15 | 0.4   |       25 | -60.7   | -0.243 |
|      5 |  11 |   8 | 0.579 |       19 |  18.564 |  0.098 |
|      6 |  10 |   9 | 0.526 |       19 |  -1.004 | -0.005 |
|      7 |  10 |   9 | 0.526 |       19 |   0.111 |  0.001 |
|      8 |  11 |   5 | 0.688 |       16 |  47.058 |  0.294 |

TOTAL 62-61 hit 0.504 priced 123 P/L $-57.05 ROI -4.6%; market Brier 0.2497 (n=123)

Slips (<=5/game day, 3-4 legs, $10):
|   week |   slips |   won |    pl |
|-------:|--------:|------:|------:|
|      3 |       5 |     0 | -50   |
|      4 |       5 |     0 | -50   |
|      5 |       4 |     0 | -40   |
|      6 |       4 |     0 | -40   |
|      7 |       4 |     1 |  28.7 |
|      8 |       3 |     0 | -30   |
Slips total 1/25 won, P/L $-181.30, ROI -72.5%

## C EXPLORATORY lean|strong+agree + Nov-4 rules (no tiers)

UNRESOLVED (no nflverse player-game row; not graded, not dropped silently):
|   week | game   | player      | market   | side   |   line |   price |
|-------:|:-------|:------------|:---------|:-------|-------:|--------:|
|      5 | TB@DAL | tedhurstiii | recyds   | over   |   16.5 |    -111 |
|      6 | NO@NYG | camskattebo | rushyds  | over   |   41.5 |    -112 |

|   week |   W |   L |   hit |   priced |     pl |    roi |
|-------:|----:|----:|------:|---------:|-------:|-------:|
|      5 |   9 |   1 | 0.9   |       10 | 70.785 |  0.708 |
|      6 |   6 |   3 | 0.667 |        9 | 24.06  |  0.267 |
|      7 |   5 |   5 | 0.5   |       10 | -5.272 | -0.053 |
|      8 |   6 |   1 | 0.857 |        7 | 42.641 |  0.609 |

TOTAL 26-10 hit 0.722 priced 36 P/L $132.21 ROI +36.7%; market Brier 0.2507 (n=36)

Slips (<=5/game day, 3-4 legs, $10):
|   week |   slips |   won |     pl |
|-------:|--------:|------:|-------:|
|      5 |       2 |     1 | 108.45 |
|      6 |       1 |     0 | -10    |
|      7 |       2 |     0 | -20    |
|      8 |       1 |     0 | -10    |
Slips total 1/6 won, P/L $68.45, ROI +114.1%

## CT EXPLORATORY C + Rico +1/+3 tiers

|   week |   W |   L |   hit |   priced |   pl |   roi |
|-------:|----:|----:|------:|---------:|-----:|------:|
|      7 |   0 |   1 |     0 |        1 |  -10 |    -1 |

TOTAL 0-1 hit 0.0 priced 1 P/L $-10.00 ROI -100.0%; market Brier 0.2521 (n=1)

Slips: none (fewer than 3 eligible legs per day)

Tier counts (C pool): {'cut (no model edge)': 23, 'cut': 14, 'lean': 1}; anchored edge range -0.91..+1.14 pts (n with sim=42)

## Rule attrition (lean|strong+agree, n=131)
N1 cut 8; §7 fail 89; last-2 downgrades 2; unpriced 5
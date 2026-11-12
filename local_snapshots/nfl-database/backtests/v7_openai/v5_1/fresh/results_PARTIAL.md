# v5.1 FRESH Grok reads — PARTIAL results (22/88 games read; 0 picks unmatched to lines)

Pre-registered verdict (Wk3-6: >=40 priced, ROI>0, beats v5 ROI and $): **INSUFFICIENT (PARTIAL — not final)** — priced 11, ROI 0.028, $ 3.03 vs v5 -0.138/-119.83

## Side by side

| set                              | split        |   W |   L |     hit |   priced |      pl |     roi |
|:---------------------------------|:-------------|----:|----:|--------:|---------:|--------:|--------:|
| v5.1 FRESH reads                 | train(3-6)   |   6 |   7 |   0.462 |       11 |    3.03 |   0.028 |
| v5.1 FRESH reads                 | holdout(7-8) |   0 |   0 | nan     |        0 |    0    | nan     |
| v5 PRIMARY (all games)           | train(3-6)   |  49 |  63 |   0.438 |       87 | -119.83 |  -0.138 |
| v5 PRIMARY (all games)           | holdout(7-8) |  31 |  20 |   0.608 |       40 |   68.63 |   0.172 |
| v5 PRIMARY (same games as fresh) | train(3-6)   |  19 |  25 |   0.432 |       33 |  -29.55 |  -0.09  |
| v5 PRIMARY (same games as fresh) | holdout(7-8) |   0 |   0 | nan     |        0 |    0    | nan     |
| v5.1 locked-reads                | train(3-6)   |  14 |  12 |   0.538 |       21 |   -1.58 |  -0.008 |
| v5.1 locked-reads                | holdout(7-8) |   6 |   3 |   0.667 |        9 |   23.1  |   0.257 |
| v6 READS                         | train(3-6)   |  39 |  68 |   0.364 |       94 | -255.17 |  -0.271 |
| v6 READS                         | holdout(7-8) |  27 |  22 |   0.551 |       47 |   -9.78 |  -0.021 |
| v6 GATED                         | train(3-6)   |  19 |  38 |   0.333 |       53 | -192.95 |  -0.364 |
| v6 GATED                         | holdout(7-8) |  18 |  12 |   0.6   |       28 |   20.15 |   0.072 |
| rush-under baseline              | train(3-6)   | 207 | 154 |   0.573 |      293 |  124.94 |   0.043 |
| rush-under baseline              | holdout(7-8) |  89 |  75 |   0.543 |      133 |   -8.49 |  -0.006 |

## FRESH by week

|   week |   W |   L |   hit |   priced |      pl |    roi |
|-------:|----:|----:|------:|---------:|--------:|-------:|
|      3 |   2 |   7 | 0.222 |        7 | -32.603 | -0.466 |
|      4 |   4 |   0 | 1     |        4 |  35.637 |  0.891 |

## FRESH by split x market x side

|                                      |   W |   L |   hit |   priced |      pl |    roi |
|:-------------------------------------|----:|----:|------:|---------:|--------:|-------:|
| ('train(3-6)', 'recyds', 'over')     |   3 |   4 | 0.429 |        6 |  -3.754 | -0.063 |
| ('train(3-6)', 'recyds', 'under')    |   0 |   1 | 0     |        1 | -10     | -1     |
| ('train(3-6)', 'rushrecyds', 'over') |   0 |   1 | 0     |        0 |   0     |  0     |
| ('train(3-6)', 'rushyds', 'over')    |   2 |   1 | 0.667 |        3 |   7.778 |  0.259 |
| ('train(3-6)', 'rushyds', 'under')   |   1 |   0 | 1     |        1 |   9.009 |  0.901 |

## FRESH by split x side

|                         |   W |   L |   hit |   priced |     pl |    roi |
|:------------------------|----:|----:|------:|---------:|-------:|-------:|
| ('train(3-6)', 'over')  |   5 |   6 | 0.455 |        9 |  4.024 |  0.045 |
| ('train(3-6)', 'under') |   1 |   1 | 0.5   |        2 | -0.991 | -0.05  |

## Slips, pre-registered (<=5/week, 3-4 legs, $10)

|   week | won   |     pl |
|-------:|:------|-------:|
|      3 | 0/2   | -20    |
|      4 | 1/1   | 117.84 |

## Slips, <=5 per game day variant ($10)

|   week | won   |     pl |
|-------:|:------|-------:|
|      3 | 0/2   | -20    |
|      4 | 1/1   |  57.82 |

## Grading gap

v5 gap resolved: Week 6 NYJ@NE Kenyon Sadiq recyds OVER 20.5 (actual 12, LOSS) carried an invalid saved price of -6. v5 grade.py treated it as unpriced (−$119.83); the first shared-harness pass decoded -6 as odds and booked −$10 (−$129.83). Harness now treats |price|<100 as unpriced; v5 Weeks 3-6 = −$119.83. The locked-reads v5.1 also kept Sadiq at -6, so its Wk3-6 moves from −$11.58 to −$1.58 (21 priced).

## Grok usage

Logged cost $3.04 (cap $10; script stops new calls at $9.20). Rejects: 6. Dropped: w4_DET@CAR. Stops: none
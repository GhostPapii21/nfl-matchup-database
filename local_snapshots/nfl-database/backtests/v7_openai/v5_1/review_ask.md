Your locked v5.1 (plan below) ran with no crashes and no fixes. Results from our shared harness:
set                              | split        |   W |   L |   hit |   priced |      pl |    roi |
|:---------------------------------|:-------------|----:|----:|------:|---------:|--------:|-------:|
| v5 PRIMARY                       | train(3-6)   |  49 |  63 | 0.438 |       88 | -129.83 | -0.148 |
| v5 PRIMARY                       | holdout(7-8) |  31 |  20 | 0.608 |       40 |   68.63 |  0.172 |
| v5.1 (locked)                    | train(3-6)   |  14 |  12 | 0.538 |       22 |  -11.58 | -0.053 |
| v5.1 (locked)                    | holdout(7-8) |   6 |   3 | 0.667 |        9 |   23.1  |  0.257 |
| ablation: strong+agree @v5 price | train(3-6)   |  14 |  12 | 0.538 |       22 |  -12.94 | -0.059 |
| ablation: strong+agree @v5 price | holdout(7-8) |   6 |   3 | 0.667 |        9 |   22.71 |  0.252 |
| v6 READS                         | train(3-6)   |  39 |  68 | 0.364 |       94 | -255.17 | -0.271 |
| v6 READS                         | holdout(7-8) |  27 |  22 | 0.551 |       47 |   -9.78 | -0.021 |
| v6 GATED                         | train(3-6)   |  19 |  38 | 0.333 |       53 | -192.95 | -0.364 |
| v6 GATED                         | holdout(7-8) |  18 |  12 | 0.6   |       28 |   20.15 |  0.072 |
| rush-under baseline              | train(3-6)   | 207 | 154 | 0.573 |      293 |  124.94 |  0.043 |
| rush-under baseline              | holdout(7-8) |  89 |  75 | 0.543 |      133 |   -8.49 | -0.006 |

## v5.1 by week

|   week |   W |   L |   hit |   priced |      pl |    roi |
|-------:|----:|----:|------:|---------:|--------:|-------:|
|      3 |   2 |   4 | 0.333 |        4 | -21.453 | -0.536 |
|      4 |   7 |   4 | 0.636 |       10 |  13.748 |  0.137 |
|      5 |   2 |   1 | 0.667 |        3 |   7.94  |  0.265 |
|      6 |   3 |   3 | 0.5   |        5 | -11.818 | -0.236 |
|      7 |   3 |   2 | 0.6   |        5 |   6.628 |  0.133 |
|      8 |   3 |   1 | 0.75  |        4 |  16.471 |  0.412 |

## v5 PRIMARY by week (harness regrade)

|   week |   W |   L |   hit |   priced |      pl |    roi |
|-------:|----:|----:|------:|---------:|--------:|-------:|
|      3 |  11 |  21 | 0.344 |       22 | -69.695 | -0.317 |
|      4 |  12 |  17 | 0.414 |       24 | -52.346 | -0.218 |
|      5 |  15 |  10 | 0.6   |       19 |  53.893 |  0.284 |
|      6 |  11 |  15 | 0.423 |       23 | -61.686 | -0.268 |
|      7 |  16 |  10 | 0.615 |       21 |  33.627 |  0.16  |
|      8 |  15 |  10 | 0.6   |       19 |  35.002 |  0.184 |

## v5.1 by split x market x side

|                                        |   W |   L 
## Slips by week ($10, 3-4 legs; v5.1 FanDuel-style product of saved prices)

|   week | v5.1_slips_won   |   v5.1_pl | v5_slips_won   |   v5_pl |
|-------:|:-----------------|----------:|:---------------|--------:|
|      3 | 0/1              |       -10 | 0/5            |  -50    |
|      4 | 0/2              |       -20 | 0/5            |  -50    |
|      5 | 0/1              |       -10 | 1/5            |   72.53 |
|      6 | 0/1              |       -10 | 0/5            |  -50    |
|      7 | 0/1              |       -10 | 1/5            |   15.23 |
|      8 | 0/1              |       -10 | 2/4            |  207.62 |
Notes: harness v5 train P/L -129.83 vs v5 report -119.83 (one leg settles differently). Baseline counts include unpriced legs in W-L. The ablation row (gate only, original prices) is ours, diagnostic.
Ask (<=450 words): 1) honest read vs your pre-declared criterion (>=40 settled priced Wk3-6 legs, positive ROI, beats v5 ROI and $) — PASS/FAIL/INSUFFICIENT; signal or noise; what the re-pricing change actually contributed. 2) Confirm or minimally amend the Week 10+ forward shadow protocol for v5.1 (no tuning on Wk1-8): run alongside v5 PRIMARY, sample threshold, kill rule, slip policy given v5.1 makes ~1-2 slips/week. 3) Anything wrong with our harness or comparison.

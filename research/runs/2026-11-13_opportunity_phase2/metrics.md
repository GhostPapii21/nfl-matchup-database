# Phase 2 opportunity model: walk-forward Weeks 4-9 (2026), name-locked (main) vs opportunity model

n = 2000 trials per game, 88 games, seed 20261113; engine git head d48dbfe (engine dirty=False). 95% CIs: game-cluster bootstrap (2000 resamples). Reconciliation failures: name-locked 0, opportunity 0. Research only, not validated; projection_ready=false.

## Opportunity calibration (sim vs actual per player-game)

| pos | stat | player-games | actual mean | ME main | ME opp | MAE main | MAE opp | MAE opp-main | p10-p90 cov main | p10-p90 cov opp | cov opp-main |
|---|---|---|---|---|---|---|---|---|---|---|---|
| QB | pass_att | 270 | 21.507 | +0.874 [+0.082, +1.598] | -1.294 [-2.095, -0.513] | 10.510 [9.230, 11.690] | 6.187 [5.323, 7.131] | -4.323 [-5.468, -3.171] | 0.348 [0.279, 0.426] | 0.726 [0.671, 0.779] | +0.378 [+0.303, +0.450] |
| QB | carries | 212 | 2.349 | +0.111 [-0.139, +0.366] | -0.063 [-0.321, +0.179] | 1.768 [1.547, 2.014] | 1.360 [1.179, 1.559] | -0.407 [-0.568, -0.264] | 0.684 [0.613, 0.752] | 0.835 [0.786, 0.884] | +0.151 [+0.100, +0.203] |
| RB | carries | 583 | 6.808 | +0.109 [-0.144, +0.342] | -0.572 [-0.833, -0.341] | 4.324 [3.977, 4.686] | 3.552 [3.266, 3.857] | -0.772 [-1.067, -0.473] | 0.479 [0.429, 0.527] | 0.779 [0.745, 0.809] | +0.300 [+0.254, +0.347] |
| RB | targets | 486 | 2.051 | -0.007 [-0.149, +0.135] | -0.006 [-0.161, +0.143] | 1.671 [1.548, 1.796] | 1.513 [1.394, 1.635] | -0.158 [-0.240, -0.073] | 0.712 [0.671, 0.749] | 0.815 [0.782, 0.846] | +0.103 [+0.073, +0.133] |
| WR | targets | 895 | 3.579 | +0.148 [-0.006, +0.309] | -0.312 [-0.482, -0.150] | 2.315 [2.165, 2.471] | 2.038 [1.877, 2.208] | -0.277 [-0.382, -0.171] | 0.655 [0.617, 0.692] | 0.782 [0.753, 0.811] | +0.127 [+0.094, +0.161] |
| TE | targets | 478 | 2.856 | -0.115 [-0.298, +0.070] | -0.211 [-0.393, -0.034] | 1.668 [1.554, 1.783] | 1.593 [1.474, 1.716] | -0.075 [-0.168, +0.016] | 0.764 [0.728, 0.797] | 0.795 [0.759, 0.830] | +0.031 [-0.008, +0.070] |

Nominal p10-p90 coverage is 0.80 (counts are discrete and the interval is inclusive, so a calibrated model can sit somewhat above 0.80).

## Brier on reception / yard thresholds

| pos | stat | threshold | player-games | base rate | Brier main | Brier opp | opp-main | climatology |
|---|---|---|---|---|---|---|---|---|
| RB | rec | >= 3 | 486 | 0.2346 | 0.179 [0.157, 0.202] | 0.157 [0.138, 0.177] | -0.022 [-0.036, -0.009] | 0.1795 |
| RB | rec | >= 5 | 486 | 0.07 | 0.067 [0.051, 0.085] | 0.065 [0.052, 0.081] | -0.002 [-0.008, +0.005] | 0.0651 |
| WR | rec | >= 3 | 895 | 0.3609 | 0.164 [0.147, 0.181] | 0.157 [0.143, 0.171] | -0.008 [-0.020, +0.004] | 0.2306 |
| WR | rec | >= 5 | 895 | 0.1687 | 0.107 [0.093, 0.120] | 0.104 [0.093, 0.117] | -0.002 [-0.010, +0.005] | 0.1403 |
| TE | rec | >= 3 | 478 | 0.3201 | 0.160 [0.139, 0.182] | 0.154 [0.137, 0.173] | -0.006 [-0.019, +0.006] | 0.2176 |
| TE | rec | >= 5 | 478 | 0.1423 | 0.102 [0.086, 0.122] | 0.093 [0.078, 0.108] | -0.009 [-0.017, -0.002] | 0.122 |
| RB | rec_yds | >= 25 | 486 | 0.1626 | 0.142 [0.120, 0.165] | 0.131 [0.112, 0.150] | -0.011 [-0.021, -0.001] | 0.1361 |
| RB | rec_yds | >= 50 | 486 | 0.0514 | 0.049 [0.032, 0.067] | 0.047 [0.032, 0.064] | -0.001 [-0.006, +0.003] | 0.0488 |
| RB | rec_yds | >= 75 | 486 | 0.0062 | 0.007 [0.001, 0.014] | 0.006 [0.001, 0.014] | -0.000 [-0.001, +0.001] | 0.0061 |
| WR | rec_yds | >= 25 | 895 | 0.4045 | 0.211 [0.193, 0.230] | 0.183 [0.167, 0.199] | -0.028 [-0.042, -0.015] | 0.2409 |
| WR | rec_yds | >= 50 | 895 | 0.2279 | 0.150 [0.135, 0.165] | 0.137 [0.124, 0.150] | -0.013 [-0.022, -0.004] | 0.176 |
| WR | rec_yds | >= 75 | 895 | 0.1128 | 0.091 [0.078, 0.104] | 0.085 [0.074, 0.098] | -0.005 [-0.011, +0.001] | 0.1001 |
| TE | rec_yds | >= 25 | 478 | 0.3117 | 0.166 [0.144, 0.189] | 0.159 [0.142, 0.176] | -0.007 [-0.018, +0.004] | 0.2145 |
| TE | rec_yds | >= 50 | 478 | 0.1464 | 0.106 [0.088, 0.127] | 0.095 [0.079, 0.112] | -0.011 [-0.019, -0.004] | 0.125 |
| TE | rec_yds | >= 75 | 478 | 0.0502 | 0.048 [0.032, 0.064] | 0.042 [0.028, 0.056] | -0.006 [-0.011, -0.001] | 0.0477 |
| RB | rush_yds | >= 25 | 583 | 0.3928 | 0.202 [0.180, 0.226] | 0.163 [0.143, 0.184] | -0.039 [-0.057, -0.022] | 0.2385 |
| RB | rush_yds | >= 50 | 583 | 0.2281 | 0.135 [0.115, 0.158] | 0.124 [0.108, 0.141] | -0.011 [-0.022, -0.000] | 0.1761 |
| RB | rush_yds | >= 75 | 583 | 0.1115 | 0.081 [0.066, 0.097] | 0.079 [0.065, 0.094] | -0.002 [-0.008, +0.004] | 0.0991 |
| QB | rush_yds | >= 25 | 212 | 0.1792 | 0.164 [0.130, 0.202] | 0.139 [0.109, 0.171] | -0.025 [-0.046, -0.007] | 0.1471 |
| QB | rush_yds | >= 50 | 212 | 0.0519 | 0.057 [0.033, 0.081] | 0.057 [0.034, 0.081] | -0.001 [-0.004, +0.002] | 0.0492 |
| QB | rush_yds | >= 75 | 212 | 0.0142 | 0.015 [0.001, 0.032] | 0.014 [0.001, 0.031] | -0.000 [-0.002, +0.000] | 0.014 |

Negative opp-main = the opportunity model is better (lower MAE / Brier). A CI that crosses 0 is not a demonstrated difference.

Brier summary (computed): 10 of 21 thresholds have a 95% CI fully below 0 (RB rec >= 3, TE rec >= 5, RB rec_yds >= 25, WR rec_yds >= 25, WR rec_yds >= 50, TE rec_yds >= 50, TE rec_yds >= 75, RB rush_yds >= 25, RB rush_yds >= 50, QB rush_yds >= 25); 0 fully above 0; 21 of 21 point estimates <= 0.

## History-capped events: QB interceptions (QBs with >= 10 actual attempts)

| model | QB-games | games with P(INT>=1)=0 | of those, actual INT games | mean P(INT>=1) | actual rate | Brier |
|---|---|---|---|---|---|---|
| name_locked_main | 178 | 30 | 11 | 0.384 | 0.522 | 0.2982 |
| opportunity | 178 | 19 | 8 | 0.402 | 0.522 | 0.3016 |

INT Brier is slightly WORSE with the opportunity model (0.3016 vs 0.2982); the gain is only in the zero-probability column. Do not price INT props from this model.

Opportunity-model P(INT>=1)=0 games by reason: not a candidate 9, team row pool had no INT row before the eval week 10 (engine-level cap), other 0:

| game | team | QB | opp mean att | team pool INT rows | reason |
|---|---|---|---|---|---|
| 2026_04_DAL_HOU | HOU | C.Stroud | 32.7 | 0 | team_pool_no_int_rows |
| 2026_04_DET_CAR | DET | J.Goff | 35.3 | 0 | team_pool_no_int_rows |
| 2026_04_IND_WAS | WAS | A.Kaliakmanis | 0.0 | 0 | not_a_candidate |
| 2026_04_NYJ_CHI | CHI | T.Bagent | 0.0 | 1 | not_a_candidate |
| 2026_04_NYJ_CHI | NYJ | G.Smith | 28.8 | 0 | team_pool_no_int_rows |
| 2026_05_CHI_GB | CHI | C.Keenum | 0.0 | 2 | not_a_candidate |
| 2026_05_CLE_NYJ | NYJ | G.Smith | 28.6 | 0 | team_pool_no_int_rows |
| 2026_05_DET_ARI | DET | J.Goff | 37.9 | 0 | team_pool_no_int_rows |
| 2026_05_HOU_TEN | HOU | C.Stroud | 34.7 | 0 | team_pool_no_int_rows |
| 2026_06_CAR_PHI | PHI | T.McKee | 0.0 | 4 | not_a_candidate |
| 2026_06_HOU_JAX | HOU | C.Stroud | 32.8 | 0 | team_pool_no_int_rows |
| 2026_06_NYJ_NE | NYJ | G.Smith | 28.0 | 0 | team_pool_no_int_rows |
| 2026_07_GB_DET | DET | J.Goff | 38.0 | 0 | team_pool_no_int_rows |
| 2026_08_ARI_DAL | ARI | G.Minshew | 0.0 | 6 | not_a_candidate |
| 2026_08_BAL_BUF | BAL | J.Fagnano | 0.0 | 2 | not_a_candidate |
| 2026_08_MIN_DET | DET | J.Goff | 35.3 | 0 | team_pool_no_int_rows |
| 2026_09_ARI_SEA | SEA | D.Lock | 0.0 | 9 | not_a_candidate |
| 2026_09_BUF_MIN | MIN | C.Wentz | 0.0 | 3 | not_a_candidate |
| 2026_09_NYG_PHI | PHI | J.Milton | 0.0 | 6 | not_a_candidate |

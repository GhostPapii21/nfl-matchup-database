# Coverage, pressure and opponent-tier adjustments: fit 2023-2024, test 2025

Fit on 5561 player-games. Tested on 2757 player-games from 2025 that the fit never saw (weeks 5+, pass catchers: {'WR': 1382, 'TE': 702, 'RB': 673}).

Every input uses only the previous season and earlier weeks. Brier score: lower is better. Yardage miss: average gap between projected and actual receiving yards.

## Summary

None of the three ideas passed the test. The board should not apply any of them. Details:

- **Coverage fit, man vs zone: do not use.** Fit 2023-2024: yards per target: best prior weight m=0, strength 0.637 (t 1.42; same regression on 2025: 0.126, t 0.2); targets: best prior weight m=80, strength 1.17 (t 2.14; same regression on 2025: 0.744, t 0.92). Test 2025 with the fitted version: average Brier -0.00003 on a base of 0.11163 (-0.02%, 90% range -0.00017 to +0.00011); yardage miss +0.009 yards on a base of 20.01. Fit rule met: yes. Holdout rule met: no.
- **Coverage fit, middle of field open vs closed: do not use.** Fit 2023-2024: yards per target: no prior weight gave a positive strength; targets: best prior weight m=20, strength 1.71 (t 2.51; same regression on 2025: 0.539, t 0.53). Test 2025 with the fitted version: average Brier -0.00002 on a base of 0.11163 (-0.02%, 90% range -0.00016 to +0.00012); yardage miss -0.000 yards on a base of 20.01. Fit rule met: yes. Holdout rule met: no.
- **Pressure fit: do not use.** Fit 2023-2024: yards per attempt: no prior weight gave a positive strength; completion rate: no prior weight gave a positive strength; attempts: best prior weight m=0, strength 0.125 (t 0.1; same regression on 2025: 3.229, t 1.93). Test 2025 with the fitted version: average Brier -0.00003 on a base of 0.11163 (-0.03%, 90% range -0.00009 to +0.00002); yardage miss +0.000 yards on a base of 20.01. Fit rule met: no. Holdout rule met: no.
- **Opponent tier (average vs top-10 vs bottom-10 defenses): do not use.** Used raw in place of the defense factor it is clearly worse: average Brier +0.00309 on a base of 0.11163 (+2.76%, 90% range +0.00207 to +0.00409); yardage miss +0.842 yards on a base of 20.01. Shrunk hard it only falls back to a weak league effect. His own tier split on top of the current model: average Brier +0.00001 on a base of 0.11163 (+0.01%, 90% range -0.00002 to +0.00004); yardage miss -0.003 yards on a base of 20.01.
- **Weight on the current defense factor.** The fit prefers 0.125 over the current 0.5 (mean squared yardage error 776.277 vs 779.165; with no defense factor at all 776.919). On 2025: average Brier -0.00031 on a base of 0.11163 (-0.27%, 90% range -0.00063 to +0.00000); yardage miss -0.026 yards on a base of 20.01. On 2026 to date: average Brier -0.00018 (90% range -0.00068 to +0.00034). The direction is the same in every season, but the gain is too small to tell apart from luck. It is reported here and nothing is changed. What it does say: the defense factor is not adding measurable value at any weight.
- **Closest thing to a signal:** targets (not yards) by coverage. Running backs draw a larger share of targets against zone-heavy defenses. The fit-season strength was positive and the 2025 regression pointed the same way, but it moved the 2025 scores by less than 0.03%. Not used.

Why these did not help, in plain words:

- The splits are thin. The typical player had 29 prior targets against man and 45 against zone, and 6 prior games against the opponent's tier. That is mostly noise.
- Defenses do not differ enough. Nine in ten opponents play man between 24% and 41% of the time, and pressure the passer between 25% and 33%.
- So the adjustments are tiny even when taken at face value: most players move by about 2% or less (man/zone yards multiplier 0.98 to 1.019, pressure 0.989 to 1.012). One game's yards swing far more than that.
- A player's own numbers already carry most of it. His catch rate and yards per catch were earned against a mix of coverages and pass rushes.
- Pressure is real at team level (a high-pressure defense does produce more pressure and more sacks) but the link to yards per attempt is weak and changed sign between the fit seasons and 2025.
- The coverage labels are not consistent between seasons (league man rate 41% in 2023, 48% in 2024, 32% in 2025), which limits how much last season's split can say about this season.

## Holdout results (2025)

| Model | Yds 40+ | Yds 60+ | Yds 70+ | Yds 80+ | Rec 4+ | Rec 6+ | Avg Brier | Change (90% range) | Yardage miss | Change (90% range) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| current model | 0.1615 | 0.1084 | 0.0850 | 0.0676 | 0.1595 | 0.0878 | 0.11163 |  | 20.01 |  |
| + coverage fit man/zone, as derived (m=40, strength 1) | 0.1616 | 0.1085 | 0.0850 | 0.0677 | 0.1594 | 0.0878 | 0.11166 | +0.00002 (-0.00011 to +0.00016) | 20.02 | +0.010 (-0.006 to +0.027) |
| + coverage fit man/zone, as fitted | 0.1615 | 0.1085 | 0.0850 | 0.0676 | 0.1593 | 0.0877 | 0.11161 | -0.00003 (-0.00017 to +0.00011) | 20.02 | +0.009 (-0.012 to +0.030) |
| + coverage fit middle open/closed, as derived (m=40, strength 1) | 0.1615 | 0.1085 | 0.0850 | 0.0676 | 0.1594 | 0.0878 | 0.11163 | -0.00000 (-0.00011 to +0.00011) | 20.01 | +0.006 (-0.007 to +0.020) |
| + coverage fit middle open/closed, as fitted | 0.1616 | 0.1084 | 0.0849 | 0.0675 | 0.1593 | 0.0879 | 0.11161 | -0.00002 (-0.00016 to +0.00012) | 20.01 | -0.000 (-0.019 to +0.018) |
| + pressure fit, as derived (m=100, strength 1) | 0.1613 | 0.1083 | 0.0850 | 0.0676 | 0.1592 | 0.0877 | 0.11153 | -0.00011 (-0.00024 to +0.00003) | 20.01 | +0.000 (-0.019 to +0.017) |
| + pressure fit, as fitted | 0.1615 | 0.1084 | 0.0849 | 0.0676 | 0.1594 | 0.0877 | 0.11160 | -0.00003 (-0.00009 to +0.00002) | 20.01 | +0.000 (-0.004 to +0.004) |
| no defense factor at all (weight 0) | 0.1616 | 0.1080 | 0.0846 | 0.0672 | 0.1594 | 0.0873 | 0.11134 | -0.00029 (-0.00073 to +0.00013) | 19.99 | -0.017 (-0.101 to +0.062) |
| defense factor at fitted weight 0.125 | 0.1615 | 0.1079 | 0.0846 | 0.0673 | 0.1594 | 0.0874 | 0.11133 | -0.00031 (-0.00063 to +0.00000) | 19.98 | -0.026 (-0.089 to +0.033) |
| tier split replaces defense factor: raw average vs top-10 / bottom-10 (m=0) | 0.1697 | 0.1135 | 0.0884 | 0.0700 | 0.1594 | 0.0873 | 0.11472 | +0.00309 (+0.00207 to +0.00409) | 20.85 | +0.842 (+0.602 to +1.093) |
| tier split replaces defense factor, as fitted (m=inf, strength 0.081) | 0.1615 | 0.1079 | 0.0845 | 0.0672 | 0.1594 | 0.0873 | 0.11131 | -0.00033 (-0.00075 to +0.00008) | 19.98 | -0.030 (-0.110 to +0.046) |
| + his own tier split on top, as fitted (m=0, strength 0.018) | 0.1615 | 0.1084 | 0.0850 | 0.0676 | 0.1595 | 0.0878 | 0.11164 | +0.00001 (-0.00002 to +0.00004) | 20.01 | -0.003 (-0.007 to +0.002) |
| + targets the defense allows his position (strength 0.054) | 0.1615 | 0.1084 | 0.0849 | 0.0676 | 0.1593 | 0.0877 | 0.11158 | -0.00005 (-0.00014 to +0.00004) | 20.00 | -0.004 (-0.015 to +0.006) |

### Second check: 2026 to date (weeks 5-10, 865 player-games)

Coverage and pressure data are not published for this season, so only the defense weight and tier rows can be checked.

| Model | Avg Brier | Change (90% range) | Yardage miss | Change (90% range) |
| --- | --- | --- | --- | --- |
| current model | 0.12282 |  | 21.46 |  |
| no defense factor at all (weight 0) | 0.12277 | -0.00005 (-0.00075 to +0.00064) | 21.41 | -0.041 (-0.190 to +0.109) |
| defense factor at fitted weight 0.125 | 0.12265 | -0.00018 (-0.00068 to +0.00034) | 21.40 | -0.052 (-0.167 to +0.062) |
| tier split replaces defense factor: raw average vs top-10 / bottom-10 (m=0) | 0.12686 | +0.00404 (+0.00204 to +0.00616) | 22.36 | +0.904 (+0.423 to +1.397) |
| tier split replaces defense factor, as fitted (m=inf, strength 0.081) | 0.12270 | -0.00012 (-0.00076 to +0.00051) | 21.41 | -0.042 (-0.177 to +0.095) |
| + his own tier split on top, as fitted (m=0, strength 0.018) | 0.12279 | -0.00003 (-0.00009 to +0.00003) | 21.44 | -0.013 (-0.022 to -0.004) |
| + targets the defense allows his position (strength 0.054) | 0.12292 | +0.00010 (-0.00007 to +0.00027) | 21.48 | +0.025 (+0.005 to +0.046) |

A negative change is an improvement. If the range includes zero, the change cannot be told apart from luck.

By position (change in average Brier / change in yardage miss):

- + coverage fit man/zone, as derived (m=40, strength 1): WR -0.00009 / +0.000, TE +0.00032 / +0.048, RB -0.00004 / -0.010
- + coverage fit man/zone, as fitted: WR -0.00016 / +0.006, TE +0.00026 / +0.043, RB -0.00004 / -0.021
- + coverage fit middle open/closed, as derived (m=40, strength 1): WR -0.00005 / +0.006, TE -0.00004 / +0.010, RB +0.00013 / +0.004
- + coverage fit middle open/closed, as fitted: WR -0.00022 / -0.018, TE +0.00019 / +0.025, RB +0.00015 / +0.010
- + pressure fit, as derived (m=100, strength 1): WR -0.00017 / +0.005, TE +0.00001 / +0.006, RB -0.00009 / -0.017
- + pressure fit, as fitted: WR -0.00005 / +0.003, TE -0.00009 / -0.005, RB +0.00005 / -0.000
- no defense factor at all (weight 0): WR -0.00050 / -0.021, TE -0.00003 / -0.081, RB -0.00013 / +0.057
- defense factor at fitted weight 0.125: WR -0.00049 / -0.029, TE -0.00014 / -0.077, RB -0.00010 / +0.033
- tier split replaces defense factor: raw average vs top-10 / bottom-10 (m=0): WR +0.00376 / +0.976, TE +0.00354 / +1.002, RB +0.00122 / +0.402
- tier split replaces defense factor, as fitted (m=inf, strength 0.081): WR -0.00054 / -0.026, TE -0.00009 / -0.098, RB -0.00014 / +0.034
- + his own tier split on top, as fitted (m=0, strength 0.018): WR +0.00001 / -0.002, TE +0.00002 / +0.004, RB -0.00002 / -0.010
- + targets the defense allows his position (strength 0.054): WR -0.00008 / +0.000, TE -0.00008 / -0.010, RB +0.00002 / -0.007

## Fit details (2023-2024)

m = league-average chances blended into the player's own split (inf = league effect only). beta = fitted strength (1 = right as derived, 0 = no information). t = beta / its standard error. sd_log_mult = how much the multiplier moves from player to player. sse_drop_pct = share of squared error removed. beta_2025 / t_2025 = the same regression run on the holdout season, shown only to see whether the fit-season answer repeats.

### Coverage fit: man vs zone

Yards per target:

| m | beta | se | t | sd_log_mult | sse_drop_pct | beta_2025 | t_2025 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.637 | 0.45 | 1.42 | 0.0364 | 0.0372 | 0.126 | 0.2 |
| 10 | 0.4 | 0.691 | 0.58 | 0.0197 | 0.0076 | -0.348 | -0.31 |
| 20 | 0.288 | 0.82 | 0.35 | 0.0161 | 0.003 | -0.577 | -0.44 |
| 40 | 0.107 | 1.0 | 0.11 | 0.0129 | 0.0003 | -0.899 | -0.57 |
| 80 | -0.147 | 1.226 | -0.12 | 0.0106 | 0.0004 | -1.265 | -0.66 |
| 160 | -0.414 | 1.446 | -0.29 | 0.0092 | 0.0025 | -1.517 | -0.68 |
| 320 | -0.59 | 1.591 | -0.37 | 0.0086 | 0.0044 | -1.545 | -0.64 |
| inf | -0.669 | 1.676 | -0.4 | 0.0082 | 0.0054 | -1.231 | -0.51 |

Targets:

| m | beta | se | t | sd_log_mult | sse_drop_pct | beta_2025 | t_2025 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.719 | 0.37 | 1.94 | 0.0294 | 0.0981 | 0.63 | 1.11 |
| 10 | 0.906 | 0.446 | 2.03 | 0.0242 | 0.1124 | 0.614 | 0.89 |
| 20 | 1.003 | 0.482 | 2.08 | 0.0223 | 0.119 | 0.636 | 0.86 |
| 40 | 1.102 | 0.519 | 2.12 | 0.0206 | 0.1246 | 0.683 | 0.87 |
| 80 | 1.17 | 0.546 | 2.14 | 0.0196 | 0.1265 | 0.744 | 0.92 |
| 160 | 1.197 | 0.559 | 2.14 | 0.0192 | 0.1249 | 0.798 | 0.98 |
| 320 | 1.197 | 0.564 | 2.12 | 0.019 | 0.1221 | 0.832 | 1.03 |
| inf | 1.174 | 0.564 | 2.08 | 0.019 | 0.1162 | 0.87 | 1.09 |

- WR: yards m=40 beta -0.375 (t -0.32); m=inf beta -0.911 (t -0.42) | targets m=40 beta 0.295 (t 0.36); m=inf beta 0.548 (t 0.53)
- TE: yards m=40 beta 1.519 (t 0.8); m=inf beta 0.364 (t 0.14) | targets m=40 beta 1.719 (t 1.04); m=inf beta -0.636 (t -0.25)
- RB: yards m=40 beta 2.723 (t 1.08); m=inf beta -9.247 (t -1.37) | targets m=40 beta 2.078 (t 3.52); m=inf beta 1.952 (t 3.25)

### Coverage fit: middle of field open vs closed

Yards per target:

| m | beta | se | t | sd_log_mult | sse_drop_pct | beta_2025 | t_2025 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | -0.747 | 0.721 | -1.04 | 0.0236 | 0.0214 | -0.334 | -0.3 |
| 10 | -1.312 | 1.173 | -1.12 | 0.0116 | 0.0291 | -1.116 | -0.58 |
| 20 | -1.659 | 1.436 | -1.16 | 0.0089 | 0.032 | -1.634 | -0.69 |
| 40 | -2.299 | 1.879 | -1.22 | 0.0064 | 0.0367 | -2.448 | -0.79 |
| 80 | -3.488 | 2.648 | -1.32 | 0.0043 | 0.0428 | -3.616 | -0.84 |
| 160 | -5.685 | 3.988 | -1.43 | 0.0028 | 0.0494 | -4.896 | -0.8 |
| 320 | -9.367 | 6.115 | -1.53 | 0.0019 | 0.0542 | -5.115 | -0.61 |
| inf | -8.927 | 11.592 | -0.77 | 0.0014 | 0.0102 | 5.914 | 0.54 |

Targets:

| m | beta | se | t | sd_log_mult | sse_drop_pct | beta_2025 | t_2025 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1.129 | 0.487 | 2.32 | 0.0206 | 0.1119 | 0.155 | 0.19 |
| 10 | 1.544 | 0.613 | 2.52 | 0.016 | 0.139 | 0.372 | 0.4 |
| 20 | 1.71 | 0.682 | 2.51 | 0.0143 | 0.1397 | 0.539 | 0.53 |
| 40 | 1.848 | 0.765 | 2.41 | 0.0127 | 0.1311 | 0.796 | 0.73 |
| 80 | 1.894 | 0.843 | 2.25 | 0.0116 | 0.1145 | 1.102 | 0.94 |
| 160 | 1.842 | 0.897 | 2.05 | 0.0111 | 0.0962 | 1.36 | 1.11 |
| 320 | 1.752 | 0.926 | 1.89 | 0.0109 | 0.0821 | 1.523 | 1.21 |
| inf | 1.574 | 0.95 | 1.66 | 0.0108 | 0.0633 | 1.691 | 1.31 |

- WR: yards m=40 beta -4.015 (t -1.76); m=inf beta 11.667 (t 0.43) | targets m=40 beta 1.446 (t 1.13); m=inf beta 0.8 (t 0.42)
- TE: yards m=40 beta 7.977 (t 2.11); m=inf beta -48.772 (t -1.1) | targets m=40 beta 2.725 (t 0.97); m=inf beta 1.249 (t 0.18)
- RB: yards m=40 beta -4.233 (t -1.0); m=inf beta -18.034 (t -1.76) | targets m=40 beta 2.218 (t 2.36); m=inf beta 2.168 (t 2.1)

### Pressure fit

Yards per attempt:

| m | beta | se | t | sd_log_mult | sse_drop_pct | beta_2025 | t_2025 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | -1.03 | 1.124 | -0.92 | 0.0104 | 0.019 | -0.208 | -0.11 |
| 10 | -1.431 | 1.637 | -0.87 | 0.0082 | 0.0231 | 0.788 | 0.32 |
| 20 | -1.534 | 1.763 | -0.87 | 0.0078 | 0.0239 | 1.039 | 0.41 |
| 40 | -1.633 | 1.851 | -0.88 | 0.0074 | 0.025 | 1.309 | 0.51 |
| 80 | -1.757 | 1.918 | -0.92 | 0.0072 | 0.0271 | 1.626 | 0.62 |
| 160 | -1.919 | 1.962 | -0.98 | 0.007 | 0.0307 | 1.991 | 0.75 |
| 320 | -2.105 | 1.984 | -1.06 | 0.0069 | 0.0357 | 2.368 | 0.88 |
| inf | -2.558 | 2.008 | -1.27 | 0.0068 | 0.0492 | 3.463 | 1.26 |

Completion rate (tested on receptions):

| m | beta | se | t | sd_log_mult | sse_drop_pct | beta_2025 | t_2025 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | -1.601 | 0.935 | -1.71 | 0.0107 | 0.0703 | 2.566 | 1.78 |
| 10 | -1.511 | 1.051 | -1.44 | 0.01 | 0.0548 | 3.332 | 2.11 |
| 20 | -1.434 | 1.063 | -1.35 | 0.0099 | 0.0484 | 3.464 | 2.14 |
| 40 | -1.348 | 1.072 | -1.26 | 0.0098 | 0.042 | 3.533 | 2.14 |
| 80 | -1.261 | 1.077 | -1.17 | 0.0097 | 0.0364 | 3.534 | 2.12 |
| 160 | -1.187 | 1.079 | -1.1 | 0.0097 | 0.032 | 3.482 | 2.09 |
| 320 | -1.13 | 1.08 | -1.05 | 0.0097 | 0.029 | 3.406 | 2.06 |
| inf | -1.027 | 1.085 | -0.95 | 0.0097 | 0.0239 | 3.251 | 2.02 |

Attempts lost to sacks (tested on targets):

| m | beta | se | t | sd_log_mult | sse_drop_pct | beta_2025 | t_2025 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.125 | 1.197 | 0.1 | 0.0089 | 0.0004 | 3.229 | 1.93 |
| 10 | -0.134 | 1.144 | -0.12 | 0.0086 | 0.0004 | 2.79 | 1.58 |
| 20 | -0.186 | 1.146 | -0.16 | 0.0085 | 0.0008 | 2.647 | 1.48 |
| 40 | -0.22 | 1.152 | -0.19 | 0.0084 | 0.0011 | 2.518 | 1.39 |
| 80 | -0.24 | 1.16 | -0.21 | 0.0083 | 0.0013 | 2.41 | 1.32 |
| 160 | -0.255 | 1.167 | -0.22 | 0.0083 | 0.0014 | 2.319 | 1.27 |
| 320 | -0.27 | 1.17 | -0.23 | 0.0082 | 0.0016 | 2.239 | 1.23 |
| inf | -0.321 | 1.169 | -0.27 | 0.0083 | 0.0022 | 2.052 | 1.16 |

Team level, 2023-2024 (832 team-games). Correlation of the pre-game number with what the offense then did:

- pressure rate allowed in the game: opponent pressure rate +0.175, expected pressure rate (QB x opponent) +0.227
- sack rate: opponent pressure rate +0.065, expected pressure rate (QB x opponent) +0.202
- completion %: opponent pressure rate -0.033, expected pressure rate (QB x opponent) -0.129
- yards per attempt: opponent pressure rate +0.037, expected pressure rate (QB x opponent) -0.044
- yards per dropback: opponent pressure rate +0.023, expected pressure rate (QB x opponent) -0.081

Team level, 2025 (416 team-games). Correlation of the pre-game number with what the offense then did:

- pressure rate allowed in the game: opponent pressure rate +0.134, expected pressure rate (QB x opponent) +0.202
- sack rate: opponent pressure rate +0.139, expected pressure rate (QB x opponent) +0.183
- completion %: opponent pressure rate -0.149, expected pressure rate (QB x opponent) -0.127
- yards per attempt: opponent pressure rate -0.072, expected pressure rate (QB x opponent) -0.083
- yards per dropback: opponent pressure rate -0.097, expected pressure rate (QB x opponent) -0.112

### Opponent tier and the defense factor weight

Mean squared yardage error on the fit seasons: no defense factor 776.919, current half weight 779.165, best weight 0.125 (capped) 776.277.

Weight on the defense's catch rate and yards per catch allowed (capped at +/-20% as now):

| weight | mse | mae |
| --- | --- | --- |
| 0.0 | 776.919 | 20.352 |
| 0.125 | 776.277 | 20.3618 |
| 0.25 | 776.456 | 20.3808 |
| 0.375 | 777.472 | 20.4109 |
| 0.5 | 779.165 | 20.4493 |
| 0.625 | 781.464 | 20.4948 |
| 0.75 | 784.133 | 20.5428 |
| 0.875 | 786.965 | 20.5897 |
| 1.0 | 789.997 | 20.6391 |
| 1.125 | 792.912 | 20.6832 |
| 1.25 | 795.732 | 20.7227 |
| 1.375 | 798.624 | 20.7609 |
| 1.5 | 801.563 | 20.7973 |

Yards per game the defense allows his position, as one factor (exponent fitted with no other defense factor): {'beta': 0.076, 'se': 0.068, 't': 1.13}

Targets per game the defense allows his position, on top of the current model: {'beta': 0.054, 'se': 0.063, 't': 0.86}

Tier split (his yards per game vs this opponent's tier / his overall) replacing the defense factor:

| m | beta | se | t | sd_log_mult | mse_as_is | mse_with_beta |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.022 | 0.048 | 0.45 | 0.3242 | 864.227 | 776.872 |
| 10 | 0.052 | 0.091 | 0.57 | 0.1644 | 800.252 | 776.845 |
| 20 | 0.063 | 0.104 | 0.61 | 0.1436 | 794.445 | 776.833 |
| 40 | 0.072 | 0.111 | 0.65 | 0.1341 | 791.817 | 776.821 |
| 80 | 0.077 | 0.113 | 0.68 | 0.1307 | 790.819 | 776.814 |
| 160 | 0.079 | 0.114 | 0.69 | 0.1297 | 790.472 | 776.81 |
| 320 | 0.08 | 0.114 | 0.7 | 0.1294 | 790.353 | 776.808 |
| inf | 0.081 | 0.114 | 0.71 | 0.1292 | 790.276 | 776.807 |

His own tier split only (league tier effect removed), on top of the current model:

| m | beta | se | t | sd_log_mult | mse_as_is | mse_with_beta |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.018 | 0.051 | 0.35 | 0.3081 | 855.833 | 779.138 |
| 10 | -0.008 | 0.147 | -0.05 | 0.0988 | 788.815 | 779.165 |
| 20 | -0.028 | 0.237 | -0.12 | 0.0603 | 783.102 | 779.162 |
| 40 | -0.063 | 0.414 | -0.15 | 0.0342 | 780.56 | 779.16 |
| 80 | -0.13 | 0.766 | -0.17 | 0.0184 | 779.625 | 779.159 |
| 160 | -0.263 | 1.468 | -0.18 | 0.0096 | 779.317 | 779.158 |
| 320 | -0.527 | 2.871 | -0.18 | 0.0049 | 779.219 | 779.158 |
| inf | 0.0 | None | 0.0 | 0.0 | 779.165 | 779.165 |

## How much data sits behind each split (2025 rows)

- Median prior targets vs man: 29; vs zone: 45; middle open: 31; middle closed: 41.
- Opponent man rate, 10th to 90th percentile: 23.6% to 41.4% (league 32.4%).
- Opponent middle-open rate: 38.0% to 51.3% (league 44.5%).
- Opponent pressure rate: 25.2% to 33.5% (league 29.4%).
- Median prior games against the opponent's tier: 6.
- Coverage multipliers as derived (m=40), 5th to 95th percentile: man/zone yards [0.98, 1.019], targets [0.967, 1.033]; middle open/closed yards [0.989, 1.011], targets [0.981, 1.018].
- Pressure yards-per-attempt multiplier as derived (m=100), 5th to 95th percentile: [0.989, 1.012].
- League rates by season (the coverage labels are not consistent from year to year, so every rate is compared with the league in the same season): 2023: man 40.9%, middle open 42.4%, pressure 29.7%; 2024: man 48.2%, middle open 39.4%, pressure 29.8%; 2025: man 32.4%, middle open 44.5%, pressure 29.4%.


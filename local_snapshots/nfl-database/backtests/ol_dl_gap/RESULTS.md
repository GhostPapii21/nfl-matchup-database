# OL-vs-DL run-matchup gap: backtest (2026 Wk3–8). Analysis only, no rules or scan changed
Generated 2026-11-01 (ET). Scripts: `bt_gap.py` builds the legs, `analyze.py` builds the tables. Every leg is in `ol_dl_gap_legs.csv`. No PFF data was used; everything comes from our own nflverse play-by-play plus the ESPN box files in `playlogs/2026_wk8`.

## Factor (walk-forward: week W uses only plays before W)
- Built on RB carries only, with QB kneels removed. Three measures per team: success rate (nflverse `success`), stuff rate (share of carries for 0 or fewer yards), and YPC.
- One-step opponent adjustment, defense mirrored.
- Composite = mean of z(success), −z(stuff), z(YPC). This is turned into an offense percentile (higher = better blocking) and a defense percentile (higher = stronger run D).
- **gap = offense percentile − defense percentile.**

## Legs
- One lead RB per team per week: most prior RB carries, at least 2 games, averaging 8+ carries. 153 legs.
- Lines: 16 real Week 8 book lines; the other 137 are stand-ins (floor of prior median + 0.5). Each leg's line type is labeled.
- p = raw sim_v6 (no calibration, to avoid leaking future data). 100k sims for each of the three models, averaged, with the game spread applied.
- Week 8 Sunday games are graded from the ESPN box files; everything else from play-by-play.

### All lead-RB legs
| Bucket | n | Over W | Over hit | 90% CI | ROI −110 | −130 | −160 | Under hit | U ROI −110 | −130 | −160 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 153 | 71 | 46.4% | 40%-53% | -11.4% | -17.9% | -24.6% | 53.6% | +2.3% | -5.2% | -12.9% |

### Gap terciles
| Bucket | n | Over W | Over hit | 90% CI | ROI −110 | −130 | −160 | Under hit | U ROI −110 | −130 | −160 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 (OL worst vs DL) | 51 | 20 | 39.2% | 29%-51% | -25.1% | -30.6% | -36.3% | 60.8% | +16.0% | +7.5% | -1.2% |
| T2 | 51 | 28 | 54.9% | 43%-66% | +4.8% | -2.9% | -10.8% | 45.1% | -13.9% | -20.2% | -26.7% |
| T3 (OL best vs DL) | 51 | 23 | 45.1% | 34%-57% | -13.9% | -20.2% | -26.7% | 54.9% | +4.8% | -2.9% | -10.8% |

### Gap quintiles
| Bucket | n | Over W | Over hit | 90% CI | ROI −110 | −130 | −160 | Under hit | U ROI −110 | −130 | −160 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 31 | 15 | 48.4% | 34%-63% | -7.6% | -14.4% | -21.4% | 51.6% | -1.5% | -8.7% | -16.1% |
| Q2 | 30 | 9 | 30.0% | 18%-45% | -42.7% | -46.9% | -51.2% | 70.0% | +33.6% | +23.8% | +13.7% |
| Q3 | 31 | 18 | 58.1% | 43%-71% | +10.9% | +2.7% | -5.6% | 41.9% | -19.9% | -25.8% | -31.9% |
| Q4 | 30 | 13 | 43.3% | 30%-58% | -17.3% | -23.3% | -29.6% | 56.7% | +8.2% | +0.3% | -7.9% |
| Q5 | 31 | 16 | 51.6% | 37%-66% | -1.5% | -8.7% | -16.1% | 48.4% | -7.6% | -14.4% | -21.4% |

Quintile gap ranges: Q1 [-88,-31], Q2 [-28,-6], Q3 [-6,16], Q4 [16,38], Q5 [38,84]

### Within sim_v6 p buckets, gap split at 0
| Bucket | n | Over W | Over hit | 90% CI | ROI −110 | −130 | −160 | Under hit | U ROI −110 | −130 | −160 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| p<.45 & gap <=0 | 31 | 11 | 35.5% | 23%-50% | -32.3% | -37.2% | -42.3% | 64.5% | +23.2% | +14.1% | +4.8% |
| p<.45 & gap >0 | 34 | 12 | 35.3% | 23%-49% | -32.6% | -37.6% | -42.6% | 64.7% | +23.5% | +14.5% | +5.1% |
| p .45-.55 & gap <=0 | 16 | 7 | 43.8% | 26%-64% | -16.5% | -22.6% | -28.9% | 56.2% | +7.4% | -0.5% | -8.6% |
| p .45-.55 & gap >0 | 17 | 11 | 64.7% | 45%-81% | +23.5% | +14.5% | +5.1% | 35.3% | -32.6% | -37.6% | -42.6% |
| p>=.55 & gap <=0 | 23 | 11 | 47.8% | 32%-64% | -8.7% | -15.4% | -22.3% | 52.2% | -0.4% | -7.7% | -15.2% |
| p>=.55 & gap >0 | 32 | 19 | 59.4% | 45%-72% | +13.4% | +5.0% | -3.5% | 40.6% | -22.4% | -28.1% | -34.0% |

### By line source
| Bucket | n | Over W | Over hit | 90% CI | ROI −110 | −130 | −160 | Under hit | U ROI −110 | −130 | −160 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| real lines | 16 | 7 | 43.8% | 26%-64% | -16.5% | -22.6% | -28.9% | 56.2% | +7.4% | -0.5% | -8.6% |
| stand-ins | 137 | 64 | 46.7% | 40%-54% | -10.8% | -17.3% | -24.1% | 53.3% | +1.7% | -5.7% | -13.4% |

### n per week × tercile
| week   |   T1 (OL worst vs DL) |   T2 |   T3 (OL best vs DL) |   All |
|:-------|----------------------:|-----:|---------------------:|------:|
| 3      |                    12 |    9 |                   11 |    32 |
| 4      |                    10 |    8 |                   10 |    28 |
| 5      |                    10 |    6 |                    9 |    25 |
| 6      |                     4 |    8 |                    9 |    21 |
| 7      |                     9 |   10 |                    8 |    27 |
| 8      |                     6 |   10 |                    4 |    20 |
| All    |                    51 |   51 |                   51 |   153 |

### What the gap predicts (Spearman, all legs)
- gap vs actual: rho +0.210 (p=0.009)
- gap vs yds_resid: rho -0.022 (p=0.790)
- gap vs ypc: rho +0.173 (p=0.033)
- gap vs ypc_resid: rho -0.094 (p=0.245)
- gap vs carries: rho +0.148 (p=0.068)
- gap vs car_resid: rho +0.102 (p=0.209)
- gap vs over_hit: rho +0.037 (p=0.649)
- (reference) sim p vs over_hit: rho +0.159 (p=0.050)
- gap vs sim p (overlap): rho +0.014

### Walk-forward logistic (train weeks < W, test W=4..8; n test=121)
| Model | log loss | Brier |
|---|---|---|
| raw sim p | 0.6918 | 0.2478 |
| logit(p) refit | 0.7045 | 0.2556 |
| logit(p) + gap | 0.7110 | 0.2588 |
Coefficients [logit p, gap/50] per test week: W4 (train n 32): [-0.082, 0.044]; W5 (train n 60): [0.37, -0.218]; W6 (train n 85): [0.324, 0.035]; W7 (train n 106): [0.337, -0.007]; W8 (train n 133): [0.381, -0.009]
In-sample full fit coef [logit p, gap/50]: [0.341, 0.066]

### Week 8 examples
| player              | team   | opp   |   off_pct |   def_pct |     gap |   line | line_src   |   p_over |   carries |   actual |   over_hit |
|:--------------------|:-------|:------|----------:|----------:|--------:|-------:|:-----------|---------:|----------:|---------:|-----------:|
| Chuba Hubbard       | CAR    | GB    |    75     |    81.25  |  -6.25  |   67.5 | standin    |    0.511 |        22 |       81 |          1 |
| Bijan Robinson      | ATL    | TB    |    90.625 |    87.5   |   3.125 |   80.5 | real       |    0.358 |        19 |       76 |          0 |
| Bucky Irving        | TB     | ATL   |    81.25  |    68.75  |  12.5   |   70.5 | real       |    0.477 |        27 |      170 |          1 |
| Quinshon Judkins    | CLE    | PIT   |    53.125 |   100     | -46.875 |   47.5 | real       |    0.557 |        11 |       25 |          0 |
| Jaylen Warren       | PIT    | CLE   |    84.375 |    56.25  |  28.125 |   64.5 | real       |    0.589 |        17 |      143 |          1 |
| Jonathan Taylor     | IND    | JAX   |    68.75  |    93.75  | -25     |   50.5 | real       |    0.65  |         8 |       23 |          0 |
| Bhayshul Tuten      | JAX    | IND   |    71.875 |    25     |  46.875 |   65.5 | real       |    0.616 |        16 |      104 |          1 |
| Ashton Jeanty       | LV     | NYJ   |     3.125 |    21.875 | -18.75  |   48.5 | standin    |    0.397 |         2 |        9 |          0 |
| Braelon Allen       | NYJ    | LV    |    31.25  |    15.625 |  15.625 |   59.5 | standin    |    0.632 |        21 |      147 |          1 |
| Jahmyr Gibbs        | DET    | MIN   |    50     |    59.375 |  -9.375 |   87.5 | real       |    0.59  |        23 |      153 |          1 |
| Derrick Henry       | BAL    | BUF   |    37.5   |    65.625 | -28.125 |   78.5 | real       |    0.414 |        11 |       53 |          0 |
| Tony Pollard        | TEN    | CIN   |    56.25  |    90.625 | -34.375 |   66.5 | real       |    0.632 |        21 |      117 |          1 |
| Chase Brown         | CIN    | TEN   |    59.375 |    34.375 |  25     |   58.5 | real       |    0.302 |        12 |       55 |          0 |
| Jeremiyah Love      | ARI    | DAL   |    25     |     9.375 |  15.625 |   41.5 | standin    |    0.773 |         9 |       23 |          0 |
| Javonte Williams    | DAL    | ARI   |    62.5   |    31.25  |  31.25  |   76.5 | real       |    0.425 |        24 |       56 |          0 |
| Omarion Hampton     | LAC    | LAR   |    43.75  |    75     | -31.25  |   31.5 | real       |    0.689 |         9 |       20 |          0 |
| Rhamondre Stevenson | NE     | MIA   |    46.875 |    28.125 |  18.75  |   60.5 | real       |    0.178 |        19 |       82 |          1 |
| Ollie Gordon II     | MIA    | NE    |    40.625 |    43.75  |  -3.125 |   60.5 | real       |    0.455 |        19 |       69 |          1 |
| Kenneth Walker III  | KC     | DEN   |    87.5   |    84.375 |   3.125 |   87.5 | real       |    0.596 |        21 |       69 |          0 |
| J.K. Dobbins        | DEN    | KC    |    78.125 |    78.125 |   0     |   28.5 | real       |    0.716 |         7 |       13 |          0 |
## Read
- **Gap alone has no signal on whether the over hits:** Spearman rho +0.04 (p = .65). The terciles and quintiles don't move in order (Q2 is the worst, Q3 the best). That is noise, not a pattern.
- **It does track raw volume and efficiency:** actual yards rho +0.21, YPC +0.17, carries +0.15. But against the player's own prior YPC and carries the effect is gone (YPC vs prior −0.09, carries vs prior +0.10, yards vs line −0.02). The line and the player's prior form already price it in.
- **On top of sim_v6:**
  - Within p buckets, gap > 0 looks better for p .45–.55 (11/17 vs 7/16) and p ≥ .55 (19/32 vs 11/23).
  - But it does nothing for p < .45, and those cells have only 16–34 legs each.
  - In the walk-forward logistic regression, adding gap made out-of-sample log loss and Brier score *worse* (0.7110 vs 0.7045 for p alone). The gap coefficient flips sign from week to week.
- **Week 8 examples:** our own play-by-play gives KC's blocking the 88th percentile, not 28th, so the Walker read isn't reproduced. Pollard (gap −34) beat it; Gibbs (gap −9) and Irving (+12.5) are mid-range. PFF's grades and play-by-play efficiency disagree a lot.
- **Small samples:** every bucket is under 55 legs, there are only 16 real lines, and weeks have 20–32 legs each.

## Recommendation
**Drop it for now** as a gate input. Don't add it as a scan factor yet either. Re-test after Week 12 (about 300 legs). The within-bucket lift at p ≥ .45 is the one thing worth watching.

## Caveats
- 137 of 153 lines are stand-ins.
- The sim isn't calibrated.
- The one-step opponent adjustment is crude, and early weeks have only 2 prior games.
- Lead-RB selection uses prior carries only, so in-game committee changes are noise.
- Rushing success rate is partly the RB's own talent, not only the line.
- There's no pass-block or box-count data.

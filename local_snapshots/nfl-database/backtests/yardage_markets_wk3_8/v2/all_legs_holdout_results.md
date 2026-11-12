## All-legs holdout reference (no rules)

Weeks 7–8; every consensus leg from frozen legs.csv. No rule, edgecap, Sharp, or one-per-player filter. Opposing sides and multiple markets for a player remain included; this is a descriptive reference, not an independent-bet portfolio. Settlement matches grade.py: $10 per graded leg, pushes return stake, ungraded legs have zero stake; hit% excludes pushes/ungraded, ROI uses graded stake. Missing player/team or price remains ungraded. Matched players with no recorded yards settle at zero; participation voids cannot be reconstructed.

All holdout legs: market, side

    market  side   n  wins  losses  pushes  ungraded          pl  stake   hit_pct        roi
    recyds  over 356   124     143       0        89 -340.920742   2670 46.441948 -12.768567
    recyds under 356   143     124       0        89   16.953709   2670 53.558052   0.634970
rushrecyds  over  85    37      36       0        12  -35.358619    730 50.684932  -4.843646
rushrecyds under  85    36      37       0        12  -53.871348    730 49.315068  -7.379637
   rushyds  over 174    60      75       0        39 -223.138257   1350 44.444444 -16.528760
   rushyds under 174    75      60       0        39   54.258600   1350 55.555556   4.019156

All holdout legs: week, market, side

 week     market  side   n  wins  losses  pushes  ungraded          pl  stake   hit_pct        roi
    7     recyds  over 186    62      76       0        48 -216.737336   1380 44.927536 -15.705604
    7     recyds under 186    76      62       0        48   50.999634   1380 55.072464   3.695626
    7 rushrecyds  over  43    18      16       0         9   -1.988670    340 52.941176  -0.584903
    7 rushrecyds under  43    16      18       0         9  -40.038540    340 47.058824 -11.776041
    7    rushyds  over  88    31      37       0        20  -99.341050    680 45.588235 -14.608978
    7    rushyds under  88    37      31       0        20   13.169668    680 54.411765   1.936716
    8     recyds  over 170    62      67       0        41 -124.183407   1290 48.062016  -9.626621
    8     recyds under 170    67      62       0        41  -34.045925   1290 51.937984  -2.639219
    8 rushrecyds  over  42    19      20       0         3  -33.369948    390 48.717949  -8.556397
    8 rushrecyds under  42    20      19       0         3  -13.832807    390 51.282051  -3.546874
    8    rushyds  over  86    29      38       0        19 -123.797207    670 43.283582 -18.477195
    8    rushyds under  86    38      29       0        19   41.088932    670 56.716418   6.132676

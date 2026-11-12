# Stage A completed

20,612 main quotes; 3,892 consensus legs. All requested artifacts are in this directory.

## Weeks 3–6 grading only

```
    market  side   n  wins  losses  pushes  ungraded          pl  stake   hit_pct        roi
    recyds  over 771   276     306       0       189 -627.652204 5820.0 47.422680 -10.784402
    recyds under 771   306     276       0       189  -68.603074 5820.0 52.577320  -1.178747
rushrecyds  over 188    49      60       0        79 -169.571530 1090.0 44.954128 -15.557021
rushrecyds under 188    60      49       0        79   34.629723 1090.0 55.045872   3.177039
   rushyds  over 372   127     167       0        78 -560.074162 2940.0 43.197279 -19.050142
   rushyds under 372   167     127       0        78  187.593842 2940.0 56.802721   6.380743
```

## Locked train cells

- recyds under: model edge >= 15 yards; n=36; ROI=9.77%.
- rushyds under: model edge >= 10 yards; n=49; ROI=14.96%.

Edgecap uses the identical rules and additionally excludes model edge >15. No holdout results were computed or printed. grade.py was written and syntax-checked, but not run.

Validation: Stage A validation passed: main-only, consensus, train lock, player/game caps, holdout withheld.

No network, environment-key reads, or git commits. v1 unchanged. Read README.md for missing prices, identity, PBP/void and payout limitations.

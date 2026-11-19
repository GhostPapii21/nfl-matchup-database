# NFL edge research 2026

Research outputs only. These results do not wire into the dashboard or make a pick list. The snapshot is based on direct-line commit `b5b791b` at 2026-11-19 22:39 UTC.

## Task 1: Pinnacle fair prices and cross-book edges

`fair_price.py` removes Pinnacle's vig when both sides are present. Same-line prices are compared directly. For different lines, it shifts the Pinnacle fair probability by the Task 3 model's change in tail probability, anchored at the Pinnacle line.

Across 30 direct-line game files, 2,569 other-book prices could be compared with a paired Pinnacle line: 1,645 at the same line and 924 after a distribution-based line shift. Another 498 mismatched prices had Pinnacle markets but no usable player context; 658 had no paired Pinnacle market. The screen returned 19 rows at or above a 2-point probability edge: 17 line-shifted and two same-line. Counts by book are BetMGM 1, BetOnline 1, BetRivers 5, Bovada 5, DraftKings 3, and FanDuel 4.

These are price-screen candidates, not statistically significant or validated betting edges. The line-shift estimates depend on the Week 8-9-researched yardage distribution and should be read with Task 3's backtest limitations.

## Task 3: Alternate ladders

`ladder.py` fits zero-inflated gamma shapes to normalized player-game yards using 2022 and 2024 nflverse play-by-play. It estimates shapes by position and aDOT band, and computes player aDOT using games strictly before each prediction. The repository has no 2023 play-by-play file. The fit used 13,095 opportunity-level player-game rows and 9,941 normalized observations, producing 22 supported shape groups.

The direct-line files contain 1,697 FanDuel rungs with a matching main line across 12 games. The archived Week 8-9 ladder file contains 5,138 graded rungs; this model produced probabilities for 5,065 rungs across 524 player-game-market clusters. The other 73 rows lack a saved pregame trailing mean. Because those archived odds contain no contemporaneous main lines or two-way alternate prices, this backtest anchors the model median to the saved pregame trailing mean and removes vig using the available FanDuel main-line average hold proxy (6.443% receiving, 6.453% rushing).

| Probability source | Brier score | Difference from book |
|---|---:|---:|
| FanDuel implied probability after hold proxy | 0.161723 | — |
| Distribution | 0.179855 | +0.018131 |
| Average of book and distribution | 0.166589 | +0.004866 |

The player-game cluster bootstrap 95% interval for distribution minus book Brier is +0.012195 to +0.024007. For the blend it is +0.001996 to +0.007665. Both differences are above zero, so both alternatives were significantly worse than the book on this proxy backtest. The comparison is descriptive and is not a main-line-matched or true no-vig alt-ladder test.

## Task 2: Closing-line value

`clv.py` reconstructs opening and last pre-kickoff prices from the direct-line commit history and checks whether Pinnacle moved toward each Task 1 edge.

As of 2026-11-19 22:39 UTC, no game had both kicked off and supplied two distinct pregame quotes in this history. Final CLV sample: n=0; mean, positive share, and 95% interval are not estimable. There are 6,448 pending quote rows with multiple snapshots; their provisional open-to-latest break-even movement averages -0.000712 (about -0.071 percentage points). These prices are not closing lines. The Week 10 LAC-BAL file has 364 rows but only one snapshot. All 19 Task 1 rows are still pending, so no Pinnacle close movement can yet be graded.

## Task 4: Residual model

`residual.py` contains the requested statsmodels Binomial GLM with the fair-book logit as an offset, chronological evaluation, and player-game clustered ROI bootstrap. It did not fit a model: there are zero finalized direct-line rows to use as settled outcomes, and the available participation CSVs list substitution participants but not routes. TPRR and route-share-change features therefore cannot be computed. The 5,138 archived alternate rungs are one-sided and do not contain the full feature set.

No coefficient, standard error, out-of-sample Brier score, or ROI is estimable from these inputs. `residual_model.json` records null coefficients rather than filling them with estimates unsupported by data. No significance claim is made.

## Files and reproduction

- `ladder.py` writes `ladder.json`.
- `fair_price.py` writes `edges_latest.json` and `fair_prices_latest.json`.
- `clv.py` writes `clv.json`.
- `residual.py` writes `residual.json` and `residual_model.json`.
- `test_edge.py` covers de-vig math, name matching, same-line comparisons, line shifting, open/close selection, and no-future-data feature filtering.

Run from the repository root with Python 3.12, pandas, NumPy, SciPy, statsmodels, and a pandas Parquet reader available:

```sh
python research/edge_2026/ladder.py
python research/edge_2026/fair_price.py
python research/edge_2026/clv.py
python research/edge_2026/residual.py
pytest research/edge_2026/test_edge.py
```

Run `ladder.py` before `fair_price.py` so line-shift pricing uses the current distribution artifact. The 2026 play-by-play snapshot included here ends at Week 9; later lines are quoted but not graded against outcomes.

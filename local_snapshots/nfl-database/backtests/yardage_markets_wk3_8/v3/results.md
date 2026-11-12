# Stage B results

Both portfolios fail the holdout target. Singles: 102 bets, 45.10% hit, −$153.84 P/L, −15.08% ROI. Slips: 26 bets, 0% hit, −$260.00 P/L, −100% ROI. Both holdout weeks lost money.

Executed frozen `grade.py` unchanged, offline. All 15 entries in `frozen_sha256.json` matched before execution, after execution, and after report formatting. No rules were refit. Train = weeks 3–6; holdout = weeks 7–8.

Singles and slips are separate $10-per-bet portfolios. W/L = wins/losses; hit excludes pushes/ungraded; ROI = P/L ÷ settled stake. All selected singles and slips have zero pushes and zero ungraded bets. Slip payouts multiply quoted decimal odds and are estimates; correlation, SGP repricing, and participation voids are unavailable. See `GAPS.md` for source coverage and leakage risks.

## Singles totals and weeks

| Period | n | W/L | Hit | P/L $ | ROI |
| --- | --- | --- | --- | --- | --- |
| holdout | 102 | 46/56 | 45.10% | -153.84 | -15.08% |
| train | 180 | 123/57 | 68.33% | +513.14 | +28.51% |
| W3 | 49 | 33/16 | 67.35% | +132.18 | +26.97% |
| W4 | 44 | 29/15 | 65.91% | +106.40 | +24.18% |
| W5 | 43 | 27/16 | 62.79% | +76.38 | +17.76% |
| W6 | 44 | 34/10 | 77.27% | +198.17 | +45.04% |
| W7 | 47 | 23/24 | 48.94% | -37.23 | -7.92% |
| W8 | 55 | 23/32 | 41.82% | -116.61 | -21.20% |

## Slips totals and weeks

| Period | n | W/L | Hit | P/L $ | ROI |
| --- | --- | --- | --- | --- | --- |
| holdout | 26 | 0/26 | 0.00% | -260.00 | -100.00% |
| train | 45 | 7/38 | 15.56% | +415.53 | +92.34% |
| W3 | 12 | 1/11 | 8.33% | +4.91 | +4.09% |
| W4 | 11 | 0/11 | 0.00% | -110.00 | -100.00% |
| W5 | 11 | 1/10 | 9.09% | +13.73 | +12.48% |
| W6 | 11 | 5/6 | 45.45% | +506.89 | +460.81% |
| W7 | 12 | 0/12 | 0.00% | -120.00 | -100.00% |
| W8 | 14 | 0/14 | 0.00% | -140.00 | -100.00% |

Market key: R = rushing yards; C = receiving yards; RR = rushing + receiving yards; O/U = over/under. Mixed slips are grouped by their full market-side composition, not attributed to individual markets. Singles market tables reflect cross-rule player deduplication.

## Singles by period × market/side

| Period | Market/side | n | W/L | Hit | P/L $ | ROI |
| --- | --- | --- | --- | --- | --- | --- |
| holdout | C O | 13 | 4/9 | 30.77% | -54.94 | -42.26% |
| holdout | C U | 27 | 9/18 | 33.33% | -100.05 | -37.06% |
| holdout | RR U | 30 | 15/15 | 50.00% | -18.38 | -6.13% |
| holdout | R O | 19 | 8/11 | 42.11% | -38.29 | -20.15% |
| holdout | R U | 13 | 10/3 | 76.92% | +57.82 | +44.48% |
| train | C O | 39 | 26/13 | 66.67% | +98.39 | +25.23% |
| train | C U | 44 | 32/12 | 72.73% | +161.25 | +36.65% |
| train | RR U | 34 | 22/12 | 64.71% | +72.95 | +21.46% |
| train | R O | 29 | 19/10 | 65.52% | +69.78 | +24.06% |
| train | R U | 34 | 24/10 | 70.59% | +110.77 | +32.58% |

## Singles by week × market/side

| Period | Market/side | n | W/L | Hit | P/L $ | ROI |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | C O | 16 | 11/5 | 68.75% | +46.43 | +29.02% |
| 3 | C U | 8 | 5/3 | 62.50% | +13.98 | +17.48% |
| 3 | RR U | 7 | 5/2 | 71.43% | +23.82 | +34.04% |
| 3 | R O | 8 | 6/2 | 75.00% | +34.97 | +43.71% |
| 3 | R U | 10 | 6/4 | 60.00% | +12.97 | +12.97% |
| 4 | C O | 10 | 9/1 | 90.00% | +69.39 | +69.39% |
| 4 | C U | 7 | 2/5 | 28.57% | -32.38 | -46.25% |
| 4 | RR U | 9 | 5/4 | 55.56% | +3.94 | +4.38% |
| 4 | R O | 7 | 4/3 | 57.14% | +7.05 | +10.07% |
| 4 | R U | 11 | 9/2 | 81.82% | +58.40 | +53.09% |
| 5 | C O | 8 | 3/5 | 37.50% | -23.68 | -29.60% |
| 5 | C U | 12 | 9/3 | 75.00% | +48.57 | +40.47% |
| 5 | RR U | 8 | 5/3 | 62.50% | +14.06 | +17.58% |
| 5 | R O | 8 | 5/3 | 62.50% | +13.22 | +16.53% |
| 5 | R U | 7 | 5/2 | 71.43% | +24.21 | +34.59% |
| 6 | C O | 5 | 3/2 | 60.00% | +6.25 | +12.49% |
| 6 | C U | 17 | 16/1 | 94.12% | +131.07 | +77.10% |
| 6 | RR U | 10 | 7/3 | 70.00% | +31.12 | +31.12% |
| 6 | R O | 6 | 4/2 | 66.67% | +14.54 | +24.23% |
| 6 | R U | 6 | 4/2 | 66.67% | +15.19 | +25.32% |
| 7 | C O | 3 | 1/2 | 33.33% | -11.45 | -38.18% |
| 7 | C U | 13 | 5/8 | 38.46% | -35.22 | -27.09% |
| 7 | RR U | 14 | 7/7 | 50.00% | -8.44 | -6.03% |
| 7 | R O | 10 | 5/5 | 50.00% | -6.03 | -6.03% |
| 7 | R U | 7 | 5/2 | 71.43% | +23.92 | +34.17% |
| 8 | C O | 10 | 3/7 | 30.00% | -43.49 | -43.49% |
| 8 | C U | 14 | 4/10 | 28.57% | -64.83 | -46.31% |
| 8 | RR U | 16 | 8/8 | 50.00% | -9.94 | -6.21% |
| 8 | R O | 9 | 3/6 | 33.33% | -32.26 | -35.84% |
| 8 | R U | 6 | 5/1 | 83.33% | +33.90 | +56.50% |

## Slips by period × market/side

| Period | Market/side | n | W/L | Hit | P/L $ | ROI |
| --- | --- | --- | --- | --- | --- | --- |
| holdout | C O, C U, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| holdout | C O, C U, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| holdout | C O, C U, R O | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| holdout | C O, RR U | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| holdout | C O, RR U, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| holdout | C U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| holdout | C U, RR U | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| holdout | C U, RR U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| holdout | C U, RR U, R U | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| holdout | C U, R O, R U | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| holdout | RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| holdout | RR U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| holdout | RR U, R O, R U | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| train | C O, C U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| train | C O, C U, RR U | 5 | 1/4 | 20.00% | +74.74 | +149.47% |
| train | C O, C U, RR U, R O | 1 | 1/0 | 100.00% | +110.95 | +1109.51% |
| train | C O, C U, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| train | C O, C U, R O | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| train | C O, C U, R O, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| train | C O, C U, R U | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| train | C O, RR U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| train | C O, RR U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| train | C O, RR U, R U | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| train | C O, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| train | C O, R O, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| train | C U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| train | C U, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| train | C U, RR U, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| train | C U, RR U, R U | 3 | 1/2 | 33.33% | +96.25 | +320.85% |
| train | C U, R O | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| train | C U, R O, R U | 3 | 1/2 | 33.33% | +93.00 | +310.00% |
| train | C U, R U | 1 | 1/0 | 100.00% | +111.94 | +1119.45% |
| train | RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| train | RR U, R O, R U | 4 | 0/4 | 0.00% | -40.00 | -100.00% |
| train | RR U, R U | 1 | 1/0 | 100.00% | +114.91 | +1149.07% |
| train | R O, R U | 2 | 1/1 | 50.00% | +103.73 | +518.65% |

## Slips by week × market/side

| Period | Market/side | n | W/L | Hit | P/L $ | ROI |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | C O, C U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 3 | C O, C U, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 3 | C O, C U, R O, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 3 | C O, C U, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 3 | C O, RR U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 3 | C O, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 3 | C O, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 3 | C O, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 3 | C U, RR U, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 3 | RR U, R U | 1 | 1/0 | 100.00% | +114.91 | +1149.07% |
| 4 | C O, C U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 4 | C O, C U, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 4 | C O, C U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 4 | C O, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 4 | C O, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 4 | C O, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 4 | C U, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 4 | C U, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 4 | RR U, R O, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 4 | R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 5 | C O, C U, RR U | 3 | 0/3 | 0.00% | -30.00 | -100.00% |
| 5 | C O, C U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 5 | C O, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 5 | C U, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 5 | C U, R O | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 5 | RR U, R O, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 5 | R O, R U | 1 | 1/0 | 100.00% | +113.73 | +1137.30% |
| 6 | C O, C U, RR U | 1 | 1/0 | 100.00% | +114.74 | +1147.37% |
| 6 | C O, C U, RR U, R O | 1 | 1/0 | 100.00% | +110.95 | +1109.51% |
| 6 | C O, C U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 6 | C O, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 6 | C U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 6 | C U, RR U, R U | 2 | 1/1 | 50.00% | +106.25 | +531.27% |
| 6 | C U, R O, R U | 2 | 1/1 | 50.00% | +103.00 | +515.00% |
| 6 | C U, R U | 1 | 1/0 | 100.00% | +111.94 | +1119.45% |
| 6 | RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 7 | C O, C U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 7 | C O, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 7 | C U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 7 | C U, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 7 | C U, RR U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 7 | C U, RR U, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 7 | C U, R O, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 7 | RR U, R O | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 7 | RR U, R O, R U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 8 | C O, C U, RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 8 | C O, C U, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 8 | C O, C U, R O | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 8 | C O, RR U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 8 | C O, RR U, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 8 | C U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 8 | C U, RR U | 2 | 0/2 | 0.00% | -20.00 | -100.00% |
| 8 | C U, RR U, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 8 | C U, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 8 | RR U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |
| 8 | RR U, R O, R U | 1 | 0/1 | 0.00% | -10.00 | -100.00% |

## Main rushing-under baselines

| Baseline | Week | n | W/L | Hit | P/L $ | ROI | Push | Ungraded |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 3 | 97 | 35/36 | 49.30% | -51.91 | -7.31% | 0 | 26 |
| all | 4 | 96 | 47/33 | 58.75% | +84.36 | +10.55% | 0 | 16 |
| all | 5 | 90 | 42/30 | 58.33% | +68.86 | +9.56% | 0 | 18 |
| all | 6 | 89 | 35/27 | 56.45% | +25.17 | +4.06% | 0 | 27 |
| all | 7 | 88 | 37/31 | 54.41% | +13.17 | +1.94% | 0 | 20 |
| all | 8 | 86 | 38/29 | 56.72% | +41.09 | +6.13% | 0 | 19 |
| one_player | 3 | 97 | 35/36 | 49.30% | -51.91 | -7.31% | 0 | 26 |
| one_player | 4 | 96 | 47/33 | 58.75% | +84.36 | +10.55% | 0 | 16 |
| one_player | 5 | 90 | 42/30 | 58.33% | +68.86 | +9.56% | 0 | 18 |
| one_player | 6 | 89 | 35/27 | 56.45% | +25.17 | +4.06% | 0 | 27 |
| one_player | 7 | 88 | 37/31 | 54.41% | +13.17 | +1.94% | 0 | 20 |
| one_player | 8 | 86 | 38/29 | 56.72% | +41.09 | +6.13% | 0 | 19 |

`all` uses every main rushing-under consensus leg; `one_player` applies the frozen player ordering. Baseline ROI includes refunded push stakes. The two baseline variants produce identical weekly summaries in this universe.

## Per-rule comparison with rushing-under baselines

| Rule | Period | Rule n | Rule ROI | All ROI | 1/player ROI | Beats all/1p |
| --- | --- | --- | --- | --- | --- | --- |
| C O | train | 39 | +25.23% | +4.44% | +4.44% | Yes/Yes |
| C O | holdout | 13 | -42.26% | +4.02% | +4.02% | No/No |
| C O | 3 | 16 | +29.02% | -7.31% | -7.31% | Yes/Yes |
| C O | 4 | 10 | +69.39% | +10.55% | +10.55% | Yes/Yes |
| C O | 5 | 8 | -29.60% | +9.56% | +9.56% | No/No |
| C O | 6 | 5 | +12.49% | +4.06% | +4.06% | Yes/Yes |
| C O | 7 | 3 | -38.18% | +1.94% | +1.94% | No/No |
| C O | 8 | 10 | -43.49% | +6.13% | +6.13% | No/No |
| C U | train | 44 | +36.65% | +4.44% | +4.44% | Yes/Yes |
| C U | holdout | 27 | -37.06% | +4.02% | +4.02% | No/No |
| C U | 3 | 8 | +17.48% | -7.31% | -7.31% | Yes/Yes |
| C U | 4 | 7 | -46.25% | +10.55% | +10.55% | No/No |
| C U | 5 | 12 | +40.47% | +9.56% | +9.56% | Yes/Yes |
| C U | 6 | 17 | +77.10% | +4.06% | +4.06% | Yes/Yes |
| C U | 7 | 13 | -27.09% | +1.94% | +1.94% | No/No |
| C U | 8 | 14 | -46.31% | +6.13% | +6.13% | No/No |
| RR U | train | 34 | +21.46% | +4.44% | +4.44% | Yes/Yes |
| RR U | holdout | 31 | -3.10% | +4.02% | +4.02% | No/No |
| RR U | 3 | 7 | +34.04% | -7.31% | -7.31% | Yes/Yes |
| RR U | 4 | 9 | +4.38% | +10.55% | +10.55% | No/No |
| RR U | 5 | 8 | +17.58% | +9.56% | +9.56% | Yes/Yes |
| RR U | 6 | 10 | +31.12% | +4.06% | +4.06% | Yes/Yes |
| RR U | 7 | 14 | -6.03% | +1.94% | +1.94% | No/No |
| RR U | 8 | 17 | -0.68% | +6.13% | +6.13% | No/No |
| R O | train | 31 | +21.97% | +4.44% | +4.44% | Yes/Yes |
| R O | holdout | 19 | -20.15% | +4.02% | +4.02% | No/No |
| R O | 3 | 9 | +48.11% | -7.31% | -7.31% | Yes/Yes |
| R O | 4 | 7 | +10.07% | +10.55% | +10.55% | No/No |
| R O | 5 | 9 | +3.58% | +9.56% | +9.56% | No/No |
| R O | 6 | 6 | +24.23% | +4.06% | +4.06% | Yes/Yes |
| R O | 7 | 10 | -6.03% | +1.94% | +1.94% | No/No |
| R O | 8 | 9 | -35.84% | +6.13% | +6.13% | No/No |
| R U | train | 37 | +37.22% | +4.44% | +4.44% | Yes/Yes |
| R U | holdout | 13 | +44.48% | +4.02% | +4.02% | Yes/Yes |
| R U | 3 | 11 | +19.98% | -7.31% | -7.31% | Yes/Yes |
| R U | 4 | 12 | +56.04% | +10.55% | +10.55% | Yes/Yes |
| R U | 5 | 8 | +41.63% | +9.56% | +9.56% | Yes/Yes |
| R U | 6 | 6 | +25.32% | +4.06% | +4.06% | Yes/Yes |
| R U | 7 | 7 | +34.17% | +1.94% | +1.94% | Yes/Yes |
| R U | 8 | 6 | +56.50% | +6.13% | +6.13% | Yes/Yes |

Each rule is independently deduplicated for baseline comparison, before competition with other rules for the same player. “Beats” means strictly higher ROI; different markets and sample sizes are not matched cohorts. Full-precision figures and selected bets are retained in the generated CSV files.

## Holdout target judgment

| Portfolio | Requirement | Observed | Verdict |
| --- | --- | --- | --- |
| singles | n ≥100 | 102 | PASS |
| singles | Hit ≥57% | 45.10% | FAIL |
| singles | ROI ≥3% | -15.08% | FAIL |
| singles | W7 P/L ≥$0 | $-37.23 | FAIL |
| singles | W8 P/L ≥$0 | $-116.61 | FAIL |
| slips | n ≥100 | 26 | FAIL |
| slips | Hit ≥57% | 0.00% | FAIL |
| slips | ROI ≥3% | -100.00% | FAIL |
| slips | W7 P/L ≥$0 | $-120.00 | FAIL |
| slips | W8 P/L ≥$0 | $-140.00 | FAIL |

The train gains did not persist in holdout. These results do not support the locked strategy meeting the specified target; no holdout-driven rule changes were made.

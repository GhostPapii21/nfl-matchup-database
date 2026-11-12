# Frozen yardage results

Rules lock: `593ec21` (user supplied). Train: week 6 only; holdout: weeks 7–8. Weeks 3–5 and rush+receiving have no admissible quotes. No rules were retuned.

Views: `qualifying_quotes` includes every quote passing the locked cell and Sharp filter, before the player cap; these quotes are correlated. `frozen_selected` applies rules.passing unchanged (one player/week, form edge then price then candidate ID). `dedup_best_price` keeps one qualifying quote per player-side-week, highest American price then candidate ID, across lines/markets/books. This requested sensitivity can change the chosen line/market and is not line-matched price shopping. Its slips then apply the frozen player/order/game caps unchanged.

Sharp ON uses the Oct27 HINDSIGHT man filter; missing values abstain. It is not point-in-time evidence. Sharp OFF ignores Sharp. $10 per settled single/slip; pending stakes excluded from ROI. Hit% = wins/(wins+losses), excluding pushes/pending. n includes pending; won counts profitable slips. Push legs contribute decimal 1, all pushes refund; any ungraded leg leaves the slip pending. Slip payouts multiply quoted odds and are illustrative: correlation/SGP repricing, limits and participation void rules are unavailable. Singles and slips are separate portfolios.

## Singles: qualifying_quotes

| Sharp | Period | Rule cell | n | Won | Lost | Push | Pending | Hit% | $10 P/L | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OFF | week 6 | recyds/under/main/edge≥20 | 53 | 34 | 19 | 0 | 0 | 64.15% | $93.77 | 17.69% |
| OFF | week 6 | rushyds/under/main/edge≥20 | 52 | 41 | 11 | 0 | 0 | 78.85% | $206.77 | 39.76% |
| OFF | week 6 | ALL | 105 | 75 | 30 | 0 | 0 | 71.43% | $300.54 | 28.62% |
| OFF | week 7 | recyds/under/main/edge≥20 | 53 | 41 | 12 | 0 | 0 | 77.36% | $210.30 | 39.68% |
| OFF | week 7 | rushyds/under/main/edge≥20 | 53 | 26 | 27 | 0 | 0 | 49.06% | $-61.65 | -11.63% |
| OFF | week 7 | ALL | 106 | 67 | 39 | 0 | 0 | 63.21% | $148.65 | 14.02% |
| OFF | week 8 | recyds/under/main/edge≥20 | 41 | 17 | 24 | 0 | 0 | 41.46% | $-114.43 | -27.91% |
| OFF | week 8 | rushyds/under/main/edge≥20 | 51 | 33 | 18 | 0 | 0 | 64.71% | $82.24 | 16.12% |
| OFF | week 8 | ALL | 92 | 50 | 42 | 0 | 0 | 54.35% | $-32.19 | -3.50% |
| OFF | train | recyds/under/main/edge≥20 | 53 | 34 | 19 | 0 | 0 | 64.15% | $93.77 | 17.69% |
| OFF | train | rushyds/under/main/edge≥20 | 52 | 41 | 11 | 0 | 0 | 78.85% | $206.77 | 39.76% |
| OFF | train | ALL | 105 | 75 | 30 | 0 | 0 | 71.43% | $300.54 | 28.62% |
| OFF | holdout | recyds/under/main/edge≥20 | 94 | 58 | 36 | 0 | 0 | 61.70% | $95.87 | 10.20% |
| OFF | holdout | rushyds/under/main/edge≥20 | 104 | 59 | 45 | 0 | 0 | 56.73% | $20.59 | 1.98% |
| OFF | holdout | ALL | 198 | 117 | 81 | 0 | 0 | 59.09% | $116.45 | 5.88% |
| ON | week 6 | recyds/under/main/edge≥20 | 53 | 34 | 19 | 0 | 0 | 64.15% | $93.77 | 17.69% |
| ON | week 6 | rushyds/under/main/edge≥20 | 50 | 41 | 9 | 0 | 0 | 82.00% | $226.77 | 45.35% |
| ON | week 6 | ALL | 103 | 75 | 28 | 0 | 0 | 72.82% | $320.54 | 31.12% |
| ON | week 7 | recyds/under/main/edge≥20 | 51 | 41 | 10 | 0 | 0 | 80.39% | $230.30 | 45.16% |
| ON | week 7 | rushyds/under/main/edge≥20 | 49 | 25 | 24 | 0 | 0 | 51.02% | $-35.28 | -7.20% |
| ON | week 7 | ALL | 100 | 66 | 34 | 0 | 0 | 66.00% | $195.01 | 19.50% |
| ON | week 8 | recyds/under/main/edge≥20 | 41 | 17 | 24 | 0 | 0 | 41.46% | $-114.43 | -27.91% |
| ON | week 8 | rushyds/under/main/edge≥20 | 50 | 33 | 17 | 0 | 0 | 66.00% | $92.24 | 18.45% |
| ON | week 8 | ALL | 91 | 50 | 41 | 0 | 0 | 54.95% | $-22.19 | -2.44% |
| ON | train | recyds/under/main/edge≥20 | 53 | 34 | 19 | 0 | 0 | 64.15% | $93.77 | 17.69% |
| ON | train | rushyds/under/main/edge≥20 | 50 | 41 | 9 | 0 | 0 | 82.00% | $226.77 | 45.35% |
| ON | train | ALL | 103 | 75 | 28 | 0 | 0 | 72.82% | $320.54 | 31.12% |
| ON | holdout | recyds/under/main/edge≥20 | 92 | 58 | 34 | 0 | 0 | 63.04% | $115.87 | 12.59% |
| ON | holdout | rushyds/under/main/edge≥20 | 99 | 58 | 41 | 0 | 0 | 58.59% | $56.95 | 5.75% |
| ON | holdout | ALL | 191 | 116 | 75 | 0 | 0 | 60.73% | $172.82 | 9.05% |

## Singles: frozen_selected

| Sharp | Period | Rule cell | n | Won | Lost | Push | Pending | Hit% | $10 P/L | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OFF | week 6 | recyds/under/main/edge≥20 | 15 | 7 | 8 | 0 | 0 | 46.67% | $-34.95 | -23.30% |
| OFF | week 6 | rushyds/under/main/edge≥20 | 15 | 11 | 4 | 0 | 0 | 73.33% | $15.40 | 10.27% |
| OFF | week 6 | ALL | 30 | 18 | 12 | 0 | 0 | 60.00% | $-19.54 | -6.51% |
| OFF | week 7 | recyds/under/main/edge≥20 | 19 | 12 | 7 | 0 | 0 | 63.16% | $1.67 | 0.88% |
| OFF | week 7 | rushyds/under/main/edge≥20 | 13 | 5 | 8 | 0 | 0 | 38.46% | $-58.96 | -45.35% |
| OFF | week 7 | ALL | 32 | 17 | 15 | 0 | 0 | 53.12% | $-57.29 | -17.90% |
| OFF | week 8 | recyds/under/main/edge≥20 | 11 | 5 | 6 | 0 | 0 | 45.45% | $-35.64 | -32.40% |
| OFF | week 8 | rushyds/under/main/edge≥20 | 13 | 8 | 5 | 0 | 0 | 61.54% | $-12.98 | -9.98% |
| OFF | week 8 | ALL | 24 | 13 | 11 | 0 | 0 | 54.17% | $-48.61 | -20.25% |
| OFF | train | recyds/under/main/edge≥20 | 15 | 7 | 8 | 0 | 0 | 46.67% | $-34.95 | -23.30% |
| OFF | train | rushyds/under/main/edge≥20 | 15 | 11 | 4 | 0 | 0 | 73.33% | $15.40 | 10.27% |
| OFF | train | ALL | 30 | 18 | 12 | 0 | 0 | 60.00% | $-19.54 | -6.51% |
| OFF | holdout | recyds/under/main/edge≥20 | 30 | 17 | 13 | 0 | 0 | 56.67% | $-33.97 | -11.32% |
| OFF | holdout | rushyds/under/main/edge≥20 | 26 | 13 | 13 | 0 | 0 | 50.00% | $-71.94 | -27.67% |
| OFF | holdout | ALL | 56 | 30 | 26 | 0 | 0 | 53.57% | $-105.90 | -18.91% |
| ON | week 6 | recyds/under/main/edge≥20 | 15 | 7 | 8 | 0 | 0 | 46.67% | $-34.95 | -23.30% |
| ON | week 6 | rushyds/under/main/edge≥20 | 14 | 11 | 3 | 0 | 0 | 78.57% | $25.40 | 18.15% |
| ON | week 6 | ALL | 29 | 18 | 11 | 0 | 0 | 62.07% | $-9.54 | -3.29% |
| ON | week 7 | recyds/under/main/edge≥20 | 18 | 12 | 6 | 0 | 0 | 66.67% | $11.67 | 6.48% |
| ON | week 7 | rushyds/under/main/edge≥20 | 11 | 4 | 7 | 0 | 0 | 36.36% | $-52.60 | -47.82% |
| ON | week 7 | ALL | 29 | 16 | 13 | 0 | 0 | 55.17% | $-40.93 | -14.11% |
| ON | week 8 | recyds/under/main/edge≥20 | 11 | 5 | 6 | 0 | 0 | 45.45% | $-35.64 | -32.40% |
| ON | week 8 | rushyds/under/main/edge≥20 | 12 | 8 | 4 | 0 | 0 | 66.67% | $-2.98 | -2.48% |
| ON | week 8 | ALL | 23 | 13 | 10 | 0 | 0 | 56.52% | $-38.61 | -16.79% |
| ON | train | recyds/under/main/edge≥20 | 15 | 7 | 8 | 0 | 0 | 46.67% | $-34.95 | -23.30% |
| ON | train | rushyds/under/main/edge≥20 | 14 | 11 | 3 | 0 | 0 | 78.57% | $25.40 | 18.15% |
| ON | train | ALL | 29 | 18 | 11 | 0 | 0 | 62.07% | $-9.54 | -3.29% |
| ON | holdout | recyds/under/main/edge≥20 | 29 | 17 | 12 | 0 | 0 | 58.62% | $-23.97 | -8.26% |
| ON | holdout | rushyds/under/main/edge≥20 | 23 | 12 | 11 | 0 | 0 | 52.17% | $-55.57 | -24.16% |
| ON | holdout | ALL | 52 | 29 | 23 | 0 | 0 | 55.77% | $-79.54 | -15.30% |

## Singles: dedup_best_price

| Sharp | Period | Rule cell | n | Won | Lost | Push | Pending | Hit% | $10 P/L | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OFF | week 6 | recyds/under/main/edge≥20 | 15 | 6 | 9 | 0 | 0 | 40.00% | $-33.53 | -22.35% |
| OFF | week 6 | rushyds/under/main/edge≥20 | 15 | 11 | 4 | 0 | 0 | 73.33% | $42.65 | 28.44% |
| OFF | week 6 | ALL | 30 | 17 | 13 | 0 | 0 | 56.67% | $9.12 | 3.04% |
| OFF | week 7 | recyds/under/main/edge≥20 | 19 | 11 | 8 | 0 | 0 | 57.89% | $8.29 | 4.36% |
| OFF | week 7 | rushyds/under/main/edge≥20 | 13 | 3 | 10 | 0 | 0 | 23.08% | $-75.02 | -57.70% |
| OFF | week 7 | ALL | 32 | 14 | 18 | 0 | 0 | 43.75% | $-66.73 | -20.85% |
| OFF | week 8 | recyds/under/main/edge≥20 | 11 | 4 | 7 | 0 | 0 | 36.36% | $-42.06 | -38.24% |
| OFF | week 8 | rushyds/under/main/edge≥20 | 13 | 6 | 7 | 0 | 0 | 46.15% | $-24.74 | -19.03% |
| OFF | week 8 | ALL | 24 | 10 | 14 | 0 | 0 | 41.67% | $-66.80 | -27.83% |
| OFF | train | recyds/under/main/edge≥20 | 15 | 6 | 9 | 0 | 0 | 40.00% | $-33.53 | -22.35% |
| OFF | train | rushyds/under/main/edge≥20 | 15 | 11 | 4 | 0 | 0 | 73.33% | $42.65 | 28.44% |
| OFF | train | ALL | 30 | 17 | 13 | 0 | 0 | 56.67% | $9.12 | 3.04% |
| OFF | holdout | recyds/under/main/edge≥20 | 30 | 15 | 15 | 0 | 0 | 50.00% | $-33.77 | -11.26% |
| OFF | holdout | rushyds/under/main/edge≥20 | 26 | 9 | 17 | 0 | 0 | 34.62% | $-99.75 | -38.37% |
| OFF | holdout | ALL | 56 | 24 | 32 | 0 | 0 | 42.86% | $-133.53 | -23.84% |
| ON | week 6 | recyds/under/main/edge≥20 | 15 | 6 | 9 | 0 | 0 | 40.00% | $-33.53 | -22.35% |
| ON | week 6 | rushyds/under/main/edge≥20 | 14 | 11 | 3 | 0 | 0 | 78.57% | $52.65 | 37.61% |
| ON | week 6 | ALL | 29 | 17 | 12 | 0 | 0 | 58.62% | $19.12 | 6.59% |
| ON | week 7 | recyds/under/main/edge≥20 | 18 | 11 | 7 | 0 | 0 | 61.11% | $18.29 | 10.16% |
| ON | week 7 | rushyds/under/main/edge≥20 | 11 | 2 | 9 | 0 | 0 | 18.18% | $-68.65 | -62.41% |
| ON | week 7 | ALL | 29 | 13 | 16 | 0 | 0 | 44.83% | $-50.37 | -17.37% |
| ON | week 8 | recyds/under/main/edge≥20 | 11 | 4 | 7 | 0 | 0 | 36.36% | $-42.06 | -38.24% |
| ON | week 8 | rushyds/under/main/edge≥20 | 12 | 6 | 6 | 0 | 0 | 50.00% | $-14.74 | -12.28% |
| ON | week 8 | ALL | 23 | 10 | 13 | 0 | 0 | 43.48% | $-56.80 | -24.69% |
| ON | train | recyds/under/main/edge≥20 | 15 | 6 | 9 | 0 | 0 | 40.00% | $-33.53 | -22.35% |
| ON | train | rushyds/under/main/edge≥20 | 14 | 11 | 3 | 0 | 0 | 78.57% | $52.65 | 37.61% |
| ON | train | ALL | 29 | 17 | 12 | 0 | 0 | 58.62% | $19.12 | 6.59% |
| ON | holdout | recyds/under/main/edge≥20 | 29 | 15 | 14 | 0 | 0 | 51.72% | $-23.77 | -8.20% |
| ON | holdout | rushyds/under/main/edge≥20 | 23 | 8 | 15 | 0 | 0 | 34.78% | $-83.39 | -36.26% |
| ON | holdout | ALL | 52 | 23 | 29 | 0 | 0 | 44.23% | $-107.16 | -20.61% |

## Slips: frozen_selected

| Sharp | Period | n | Won | Lost | Push | Pending | Hit% | $10 P/L | ROI |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OFF | week 6 | 7 | 3 | 4 | 0 | 0 | 42.86% | $114.42 | 163.46% |
| OFF | week 7 | 8 | 0 | 8 | 0 | 0 | 0.00% | $-80.00 | -100.00% |
| OFF | week 8 | 6 | 0 | 6 | 0 | 0 | 0.00% | $-60.00 | -100.00% |
| OFF | train | 7 | 3 | 4 | 0 | 0 | 42.86% | $114.42 | 163.46% |
| OFF | holdout | 14 | 0 | 14 | 0 | 0 | 0.00% | $-140.00 | -100.00% |
| ON | week 6 | 7 | 3 | 4 | 0 | 0 | 42.86% | $115.16 | 164.51% |
| ON | week 7 | 7 | 0 | 7 | 0 | 0 | 0.00% | $-70.00 | -100.00% |
| ON | week 8 | 6 | 0 | 6 | 0 | 0 | 0.00% | $-60.00 | -100.00% |
| ON | train | 7 | 3 | 4 | 0 | 0 | 42.86% | $115.16 | 164.51% |
| ON | holdout | 13 | 0 | 13 | 0 | 0 | 0.00% | $-130.00 | -100.00% |

## Slips: dedup_best_price

| Sharp | Period | n | Won | Lost | Push | Pending | Hit% | $10 P/L | ROI |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OFF | week 6 | 7 | 1 | 6 | 0 | 0 | 14.29% | $19.75 | 28.21% |
| OFF | week 7 | 8 | 0 | 8 | 0 | 0 | 0.00% | $-80.00 | -100.00% |
| OFF | week 8 | 6 | 0 | 6 | 0 | 0 | 0.00% | $-60.00 | -100.00% |
| OFF | train | 7 | 1 | 6 | 0 | 0 | 14.29% | $19.75 | 28.21% |
| OFF | holdout | 14 | 0 | 14 | 0 | 0 | 0.00% | $-140.00 | -100.00% |
| ON | week 6 | 7 | 1 | 6 | 0 | 0 | 14.29% | $20.13 | 28.76% |
| ON | week 7 | 7 | 0 | 7 | 0 | 0 | 0.00% | $-70.00 | -100.00% |
| ON | week 8 | 6 | 0 | 6 | 0 | 0 | 0.00% | $-60.00 | -100.00% |
| ON | train | 7 | 1 | 6 | 0 | 0 | 14.29% | $20.13 | 28.76% |
| ON | holdout | 13 | 0 | 13 | 0 | 0 | 0.00% | $-130.00 | -100.00% |

## Frozen input SHA-256

- `rules.py`: `32de0d887d455d62597b71d7aa7f3790002b61e826d42ff699ba7540b27407a7`
- `locked_rules.json`: `8d65368056a5552611ded23f8e3b301a313d5047ec73fc0cab8a5b07c747ddda`
- `slip_method.md`: `3f1d47e52986d60aeac8d2fd34911942e692ea2c13d68ffd803961979c293cf5`

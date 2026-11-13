# NFL-75 item 5: fitted dispersion (opt-in, default off). Research only, not validated.

Builds on PR #23 (`market_calibration/dispersion.py`, frozen NFL-64 baselines, unchanged). `projection_ready` untouched.

## Flag
`market_calibration/fitted_dispersion.py`: `mode="fixed"` (default) returns exactly today's hand-set values
(margin SD 13.5, total SD 13.0 from `research/runs/2026-11-12_TNF_WAS_NYG_layers/script_layer.py`; lognormal sigmas
WR 0.70 / TE 0.75 / RB rush 0.45 typed in `legs.py`). `mode="fitted_nflverse_v1"` (or env `NFL_DISPERSION_MODE`)
reads `dispersion_fit_nflverse_v1.json`. No existing caller is changed, so default output is identical to main.

**Centre guard.** Fitted player sigmas are dispersion of log(yards) around the player's **trailing mean** (centre =
trailing mean x fitted median ratio, with a fitted p0). The fixed `legs.py` sigmas are centred on the **book main
line**. They are not interchangeable. `yard_sigma(..., mode="fitted_nflverse_v1")` and `yard_cell` raise unless
called with `reference="trailing_mean"`; `reference="book_line"` (or none) raises. The JSON carries
`player_sigma_reference: "trailing_mean"`. Do not use them in `legs.py` / line-centred pricing until they are
re-tested against saved prop lines (PR #25 inventory). Game SDs are residual SDs around the close.

## Source
nflverse-data release assets `play_by_play_2018..2026.parquet` + `players.parquet`, retrieved 2026-11-13 05:25-05:26 UTC
(12:25-12:26 AM ET); sha256 of each file is in the JSON. Regular season only. Fit window 2018 .. 2026 week 9.

## Fitted values (2018-2026 W9, n = 2,263 games)
Margin residual (final margin - spread_line) SD by |spread|: all 12.73 | [0,3) 12.39 (n 511) | [3,7) 12.75 (1,099) |
[7,10) 12.92 (367) | 10+ 13.00 (286).
Total residual (total - total_line) SD by total line: all 13.14 | <41 13.18 (339) | [41,45) 12.33 (752) |
[45,49) 13.87 (694) | 49+ 13.29 (478).
Player-yard lognormal sigma by trailing-mean bin (line-size proxy; no historical prop lines exist in our sources):

| stat:pos | [0,30) | [30,50) | [50,70) | 70+ |
|---|---|---|---|---|
| rec:WR | 1.002 | 0.855 | 0.775 | 0.724 |
| rec:TE | 0.962 | 0.845 | 0.763 | 0.634 |
| rec:RB | 1.007 | 0.897 | 0.839 | 0.906 (n 12) |
| rush:RB | 1.133 | 0.990 | 0.780 | 0.668 |
| rush:QB | 1.119 | 0.945 | 0.710 | 0.969 (n 37) |
| pass:QB (bins 0/200/240/270) | 0.479 | 0.386 | 0.351 | 0.330 |

p0 and median ratio per cell are in the JSON. Sigma here is predictive spread around a trailing-mean centre, which is
noisier than spread around a market line, so it is wider than sigmas centred on a book's line.

## Walk-forward backtest, 2026 weeks 4-9 (`backtest_dispersion_wk04_09.json`)
Per test week w: fit on 2018-2025 + 2026 W1..w-1, frozen, scored on week w. Weeks >= 10 never used.
Engine centres: `calibration/outputs/backtest_after_wp12_n2000_per_game.csv` (main engine, adjustments off).
Close: `ba83615:data/lines/lines_wk04_09_2026.csv` (sha256 matches README). Bootstrap 2,000, seed 20261113.

| market (n) | Brier fixed | Brier fitted | diff [95% CI] | ECE fixed -> fitted |
|---|---|---|---|---|
| home win, engine centre (87) | 0.2504 | 0.2529 | +0.0026 [+0.0005, +0.0049] | 0.137 -> 0.187 |
| over close total, engine centre (88) | 0.2841 | 0.2849 | +0.0008 [-0.0007, +0.0024] | 0.200 -> 0.200 |
| home cover close, engine centre (85) | 0.2915 | 0.2957 | +0.0043 [+0.0021, +0.0064] | 0.193 -> 0.190 |
| home win, close centre (87) | 0.2088 | 0.2079 | -0.0009 [-0.0021, +0.0004] | 0.110 -> 0.115 |

Player level (headline = per threshold, CI = **game-cluster bootstrap**, 88 games, B 2,000):

| stat (n per threshold) | 0.5x trailing mean | 0.75x | 1.0x | all thresholds |
|---|---|---|---|---|
| rec:WR (629) | -0.0010 [-0.0046, +0.0025] | -0.0015 [-0.0041, +0.0011] | -0.0006 [-0.0016, +0.0004] | -0.0010 [-0.0031, +0.0010] |
| rec:TE (339) | -0.0024 [-0.0065, +0.0016] | -0.0015 [-0.0041, +0.0012] | -0.0004 [-0.0013, +0.0006] | -0.0014 [-0.0036, +0.0006] |
| rush:RB (393) | -0.0060 [-0.0204, +0.0079] | +0.0009 [-0.0038, +0.0055] | **-0.0243 [-0.0332, -0.0157]** | **-0.0098 [-0.0146, -0.0047]** |

(Brier diff fitted - fixed; both arms share the fitted p0 / median ratio, only sigma differs. RB rush Brier all
thresholds 0.2447 -> 0.2349; at 1.0x 0.2735 -> 0.2492. The RB gain is essentially all at the 1.0x threshold.)

Reference: close de-vigged moneyline Brier 0.2055 (ECE 0.116), engine sim P(home) Brier 0.2515.
Margin / total MAE do not depend on the SD: engine 10.69 / 11.39, close 8.98 / 10.33 (same before and after).

## Read
- Game SDs: the fitted SDs (~12.4-13.0 margin) are slightly tighter than 13.5. Around the close that is neutral
  (CI spans 0). Around the engine's mean it is worse (CI excludes 0) because the engine's centre is far from the close
  (mean |model - close| margin 5.8), so a wider SD is hiding centre error. Do not turn fitted game SDs on for engine-centred probabilities.
- Props: fitted sigmas are better for RB rushing (CI excludes 0), neutral-to-slightly-better for WR/TE.
- Player-level CIs are clustered by game (row-bootstrap CIs are also in the JSON). Positions come from the current
  nflverse `players.parquet`, not as of each game (minor point-in-time caveat). Weeks 4-9 were already seen while building the engine; not a clean holdout.
- Recommendation: fitted RB rush sigma only, and only around a trailing-mean centre (the 1.0x result); keep game SDs
  fixed for engine-centred probabilities; do not use any fitted player sigma around a book line.

Tests: `tests/test_fitted_dispersion.py` refits from the pinned nflverse files (sha256-checked; skipped with the reason
when absent or re-published; dir = `NFLVERSE_PBP_DIR`, default `/tmp/nflverse_pbp`) and reproduces the committed fit to
1e-12 plus the frozen week-4 walk-forward SDs.

Reproduce: `python3 -m market_calibration.fit_dispersion_nflverse --pbp-dir <dir> --players <players.parquet>` then
`python3 -m market_calibration.backtest_dispersion_wk04_09 --pbp-dir <dir> --players <players.parquet>` (needs scipy).

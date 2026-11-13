# NFL-75 item 6: opt-in weather and injury adjustments. Research only, not validated. Default OFF.

`projection_ready` untouched. No engine weight or default changed. Not turned on anywhere.

**Both stay OFF** until (a) a forecast-based weather version (pregame NWS / forecast snapshot) exists and is
backtested -- the weather test below used kickoff observations, which makes it optimistic -- and (b) injury evidence
with known publication times is available.

Rebased onto main 6bc0c54 (PR #36 player box recorder). Off is bit-identical to 6bc0c54 on the full output including
`player_box` (5 configs, n=60, seed 20261113: WAS@NYG w10, JAX@BAL w9, IND@PIT w5, CLE@NYJ w5, SEA@DEN w6).

## What changed
- `core/possession_engine_v0/environment_adjust.py` (new) + three opt-in hooks in `simulate.py` and an optional
  `extra_cols` argument in `pbp_filter.load_team_history` (default `()` = unchanged column set).
- Weather `cfg["environment"]["weather"] = {"mode": "rain_wind_v1", rain, wind_mph, effects_path, evidence}`:
  per completed non-sack pass, keep the completion with prob `1 + c_rain*R + c_wind*W` and scale yards by
  `1 + y_rain*R + y_wind*W` (W = max(0, wind-10)/10). Coefficients = "pooled" completion_pct and yards_per_completion
  from a `fit_rain_effects.py` JSON, used only where marked clear. Pass rate / attempts / INT / sack not modelled.
- Injury `cfg["availability"] = {"mode": "injury_report_out_v1", out_player_ids, evidence}`: drops the listed
  players' passer/rusher/receiver history rows from their team's catalog; if that leaves < 50 pass rows the passer
  rows are kept and flagged (existing adjustments.py sparse-QB threshold). Nothing fabricated.
- Both refuse to run without `evidence.source` + `evidence.asof`, and unless named in
  `simulate_games(research_unaccepted=...)` with n <= 20,000, so no lock / 100k / rocket path can use them.

## Deterministic regression (written and recorded on main 3dad900 before the engine edit)
`tests/test_environment_adjust.py`: 4 configs (WAS@NYG w10, JAX@BAL w9, IND@PIT w5, CLE@NYJ w5), n=60, seed 20261112,
key absent and explicit "off": fg score hashes identical to 3dad900 (18984268e877d4cb, a59ceb83b0aec394,
4869e54224982391, 83f0455a297eb30a); no new output keys. Also: the backtest's baseline arm re-simulated 72 games at
n=2000 and matched `backtest_after_wp12_n2000_per_game.csv` on all 72.

## Walk-forward backtest, 2026 weeks 4-9 (`weather_injury_backtest_wk04_09_n2000.json`)
- Weather coefficients refit on 2018-2025 ONLY (`research/weather/rain_effects_train_2018_2025.json`), frozen, then
  applied to 2026. Committed `rain_effects.json` includes 2026 W4-9 and is not used. Engine history = weeks 1..w-1.
  Train coefficients: completion -5.55% rain, -3.42% per 10 mph; yards/completion -5.51% rain, -5.09% per 10 mph.
- Evidence: weather = the game's nflverse `weather`/`roof`/`wind` (kickoff observation; wind parsed from the text when
  the numeric field is blank) -- available at kickoff, not a pregame forecast, so optimistic.
  Injuries = nflverse `injuries_2026`, report_status Out, QB/RB/WR/TE/FB; file committed as
  `data/historical/nflverse/injuries_2026_pulled_20261113T0526Z.parquet`. **Publication time UNKNOWN**: the file has
  no publication or modified timestamp, so "published before kickoff" cannot be verified from it. Consistency check
  only: 0 of the 148 W4-9 skill-position Out rows recorded a pass, rush or target for that team that week.
- Graded vs consensus close (`ba83615:data/lines/lines_wk04_09_2026.csv`). Each arm vs baseline on the games it
  touches. Bootstrap 2,000 (seed 20261113). n = 2,000 sims/game. Weeks >= 10 never used.

| arm (games) | Brier base -> arm | diff [95% CI] | ECE base -> arm | margin MAE base -> arm [diff CI] | total MAE base -> arm [diff CI] | close Brier / margin MAE / total MAE |
|---|---|---|---|---|---|---|
| weather (19; 6 rain, 13 wind>10 dry) | 0.3079 -> 0.3102 | +0.0023 [-0.0078, +0.0113] | 0.301 -> 0.252 | 13.77 -> 13.84 [-0.20, +0.31] | 12.92 -> 12.76 [-1.41, +1.19] | 0.2068 / 10.34 / 11.34 |
| injury (70; 69 decided) | 0.2565 -> 0.2502 | -0.0063 [-0.0234, +0.0103] | 0.166 -> 0.162 | 10.82 -> 10.96 [-0.53, +0.83] | 11.53 -> 12.09 [-0.24, +1.34] | 0.2093 / 9.36 / 10.48 |

Weather moves the total -1.99 on average (rain games -3.0 to -8.3; wind-only games -1.7 to +0.75). On the 6 rain
games, total MAE 14.69 -> 13.86 and bias +2.40 -> -2.72 (n = 6, not meaningful). Injury: 3,326 history rows removed;
in 10 games a listed-Out QB's passer rows were kept because the backup had < 50 pass rows (flagged in output).
ECE with <= 70 games over 10 bins is very noisy.

Provenance: the committed backtest JSON/CSV were generated at 4e33c39; Ghost6 re-ran at bc8d12f and got a
byte-identical per-game CSV and identical `results` (only `engine` and `runtime_sec` differ). After this change the
script writes its train-only weather fit and outputs to `calibration/outputs/runs/weather_injury_<UTC tag>/`
(git-ignored) and records whether that fit is byte-identical to the committed
`research/weather/rain_effects_train_2018_2025.json` (it is: smoke run 2026-11-13); the committed files are never overwritten.

## Recommendation
Do not turn either on (see the OFF conditions above). Every CI spans zero, the engine stays well behind the close on every metric, and the
weather sample is tiny. Revisit after the Weeks 10-12 holdout is graded (not used for tuning here).

Reproduce: `python3 -m calibration.weather_injury_backtest --pbp-dir <folder of nflverse play_by_play_2018..2025.parquet> --n 2000 --workers 8 [--run-tag TAG]` (~53 min on 8 cores).

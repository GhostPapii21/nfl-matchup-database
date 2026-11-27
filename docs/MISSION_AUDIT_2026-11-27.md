# Audit: Rico's 12-priority NFL mission vs what exists (2026-11-27)

Research only. refs NFL-47. `projection_ready` stays false. Status words: **HAVE** (built and in the repo or a draft PR),
**PARTIAL**, **NEW** (added in this PR), **GAP** (not computable from free data we hold), **NOT BUILT** (computable, not
done yet). Paths are repo paths unless they start with `/workspace` (box-only).

## P1 Defensive coverage profile

| Item | Status | Where / why |
|---|---|---|
| MOFO / MOFC, man / zone, season | HAVE | `data/coverage/sharp_coverage_2026.csv` (Sharp page, `pregame/coverage_rates.py`); PR #143 `team_scheme_rates.csv` (Sharp + StatRankings, conflict flag) |
| Single-high / two-high | HAVE (StatRankings only) | PR #143 `team_scheme_rates.csv` `sr_single_high`, `sr_two_high` |
| Cover 0/1/2/2M/3/4/6 frequency | PARTIAL | PR #143 `team_shell_mix.json`: StatRankings season shares, some shells IMPUTED (flagged per team). Season only, one source |
| Man rate by window (L10/L5/L3) and trend | NEW | `sharp_defense_windows.csv` from Sharp per-game box scores, **weeks 1-10 only** |
| Coverage frequency by down/distance, red zone, formation | GAP | No free 2026 source publishes per-play coverage calls. nflverse 2026 participation (where NGS `defense_coverage_type` lived through 2025) returns "Not Found"; free NGS has no per-play coverage; FTN via nflverse has no coverage column |
| Results allowed by down/distance, red zone, shotgun vs under center, play-action, blitz | NEW | `situational_allowed.csv` (pbp + FTN). These are results, not coverage frequencies |
| Short / intermediate / deep, middle vs outside weakness | HAVE season (PR #143 `team_allowed_by_zone.csv`, short/deep at 15 air yds); NEW windows + 3 depth bands + opp-adjusted | `team_game_allowed.csv`, `allowances_windows.csv` |
| Slot vs outside vulnerability | PARTIAL | Sharp season YPT outside vs slot only (PR #143). Per-play alignment: GAP (no 2026 participation/route data) |
| Season / L10 / L5 / L3, tendency change | NEW | `allowances_windows.csv`, `allowance_trends.csv`, `sharp_defense_windows.csv` |
| Opponent-quality adjustment | NEW | leave-one-out `_oa_pg` columns |
| Per-defender coverage quality | HAVE (PR #143) | `defender_grades.csv`, inferred attribution (held-out top-1 accuracy 25%) |

## P2 Positional weaknesses

| Item | Status | Where |
|---|---|---|
| WR1 / WR2 / WR3 allowed | NEW | rank by prior-game targets |
| Slot / outside WR allowed | GAP (per player) | see P1 |
| Targets, receptions, yards, TD, 20+ catches, short/int/deep | NEW (windows) | `allowances_windows.csv` |
| TE targets, receptions, yards, Y/R, TD, red-zone targets, short/int | NEW | group TE |
| RB rush att/yds/YPC/TD/10+/20+, success | NEW | group RB |
| RB targets/rec/yds/Y/R | HAVE season (PR #143), NEW windows | group RB |
| Screens and checkdowns | NEW, partial | FTN screens through week 11; "behind the line" targets as a checkdown stand-in |
| QB pass yds, cmp %, TD, INT, scrambles, designed runs | NEW | group QB |
| Pressure rate | PARTIAL | Sharp per-game pressure (weeks 1-10) in `sharp_defense_windows.csv`; pbp has no pressure field; 2026 participation `was_pressure` unavailable |
| Blitz response | NEW, partial | FTN blitz / no-blitz EPA per dropback (through week 11); Sharp blitz rate windows |
| Passing efficiency vs coverage type | GAP | needs per-play coverage call |
| Receptions vs yards kept separate | yes | separate columns everywhere |

## P3 Player opportunity and production

| Item | Status | Where |
|---|---|---|
| Targets, share, rec, yds, aDOT, air yards, RZ targets, carries, snaps | HAVE | `data/scheme_profiles/2026/teams/*.json` (players, last-5/8 windows), `calibration/opportunity_*`, nflverse snap counts |
| Routes run, route participation, TPRR | GAP | no free 2026 route data (PFF/FTN routes are paid; participation `route` column not published for 2026) |
| Slot vs outside alignment per player | GAP | same |
| L3 / L5 / L10 / season player windows | PARTIAL | scheme profiles have season and last-5/8; L3/L10 player windows NOT BUILT |
| Personnel package usage | PARTIAL | Sharp team-level 11/12 personnel per game (box scores w1-10); per-player GAP |

## P4-P6 Weather

| Item | Status | Where |
|---|---|---|
| NWS + Open-Meteo pregame forecast | HAVE | `pregame/weather.py` and packets (repo); `/workspace/nfl-database/tools/weather_forecast.py` (Phase 11a, box only) |
| Rain / wind effects on passing, fitted 2018-2025 | HAVE | `research/weather/` (rain_effects*.json, README), `pregame/rain_model.py` |
| Opt-in weather adjustment backtest | HAVE, default OFF | `calibration/weather_injury_backtest.py`, `calibration/outputs/WEATHER_INJURY_EVIDENCE.md` (used kickoff observations, so optimistic) |
| 6-category classification (normal ... combined) | NOT BUILT | proposal in `docs/proposed_skill_changes/WEATHER_CATEGORIES_PROPOSAL.md` |
| Team- and QB-specific weather response | NOT BUILT | team rain samples are tiny in 2026; would need 2018-2025 pbp per team-coach |
| Rain intensity, accumulation, field conditions | PARTIAL | Open-Meteo gives hourly precipitation mm; field condition not in any free feed we hold |
| Weather effect on rushing volume / YPC | PARTIAL | README covers pass rate (-3.3% in rain); YPC effect not fitted |
| A/B/C scenario projections | NOT BUILT | existing sim runs one scenario plus game-script variants |

## P7-P8 Strong read / soft lean / ceiling

| Item | Status |
|---|---|
| 0-100 mismatch conviction score | NOT BUILT; proposal only (`STRONG_READ_SOFT_LEAN_CEILING_PROPOSAL.md`) |
| Opportunity ceiling board | NOT BUILT; proposal only |
| Conservative / median / upper projections, line probabilities | HAVE inside the sim (p10/p50/p90, three 100k models) |

## P9-P10 Grading and validation

| Item | Status | Where |
|---|---|---|
| Frozen projections with timestamps, postgame grading | HAVE | `grading/`, `runs/`, `slips/`, postgame companion CSV (box) |
| Opportunity calibration (MAE, p10-p90 coverage, Brier) | HAVE | `calibration/opportunity_report.py`, `opportunity_holdout_grade.py` |
| CLV | HAVE | `calibration/clv_tracking.py` |
| Hit rate by conviction / matchup / weather category | NOT BUILT | needs the conviction score and weather categories first |
| Missed-opportunity board | PARTIAL | postgame reviews list missed edges by category (PHASE_SCRIPT rule 10); not a standing board |

## P11 Report format

PARTIAL. Briefs (`research/briefs/2026/*/brief.json`) carry weather, availability, defenses, reads and picks. The new
boards (strong read, soft lean, ceiling) and weather-adjusted scenarios are not in the format yet.

## Data we checked and could not use

- nflverse `pbp_participation_2026.parquet`: release asset returns "Not Found" (the local copy is a 9-byte error body).
  2025 participation exists locally with coverage types on 49% of plays, but it is last season.
- Sharp advanced box scores: weeks 1-10 in the repo; weeks 11-12 not pulled.
- FTN charting via nflverse: through week 11.

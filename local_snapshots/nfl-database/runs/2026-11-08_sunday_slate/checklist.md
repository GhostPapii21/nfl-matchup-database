# Week 9 Sunday slate — BLOCKED game-day checklist
**Slate:** NFL 2026 Week 9 Sunday (plus context TNF JAX@BAL final; MNF BUF@MIN not kicked)
**Run folder:** `/workspace/nfl-database/runs/2026-11-08_sunday_slate/`
**Fired:** 2026-11-08 07:09 America/New_York (routine NFL game-day script run)
**Input cutoff:** 2026-11-08 07:15 America/New_York
**projection_ready:** false
**Picks:** none
**Simulations:** SIMULATION NOT RUN (Monte Carlo / Bias / Game Randomness 100k triad not executed; no seed)

## Gates that block this run
| Gate | Status | Evidence | Pulled (ET) |
|---|---|---|---|
| GitHub model PR #1 | FAIL (unmerged) | [PR 1](https://github.com/GhostPapii21/nfl-matchup-database/pull/1) state=open, merged=false, head `fe2e3711b766d8894c49ec4dc571e6731628dc55` | 07:10 |
| Adopt main as model | FAIL (forbidden until merge) | main HEAD `6e1b9325851eaf5683a9286e876f8adb443ad1ee` (06:53 ET tracker formatting); not the checkpoint | 07:10 |
| NFL-49 production acceptance | FAIL | Todo; ACCEPTANCE_NOT_MET; four pillars not passed | 07:10 |
| NFL-56 15-phase + 100k workflow | FAIL | Todo; executable ledger/workflow incomplete; Phase 15 NOT_YET | 07:10 |
| projection_ready | FAIL | false on checkpoint PR body and local Sat refresh | 07:10 |

## Slate-level 15-phase status (no priced legs)
No candidate leg was priced. Rows are slate-wide, not per-player.

| Leg | Phase | Status | Number | Source | Pulled (ET) |
|-----|-------|--------|--------|--------|-------------|
| SLATE (no priced leg) | 1 Data pull/reconcile | PASS (partial) | ESPN scoreboard 15 events (week 9); CIN@ATL 9:30 AM ET scheduled indoor Bernabéu; TNF JAX@BAL final | ESPN scoreboard sha256 `d7eac2d6ae4be464…` | 2026-11-08 07:12 |
| SLATE (no priced leg) | 2 Opportunity | MISSING | No priced legs; opportunity math not run without a validated engine | NFL-56 / NFL-49 | 07:15 |
| SLATE (no priced leg) | 3 Defensive profile | MISSING | Team/position allowances not assembled this run | — | — |
| SLATE (no priced leg) | 4 Defender coverage | MISSING | Named-defender + man/zone + MOF fields not pulled; NFL-47 effects disabled | checkpoint docs/SOURCE_STATUS.md | 07:10 |
| SLATE (no priced leg) | 5 Pressure/blitz | MISSING | FTN charting hash-only in public package; effects disabled | NFL-47 | 07:10 |
| SLATE (no priced leg) | 6 QB grade card | MISSING | §15 cards not run | — | — |
| SLATE (no priced leg) | 7 Role/RB rules | N/A | No priced RB leg; committee/carry-share gates not applied | — | — |
| SLATE (no priced leg) | 8 Injuries | PASS (research designations) | ESPN injuries feed timestamp 2026-11-08T12:12:19Z; full body hashed `6d0a3c335555e9cc…`; see report | ESPN injuries API | 2026-11-08 07:12 |
| SLATE (no priced leg) | 9 NGS | MISSING | Public NGS tables not pulled | NFL-47 | — |
| SLATE (no priced leg) | 10 Film | MISSING | No film URLs or play-by-play matches claimed | — | — |
| SLATE (no priced leg) | 11 Environment | PASS (forecast pulled) | Fresh SRC-1 forecast `2026-11-08T07:11`; flags below | tools/weather_forecast.py sha256 `7b96dd6af6d5a2e2…` | 2026-11-08 07:11 |
| SLATE (no priced leg) | 12 Source audit | PASS (gaps listed) | Manifest `7dac4e58562ab4ad…`; required map categories logged SUCCESS/SAVED_ONLY/MISSING | source_manifest.json | 07:15 |
| SLATE (no priced leg) | 13 Script/underdog | MISSING | Spreads from ESPN/DK display only; FanDuel price of record not refreshed; actionable consensus NOLINE | NFL-45 | 07:12 |
| SLATE (no priced leg) | 14 Models/price/edge | FAIL (blocked) | SIMULATION NOT RUN; no seed; no trials; no edge vs no-vig | NFL-49 / NFL-56 standing order | 07:15 |
| SLATE (no priced leg) | 15 Inactives | NOT_YET | 1 PM window ~11:30 AM ET; Madrid CIN@ATL window ~8:00 AM ET (after this cutoff); SNF ~6:50 PM ET | skill Phase 15 | 07:15 |

## Weather flags (worse of NWS + Open-Meteo; retractable treated as open-air by the runner)
| Game | kickoff_et | status | flag | why | precip% | gust mph | wind mph | notes |
|---|---|---|---|---|---|---|---|---|
| JAX@BAL | 2026-11-05T20:15 | MISSING | None | — | None | None | None | nws missing; open_meteo missing; nws: kickoff beyond hourly range |
| CIN@ATL | 2026-11-08T09:30 | OK | False | — | 5 | 14.1 | 4.5 | nws missing |
| DAL@IND | 2026-11-08T13:00 | OK | True | gusts 26.8 mph | 0 | 26.8 | 13 | — |
| NYJ@KC | 2026-11-08T13:00 | OK | False | — | 0 | 13.9 | 6.8 | — |
| DET@MIA | 2026-11-08T13:00 | OK | False | — | 3 | 6.0 | 7 | — |
| CLE@NO | 2026-11-08T13:00 | INDOOR | False | — | None | None | None | — |
| NYG@PHI | 2026-11-08T13:00 | OK | True | gusts 20.4 mph | 0 | 20.4 | 11.7 | — |
| LAR@WSH | 2026-11-08T13:00 | OK | True | gusts 21.7 mph | 0 | 21.7 | 11.0 | — |
| DEN@CAR | 2026-11-08T13:00 | OK | False | — | 0 | 11.6 | 8.2 | — |
| HOU@LAC | 2026-11-08T16:05 | INDOOR | False | — | None | None | None | — |
| LV@SF | 2026-11-08T16:25 | OK | False | — | 0 | 11.9 | 7.3 | — |
| ARI@SEA | 2026-11-08T16:25 | OK | False | — | 4 | 19.9 | 10.3 | — |
| GB@NE | 2026-11-08T16:25 | OK | False | — | 1 | 16.6 | 7.5 | — |
| TB@CHI | 2026-11-08T20:20 | OK | True | gusts 27.3 mph | 0 | 27.3 | 10 | — |
| BUF@MIN | 2026-11-09T20:15 | INDOOR | False | — | None | None | None | — |

Material vs Saturday 10:01 ET forecast: NYG@PHI newly flagged (gusts 20.4, was 19.0 unflagged); LAR@WSH newly flagged (gusts 21.7, was 17.9); TB@CHI still flagged (27.3); ARI@SEA remains unflagged but gusts 19.9 (near 20; Saturday 14.3); GB@NE unflagged at 16.6; DAL@IND runner-flagged at 26.8 because retractable/unknown roofs count as open-air — ESPN lists Lucas Oil indoor=True, Saturday refresh treated it as indoor. HOU@LAC runner INDOOR vs ESPN SoFi indoor=False (conflict, not resolved). CIN@ATL NWS missing; Open-Meteo precip 5% / gust 14.1.

## Summary
- Legs that passed: **0**
- Legs cut: n/a (no priced candidates)
- SIMULATION NOT RUN (no seed, 0 trials)
- Data gaps: coverage/man-zone/MOF, NGS, film, FTN charting, PFF second-source, FanDuel/Pinnacle actionable quotes, Phase 15 inactives, 100k triad
- Restricted data: full ESPN injuries body hashed only (`6d0a3c335555e9cc85116fa3ec9de852e8cf31038a7fb69332a125f97e66b21e`)

VETTED: pending Ghost6

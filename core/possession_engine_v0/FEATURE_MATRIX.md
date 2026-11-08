# possession_engine_v0 — implemented / missing / scenario-only matrix

As-of: **2026-11-05 14:00 America/New_York (EST)**. Research-only. Not a betting edge claim.

| Feature | Status | Source / definition | As-of / freshness | Effective n (JAX/BAL W1–8) | Reproducibility | Notes |
|---|---|---|---|---|---|---|
| Team-only PBP load W1–8 | **IMPLEMENTED** | Local `play_by_play_2026.parquet` (nflfastR-shaped) | File on disk; season=2026 weeks≤8 | 15 games / 2567 involvements; offense catalog ~2.5k posteam rows | Deterministic filter | No league/future fallback |
| State: down/distance/YL/clock/score/poss | **IMPLEMENTED** | Engine `state.py` | Code freeze this commit | n/a | Stable seed SHA256 | Clock costs = fixed means (limitation) |
| Empirical snap resample by state cell | **IMPLEMENTED** | Team snaps; sparse → same-team coarser fallback with flag | W1–8 | Many cells n&lt;5 (see evidence) | Seeded | **No silent league pool** |
| Kickoff / halftime / OT / FG / PAT / turnover | **IMPLEMENTED** | Explicit transitions + team special teams rows | W1–8 | FG/PAT/punt n per team small | Seeded | OT = single-possession approx |
| Joint player yards from same events | **IMPLEMENTED** | passer/rusher/receiver on resampled rows | W1–8 | Varies by player | Seeded | Not a prop model |
| Config freeze data_only vs script_adjusted | **IMPLEMENTED** | `config/*.json` | frozen_at_et in file | n/a | JSON hashable | Adjustments off vs on |
| Forward QB filter (Fagnano / Lamar OUT) | **IMPLEMENTED** | Dated adjustments JSON; brainstorm_read 2026-11-03 notes | asof_et in config | BAL pass after filter = Fagnano only (~24) | Deterministic filter | **No fabricated history** |
| Proposed pooling switch | **IMPLEMENTED (default off)** | `proposed_pooling.enabled` | config | n/a | Explicit | Never silent |
| 3rd-down conversion freq + conditional success | **IMPLEMENTED (audit table)** | PBP `third_down_converted` / `third_down_failed` | W1–8 team | See `situational` artifact | Scripted | Opportunity rate AND convert\|opportunity |
| Red-zone TD/score rates | **IMPLEMENTED (audit table)** | Plays with `yardline_100≤20`; drive_inside20 | W1–8 | See artifact | Scripted | Freq of RZ trips + score\|RZ |
| QB completion split by `qb_hit` | **IMPLEMENTED as PROXY** | `qb_hit` column — **not** measured blitz/pressure | W1–8 by passer | Fagnano n small | Scripted | Label **PROXY_NOT_PRESSURE**; blitz/pressure cols **absent** |
| True blitz / pressure / # rushers | **MISSING** | Columns `blitz`,`was_pressure`,`number_of_pass_rushers` **not in local PBP** | — | 0 | — | Do not invent |
| Man/zone, coverage type, routes, open middle | **MISSING** | No `defense_man_zone_type`,`defense_coverage_type`,`route` | — | 0 | — | PBP cannot establish; **not** proxied as measured |
| Primary CB/S vs WR/TE matchup | **MISSING** | `pass_defense_1_player_name` ≠ assigned coverage | — | — | — | Do not label as primary defender |
| Opponent-adjusted RB YPC (team vs that defense) | **IMPLEMENTED (audit)** | Runs vs `defteam` in team games W1–8 | W1–8 | Per-opponent n small | Scripted | JAX vs BAL D: only if prior H2H in window — else SPARSE |
| DT missing / replacement OL-DL effects | **MISSING / SCENARIO-ONLY** | No DT snap chart in PBP | — | — | — | Sensitivity only if params mapped |
| WR/TE field zones vs CB replacements | **MISSING** | Need charting; PBP `pass_location` only | — | pass_location counts only | — | Location ≠ route vs CB |
| Q1–4 / H1 / H2 margin distributions | **PARTIAL** | Reconstruct from period_engine or possession events | W1–8 | 15 games historical; sim outputs FG/reg | Seeded sim | Period margins from possession slice limited (no full period scoreboard yet) |
| BAL upset / Fagnano 200+ tails | **SCENARIO-ONLY** | Sensitivity params in `scenarios/` — **not** verified probs | 2026-11-05 | Fagnano pass attempts ~24 | Labeled | Research tails; not calibrated |
| Road / rest / travel / practice availability | **EVIDENCE STUB** | Schedule + notes; practice DNP text from miss_audit | notes 2026-11-03–05 | Qualitative | Provenance rows | Unknown→unknown; no weights |
| Weather | **EVIDENCE STUB** | Needs dated weather pull; not auto-ingested here | — | — | — | Status UNKNOWN until sourced |
| Market spread/total conditioning | **SEPARATE CONFIG ONLY** | `config/*_market_informed.json` if present | — | — | — | Must **not** contaminate data_only baseline; not independent edge proof |
| Narrative comments → auto calibration | **FORBIDDEN** | — | — | — | — | Comments → auditable param map or sensitivity label |
| Betting edge / Pin ROI | **NOT CLAIMED** | — | — | — | — | Research-only |


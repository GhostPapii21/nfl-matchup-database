# NFL-56 15-phase status — MNF BUF @ MIN (research / source-of-truth only)
Run: 2026-11-09, checked 15:00–15:25 ET. Game: 2026 Week 9, ESPN event 401873051, kickoff 8:15 PM ET (2026-11-10T01:15Z), U.S. Bank Stadium (fixed roof, ESPN indoor=True).
Phase authority: skill `nfl-game-script-run` (15 phases), plus `nfl-projection-source-preflight`. No BUF@MIN run folder exists under /workspace/nfl-database/runs/ (checked 15:03 ET). Nothing was written to production paths.
projection_ready=false (unchanged). SIMULATION NOT RUN (0 trials, no seed).

| # | Phase | Status | Evidence / reason |
|---|---|---|---|
| 1 | Data pull/reconcile | MISSING (game identity PASS only) | ESPN scoreboard+summary pulled 15:01 ET (`injuries/espn_scoreboard_20261109.json`, `injuries/espn_summary_401873051.json`). No nflverse pbp/snaps/participation/FTN pull for this game; no BUF@MIN run folder. GitHub main has gamebook-verified quarter linescores (`research/WEEK9_MNF_BUF_MIN_PREGAME_QUARTER_BOARD_20261109.md`, 03:12 ET) — research context, not reconciled into a run. |
| 2 | Opportunity gate | MISSING | No projected volume/target-share math. Palmer OUT (BUF) and Jennings/Claiborne OUT (MIN) redistribution not computed. Needs a validated engine (NFL-49). |
| 3 | Defensive profile | MISSING | Not assembled in a run. Unvetted context exists on GitHub main (`data/redistributable/teams/defense/BUF.md`, `MIN.md`; `research/WEEK9_MNF_*_OFFENSE_VS_*_DEFENSE_20261109.md`, 03:17–03:26 ET), not pulled/vetted here. |
| 4 | Defender coverage | MISSING | Named-defender + man/zone + MOF not verified for this game; prior 28 named-assignment gaps still open; MIN S Theo Jackson / Jay Ward questionable would force a Phase 4 re-run if inactive. |
| 5 | Pressure/blitz/checkdown | MISSING | FTN blitz / pressure / NGS TTT not pulled (NFL-47 effects disabled). |
| 6 | QB grade card (§15) | MISSING | Not run. MIN starter Carson Wentz (official Vikings preview + ESPN/Rapoport note); BACKUP_QB §7 exemption still pending Rico. |
| 7 | Role/RB rules | MISSING | No candidate legs. MIN backfield changes (Claiborne OUT; DeeJay Dallas signed) not evaluated. |
| 8 | Injuries (both sides) | PASS (designations; conflicts logged) | Official NFL.com + Bills + Vikings final Saturday reports and ESPN feed (ts 2026-11-09T20:01:34Z = 3:01 PM ET). See `injuries/INJURY_SUMMARY.md`. |
| 9 | Next Gen Stats | MISSING | Public NGS pages not pulled. |
| 10 | Film | MISSING | No film cited; nothing UNVERIFIED elevated. |
| 11 | Environment | PASS | Dome → weather neutral. SRC-1 runner `tools/weather_forecast.py --week 9 --out-dir <research>` at 15:00 ET → BUF@MIN `INDOOR`, flag False. Outdoor reference: NWS (updated 1:26 PM ET) clear, 49–53°F, 5 mph, 0%; Open-Meteo gust 16.3. Rest/travel/stakes not assessed. |
| 12 | Source audit | PASS (gaps listed) | `source_manifest.json` in this folder; unused categories: coverage, NGS, film, odds price of record, sims. |
| 13 | Script / underdog gate | MISSING | DK display only (ESPN, 15:01 ET): BUF -3.5, total 45.5. FanDuel price of record not pulled (no Odds API credits authorized) → NOLINE. |
| 14 | Models / price / edge | BLOCKED | DEFERRED_100K_UNFINISHED_OFFICIAL_SEMANTICS; NFL-49 ACCEPTANCE_NOT_MET; NFL-42 entrypoint not enforced. MC/Bias/GR 0/0/0 trials, no seed (`/workspace/research/sim_v6_100k_attempt_2026-11-08/BLOCKER_LOG.md`). |
| 15 | Inactives check | NOT_YET | Official 90-min inactives ~6:45 PM ET, not posted at 15:05 ET. Bills Hancock (IR) / Shavers (PUP) activation deadline "Monday afternoon" — no activation found by 15:05 ET web search (not proof of none). |

Counts: PASS 3 (8, 11, 12) · MISSING 10 (1–7, 9, 10, 13; phase 1 has identity only) · BLOCKED 1 (14) · NOT_YET 1 (15).

## Sunday Nov 8 slate — recorded status (not re-run)
From `/workspace/nfl-database/runs/2026-11-08_sunday_slate/checklist.md` (cutoff 07:15 ET Nov 8, VETTED: pending Ghost6): P1 PASS(partial), P2 MISSING, P3 MISSING, P4 MISSING, P5 MISSING, P6 MISSING, P7 N/A, P8 PASS(research designations), P9 MISSING, P10 MISSING, P11 PASS(forecast; GUST20 flags), P12 PASS(gaps), P13 MISSING, P14 FAIL(blocked, SIMULATION NOT RUN), P15 NOT_YET. Games are now final; that run was never updated after 07:15 ET.

Separate GitHub ledger (different phase taxonomy) `research/WEEK9_PHASE_LEDGER_20261108_2311ET.md` on main: 1 COMPLETE; 2–6,10 PARTIAL; 7–8 BLOCKED_QUALITATIVE; 9 PARTIAL_NOT_IN_CURRENT_SIM; 11 PARTIAL (MNF inactives not due); 12 PARTIAL (MNF fixed roof); 13 PARTIAL; 14 PARTIAL_RESEARCH_ONLY; 15 PENDING. Its validator claims "471 x 100000 simulations" integrity PASS but production FAIL-CLOSED. CONFLICT: the repo README and PROPOSED_ROUTINE_BOOTSTRAP say the 15-phase ledger and 100k workflow "are not implemented." Those 100k files are research-only and not the sanctioned sim_v6 MC/Bias/GR triad.

Also seen (read-only, not adopted): branch `research/wentz-2025-third-down-drive-audit` ran a GitHub Actions workflow `nfl-mnf-100k-conditional-simulation.yml` today, 10:14–10:22 AM ET: "900k conditional trials (100k × 3 scenarios × 3 sensitivities), seed 20261109", using DK/FD quotes captured at 09:51/10:01 ET. It is unmerged and not the NFL-56/NFL-49-gated triad, so it does not change Phase 14 status.

## Linear (read-only, 15:02 ET)
| Issue | Status | Last updated (ET) | Key |
|---|---|---|---|
| NFL-56 | Todo (High) | 2026-11-08 09:04 | 5 AC unmet; "projection_ready=false; DEFERRED_100K; Phase15 NOT_YET; NOLINE" |
| NFL-49 | Todo (Urgent) | 2026-11-08 09:04 | ACCEPTANCE_NOT_MET; four pillars |
| NFL-42 | Todo (Urgent) | 2026-11-06 13:29 | Not implemented; paused by usage-cut |

## NFL-56 acceptance criteria vs evidence
1. Runnable per-phase workflows with MISSING/NOT_YET statuses: NOT MET. The phase ledgers are documents, and run_gate.py is local only.
2. News/weather adapters documented with freshness windows: PARTIAL. The weather runner sets a ≤24h gate and a kickoff to +3.5h window, but it is local only. The repo's SOURCE_ADAPTERS has no freshness window for injuries. The weather runner has no observed/past-game mode.
3. 100k entrypoint exists but is fail-closed: NOT MET / CONFLICT. There is no gated entrypoint. Ungated research 100k jobs exist on main and on a research branch.
4. Routine bootstrap: NOT MET. See `bootstrap/BOOTSTRAP_STATUS.md`.
5. README goal vs readiness: PARTIAL. The main README has a checkpoint table. Proposed replacement text is in `README_PROPOSED_NFL56_SECTION.md`.

# NFL-16 — BetGuru market/calibration autonomous iteration log
**Linear:** https://linear.app/nfl-database/issue/NFL-16/nfl-sim-model-autonomous-iteration-and-validation-tracking  
**Project:** db3214f2cc1d  
**Sync status:** LOCAL ONLY — Linear connector needsAuth in parent; no browser/alternate auth. Pending sync when parent connector ready.  
**Owner slice:** BetGuru — `research/market_calibration/` only  
**Worktree:** `/workspace/wt-market-calibration` branch `betguru-market-calibration-2026-11-06` @ base `3448ad7`  
**Zone times:** America/New_York (box-local)

## Measured improvement / harm policy
- Improvement = tests green that previously failed for the right reason; honest NOLINE where quotes absent; raw vs anchored kept separate; no false PASS in MANIFEST.
- Harm = fitting to TNF then claiming validation; inventing quotes; editing Blitz CORE; claiming FITTED without coefficients; silent identity mismatches.

## Step log

### 2026-11-06 ~06:05–06:08 ET — Availability + isolation
- Codex CLI `0.163.0` present; `codex login status` → Logged in using ChatGPT (no credential files read).
- Audit read: `/workspace/research/model_rerun_audit_2026-11-06/AUDIT_COMPLETION.json` — bias_calib UNIMPLEMENTED; market_informed PINNACLE_MISSING_SCREENSHOT_ONLY_NOT_WIRED_TO_SAMPLER; engines lack target/carry counts.
- Created isolated worktree `/workspace/wt-market-calibration` from `3448ad7` (no remote). Reserved `research/market_calibration/`.
- Did not touch Blitz `/workspace/wt-period-engine` dirty untracked reviews or CORE.

### 2026-11-06 ~06:08 ET — Codex v1 interrupted
- First `codex exec --approve-for-me` failed (incompatible with `--sandbox`).
- Second run with `--approve-for-me` started inspecting quotes then was interrupted; no package code written.
- Evidence: `reviews/codex_stderr_v1.txt`.

### 2026-11-06 ~06:10 ET — Codex v2 relaunch (TDD)
- Relaunched Blitz-compatible: `codex exec -s workspace-write -C wt-market-calibration` PID tracked.
- Prompt: `reviews/prompt_codex_implement_v2.txt` (TDD, raw vs anchored, no TNF validation claim, NOLINE).
- Observed RED attempt: wrote tests under `tests/` then `python: command not found` (exit 127). Codex continuing to fix→rerun.

### Saved quote facts (market-check baseline)
- r6 `odds_jaxbal_game.csv`: Pinnacle present for Q1/H1 h2h+spreads + team_totals; **Pinnacle Q2–Q4 period spreads ABSENT** → must NOLINE.
- Cleared FD/DK period CSV has Q1–Q3 retail sides; do not treat grade columns as quote inputs.

### Remaining gaps (open)
- [ ] Package modules implemented + pytest green
- [ ] Independent Codex read-only review pass
- [ ] Align to Blitz `core_contract.md` when it appears (dir exists; file not yet)
- [ ] Ghost final integrated vet (handoff artifacts)
- [ ] Linear sync of this log to NFL-16

### Harm checks so far
- No paid odds pulls.
- No CORE overwrites.
- No fabricated Pinnacle Q2–Q4.

### 2026-11-06 ~06:12–06:13 ET — TDD RED verified + Linear live
- Codex wrote failing tests (quotes/calibration/settlement/contract_manifest).
- pytest_initial_red.txt: 4 collection ERROR ModuleNotFoundError (expected RED).
- Metric class: IMPROVED scaffolding; forecast accuracy NOT MEASURED.
- Posted Linear NFL-16 comment (TDD RED milestone).
- Blitz core_contract.md now present — do not overwrite; align after GREEN.
- Codex continuing implementation (stderr notes python3 wrapper).

### 2026-11-06 ~06:15–06:19 ET — first GREEN + second-review RED
- Modules: quotes/settlement/calibration/joint_trial_adapter/manifest + MANIFEST + raw/anchored artifacts.
- pytest_first_green.txt: **74 passed in 0.09s** (IMPROVED vs 4 collection ERROR).
- Codex then added test_second_review.py; pytest_second_review_red.txt: **17 failed, 76 passed** — honesty/leakage gates (IMPROVED coverage; not fully green).
- Forecast accuracy vs books/W1–8: NOT MEASURED.
- Linear NFL-16 comment posted for this milestone.
- Codex still fixing second-review failures.

### 2026-11-06 ~06:20 ET — second-review GREEN + t349u source inventory + 15-phase eng checklist
- Parent independent verify: `python3 -m pytest research/market_calibration/tests -q` → **93 passed in 0.11s** (also `pytest_second_review_green.txt`).
- Same-set: vs first GREEN 74 passed → **IMPROVED** (+19 honesty/contract tests). Forecast Brier/MAE **NOT MEASURED**.
- Rico t349u: loaded betting-game-brainstorm + nfl-game-script-run; wrote SOURCE_INVENTORY + WORKFLOW_15PHASE_ENGINEERING (phases 2–13/15 N/A with reasons).
- Live probes: ESPN/nflverse/NGS/PFF/DK/Pin SUCCESS 200; PFR+FD LIVE_HTTP_403; Odds API key SET but no network spend.
- Cached Pin Q2–Q4 spreads ABSENT → NOLINE.
- Codex still writing COMPLETION/README after green.

### 2026-11-06 ~06:24–06:26 ET — Codex final 97 green + Ghost-route preflight
- Parent verify: **97 passed in 0.14s** (`pytest_parent_verify_final.txt`). Same-set vs 93: **IMPROVED** (+saved-audit/grade arithmetic). Forecast edge **NOT MEASURED**.
- Codex COMPLETION_CODEX.md + codex_exec_evidence.json delivered under market_calibration/reviews/.
- Loaded `nfl-projection-source-preflight`. Ghost routes freshness JSON written. Blitz owns gate — no duplicate run_gate.
- Connector endpoint attempts: sports-leader SUCCESS; balldontlie SUCCESS; statshawk free 4997/5000; open-leagues MIXED (ESPN 403 via their probe); muffed SUCCESS; prediction-markets-picks SUCCESS; odds-bridge LOGIN_REQUIRED no bypass.
- pull_props.py MISSING at canonical tools path. Outlier SAVED_ONLY. Pin Q2–Q4 spreads NOLINE in saved r6.

### 2026-11-06 ~06:27 ET — t353u: coordinator-only; Codex independent review launched
- Policy: substantial work via Codex ChatGPT-plan; no inline implement/analyze.
- Launched codex independent review PID for INDEPENDENT_CODEX_REVIEW.md + GHOST_HANDOFF_MARKET_ADAPTER.md.
- No local heavy sims; no paid cloud; Linear is shared tracking place.
- Impact: NOT MEASURED until review artifacts + pytest re-run land.

### 2026-11-06 ~06:31–06:41 ET — Codex independent review + P2 audit regen (t353u coordinator)
- Independent review artifacts written by Codex; parent verified **108 passed** combined.
- IMPROVED: 11 false-PASS regressions red→green (snapshot identity + manifest overclaims).
- P2 OPEN then CLOSED by Codex audit-regen: prior audit sha 3d1ff2de… preserved; new a376a9ff…; 76 pair_id leaves only.
- Parent verify post-regen: see pytest_parent_verify_post_audit_regen.txt (expect 109).
- Forecast accuracy NOT MEASURED. No paid odds/sims. Linear NFL-16 updated.

### 2026-11-06 ~06:54 ET — B01 wire agreement Codex LAUNCHED (adapter-only)
- Ghost packet: 59 passed / 1 failed (DIRECT producer→adapt_joint_trials missing trial fields).
- Mismatches: status object vs scalar; input_manifest_digest vs hash; component_version/dependencies vs plurals; stats.points vs points; OT under status.
- Codex job: accept unchanged producer wire in market_calibration only; no CORE edits; no silent remap.
- Impact predictive: NOT MEASURED. Engineering pending Codex evidence.

### 2026-11-06 ~07:05 ET — Authorized SHA rebind Codex LAUNCHED
- Auth docs: CONTRACT_BINDING_AUTHORIZATION + HANDOFF_TO_BETGURU_BINDING.
- Rebind target 6471e69b… (historical d6a4689f… + companion wire link only).
- Example 50be826a… unchanged. Wire 1.0.0-producer locked.
- Pending: market suite + DIRECT fresh results from Codex.

### 2026-11-06 ~07:11 ET — Authorized SHA rebind COMPLETE + parent verify PASS
- Bound full SHA: `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`
- Example unchanged: `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd`
- Codex: market 179 / DIRECT 1 / binding 6
- Independent Grok parent: market 179 / DIRECT 1 / binding 6 (fresh)
- Claims: NOLINE; Bias UNIMPLEMENTED; source_readiness false; Ghost NOT_CLAIMED; impact NOT_MEASURED
- Impact class for transport SHA guard: **IMPROVED** (was blocking DIRECT; now GREEN). Forecast/calib still NOT MEASURED.

### 2026-11-06 ~07:18 ET — ≥40pp anomaly delivery guard IN PROGRESS (Codex, no duplicate launch)
- Rico t367u / phase5_anomaly_delivery_guard.txt; market_calibration ONLY.
- Existing CORE-launched Codex PID 3846877 on wt-market-calibration (TDD RED: test_delivery_guard ImportError pending implementation).
- Quote extraction (authorized saved): loader 132 records (FD 62 / DK 42 / Pin 28); pairing probe MATCHED 60 research pairs @ asof 2026-11-06T04:00:00Z; Pin Q2–Q4 spreads ABSENT→NOLINE.
- Firecrawl Pin: ERROR (blocked). Public curl Pin/DK/ESPN 200; FD 403. Odds API: no spend.
- Data sufficiency for Bias fit: **false**. Claims: NOLINE / Bias UNIMPLEMENTED / no Ghost final / no manufactured quotes.
- Artifacts: reviews/QUOTE_EXTRACTION_INVENTORY_2026-11-06.json, PUBLIC_METHOD_PROBES, tracking/PREFLIGHT|BRAINSTORM|WORKFLOW_15PHASE_ANOMALY_GUARD_*.
- Impact: **NOT MEASURED** until detector tests green + parent verify.

### 2026-11-06 ~2026-11-06 07:25:31 ET — ≥40pp anomaly delivery guard COMPLETE + parent verify PASS
- Detector: `delivery_guard.guard_edge_delivery`; threshold 0.40; DIAGNOSTIC_ANOMALY; raw preserved; no anchor hide.
- Codex market: **235 passed**; Parent: **246 passed** (incl. independent false-pass); guard tests: **67**.
- Contract preserved `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`; example `50be826a…`.
- Quotes: loader 132; MATCHED research pairs 60; Pin Q2–Q4 spreads NOLINE; Firecrawl Pin ERROR; Odds API spend 0.
- Data sufficiency Bias fit: **false**. NOLINE / Bias UNIMPLEMENTED / source_readiness false / Ghost NOT_CLAIMED.
- Impact: **IMPROVED** (detector/quarantine plumbing). Forecast edge still **NOT MEASURED**.
- Ghost packet: `reviews/GHOST_INDEPENDENT_PACKET_ANOMALY_GUARD_2026-11-06.json`
- Exhausted blockers: Pin Q2–Q4 saved absent; Odds API no-spend; Firecrawl Pin blocked; no package Provenance train rows for Bias.fit.

### 2026-11-06 07:50:49 ET — DAL@IND prospective quote recovery (wk folder mismatch → week **9**)
- Identity VERIFIED: ESPN `401873040` / nflverse `2026_09_DAL_IND` / kickoff `2026-11-08T18:00:00Z` / **week 9** (folder name wk10 is label-only).
- Pin: **ERROR** (Firecrawl blocked). Circa: **MISSING/APP_REQUIRED** (404 sportsbook path; menu has no live lines).
- ESPN providers for event: **DraftKings only** (FD/Caesars/BetMGM/ESPN BET empty). DK research snapshot FG -5.5/-105 vs +5.5/-115, total 51.5 -110/-110, ML -230/+190 @ retrieval `2026-11-06T12:50:49Z` — **no book last_update_utc** → actionable **NOLINE**.
- odds-bridge **LOGIN_REQUIRED** (no bypass). Odds API spend **0**. JAX@BAL caches **excluded** (wrong event).
- HTTP200 alone not treated as quote access. No Pin/Circa paired provenance → no market comparisons / no picks.
- Evidence: `research/market_calibration/reviews/dal_ind_quotes_2026-11-06/` and packet `integration/prospective_wk10_2026-11-08/market_quotes_betguru/`.
- Impact: **NOT MEASURED**. Source readiness remains false for actionable quotes.

### 2026-11-06 ~07:52 ET — CORE fold-in of DAL@IND quote packet (research)
- CORE copied BetGuru `dal_ind_quotes_2026-11-06` → prospective `market_quotes_betguru/` with STRICT=NOLINE / RESEARCH=observed DK only.
- CORE continues usage-cell fit independent of actionable odds.

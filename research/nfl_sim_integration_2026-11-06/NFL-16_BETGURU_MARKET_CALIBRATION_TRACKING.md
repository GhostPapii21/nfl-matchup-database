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

### 2026-11-06 ~07:51–07:52 ET — CORE prospective + BetGuru quotes fold-in (executor)
- **Labels:** verified 01:15Z = TNF kickoff Thu 20:15 ET (not postgame); packet wk10 dir misnomer → week **9** `2026_09_DAL_IND` / ESPN 401873040 (BetGuru EVENT_IDENTITY_VERIFY agrees).
- **Eligibility:** ESPN 78≠ACT; Pierce IR/RES excluded; 8 Q as AVAILABLE_WITH_UNCERTAINTY; Phase 15 inactives NOT_YET.
- **Quotes:** BetGuru packet copied to `integration/prospective_wk10_2026-11-08/market_quotes_betguru/`. Strict **NOLINE**; DK ESPN snapshot research-only (no book_last_update). No paid pulls; bridge not bypassed.
- **Paths:** joint n5 vs empirical n500 documented **NONINTEGRATED** pending usage-cell bridge (`PATH_SEMANTICS_JOINT_VS_EMPIRICAL.md`).
- **Codex usage fit (in progress):** `fit_prospective_usage.py` → sample_size 1068, 8 usage / 20 outcome cells; forecast after sha256:32dfd895…; reproducibility bug (runs/ polluting source hash) being fixed by Codex. pytest joint after fit: check pending.
- **15-phase:** brainstorm + checklist + report written under `nfl-database/runs/2026-11-08_DAL@IND/` — preliminary, **no picks**.
- **Acceptance:** projection_ready still false; full integration acceptance **not** claimed. Genuine blockers: inactives unpublished; actionable quotes NOLINE; coverage/NGS MISSING; Bias unfitted; usage-fit reproducibility + packet promotion pending.
- Metric class: IMPROVED source/eligibility/label honesty; forecast edge **NOT MEASURED**.

### 2026-11-06 ~07:54–07:55 ET — usage fit promoted + quotes research fold-in
- Codex `fit_prospective_usage.py`: n=1068 → 8 usage / 20 outcome; source-hash runs/ exclusion fix; pytest **81 passed**; reproducibility identical True; forecast sha256:09f1c433…
- Packet: fitted model.json promoted; registry/splits/run_spec packet-authoritative restored; reviews/codex_usage_fit/* + COMPLETION_PHASES_AND_FIT.md + PATH SHARED_PARTIAL.
- market_quotes_betguru/: STRICT NOLINE; RESEARCH DK snapshot labeled; no conditioning into data_only.
- Independent Grok assumption/output review vs research DK written (not schema counts).
- Acceptance: projection_ready still false. Blockers: inactives; verified multi-book quotes; coverage; Bias; full lineage integration; no 100k triad / no picks.
- Metric: IMPROVED empirical usage plumbing + label/quote honesty; forecast edge NOT MEASURED.

### 2026-11-06 ~07:56–07:58 ET — final fitted freeze + dual independent reviews
- Codex usage-fit COMPLETE (sandbox-staged): sample 1068; 8/20 cells; source-hash + validation-order fixes; pytest **82 passed**; authoritative forecast `sha256:40c23caa…`; means DAL 27.2/IND 14.2 reproducible.
- Packet promoted model + reviews/codex_usage_fit + FORECAST_ID_RECONCILIATION; PATH SHARED_PARTIAL.
- BetGuru quotes: STRICT NOLINE; RESEARCH DK snapshot labeled; not conditioned.
- Independent Grok + independent Codex assumption/output reviews written (not schema-count acceptance).
- projection_ready=false; Phase15 NOT_YET; full integration acceptance false.
- Genuine blockers: inactives; verified multi-book quotes; coverage/NGS; player equal-weight roles; accounting lineage; 100k triad / Bias attributed.
- Metric: IMPROVED empirical usage + honesty/reproducibility; edge NOT MEASURED.

### 2026-11-06 ~07:58 ET — empirical n500 stale source_composition
- `runs/sim_dal_ind_summary.json` source_composition still says `..._JAX_BAL_...` while config_id is dal_ind — **stale label**, not wrong game IDs. Logged in reviews/EMPIRICAL_N500_STALE_LABEL_NOTE.md. adapter_projection_allowed=false / UNIMPLEMENTED_LEGACY_YARD_ROW_BOOTSTRAP.

### 2026-11-06 ~07:59–08:00 ET — roles/unify/JAX_BAL Codex launched
- Baseline BEFORE_METRICS written (equal-weight roles; stale JAX_BAL source_composition in simulate.py + sim summary).
- Codex PID logged in prospective logs/codex_roles_unify.pid — TDD empirical roles + shared accounting bridge + config-derived source_composition.
- Quotes/inactives/coverage remain explicit NOLINE/NOT_YET/MISSING; not used as stop reason.
- 100k Bias triad deferred until shared semantics ready.

### 2026-11-06 ~08:00–08:08 ET — roles unify + SHARED_ACCOUNTING_V1 (Codex)
- **Before:** all rotation_weights equal_weight=True; PATH SHARED_PARTIAL; simulate source_composition hardcoded JAX_BAL.
- **After:** EMPIRICAL_ROLES + TEAM_PRIOR_DIRICHLET_HALF_SHRINKAGE_20; PATH SHARED_ACCOUNTING_V1; source_composition(cfg) → `team_only_2026_w1_8_DAL_IND_...`.
- Same-set: equal→empirical KL→0 on train (identity). Heldout: DAL target/carry + IND target improve; **IND carry KL 0.45→2.26 worsen** (retained).
- n=5: before means DAL 27.2/IND 14.2 → after 18.8/14.2; conservation 0→0; opp/yard crosscheck 60 checks / 0 fail; seeded_repeat identical True; forecast `sha256:5cf792ce…`.
- Tests: targeted **86 passed**; full suite 126 pass / 36 fail (legacy/missing parquet) — no whole-engine green claim.
- Quotes NOLINE / Phase15 NOT_YET / coverage MISSING preserved. DEFERRED_100K_UNFINISHED_SEMANTICS.
- Metric class: IMPROVED roles+shared accounting honesty; forecast edge NOT MEASURED; heldout mixed.
- Packet: `core_roles_unify/`, model promoted, READINESS updated, Grok independent review written.

### 2026-11-06 ~08:08–08:10 ET — independent Codex roles review
- Verdict: accept narrow research engineering (empirical roles + SHARED_ACCOUNTING_V1); not full semantic/predictive readiness.
- IND carry heldout KL 0.45→2.26 = substantive failure (disclosed); 100k deferral correct; quotes/Phase15 not blockers for data_only accounting closure.
- Artifact: prospective `reviews/INDEPENDENT_CODEX_ROLES_UNIFY_REVIEW.txt` (+ Grok sibling).

### 2026-11-06 ~08:15 ET — next Codex: full-suite 36 + IND carry + score sensitivity
- BEFORE hashes: prospective `reviews/NEXT_PASS_BEFORE_HASHES.json` (immutable prior core_roles_unify).
- Fresh full suite pre: 126 passed / 36 failed (logs/pytest_full_suite_pre.txt). Dominant symptom PBP_MISSING at `research/period_engine_v0/data/play_by_play_2026.parquet`; also KeyError player_samples/adjustments_meta; NoneType in empirical/adjustments when history None.
- IND carry heldout KL worsen is REGRESSION — do not promote as better forecast.
- Old artifacts immutable.

### 2026-11-06 ~08:16–08:25 ET — suite fix Codex COMPLETE
- Before: 36 failed / 126 passed. After: **167 passed / 0 failed**.
- Classification: 36/36 MISSING_DEPENDENCY_OR_FIXTURE (PBP symlink to packet parquet); 0 REAL_REGRESSION per Codex (adversarial review pending).
- IND carry MLE KL 2.26 = EMPIRICAL_IND_CARRY_REGRESSION — **not promoted**. Selected mix_equal_0.25 on train/dev; W6 leak-safe window; W7–8 inspected-holdout KL 0.15 vs equal 0.45 / MLE 2.26; mixed other roles.
- Score sensitivity: prior 27.2→18.8 was input-hash seed confound; v2 seed + player RNG split → team means identical DAL 21.8 / IND 13.6 across equal/empirical/robust; conservation 0.
- Semantics: penalties/returns/official_OT UNSUPPORTED stubs; DEFERRED_100K.
- Protected old sha256 trees immutable (PROTECTED_ARTIFACT_INVENTORY).
- Packet: reviews/dal_ind_suite_fix_2026-11-06/; model=selected_robust; readiness suite_fix FULL_SUITE_GREEN_167.
- Metric: IMPROVED suite+invariance+role honesty; edge NOT MEASURED.

### 2026-11-06 ~08:25–08:27 ET — adversarial Codex review of suite fix
- Verdict: accept limited research repair; reject leak-safe promotion / complete invariance / official semantics.
- Finding: candidate ranking train/dev-only but **acceptance gate uses inspected W7–8** IND carry KL — disclosed contamination; not pristine validation.
- Classification: original 36 fixture-consistent; repair also hardened APIs — not “fixture only”.
- Invariance: architectural support + n=5 paired evidence; incomplete terminal/OT coverage.
- UNSUPPORTED stubs = research containment, not official-rules acceptance. DEFERRED_100K correct.
- READINESS updated with leak_note + blockers. projection_ready=false. No picks.

### 2026-11-06 ~09:10 ET — invariance/decontaminate/materiality Codex launched
- BEFORE hashes: `reviews/INVARIANCE_PASS_BEFORE_HASHES.json`. Suite167 green acknowledged; no intermediate user pings.
- Priorities: broader role-attribution invariance; remove W7–8 from acceptance (dev-only/inspected); freeze provisional policy; penalties/returns/OT materiality; external activation engineering check; no 100k; no quotes bypass; old artifacts immutable; PFF quarter collection separate (consume only when ready).

### 2026-11-06 ~09:10–09:17 ET — invariance/decontam Codex COMPLETE
- Invariance: **PASS** 400 trials × 4 policies × 5 seeds; OT×4; halftime×100; team paths identical; player attribution differed 15 comparisons (allowed). Coupling=false; forced coupling UNSUPPORTED.
- Decontam: new validate.py — W7–8 INSPECTED_DEV_REPORTING_ONLY (no gate); W1–3/W4–5 selection only; mix_equal_0.25 = **RESEARCH_PROVISIONAL_NOT_PROMOTED**. Old suite_fix validate immutable.
- Pristine plan: future games after 2026-11-08; excludes W1–8 and 2026_09_DAL_IND; historical_pristine_claim=false.
- Materiality: DAL/IND penalty ~7–9% rows; OT 1/8 each; league OT 11/121; punt-net supported; official OT/penalties/returns UNSUPPORTED.
- Activation engineering: consumer replay forecast `sha256:6ecf9e36…` trials_exact true; NOT readiness.
- Protected: 657 hashes unchanged; engine suite 167 passed; repo-wide 2 missing fixture collection errors.
- PFF NOT_READY_NO_DUPLICATE. DEFERRED_100K. projection_ready=false.

### 2026-11-06 ~09:17–09:19 ET — adversarial review + quarantine sidecar
- Independent Codex: W7–8 removed from NEW validator only; old suite_fix validate still has contaminated gate → SUPERSEDED_PROMOTION_PATH.md sidecar (bytes immutable).
- Invariance = 100 scenarios × 4 policies (not universal). Pristine plan honest; protocol incomplete. Materiality ≠ adequacy.
- Grok concurs. projection_ready=false. No picks.

### 2026-11-06 ~09:24 ET — entrypoint/protocol/semantics/invariance Codex launched
- BEFORE: reviews/ENTRYPOINT_PASS_BEFORE_HASHES.json. Prioritize enforced single validation entrypoint; reject old contaminated gate with regression tests; complete pristine future eval protocol; semantics bounds; expand invariance; fixture provenance without skips. No 100k/readiness; PFF separate no duplicate; artifacts immutable.

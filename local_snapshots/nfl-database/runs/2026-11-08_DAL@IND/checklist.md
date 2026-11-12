# DAL @ IND — Week 9 PRELIMINARY RESEARCH checklist (15 phases)
**Game:** ESPN 401873040 / nflverse 2026_09_DAL_IND / balldontlie 1392339  
**Kickoff:** 2026-11-08 13:00 America/New_York (2026-11-08T18:00:00Z)  
**Venue:** Lucas Oil Stadium (retractable)  
**Pulled_et:** 2026-11-06 ~07:39–07:50 ET (sources below)  
**Input cutoff (freeze):** 2026-11-06T12:40:00Z  
**Phase status:** PRELIMINARY RESEARCH — **not** Phase-15 final. **No picks. Quotes NOLINE.**  
**Directory note:** packet path `prospective_wk10_*` is a misnomer; authoritative week is **9**.  
**Retrospective label note:** certified_asof `2026-11-06T01:15:00Z` = TNF kickoff Thu 20:15 ET, **not** postgame (see LABEL_CORRECTIONS_ADDENDUM; frozen bytes unchanged).

| Scope | Phase | Status | Number / note | Source | Pulled (ET) |
|---|---|---|---|---|---|
| GAME | 1 Data pull/reconcile | PASS (partial) | ESPN scoreboard+summary+rosters SUCCESS; nflverse games.csv SUCCESS (schedules.csv stub 404→games); PBP W1–8 extract SUCCESS; box/snaps/participation partial | raw/espn_*; raw/nflverse_games.csv; records/pbp_DAL_IND_w1_8.csv.gz | 2026-11-06 07:39 |
| GAME | 2 Opportunity gate | MISSING (no priced leg) | No candidate legs; empirical usage-cell fit PENDING/IN_PROGRESS; placeholder terminals only in joint model | inputs/model.json flags EMPIRICAL_USAGE_PENDING | 07:46 |
| GAME | 3 Defensive profile | MISSING | Team yards/points allowed not assembled this pass; Sharp/FTN not pulled | — | — |
| GAME | 4 Defender coverage | MISSING | allows_sim_effect=false; no named-defender mapping; coverage UNKNOWN | joint missing_features | 07:46 |
| GAME | 5 Pressure/blitz | MISSING | enable_blitz_strata=false; FTN charting not loaded | config effects | 07:45 |
| GAME | 6 QB grade card | MISSING | §15 card not run this preliminary pass | — | — |
| GAME | 7 Role/RB rules | PARTIAL | Registry ACT skill roles present; Pierce IR excluded; no priced RB leg | records/active_eligibility_audit.json; inputs/registry.json | 07:48 |
| GAME | 8 Injuries | PASS (preliminary) | Pierce IR/RES not ACT; 8 Questionable retained AVAILABLE_WITH_UNCERTAINTY; final inactives UNKNOWN | ESPN summary + nflverse roster | 07:48 |
| GAME | 9 NGS | MISSING | Public NGS routes/sep/TTT not pulled this pass | — | — |
| GAME | 10 Film | MISSING | No film claims; UNVERIFIED not elevated | — | — |
| GAME | 11 Environment | PASS (preliminary) | NWS sunny ~56°F wind 10 mph precip 0%; Open-Meteo agrees; roof retractable → WEATHER ALERT not auto-applied | src/weather/* | 07:48 |
| GAME | 12 Source audit | PASS (partial) | SOURCE_LEDGER_PROSPECTIVE success≈11; projection_ready=false; freshness stamped; coverage/NGS/odds gaps listed | SOURCE_LEDGER_PROSPECTIVE.json; READINESS_PROSPECTIVE.json | 07:43 |
| GAME | 13 Script/underdog gate | MISSING | Spread NOLINE (multi-book consensus unavailable); qualitative brainstorm only | brainstorm.md; quotes NOLINE | 07:48 |
| GAME | 14 Models/price/edge | PARTIAL / NOT MEASURED edge | Joint n=5 conservation PASS (forecast sha256:8be81b96…); empirical n=500 score_means recorded; Bias UNIMPLEMENTED; 100k×3 NOT RUN (no heavy); quotes NOLINE → no edge; paths NONINTEGRATED | runs/joint_*; runs/sim_dal_ind_summary.json; PATH_SEMANTICS_*.md | 07:44–07:46 |
| GAME | 15 Inactives | NOT_YET | Inactives unpublished (~90 min prekick Sun ~11:30 ET). Do not pretend known. | — | — |

## Eligibility (roster ≠ active)
- ESPN roster endpoint DAL=78 IND=78 = full squad listing, **not** game-day actives.
- nflverse ACT: DAL 53 / IND 53; registry ACT players 106; AVAILABLE 98 + AVAILABLE_WITH_UNCERTAINTY 8.
- Pierce: Injured Reserve / roster status RES — correctly **not** in ACT opportunity pool.
- Questionable retained with uncertainty (recheck Phase 15): Davis-Gaither, Tyler Smith, Ferguson, Overshown, Porter Jr., Gould, Walley, Ogletree (see audit JSON).

## Path semantics
- Joint producer (n=5) vs empirical possession (n=500): **NONINTEGRATED** until usage cells share PBP-fitted opportunity/yard/accounting with explicit bridge (see packet PATH_SEMANTICS_JOINT_VS_EMPIRICAL.md).

## Summary
- Legs published: **0** (research only; no picks)
- CUT: n/a
- Genuine blockers: Phase 15 inactives not published; multi-book quotes NOLINE / odds-bridge LOGIN_REQUIRED (BetGuru owns auth; no bypass); coverage/NGS/FTN MISSING; Bias unfitted; usage-cell empirical fit in progress; full integration acceptance **not** claimed
- Seeds: empirical seed 1329861859 / seed_base 20261108; joint forecast_id sha256:8be81b9695085def31df5ec99cbe78cffa637ca1a6c32c87d49581ce8d5745a5
- Trial note: joint_trials_summary lists trial 4 state INCOMPLETE while complete_pass claims 5/5 — honesty flag; treat as n_usable accounting needs reconcile on next freeze

VETTED: pending independent Grok/Codex assumption+output review (not schema-count acceptance)

## BetGuru quote packet fold-in (2026-11-06 07:52 EST)
- Copied → packet `market_quotes_betguru/` (JSON + INTERPRETATION + STRICT_VS_RESEARCH).
- Actionable: **NOLINE** (Pin blocked, Circa missing, bridge LOGIN_REQUIRED, DK missing book_last_update).
- Research-only DK observed: DAL -5.5 / IND +5.5, total 51.5, ML -230/+190 @ fetch 07:50:49 ET — **not** verifiedquote.
- Phase 13/14 remain MISSING/PARTIAL for priced edge; CORE stays independent.

## Codex usage-cell fit fold-in (2026-11-06 07:54 EST)
- Staged under CORE `runs/dal_ind_usage_fit/`; promoted fitted `model.json` only into packet inputs (registry/splits/run_spec restored packet-authoritative).
- Metrics: sample_size 1068; usage 8; outcome 20; forecast `sha256:09f1c433…`; means DAL 27.2 / IND 14.2; 5/5 PASS; reproducibility identical True; pytest **81 passed**.
- PATH: **SHARED_PARTIAL_SEMANTICS** (PBP subset shared; opportunity/roles/accounting/OT/lineage still separate).
- Phase 2: PARTIAL empirical usage cells now present — still **no priced leg** (quotes NOLINE actionable).
- Phase 14: PARTIAL plumbing improved; edge still NOT MEASURED; research DK comparison only (see INDEPENDENT_GROK review).
- Codex staged checklist/report sidecars: `checklist_CODEX_STAGED.md`, `report_CODEX_STAGED.md`.

## Final fit freeze + independent Codex review (2026-11-06 07:58 EST)
- Authoritative fitted forecast_id: `sha256:40c23caa5a0327c8ebc757520ad430e1401305518cd653549d542cc0300a3919` (after=repeat; means DAL 27.2 / IND 14.2).
- pytest joint_producer: **82 passed**.
- Independent Codex review: `reviews/INDEPENDENT_CODEX_ASSUMPTION_OUTPUT_REVIEW.txt` — SHARED_PARTIAL justified; provenance ID cites needed reconcile (done); research DK tension diagnostic only; NOLINE actionable; no full integration; no picks.
- Projection_ready: **false**. Phase 15: **NOT_YET**.

## Roles unify + SHARED_ACCOUNTING_V1 (2026-11-06 08:07 EST)
- Empirical roles promoted (equal_weight False all cells); Pierce excluded; Q retained.
- Heldout: most improve; IND carry KL worsens (explicit). PATH: SHARED_ACCOUNTING_V1.
- source_composition config-derived; new DAL@IND sims ≠ JAX_BAL; old summary stale string retained.
- Targeted tests 86 pass; full suite 126/36 fail. forecast after `sha256:5cf792ce…` means DAL 18.8 / IND 14.2; repeat identical.
- Phase15 NOT_YET; quotes NOLINE; 100k DEFERRED. No picks.
- Artifacts: `core_roles_unify/`, `reviews/codex_roles_unify/`, Grok review above; Codex independent review launching.

## Independent Codex roles review (2026-11-06 08:10 EST)
- Saved `reviews/INDEPENDENT_CODEX_ROLES_UNIFY_REVIEW.txt`.
- Accepts narrow engineering result (empirical roles + SHARED_ACCOUNTING_V1); rejects full predictive readiness.
- IND carry heldout KL failure retained; 100k deferral endorsed; Phase15/quotes not blockers for data_only accounting close.

## Suite fix + robust roles (2026-11-06 08:25 EST)
- Full suite 36→0 fails (167 passed) after PBP fixture symlink; classification MISSING_FIXTURE.
- Role policy: mix_equal_0.25 ROBUST; empirical MLE IND carry NOT promoted (regression).
- Score 27.2→18.8 was RNG confound; paired invariant means DAL 21.8 / IND 13.6 across role variants.
- Penalties/returns/official OT UNSUPPORTED stubs; DEFERRED_100K.
- Phase15 NOT_YET; quotes NOLINE. Old artifacts immutable. Adversarial Codex review launching.

## Adversarial Codex suite review (2026-11-06 08:27 EST)
- Saved `reviews/INDEPENDENT_CODEX_ADVERSARIAL_SUITE_FIX_REVIEW.txt`.
- Accepts limited research repair; rejects leak-safe promotion / complete invariance / full NFL semantics acceptance.
- Key: validate.py acceptance uses inspected W7–8 IND carry KL — contamination disclosed; ROLES_POLICY_ROBUST remains research staging not pristine holdout win.

## Invariance + decontam (2026-11-06 09:18 EST)
- Attribution invariance PASS (400 trials, multi-seed, OT). W7–8 not acceptance gate. Policy RESEARCH_PROVISIONAL_NOT_PROMOTED.
- Materiality quantified; official OT/penalties/returns still UNSUPPORTED. Activation engineering replay OK — not projection_ready.
- PFF NOT_READY (no duplicate). Adversarial Codex review launching. No picks.

## Adversarial invariance review (2026-11-06 09:20 EST)
- Codex+Grok: partial decontam; quarantine sidecar on old validate; invariance narrow-scope PASS; pristine plan honest; no readiness. No picks.

# Package note from before this public commit

The root `README.md` is the status of the published tree. This file is the checkpoint note that traveled with the archive. Where it says an executor must not push, that was the packager speaking to a local executor. The public branch is this commit.

# NFL model portable checkpoint (sanitized) — toward GitHub source of truth

**Stamped:** 2026-11-06 13:32 EST (America/New_York)  
**Upload target (parent/cloudagent only):** https://github.com/GhostPapii21/nfl-matchup-database (PUBLIC `main`)  
**Linear:** [NFL-16](https://linear.app/nfl-database/issue/NFL-16/nfl-sim-model-autonomous-iteration-and-validation-tracking) · [NFL-41](https://linear.app/nfl-database/issue/NFL-41/packaging-portable-nfl-model-checkpoint-github-upload-bootstrap-public) · [NFL-56](https://linear.app/nfl-database/issue/NFL-56/github-source-of-truth-completeness-15-phase-newsweather-100k)

## Production GOAL vs CURRENT readiness

| | Goal (Rico t367u) | Current in this package |
|---|---|---|
| Role | Complete GitHub SoT: projection→sim, source pulls, tests, brainstorm, news, weather, **all 15 phases**, **100k** workflows; bots fetch/run from repo | **Incomplete integration** — packaging toward goal |
| `projection_ready` | true after gate | **false** |
| Quotes / calibration | Pinnacle + books + ORCA comparison with provenance | **NOLINE**; calibration FITTED **false**; ORCA/FTN **ACCESS_UNKNOWN** |
| Official semantics | Supported or bounded | penalties/returns/OT **UNSUPPORTED**; DEFERRED_100K |
| Phase15 / inactives | Complete ledger | **NOT_YET** |
| Validation entrypoint | Single enforced path | **Not implemented**; contaminated suite_fix validator superseded (do not promote) |
| Picks | Allowed only after acceptance | **None** |

Open work: [`OPEN_LINEAR_ITEMS.md`](OPEN_LINEAR_ITEMS.md). Market registry: [`docs/source_registry/SOURCE_REGISTRY.md`](docs/source_registry/SOURCE_REGISTRY.md).

## Layout
- `core/possession_engine_v0/` — engine + tests + selected run docs
- `research/` — prospective DAL@IND packet (quote dumps hash-only removed)
- `fixtures/` — 20 materialized files
- `market_calibration/` — incomplete BetGuru slice
- `workflows/operational_specs/` — PHASE_SCRIPT, 15-phase workflow, core_contract (user operational)
- `workflows/user_skills_snapshot/` — user skill_draft / brainstorm snapshots (**not** Cursor managed/developer skills)
- `workflows/prompts/` — own workflow prompts only
- `docs/source_registry/` — Pinnacle/books/ORCA/FTN/PFF placeholders + status
- `known_flags/`, `unfinished_legacy/`, `inventory/`

## Executable portability smoke (bounded) vs incomplete integration
```bash
bash scripts/smoke_offline.sh
# expects: 9 passed (test_suite_fix + test_roles_unify)
```
Evidence: `inventory/smoke_offline.log`. Smoke proves **portable engine subset** imports/runs offline. It does **not** prove 15-phase completeness, live quotes, 100k, Phase15, or production acceptance.

Ephemeral `.git` may be created locally for `git rev-parse` inside freeze_run — **strip before upload**; it is not proof of GitHub sync.

## Data pull / update
See `docs/SOURCE_ADAPTERS.md` + `docs/source_registry/SOURCE_REGISTRY.md`.  
Auth connectors (odds-bridge) remain needsAuth — **no keys in package**. Never invent ORCA/FTN/Pinnacle quotes.

## Public sanitization
`inventory/PUBLIC_SANITIZATION.json` — removed/hash-only proprietary & raw quote dumps.

## Upload blockers (parent)
1. Executor must not push; use cloudagent/sanctioned uploader.
2. Public secret scanning / license review (nflverse etc.).
3. Strip ephemeral `.git`; consider LFS/slim for large `trials.jsonl`.
4. Re-verify Linear OPEN_LINEAR_ITEMS URLs/status before announcing full tracking.

## Proposed routine bootstrap
`docs/PROPOSED_ROUTINE_BOOTSTRAP.md` (parent edits routines only).

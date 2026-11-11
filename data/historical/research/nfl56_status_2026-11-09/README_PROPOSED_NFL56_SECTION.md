<!-- PROPOSED README SECTION: NOT COMMITTED. Draft 2026-11-09 ~15:25 ET for Rico/Ghost review. -->
## NFL-56: Production goal vs. current readiness

> **Current status: `projection_ready = false`.** This repository does not produce picks or betting recommendations. Nothing here is production-validated.

### Production goal (NFL-56, not yet met)
This repository is meant to become the single source of truth for the projection-to-simulation workflow. Bots should be able to fetch and run everything from the repo with routine-only maintenance. When complete it will hold:

1. **All 15 phases** as runnable workflows, each emitting an explicit status: PASS, FAIL, MISSING, STALE, NOT_YET or BLOCKED. No phase is ever skipped silently. The phases are: data reconcile; opportunity; defensive profile; defender coverage; pressure/blitz; QB card; roles/RB rules; injuries; NGS; film; environment; source audit; game script; models/price/edge; inactives.
2. **News and weather adapters** with documented freshness windows:
   - Injuries and inactives come from official NFL/team reports, cross-checked against ESPN.
   - Weather comes only from NWS and Open-Meteo, for the window from kickoff to kickoff+3.5h, and must be no more than 24h old.
   - Every pull carries a source timestamp.
3. **A 100,000-trial entrypoint** for Monte Carlo, Bias and Game Randomness:
   - Each run is seeded and logged.
   - It must fail closed while DEFERRED_100K or NFL-49 is open.
4. **A routine bootstrap** that pulls, runs and pushes on a schedule without a continuously awake session. Pushes go through a branch and PR, never a force-push.
5. This README section, kept current.

### Current readiness (as of 2026-11-09)
| Item | Status |
|---|---|
| `projection_ready` / `full_integration_acceptance` | **false / false** |
| NFL-49 production acceptance (four pillars) | ACCEPTANCE_NOT_MET |
| NFL-42 single validation entrypoint | Not implemented; contaminated `dal_ind_suite_fix_2026-11-06/validate.py` must not be promoted |
| NFL-43 official semantics (penalties/returns/OT) | Unsupported → **DEFERRED_100K** |
| 15-phase workflow | Documented in skills and dated ledgers, **not runnable from this repo** |
| 100k MC/Bias/GR triad | **Not run** (0 trials, no seed). Research-only 100k files in `research/` and research branches are ungated sensitivity work, not the production triad |
| Phase 15 (official inactives) | NOT_YET until each game's 90-minute window |
| Quotes / calibration | NOLINE; calibration not fitted |
| Weather adapter | Local `tools/weather_forecast.py` (NWS + Open-Meteo, 24h gate). Not yet in this repo, and it has no observed/past-game mode |
| Routine bootstrap | **Does not exist.** `docs/PROPOSED_ROUTINE_BOOTSTRAP.md` is a proposal. `scripts/smoke_offline.sh` runs only two offline test modules |

### Rules while readiness is false
- Never set `projection_ready=true` outside the NFL-49 gate with attached evidence.
- Don't change model weights or formulas without a ticket.
- Never invent stats, inactives, assignments or quotes. A missing value is MISSING, not zero.
- Don't spend paid or Odds API credits without explicit authority.
- Label agent-asserted information as such until it's verified against an official source.

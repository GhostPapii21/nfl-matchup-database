## NFL-56: production goal vs current readiness

**Goal (NFL-56, not yet met).** NFL-56 is the source-of-truth target for game projections. Every game run would produce a 15-phase ledger with an explicit PASS / FAIL / MISSING / STALE / NOT_YET status per phase and per leg, plus three seeded 100,000-trial models (Monte Carlo, Bias, Game Randomness) from one accepted entrypoint. Inputs would be dated and sourced, and prices would come from authenticated books. Nothing would be published as a pick until an independent vet signs off.

**Current readiness: `projection_ready` is false.**

| Item | Status |
| --- | --- |
| NFL-42 validation entrypoint | Not enforced. The historical validator is contaminated and must not be promoted. |
| NFL-43 penalties, returns, official overtime | Unsupported. |
| NFL-44 pristine evaluation | Protocol incomplete. Inspected weeks are development evidence, not a holdout. |
| NFL-45 calibration | Not fitted. Quotes stay `NOLINE` without authenticated book access. |
| NFL-49 final acceptance | Not met. Acceptance is fail-closed. |
| NFL-56 15-phase ledger and 100k triad | Deferred (`DEFERRED_100K`). Phase 15 inactives are `NOT_YET` until the official list is released. |

Until every item above is closed and recorded here, any 15-phase checklist produced from this repository is a research ledger, not an accepted projection. Simulation sections must read `SIMULATION NOT RUN`, with the blocker stated. Research-branch simulations, such as the 900k conditional BUF@MIN run, are labelled research-only and are not engine output. Nothing in this repository places bets, sets `projection_ready`, or changes model weights.

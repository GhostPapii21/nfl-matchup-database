# Proposed routine bootstrap

This file is a proposal. It does not install a routine. The parent edits saved routines only after the published commit is verified. The routine is on demand. It is not a continuous repair loop.

Suggested name: NFL model GitHub sync (routine-only).

## Steps

1. Pull latest `main` from `GhostPapii21/nfl-matchup-database` only when the worktree is clean. Use `git pull --ff-only`. If the worktree is dirty, stop and leave the local work in place.
2. Read `inventory/RESTORE_VERIFICATION.json`, `manifest.json`, and `docs/SOURCE_STATUS.md`. Certified freshness means those committed hashes and the source status, not a live odds pull.
3. Refresh a source only by the steps in `docs/DATA_UPDATE.md`. If authentication is missing, leave quotes `NOLINE`.
4. Run `bash scripts/smoke_offline.sh` when the tree still matches the commit you intend to test. The smoke test is the gate that exists today. It is not a production acceptance gate.
5. Do not start a batch simulation or a promotion while `known_flags/KNOWN_LIMITATIONS.json` has `projection_ready` false, the entrypoint is unenforced, penalties/returns/official overtime are unsupported, calibration is unfitted, or the pristine protocol is incomplete.
6. Push updates with a normal branch and pull request. Do not force-push.
7. Linear logging of the result is a parent step after verification. This repository does not post to Linear by itself. The open set is `OPEN_LINEAR_ITEMS.md`.

## Do not

- Self-expand the deferred public-research item NFL-34.
- Bypass odds authentication or invent ORCA, FTN, or Pinnacle quotes.
- Duplicate the PFF browser lane.
- Claim `projection_ready` without the NFL-49 gate.
- Treat the 15-phase ledger or the 100k workflow as present. They are the NFL-56 goal, and they are not implemented.

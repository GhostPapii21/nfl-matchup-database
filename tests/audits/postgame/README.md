# Postgame grading audit tests

Isolated tests for `docs/audits/postgame_grading_audit.md`. They import the existing grading code read-only, build any
git history they need in pytest's `tmp_path`, and never write inside the repository. No network, no paid API.

    python3 -m pytest -q -p no:cacheprovider -rx tests/audits/postgame

- `test_audit_pg_denpit_regression.py`: DEN@PIT Week 12 (PR #146) as the first regression case: final box from the
  committed ESPN summary, the packet the grader picks vs the PR #141 lock hash, CLV, zero-stat and absent players,
  Rico's leg strings, and the research grade of the lock.
- `test_audit_pg_leakage.py`: packet and research-artifact timestamps, closing-quote cut-off, holdout ordering,
  readiness spot counting.
- `test_audit_pg_participation.py`: gamebook participation (started / substitution / did not play / not active),
  special-teams-only appearances, suffix-insensitive names, opportunity vs efficiency error split.
- `pg_audit_reference.py`: the audit's proposed helpers. Nothing outside this folder imports it.

`test_current_*` tests pin today's behaviour. Tests marked `xfail(strict=True)` describe a proposed fix and name a gap id
(`G-xx`) from the report; once that fix lands they fail as XPASS, which is the cue to remove the marker.

Tests that walk the packet's git history skip on a depth-1 checkout (the offline-tests workflow uses one). This folder
is not wired into `scripts/test_offline.sh`; adding it there is a separate, reviewed change.

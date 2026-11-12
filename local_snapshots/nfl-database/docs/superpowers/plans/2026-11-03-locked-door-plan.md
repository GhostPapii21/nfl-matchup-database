# Locked Door plan
Phase 0: git init + baseline commit (done: 3152576 nfl-database, bacb31b pro-edge).
Phase 1: rulebook.py + tests (red), then wire run_gate/rico_nov2/snf/rico4/press_tier activation + thresholds to it (green). Commit.
Phase 2: SCHEME_EDGE changes (last-2 WARN, explanation required) + depth receiver rule replacing the #3/#4 ban. Tests first. Commit.
Phase 3: shrink leftovers in sim_v6.py / sim_v5.py (oppadj full strength, drop `shrunk`, fix divide-by-zero), stale wording; deprecate sim_v6_fix. Commit.
Phase 4: door.py (build/check/swap/override) + verify_stamp.py + slip rules + team-file loader + ledger BLOCK. Tests first. Commit.
Phase 5: assemble.py fields + exit non-zero on gate FAIL; pro-edge banner. Commit.
Phase 6: regression tests from real misses; delete stale test; full suite. Commit.
Phase 7: docs/RULES_TO_CODE.md + CONTRIBUTING.md; run Thursday build through the door. Commit.

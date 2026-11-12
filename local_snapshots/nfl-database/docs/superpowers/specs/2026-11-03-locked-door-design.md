# Locked Door design (Rico approved 2026-11-03 00:32 ET: "Fix all of these issues and make it critical")

## Goal
Every slip goes through one door (`tools/door.py`). A slip without a valid stamp can't be shown to Rico or posted.

## Parts
A. **Rulebook** `rules/rulebook.py`. Each rule has an id, plain-words text, approved_by, approved_at, effective date, severity (BLOCK/FLAG/WARN) and params. Its version is the sha256 of the file. Activation is `active(id, game_date, now)`: a rule is on when max(game_date, real clock date) >= effective, or always if it has no date. Backdating a manifest therefore can't turn a rule off, because the door always runs on the real clock. Thresholds in run_gate / rico_nov2 / snf / press_tier / rico4 are read from the rulebook.
B. **Door** `tools/door.py`:
   - `build <slip.json>`: for each leg, load its run, run `run_gate` (real clock) and require a gate PASS with the leg live. It then auto-loads both teams' files, runs the ledger coverage check (BLOCK), the leg rules and the slip rules.
   - PASS writes `approved/<date>/<slip_id>.json` with a stamp: sha256(canonical slip + rulebook version + test status).
   - FAIL exits 1 and writes `blocked/<date>/<slip_id>.md`/.json listing rule, leg, value vs threshold and plain words. It also writes alerts/ breakdowns for SCHEME_EDGE flags.
   - On a block it offers two choices, and neither is applied automatically:
     - **SWAP**: `door.py swap <slip_id>` proposes `proposals/<slip_id>_swap.json` using the next-best leg that passes every rule from the same game/slate. `door.py swap <slip_id> --approve --approved-by Rico --at <ts> --text '...'` re-runs the door on it and stamps it.
     - **OVERRIDE**: `door.py override <slip_id> --rule <id> --reason '...' --approved-by Rico --at <ts> --text '<Rico's words>'`. This stamps the slip OVERRIDDEN, lists the rules overridden, and appends to `overrides.log`. approved-by must be Rico, and a time plus his approval text are required. Agent-relayed approvals and bot names are refused. An override can only cover rules that actually failed.
   - `check <slip.json>` runs the same checks as build but writes nothing to approved/.
C. **verify_stamp** `tools/verify_stamp.py <approved.json>` recomputes the hash and checks the rulebook version. A hand-built slip has no stamp and fails. assemble.py exits non-zero on a gate FAIL. pro-edge outputs are labeled CANDIDATES and must go through the door.
D. Gap fixes from the 2026-11-03 audit: shrink leftovers; assemble fields; SCHEME_EDGE last-2 becomes WARN and the explanation is required; the depth receiver rule replaces the #3/#4 ban; slip rules; team files are loaded from Blitz's files, fail closed; the ledger check is a BLOCK.
E. Regression tests from the real misses (CHI@SEA Nov 2) plus door/stamp/swap/override tests.

## Non-goals
NBA rule logic is unchanged (the door only stamps NBA slips after gates.py passes). Nothing is sent, published or bet. sim_v6_fix/ is deprecated, not used.

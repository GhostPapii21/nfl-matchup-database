# Rules → code map (Locked Door)

Rulebook: `rules/rulebook.py` (version d3efafc42e54dce0). Code reads every threshold and start date from it; nothing is hard-coded twice.

| id | sev | effective | approved | enforced in | rule |
|---|---|---|---|---|---|
| NOSHRINK | BLOCK | None | Rico 2026-11-02T21:13 | tools/run_gate.py edge block; tools/sim_v6.py, sim_v5.py (shrink=1.0) | Legs are judged on the raw average of the 3 model probabilities vs the no-vig price; the old 30% shrink is gone. Edge must be +3 pts or more. |
| SCHEME_EDGE | FLAG | None | Rico 2026-11-02T23:52 | run_gate.scheme_edge_ok + door alerts/ | When matchup, scheme fit, game script and form trend all line up (each with a source), averages / 3-of-4 / sims can't cut the leg: under +3 is a FLAG, Ghost6 ch |
| SCHEME_EDGE_LAST2 | WARN | None | Rico 2026-11-03T00:31 | run_gate check_form (WARN note) | On a SCHEME_EDGE leg that misses 3-of-4, the last 2 games not clearing is a warning only. |
| MIRROR_OVER | BLOCK | 2026-11-02 | Rico 2026-11-02T21:13 | rico4_rules.py | Every under cut for a non-stop reason gets a mirror over candidate (or a logged no-rung reason). |
| FAIR_PRICE | BLOCK | None | Rico 2026-11-01T12:00 | door.leg_rules | Every leg needs a real book price and no-vig fair price. |
| SHORT_PRICE | FLAG | None | Rico 2026-11-01T12:00 | door.leg_rules (FLAG) | A leg priced -250 or shorter is flagged for Rico. |
| N1 | BLOCK | 2026-11-02 | Rico 2026-11-02T23:31 | rico_nov2_rules.check | An RB with under 60% of his team's RB carries is DO NOT PLAY. |
| N2 | BLOCK | 2026-11-02 | Rico 2026-11-02T23:31 | rico_nov2_rules.check | A receiving leg needs a verified primary defender (with a source) or it is cut. |
| N3 | BLOCK | 2026-11-02 | Rico 2026-11-02T23:31 | rico_nov2_rules.check | Half and quarter spreads must match the game-script read for that period. |
| DEPTH_RECEIVER | BLOCK | None | Rico 2026-11-02T23:59 | tools/depth_rule.py (gate+door), press_tier.py, snf_rules.py | A #3/#4 WR or backup TE is in play only when the script calls for passing, the QB targets him 5%+ and his defender/coverage has been giving it up; low rung only |
| DEPTH_CAP | WARN | None | Ghost6 (proposal, not approved) None | door slip rules (WARN) | More than one depth receiver on a slip is a warning only (cap NOT approved by Rico). |
| WEATHER | BLOCK | None | Rico 2026-11-01T12:00 | run_gate Phase 11 + door.leg_rules | Weather-flagged open-air games cut passing/receiving overs; multi-day forecast required at slip build. |
| FORECAST | BLOCK | 2026-11-05 | Rico 2026-11-01T12:00 | run_gate | Multi-day forecast block required, pulled within 24h. |
| INJURY | BLOCK | None | Rico 2026-11-01T12:00 | door.leg_rules + depth_rule | Out/Doubtful/IR/inactive players can't be on a slip. |
| FORM_3OF4 | BLOCK | None | Rico 2026-11-01T12:00 | run_gate check_form | The leg clears the exact line in 3 of the last 4 games with the current QB (unless SCHEME_EDGE). |
| RB_TRAIL | BLOCK | None | Rico 2026-11-01T12:00 | door.leg_rules | RB rushing over: 60%+ carry share in 3 of last 4, and 4+ targets per game when his team may trail. |
| COVERAGE_AGE | BLOCK | None | Rico 2026-11-01T12:00 | run_gate | Defender coverage data must be 48 hours old or less. |
| RECENT_DATA | BLOCK | None | Rico 2026-11-01T12:00 | door.leg_rules | Recent game data (feeds through last week) is required. |
| SIMV6 | BLOCK | 2026-11-05 | Rico 2026-11-01T12:00 | run_gate sims check | Runs must be priced by tools/sim_v6.py. |
| COVPROF | BLOCK | 2026-11-05 | Rico 2026-11-01T12:00 | run_gate | Passing legs need the defense man/zone + MOF profile. |
| SNF | BLOCK | 2026-11-02 | Rico 2026-11-02T08:14 | snf_rules.py | SNF postmortem rules S1-S4. |
| RICO4 | BLOCK | 2026-11-02 | Rico 2026-11-02T05:01 | rico4_rules.py | Rico four rules R1-R4 (PRESS manual review, mirror over, 22% pool, QB return). |
| GATE_PASS | BLOCK | None | Rico 2026-11-03T00:32 | door.evaluate (run_gate subprocess) | Every leg must come from a run that passed run_gate on the real clock, and be live in it. |
| SLIP_SIZE | BLOCK | None | Rico 2026-11-01T12:00 | door slip rules | Main slips have 3 or 4 legs. |
| NO_TD | BLOCK | None | Rico 2026-11-01T12:00 | door.leg_rules | Main slips have no touchdown legs. |
| TEAM_FILES | BLOCK | None | Rico 2026-11-02T23:59 | door.team_files | Both teams' database files are loaded into every build; a missing team file stops the build. |
| LEDGER | BLOCK | None | Rico 2026-11-03T00:32 | door.ledger | Every logged game must be in defender_ledger.csv; a skipped game stops the build. |
| TEST_SUITE | BLOCK | None | Rico 2026-11-03T00:32 | door test status | The full test suite must have passed on the current code before any stamp (door.py test). |
| OVERRIDE | BLOCK | None | Rico 2026-11-03T00:32 | door.check_approval/override | Overrides need Rico's recorded approval text and time; bots can't self-approve; relayed approvals don't count. |

## The one path to a slip
1. `runs/<date>_shared_src/assemble.py` builds runs; it exits 1 if any run_gate FAILs.
2. `python3 tools/door.py test` runs the full suite and records status tied to the code hash.
3. `python3 tools/door.py build <slip.json>` re-runs run_gate on every leg run, applies leg + slip rules, writes approved/<date>/<id>.json with sha256 stamp, or blocked/<date>/<id>.md (exit 1).
4. `python3 tools/verify_stamp.py <file>` — anything without a valid stamp under approved/ is not a slip.
5. Blocked: `door.py swap <id>` (proposal) then `--approve`, or `door.py override --rule --reason --approved-by Rico --at`. Rico only; bot names and relayed text are rejected; logged in overrides.log.

## Rule activation
`rulebook.active(id, game_date, now)` = max(game_date, real clock) ≥ effective. A rule can no longer be skipped by back-dating game_date. The door CLI has no --now.

## Known limits (honest)
- Approval is a record + regex checks, not cryptographic; a human could forge text.
- .door/test_status.json is local and could be hand-written; verify_stamp checks the code hash but not who ran it.
- TEAM_FILES path `teams/{team}.json` is a placeholder until Blitz lands postmortems/2026-11-03_code_notes_for_ghost6.md; every real build BLOCKs on it until then.
- DEPTH_CAP (max 1 depth leg) is a Ghost6 proposal, WARN only, needs Rico.
- SCHEME_EDGE explanation is left empty by assemble; Ghost6 must write it, else the waiver fails closed.

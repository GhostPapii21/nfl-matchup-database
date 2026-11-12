# Contributing (Locked Door)

1. New or changed rule = Rico's words first. Add it to `rules/rulebook.py` with id, text, approved_by "Rico", approved_at (ET timestamp), effective date, sev BLOCK/FLAG/WARN. Bots may add proposals only with approved_by "<bot> (proposal, not approved)" and sev WARN.
2. Code reads the rule: `_rb.param(id, key)` and `_rb.active(id, game_date, now)`. Never hard-code a threshold or a date.
3. TDD: write a failing test in `tools/tests/` (a real miss goes in `test_regressions.py`), then the code.
4. Missing data fails closed with plain words saying what is missing.
5. Run `python3 tools/door.py test` — all green — then commit (one commit per phase).
6. Slips come only from `tools/door.py build`. Never hand-build a slip, never self-approve, never treat a relayed approval as Rico's.
7. Lanes: Blitz commits data (teams/, postmortems/) and does not edit assemble.py, run_gate.py, rico4_rules.py, press_tier.py or sims. Do not overwrite another agent's data.
8. Update `docs/RULES_TO_CODE.md` when a rule's enforcement moves.

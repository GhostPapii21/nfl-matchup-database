# v5 lock (pre-grading)
- Reads: grok-4.7 via xAI API, betting-game-brainstorm 12-step format (reads/*.json, prompts reads/*.prompt.txt), 88/88 games, all sections validated; 11 re-prompts rejected (rejects_log.jsonl). Old-format reads moved to superseded_oldformat/ (not used).
- SAVED_READ: Ghost6 13d41b9 chat reads (deduped; Grok extraction kept only endorsed yardage legs with a reason) + w8 pack checklists -> saved_picks.csv. Grok reads on those games = GROK_ON_SAVED_GAME (comparison only).
- PRO_EDGE: offline reimplementation (proedge.py), applied AFTER reads as a gate/tag, not fed into Grok.
- ZONE_MOF: lock.py rule. PHASE_SCRIPT: main line + latest saved price (approximation).
- Rules frozen; train wk3-6 / holdout wk7-8 graded by grade.py after this commit. No outcomes in read step. 0 Odds API calls.

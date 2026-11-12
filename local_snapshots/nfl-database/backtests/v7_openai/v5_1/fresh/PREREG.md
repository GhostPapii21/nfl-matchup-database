# v5.1 fresh-read arm — pre-registration (locked before any read)
Approved by Rico 3:38 PM ET. Grok spend cap: hard $10; script stops new calls at $9.20 logged (cost_in_usd_ticks).
- Model grok-4.7, temp 0.3, JSON mode — same as v5. Inputs: identical v4 as-of packs (808dc89) and context builder as v5 reads.py (leak audit f80fe05 CLEAN). 88 games Wk3-8, run in week order (3->8), 3 threads (v6 reads25 also on Grok).
- Prompt = v5 SYS + V5.1 RULES (SYSTEM_PROMPT.txt): MISSING instead of guessed injury fallout; fixed must_be_true "<stat> >=|<= <number>" and kills_it "IF ... THEN ..."; data_check.disagrees vs data_check.missing, verdict flag only on disagreement. Validator enforces these; up to 3 attempts as v5.
- DEVIATION: the betting-game-brainstorm SKILL.md was edited at 14:58 ET today, after v5 (10:12); v5's exact copy was not saved, so the current skill text is used.
- Selection = locked v5.1 policy, v5_1.py copied unchanged: PRIMARY (Rico SAVED_READ legs from v5 where present, else fresh Grok legs), keep confidence=strong AND verdict=agree, best saved pre-kick price at same line, deterministic slips <=5/week 3-4 legs, $10 flat.
- Pass bar (Wk3-6): >=40 settled priced legs, ROI>0, beats v5 PRIMARY ROI and $. Wk7-8 reported separately. Also vs rush-under baseline, v5.1 locked-reads arm, v6.
- If Grok stops (quota/cap), grade only completed games and report coverage.
- Grader: ../harness.py logic (shared). 0 Odds API credits.

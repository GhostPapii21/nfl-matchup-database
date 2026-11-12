# Nov 1 2026 lessons checklist (audit ~23:45 ET)
Where it lives: BS = nfl-betting-script skill, GS = nfl-game-script-run skill, PS = PHASE_SCRIPT.md, code = tools/. The skill patches are in skill_patches/ and still need to be applied. Statuses: covered / docs-only / partial / missing.

| # | Lesson | Where it lives | Status before | Action | Status after | Test name |
|---|---|---|---|---|---|---|
| 1 | Weather alert (rain ≥50%, gust ≥20, wind ≥15), rushing overs first, re-check placed legs | run_gate weather block; BS §14; GS P11; PS | partial: code yes; BS said 70%, GS only wind 15; leaked Week 8 slips into other weeks | fixed WXSLIPS; patched BS/GS; PS §1 | covered | test_run_gate weather tests; WeatherSlipsWeekTest |
| 2 | Game script drives RB volume | run_gate RBSCRIPT; PS | partial (not in skills/PS) | PS §2, skill patches | covered (code + docs) | test_run_gate (RBSCRIPT) |
| 3 | RB fixes A/D/E/F on; B/C declined | sim_v6/run_gate; GS P13 contradicted D | partial/contradiction | GS P13 patched; PS §3; declined items untouched | covered | test_rbmiss_sim, test_sim_v6 |
| 4 | RB scan ≥20% carries, role flip | slate_scan | covered in code, docs missing | PS §4, patches | partial: the depth-chart RB1 is passed by hand (no automatic depth pull) | test_slate_scan |
| 5 | Receiving: blitz/pressure/checkdown + time to throw + targets under pressure | run_gate PRESSURE; GS P5 | partial (TTT/TUP not required) | TDD gate rule (≥11-05) + assemble preflight | covered | PressureW9Test |
| 6 | §7/§14: gate before slips; §11 one slip/player | BS; GS; gate_config overrides | covered | none | covered | test_run_gate (sec11) |
| 7 | sim_v6 calibrated Bias (flat cuts retired) | sim_v6.py; GS P14 still had flat cuts; assemble used v5 | partial/contradiction | gate check ≥11-05, assemble preflight, GS patch, PS fixed | covered | SimV6Test, Assemble9Test, test_sim_v6 |
| 8 | Press tier only after a gate PASS, live 11-05 | press_tier.py, gate_config | code covered, docs missing | PS §8, patches | covered | test_press_tier/live/wire |
| 9 | Slate scan before slips | slate_scan; BS/PS | docs-only | PS §6, patches | docs-only (the scan's run is not gated) | — |
| 10 | PFF cross-check; caution only; never weather/script/projection | BS §20 and GS said PFF missing/never cited | missing/contradiction | check_pff (caution) + FAIL on banned scope; patches | covered | PFFCrossCheckTest (9) |
| 11 | Postgame review contents + watch list | postmortems | docs-only | PS §10, patches, WATCHLIST_2026.md | docs-only | — |
| 12 | Backtests are analysis only; no rule added; pass_volume_cap off | backtests/; gate_config | covered | PS §11 | covered | config check (pass_volume_cap false) |
| 13 | Phase 15 backfield split and slip exposure | week8/inactives/phase15_*.md (by hand) | docs-only | PS §12, patches | docs-only (manual) | — |
| 14 | Week 8 misses logged; Emmett Johnson watched | missed-edges log | partial (Mike Washington Jr. missing; no watch list) | index table added; WATCHLIST_2026.md | covered | — |
| 15 | Questionable = one-rung drop (Rico) | BS §5 said do not bet | contradiction | BS patch | docs-only | — |
| 16 | Week 9 assemble uses this week's inputs, blocks on missing files | assemble.py | missing (Week 8 paths, crash) | WEEK paths + PREFLIGHT (ASM9) | covered | Assemble9Test |

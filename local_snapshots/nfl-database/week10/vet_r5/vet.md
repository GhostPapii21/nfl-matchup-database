# Vet of r5 TNF JAX@BAL (Nov 5, 2026), done Nov 4 ~05:45 ET (read-only)
## Branch
- /workspace/nfl-database is on **master** (only branch; no remote). r5 commits 8a9c154, ddc31a5, 770f73b, 5ae12b9, 750974f sit on master = de facto merge Rico never OK'd. Not pushed (no remote).
- All 5 touch only runs/2026-11-05_JAX@BAL_r5/. 8a9c154 also deletes DRAFT_bar_side_table.md and rewrites r5 files (in-dir only). Order is interleaved with eac33b2/4d4bfed/3369e16 (codex_full) commits, so moving r5 off master needs a careful rebase/revert -> Rico decision.
- Hashes: r2 read 76b563a3...5685 OK; addenda 1-4 all sha256 -c OK.
## Card recompute (pbp_2026, wk<=8)
- Henry U69.5 [102,58,45,53]: 3/4, last-2 OK. GO, BUT window is any-QB; Fagnano-only = [53] 1/1 = MISSING (Rico's open rush-window call).
- Lawrence U12.5 [0,25,11,10]: 3/4, last-2 OK. GO w/ flag. Scramble flag: 53/80 yds on 9 scrambles is SEASON (wk1-8) — correct; last-4 is 45 of 46 yds on 7 scrambles (worse). BAL D scramble 7.26% vs lg 4.83% — correct.
- BAL TT U14.5 [30,10,13,10] (Henry-check pts match): 3/4, last-2 OK. GO.
- JAX 1Q -2.5 [3,7,-7,7]: 3/4, last-2 DOWNGRADE. GO singles-only, downgraded.
- JAX 1Q ML: 3/4, DOWNGRADE. Same; -217 short price.
- Cuts correct: 1H -6.5 [10,-7,-3,28] 2/4; 1H ML 2/4; -10/-9.5 [5,2,-3,35] 1/4.
## Prices
- All from odds pulled 2026-11-03 19:15 ET (meta). Stale by kick (~24h); re-pull required. Shop dicts in policy_legs/game_legs confirm best price chosen across FD/DK/Pin where quoted. Henry U69.5 has no Pinnacle quote at 69.5 (Pin U70.5 -118 only). BAL TT only FD quoted. 1Q/1H ML shop key shows `nan` (cosmetic bug), price Pin -217/-318 per report.
## Off-read
- Strange o35.5 [95,68,44,55] 4/4 / 3/4 w/o wk8: OK. BTJ u1.5 [2,0,0,1] 3/4 OK, DK -195 best. Meyers u40.5 [33,37,83,24] 3/4 DOWNGRADE; Hunter u9.5 [0,9,59,0] 3/4 DOWNGRADE, rec u1.5 [0,1,4,0] DOWNGRADE: correct.
- Washington u4.5 [1,6,4,1] mechanically passes 3/4 + last-2 OK; OFF is a read/role call (allowed), correct per addendum 3/4.
- Washington overs: rec o4.5 1/4 correct. **Error: yds main line is 63.5 (FD -114), not 62.5**; 2/4 [7,124,64,16] holds.
## Fagnano (BAL@BUF wk8, full-game BAL totals settle)
- Hill 4 rec/20 yds (3/21 from Fagnano): o2.5, o13.5 pass. Andrews 3/14: u18.5 pass, u2.5 fails. Flowers 0 rec on 5 tgts (4 from Fagnano): unders pass, raw sim (~-31/-32) and locked read AVOID oppose. Bateman 1/22: o14.5 pass. All 1-game = MISSING unless Rico OKs.
## Slip
- (-114,-114,-120) product = +546 confirmed. Ignores correlation: Henry U and BAL TT U positively correlated (also Lawrence U with JAX script) -> real SGP lower. Meets 3-leg rule.
## Review branch
- tools/tests: 545 passed (5m07s). Bare `pytest` at repo root errors on collection (backtests/v6.../leak_test.py FileNotFound) — run scoped.
- bb93ba4: no date gate, edge never rejects in run_gate/rico4.rung_clears; tests assert flag-only on 11-10. Nit: rulebook EDGE_BAR still sev="BLOCK" (text says flag only; not enforced as cut, but label should be FLAG).

# Rule enforcement audit (phase 1, read-only) — 2026-11-03
Scope: /workspace/nfl-database (tools/, runs/2026-11-05_shared_src/), /workspace/pro-edge, /workspace/nba-codex-2026-11-02/gates.py. No code changed.

## Environment
- **No git repo** (`git log` -> "not a git repository"). History is kept only as `*.bak` / `*.pre_*` copies. Nothing is versioned or reviewable as diffs.
- Tests: `cd tools/tests && python3 -m pytest -q --ignore=test_run_gate.pre_form.py` -> **323 passed, 0 failed**, 7 RuntimeWarnings (sim_v6.py:45 and :80 divide-by-zero), 115 s.

## Entry points (is there one gate?)
The only blocking check is `tools/run_gate.py` (Gate.run, exit 1 on any miss, run_gate.py:547). Rule mixins plug in at run_gate.py:496-500 (srclist_rules, rico4_rules, snf_rules, rico_nov2_rules).
**It is not a single mandatory entry point.** Ways around it:
1. **assemble.py doesn't block on the gate.** runs/2026-11-05_shared_src/assemble.py:534-537 calls run_gate via subprocess, pastes the text into report.md and keeps going. A FAIL never stops it from writing runs or the eval JSON (assemble.py:547).
2. **Nothing checks slips.** No code reads a slip, checks that each leg came from a gate-PASS run, counts legs (3-4), or bans TDs. A bot can write slips by hand or from chat.
3. **pro-edge (edge_scan.py, game_mkts.py) is a separate path.** It has its own `gate>=0.03` (edge_scan.py:106) and a `short_flag` label for prices under -250 (edge_scan.py:106, game_mkts.py:80). It's labeled "candidates only" (edge_scan.py:2,151) but isn't wired to run_gate.
4. **NBA** has its own gates (nba-codex-2026-11-02/gates.py). Shrink was removed there (gates.py:5).
5. Other scripts call run_gate in their own way: backtests/*, runs/2026-11-01_shared_src/assemble.py, slate_scan.py, press_live.py.
6. **Rule dates come from the manifest.** NOV2_FROM / RICO4_FROM / SNF_FROM = 2026-11-02, and SIMV6/FORECAST/COVPROF = 2026-11-05 (run_gate.py:32-34). Every gate reads `game_date` from the manifest the builder writes (run_gate.py:355). A wrong or old date turns off most rules without any warning.

## Rule-by-rule
| # | Rule | Where | Block or label | Test | Status |
|---|---|---|---|---|---|
| 1 | No shrink: raw p vs no-vig, +3 | run_gate.py:457-460; rico4_rules.py:36-37; assemble.py:151; edge_scan.py:32; nba gates.py:5 | Block (unless SCHEME_EDGE) | test_run_gate / test_rico4 / test_lessons_audit | **Partial**: see gaps below (sim_v6 still computes `shrunk`, oppadj shrink=0.5, stale wording) |
| 2 | SCHEME_EDGE flag + breakdown | run_gate.py:62-69 (scheme_edge_ok), 116-120 (§7), 458-480 (edge/sim -> notes + breakdown), 527 (printed) | Label. The flag replaces the cut | test_scheme_edge.py (4), test_rico_nov2.py:46,50 | **Partial**: assemble.py never fills `scheme_edge`, so it can't fire on real runs. `explanation` is optional (prints "MISSING", run_gate.py:478, no fail). Extra rule not approved by Rico: SCHEME_EDGE §7 needs the last 2 games to clear (run_gate.py:117-119). Nothing checks that the alert was actually sent to Rico |
| 3 | Mirror overs for every cut under | rico4_rules.py:31 (mirror_eligible), 89-94 (check); assemble.py:385-403 (mirrors), 541 | Block (an under cut needs a mirror or a no_rung_reason) | test_rico4.py | **Enforced**. STOP_RX (rico4_rules.py:16) exempts weather/inactive/§11/#3/#4 cuts |
| 4 | N1 RB <60% carries = do-not-play | rico_nov2_rules.py:28-32 | Block (live RB leg) | test_rico_nov2.py:13-19 | **Partial**: needs a `carry_share{value,source}` field, and assemble.py's leg dict (assemble.py:478-489) doesn't emit one. Every assembled RB leg fails as "missing" (fails closed, but the build can't be used). assemble.py:272 has a separate 3-of-4 test at 60%, rush overs only |
| 5 | N2 verified primary defender | rico_nov2_rules.py:33-37 | Block | test_rico_nov2.py:22-24 | **Partial**: needs `defenders[i].primary is True`. No `primary` is written into coverage in assemble.py (grep finds no hits). The older WR3_TEAM_COV fallback (run_gate.py:434-435) still adds a note, but N2 overrides it |
| 6 | N3 half/quarter spread vs script | rico_nov2_rules.py:19-21, 38-44 | Block | test_rico_nov2.py:26-33 | **Partial**: only works if spreads go through the gate. Props-only assemble.py never makes spread legs, and pro-edge game_mkts.py has no script check. Detection is a regex on market/name (rico_nov2_rules.py:11-12) |
| 7 | Depth receiver rule (#3/#4 WR or backup TE allowed) | None | — | None | **Missing, and the old ban is still active**: press_tier.py:142 BLOCKS wr_rank 3/4; rico4_rules.py:66 sends #3/#4 WRs to excluded_wr34; snf_rules.py:97-98 bans WR4 overs; S4 needs >=4 targets/g (snf_rules.py:105), not >=5% target share; run_gate.py:66 docstring still says "#3/#4 WR ban". No code for the 5% QB-target / script-pass / defender-giving-up / low-rung rule, or the one-per-slip warning |
| 8a | Weather multi-day forecast | run_gate.py:200-231 (check_forecast, ≤24h, for runs ≥11-05), 171-199 (check_weather) | Block | test_weather_forecast, test_wx_roof, test_wind_parse | **Enforced** (forecast only for runs dated ≥ 2026-11-05) |
| 8b | Injury/inactives | press_tier.py:137-140 (PRESS only); assemble.py:288 Phase 8 | PRESS tier: block. Phase 8 checklist row: FAIL -> cut (run_gate.py:377-381) | test_press_tier | **Partial**: run_gate has no direct injury field check. It relies on the builder's checklist row |
| 8c | -250 flag | edge_scan.py:106 / game_mkts.py:80 `short_flag` | Label only, pro-edge only | none | **Missing in run_gate** (only mentioned in the docstring at run_gate.py:66) |
| 8d | 3-of-4 test | run_gate.py:101-120 (check_form) | Block (flag under SCHEME_EDGE) | test_run_gate | **Enforced**. Note: assemble.py doesn't write `recent_form` on manifest legs (it goes only into press, assemble.py:362-364), so every live assembled leg fails "recent_form missing" |
| 8e | RB 60% in 3 of last 4 + 4 targets when the team may trail | assemble.py:271-272 (60% in 3 of 4, rush overs only); run_gate.py check_rbmiss dog exception 70% (run_gate.py:48, 308) | Checklist FAIL | test_rbmiss_sim | **Partial**: no "4 targets when trailing" check found |
| 8f | Fair price required | run_gate.py:455-456 (no_vig needed); HOLD path run_gate.py:371-373; price_hold.py | Block | test_hold | **Enforced** |
| 8g | Recent game data | run_gate.py:107 (recent_form age), srclist_rules.py:98-116 (feed weeks SRC-5); assemble.py:24-27 preflight | Block | test_srclist | **Enforced** |
| 8h | Defender coverage ≤48h | run_gate.py:9 MAX_AGE_H coverage_matchups 48; 437-445 | Block, but an approved exception can waive it (run_gate.py:441-443) | test_run_gate | **Enforced** (exception path exists) |
| 8i | Main slips 3-4 legs, no TDs | None | — | None | **Missing** (no slip-level code) |
| 9 | Team DB per team + auto-load + playlog/ledger stop | tools/ledger_coverage_check.py:1-10 (exit 1 if a playlog game is missing from the ledger); defenders/*_secondary.md (secondaries only) | Standalone script, not called by assemble or run_gate | None | **Missing/partial**: no per-team offense+defense file, no auto-load into builds, the ledger check isn't wired in. defenders/ has only about 27 teams, all defense |

## Shrink leftovers
- tools/sim_v6.py:153,173 and sim_v6_fix/sim_v6.py:176,196 still compute `r['shrunk']=0.5+0.7*(av-0.5)-no_vig`. Not used by the gate, but anyone reading sims output can use it.
- The matchup effect is still at half strength: `oppadj(..., shrink=0.5)` in tools/sim_v6.py:43, sim_v6_fix/sim_v6.py:52 (+BIAS_OPP .5, :29), runs/2026-11-05_shared_src/sim_v5.py:21. PHASE_SCRIPT.md:151 lists this as open, pending a backtest.
- Stale wording: rico4_rules.py:2,14 ("P14 edge-shrink", MR_RX matches "shrunk|shrink"), rico4_rules.py:40 docstring "shrunk>0"; press_tier.py:3-4 ("standard shrink only"); press_tier.py:149 `shrink="none"`.
- game_mkts.py:79-80 still calls `shrink()`, which is now the identity function (edge_scan.py:32), so it's harmless.

## Top 5 gaps
1. **No single gate for slips.** assemble.py ignores the gate result, and nothing validates slips (legs, TDs, the gate PASS on each leg, the -250 flag, the one-per-slip warning). pro-edge and NBA are separate paths.
2. **The depth receiver rule isn't built, and the old #3/#4 ban is still enforced** (press_tier.py:142, rico4_rules.py:66, snf_rules.py:97).
3. **assemble.py doesn't emit the fields the new rules need** (scheme_edge, carry_share, primary defender, script_read, recent_form). SCHEME_EDGE can never fire, and N1/N2/§7 fail every live leg.
4. **The team database and ledger/playlog stop aren't wired in.** ledger_coverage_check.py is standalone, and there are no per-team offense files.
5. **No git, and rules are switched on by dates the builder controls.** Changes can't be audited, and the manifest's `game_date` silently switches rules on or off. Also still open: oppadj shrink=0.5, `shrunk` still computed in sims, and the SCHEME_EDGE `explanation` isn't required.
